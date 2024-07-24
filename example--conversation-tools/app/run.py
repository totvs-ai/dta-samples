from typing import List, Optional

from langchain_core.messages import AIMessage, HumanMessage
from langfuse.callback import CallbackHandler


def agent_run(input: str, session_id: str, thread_id: str):
    """
    Creates an agent, runs with tools using an LLM to manage via DTA Proxy,
    and register each step on DTA Monitor
    """
    from .agent import Agent, AgentState
    from .tools_apibrasil import tools_list

    def _extract_steps(response: List[AgentState]) -> List[dict]:
        steps = []

        for entry in response:
            if (
                isinstance(entry["messages"][0], AIMessage)
                and entry["messages"][0].tool_calls
            ):
                for tool in entry["messages"][0].tool_calls:
                    steps.append(
                        {
                            "type": "tool",
                            "name": tool["name"],
                            "args": tool["args"],
                        }
                    )

        return steps

    # setup
    agent = Agent.create_agent(tools_list)

    # DTA Monitor: register input and pass callback handler to agent
    tracer = __create_langfuse().trace(
        id=thread_id,
        session_id=session_id,
        name="my-agent",
        input=input,
    )
    langfuse_handler = CallbackHandler(stateful_client=tracer)

    # execution
    messages = [HumanMessage(content=input)]
    config_thread = {"configurable": {"thread_id": "1"}}
    config_langfuse = {"callbacks": [langfuse_handler]}
    response = []

    for event in agent.graph.stream(
        input={"messages": messages},
        config={**config_langfuse, **config_thread},
    ):
        for v in event.values():
            response.append(v)
            print(v["messages"])

    # output
    final_message = response[-1]["messages"][0].content
    # DTA Monitor: register output
    tracer.update(output=final_message)

    return {
        "headers": {
            "X-dta-session": session_id,
            "X-dta-thread": thread_id,
        },
        "response": {
            "content": final_message,
            "data": {"dta-chat-steps": _extract_steps(response)},
        },
    }


def register_score(score: int, comment: Optional[str], session_id: str, thread_id: str):
    """
    Register user's feedback(score) on DTA Monitor
    """

    response = __create_langfuse().score(
        trace_id=thread_id,
        name="my-agent-feedback",
        value=score,
        comment=comment,
    )

    return {
        "headers": {
            "X-dta-session": session_id,
            "X-dta-thread": thread_id,
        },
        "response": {
            "status": "ok",
        },
    }


def audio_transcription(audio_base64: str, session_id: str, thread_id: str):
    """
    Call an audio transcription model via DTA Proxy,
    and register each step on DTA Monitor
    """
    import base64
    import io

    from openai import OpenAI
    from .config import (
        DTA_PROXY_KEY,
        DTA_PROXY_URL,
    )

    # audio from payload to buffer read
    audio_data = base64.b64decode(audio_base64)
    audio_buffer = io.BytesIO(audio_data)
    audio_buffer.name = "temp.mp3"

    # DTA Monitor: register input
    tracer = __create_langfuse().trace(
        id=thread_id,
        session_id=session_id,
        name="my-agent:transcription",
        input=f"base64 len:{len(audio_base64)}",
    )

    # get transcript
    prompt = """Pergunta sobre cidades brasileiras, CEP, previsão do tempo"""
    transcript = OpenAI(
        base_url=DTA_PROXY_URL,
        api_key=DTA_PROXY_KEY,
    ).audio.transcriptions.create(model="whisper", file=audio_buffer, prompt=prompt)

    # DTA Monitor: register output
    tracer.update(output=transcript.text)

    return {
        "headers": {
            "X-dta-session": session_id,
            "X-dta-thread": thread_id,
        },
        "response": {
            "data": {"transcript": transcript.text},
        },
    }


def __create_langfuse():
    from .config import DTA_MONITOR_PUBLIC_KEY, DTA_MONITOR_SECRET_KEY, DTA_MONITOR_URL
    from langfuse.client import Langfuse

    return Langfuse(
        secret_key=DTA_MONITOR_SECRET_KEY,
        public_key=DTA_MONITOR_PUBLIC_KEY,
        host=DTA_MONITOR_URL,
    )
