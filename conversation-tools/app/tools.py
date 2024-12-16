from typing import Optional
import os
import requests
from langchain_core.tools import tool

"""

APIS from https://brasilapi.com.br/

"""


@tool
def bancos():
    """Retorna informações de todos os bancos do Brasil"""

    return _get_endpoint_api_brasil("/banks/v1")


@tool
def bancos_code(code: str):
    """Busca as informações de um banco a partir de um código"""

    return _get_endpoint_api_brasil(f"/banks/v1/{code}")


@tool
def busca_cep(cep: str):
    """Busca de localização por CEP (Código de Endereçamento Postal)"""

    return _get_endpoint_api_brasil(f"/cep/v2/{cep}")


@tool
def busca_localicade(cidade: str):
    """Informações sobre uma cidade ou localidade, como estado e latitude e longitude"""

    return _get_endpoint_api_brasil(f"/cptec/v1/cidade/{cidade}")


@tool
def previsao_tempo_lat_long(latitude: str, longitude: str):
    """Previsão meteorológica para uma localidade, pesquisando por latitude e longitude"""

    METEO_BLUE_KEY = os.environ.get("METEO_BLUE_KEY")
    url = f"https://my.meteoblue.com/packages/basic-1h_basic-day?apikey={ METEO_BLUE_KEY }&lat={ latitude }&lon={ longitude }&asl=9&format=json"
    response = requests.get(url)

    return response.json()


# NOTE: deprecated because not working for now
# @tool
# def previsao_por_codigo_cidade_hoje(cidade_code: int):
#     """Previsão meteorológica para uma cidade no dia de hoje, pesquisando por código cptec de cidade"""

#     return _get_endpoint(f"/cptec/v1/clima/previsao/{cidade_code}")

# @tool
# def previsao_clima_por_codigo_cidade_proximos_dias(
#     cidade_code: int, dias: Optional[int]
# ):
#     """Previsão meteorológica para uma cidade nos próximos dias, pesquisando por código cptec de cidade"""

#     if dias and dias > 6:
#         dias = 6

#     return _get_endpoint(f"/cptec/v1/clima/previsao/{cidade_code}/{dias}")


@tool
def pesquisa_cidades_por_ddd(
    ddd: str | int,
):
    """Retorna estado e lista de cidades por DDD, código telefônico"""

    return _get_endpoint_api_brasil(f"/ddd/v1/{ddd}")


@tool
def feriados_brasil(ano: int):
    """Feriados Nacionais"""

    return _get_endpoint_api_brasil(f"/feriados/v1/{ano}")


def _get_endpoint_api_brasil(path: str):
    url_base = "https://brasilapi.com.br/api"
    url = f"{url_base}/{path}"

    response = requests.get(url)

    return response.json()


tools_list = [
    bancos,
    bancos_code,
    busca_cep,
    busca_localicade,
    previsao_tempo_lat_long,
    # previsao_por_codigo_cidade_hoje,
    # previsao_clima_por_codigo_cidade_proximos_dias,
    pesquisa_cidades_por_ddd,
    feriados_brasil,
]
