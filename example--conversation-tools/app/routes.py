from flask import render_template, current_app as app, request, Response
from .agent import agent_run
import json


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/welcome")
def welcome():
    initial_message = {
        "data": {
            "suggestions": [
                {
                    "label": "Quais contratos estão pendente?",
                },
                {
                    "label": "O que tenho para hoje?",
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


@app.route("/completion", methods=["POST"])
def completion():
    headers = request.headers
    body = request.get_json()

    thread_id = headers.get("x-dta-thread", "")
    content = body.get("content", "")
    agent_response = agent_run(input=content, thread_id=thread_id)

    return Response(
        headers=agent_response["headers"] if "headers" in agent_response else None,
        response=json.dumps(agent_response["response"]),
    )
