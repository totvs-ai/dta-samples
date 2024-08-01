import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
    ToolMessage,
)

from langgraph.graph import END, StateGraph


class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], operator.add]


class Agent:
    @staticmethod
    def create_agent(tools):
        from .config import DTA_PROXY_KEY, DTA_PROXY_URL
        from langchain_openai import ChatOpenAI
        import datetime

        now = datetime.datetime.now()

        model = ChatOpenAI(
            openai_api_base=DTA_PROXY_URL,
            openai_api_key=DTA_PROXY_KEY,
            # model="gpt-4o",
            model="gpt-4o-mini",
            temperature=0.2,
        )

        system_prompt = f"""
          Seja um assistente útil para consulta de informações.
          Seja objetivo, e não ofereça informações que não possam ser obtidas pelas tools.
          Não responda nada sem uso de tools.

          Contexto:
          - data/hora atual é {now}
        """

        return Agent(model, tools, system=system_prompt)

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
