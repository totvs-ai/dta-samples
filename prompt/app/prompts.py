import os

from langfuse.decorators import langfuse_context, observe
from langfuse.openai import openai

DTA_PROXY_KEY = os.environ.get("DTA_PROXY_KEY")
DTA_MONITOR_PUBLIC_KEY = os.environ.get("DTA_MONITOR_PUBLIC_KEY")
DTA_MONITOR_SECRET_KEY = os.environ.get("DTA_MONITOR_SECRET_KEY")


langfuse_context.configure(
    host="https://monitor.dta.totvs.ai",
    enabled=True,
    public_key=DTA_MONITOR_PUBLIC_KEY,
    secret_key=DTA_MONITOR_SECRET_KEY,
)


@observe()
def prompt_summary(temperature: float, text: str, language: str):
    return __call_chat_model(
        model="gpt-4o-mini",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": f"Faça um resumo do texto a seguir em tópicos, sendo fiel ao contexto. \n\n Responda no idioma {language}.",
            },
            {"role": "user", "content": text},
        ],
    )


@observe()
def prompt_material(temperature: float, text: str, language: str, meio: str):
    return __call_chat_model(
        model="gpt-4o-mini",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": f"Seja um redator de marketing, e produza um texto para um {meio}, no idioma {language}",
            },
            {"role": "user", "content": text},
        ],
    )


@observe()
def prompt_analista_marketing(temperature: float, text: str):
    return __call_chat_model(
        model="gpt-4o-mini",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": f"Seja um analista de mercado, que sugere o potencial público alvo e estratégias para divulgar o produto do texto",
            },
            {"role": "user", "content": text},
        ],
    )


@observe()
def prompt_analista_marketing_conteudo(temperature: float, text: str):
    def prompt_marketing_target(temperature: float, text: str):
        return __call_chat_model(
            model="gpt-4o-mini",
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": f"Seja um analista de mercado, e defina resumidamente qual o público alvo do conteúdo a seguir, e qual o melhor estilo de redação para este público",
                },
                {"role": "user", "content": text},
            ],
        )

    def prompt_marketing_redator(temperature: float, text: str, instructions: str):
        return __call_chat_model(
            model="gpt-4o-mini",
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": f"Seja um redator publicitário e, com base no texto a seguir, produza um texto seguindo esta recomendação: {instructions}",
                },
                {"role": "user", "content": text},
            ],
        )

    response_target = prompt_marketing_target(temperature, text)

    return prompt_marketing_redator(
        temperature=temperature,
        text=text,
        instructions=response_target.choices[0].message.content,
    )


def __call_chat_model(model="gpt-4o-mini", temperature=0.2, messages=[]):
    client = openai.OpenAI(
        base_url="https://proxy.dta.totvs.ai",
        api_key=DTA_PROXY_KEY,
    )

    return client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
    )
