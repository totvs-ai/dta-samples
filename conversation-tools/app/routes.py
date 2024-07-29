from flask import Blueprint, render_template, Response, request
from .run import agent_run, register_score, audio_transcription
import json

conversation_tools = Blueprint("conversation_tools", __name__)


@conversation_tools.route("/")
def home():
    return render_template("index.html")


@conversation_tools.route("/welcome")
def welcome():
    initial_message = {
        "data": {
            "suggestions": [
                {
                    "label": "Previsão do tempo em São Paulo",
                },
                {
                    "label": "Próximo feriado a partir de hoje",
                },
            ]
        },
    }

    return {
        "messages": [initial_message],
        "config": {
            "dta-user-greeting": "Olá",
            "dta-initial-message": "Como posso te ajudar hoje?",
            "disclaimer": "Aviso: Este chat utiliza inteligência artificial e os resultados podem não ser 100% precisos.\n\nRecomendamos validar as informações críticas antes de tomar decisões com base nos resultados fornecidos.",
            "clientTimeoutSeconds": 120,
        },
        "data": {},
    }


@conversation_tools.route("/completion", methods=["POST"])
def completion():
    headers = request.headers
    body = request.get_json()

    session_id = headers.get("x-dta-session", "")
    thread_id = headers.get("x-dta-thread", "")
    content = body.get("content", "")

    response = agent_run(
        input=content,
        session_id=session_id,
        thread_id=thread_id,
    )

    return Response(
        headers=response["headers"] if "headers" in response else None,
        response=json.dumps(response["response"]),
    )


@conversation_tools.route("/feedback", methods=["POST"])
def feedback():
    headers = request.headers
    body = request.get_json()

    session_id = headers.get("x-dta-session", "")
    thread_id = headers.get("x-dta-thread", "")
    content = body.get("content", "")
    data = body.get("data", {})

    response = register_score(
        score=float(content),
        comment=data["comment"] if data and "comment" in data else None,
        session_id=session_id,
        thread_id=thread_id,
    )

    return Response(
        headers=response["headers"] if "headers" in response else None,
        response=json.dumps(response["response"]),
    )


@conversation_tools.route("/audio", methods=["POST"])
def audio():
    headers = request.headers
    body = request.get_json()

    session_id = headers.get("x-dta-session", "")
    thread_id = headers.get("x-dta-thread", "")
    audio_base64 = body.get("content", "")

    response = audio_transcription(
        audio_base64=audio_base64,
        session_id=session_id,
        thread_id=thread_id,
    )

    return Response(
        headers=response["headers"] if "headers" in response else None,
        response=json.dumps(response["response"]),
    )
