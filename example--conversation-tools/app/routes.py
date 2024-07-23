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
    query_params = request.args
    body = request.get_json()

    content = body.get("content", "")
    agent_response = agent_run(input=content)

    return Response(
        headers=agent_response["headers"] if "headers" in agent_response else None,
        response=json.dumps(agent_response["response"]),
    )


# @app.route("/fake/data-x", methods=["POST"])
# def fake_data_x():
#     query_params = request.args

#     response = prompt_analista_marketing_conteudo(
#         text=request.get_json().get("text", ""),
#         temperature=query_params.get("temperature", 0.5),
#     )

#     return {
#         "messages": response.choices[0].message.content,
#     }
