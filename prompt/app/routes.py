from flask import render_template, current_app as app, request
from .prompts import (
    prompt_summary,
    prompt_material,
    prompt_analista_marketing,
    prompt_analista_marketing_conteudo,
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/summary", methods=["POST"])
def summary():
    query_params = request.args

    response = prompt_summary(
        text=request.get_json().get("text", ""),
        language=query_params.get("language", "english"),
        temperature=query_params.get("temperature", 0.5),
    )

    return {
        "messages": response.choices[0].message.content,
    }


@app.route("/gerar_conteudo", methods=["POST"])
def gerar_conteudo():
    query_params = request.args

    response = prompt_material(
        text=request.get_json().get("text", ""),
        meio=query_params.get("meio", "email"),
        language=query_params.get("language", "english"),
        temperature=query_params.get("temperature", 0.5),
    )

    return {
        "messages": response.choices[0].message.content,
    }


@app.route("/analista_marketing", methods=["POST"])
def analista_marketing():
    query_params = request.args

    response = prompt_analista_marketing(
        text=request.get_json().get("text", ""),
        temperature=query_params.get("temperature", 0.5),
    )

    return {
        "messages": response.choices[0].message.content,
    }


@app.route("/analista_marketing_conteudo", methods=["POST"])
def analista_marketing_conteudo():
    query_params = request.args

    response = prompt_analista_marketing_conteudo(
        text=request.get_json().get("text", ""),
        temperature=query_params.get("temperature", 0.5),
    )

    return {
        "messages": response.choices[0].message.content,
    }
