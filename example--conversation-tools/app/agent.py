import operator
import os
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from .tools import tools_list

DTA_PROXY_URL = "https://proxy.dta.totvs.ai"
DTA_PROXY_KEY = os.environ.get("DTA_PROXY_KEY")
DTA_MONITOR_PUBLIC_KEY = os.environ.get("DTA_MONITOR_PUBLIC_KEY")
DTA_MONITOR_SECRET_KEY = os.environ.get("DTA_MONITOR_SECRET_KEY")


def agent_run(input: str):

    agent = _create_agent(tools_list)

    messages = [HumanMessage(content=input)]
    thread = {"configurable": {"thread_id": "1"}}
    response = []

    for event in agent.graph.stream({"messages": messages}, thread):
        for v in event.values():
            print(v["messages"])
            response.append(v)

    steps = []

    for entry in response:
        if (
            isinstance(entry["messages"][0], AIMessage)
            and len(entry["messages"][0].tool_calls) > 0
        ):
            for tool in entry["messages"][0].tool_calls:
                steps.append(
                    {
                        "type": "tool",
                        "name": tool["name"],
                        "args": tool["args"],
                    }
                )

    final_message = response[-1]["messages"][0].content

    return {
        "headers": {
            "X-dta-thread": "myvalue",
        },
        "response": {
            "content": final_message,
            "data": {"dta-steps": steps},
        },
    }


def _create_agent(tools):
    model = ChatOpenAI(
        openai_api_base=DTA_PROXY_URL,
        openai_api_key=DTA_PROXY_KEY,
        model="gpt4o-mini",
        temperature=0.2,
    ).bind_tools(tools)

    system_prompt = """
      Seja um assistente útil para consulta de informações.

      Contexto:
      - data/hora atual é {now}
    """

    return Agent(model, tools_list, system=system_prompt)


class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], operator.add]


class Agent:
    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm", self.exists_action, {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def call_openai(self, state: AgentState):
        messages = state["messages"]
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {"messages": [message]}

    def exists_action(self, state: AgentState):
        result = state["messages"][-1]
        return len(result.tool_calls) > 0

    def take_action(self, state: AgentState):
        tool_calls = state["messages"][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            result = self.tools[t["name"]].invoke(t["args"])
            results.append(
                ToolMessage(tool_call_id=t["id"], name=t["name"], content=str(result))
            )
        return {"messages": results}
