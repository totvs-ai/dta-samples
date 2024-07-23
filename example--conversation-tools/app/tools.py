from typing import List
from langchain_core.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, Literal

fake_today = "2024-04-01"
fake_now = f"{fake_today}T14:00:00Z"


@tool
def contatos(empresa: str, cargo: Optional[str] = None) -> List[dict]:
    """Buscar contatos (nome, phone, email) por empresa e cargos (opcional)"""
    return [
        {
            "name": "João Silva",
            "phone": "41999944455",
            "email": f"joao@{empresa}.com",
            "address": "Rua Getúlio Vargas, 589 - Rebouças, SP",
        }
    ]


class CalendarSchema(BaseModel):
    datetime_initial: str = Field(description="datetime YYYY-MM-DDThh:mm:ssZ")
    datetime_final: str = Field(description="datetime YYYY-MM-DDThh:mm:ssZ")


@tool("agenda", args_schema=CalendarSchema, return_direct=False)
def calendar(datetime_initial: str, datetime_final: str) -> List[dict]:
    """Pequisar agenda para datas fornecidas"""
    return [
        {
            "entry": "Compromisso importante",
            "datetime_start": f"{fake_today}T10:00:00",
            "datetime_end": f"{fake_today}T12:00:00Z",
        },
        {
            "entry": "Apresentação Projeto ABC",
            "datetime_start": f"{fake_today}T14:00:00",
            "datetime_end": f"{fake_today}T15:00:00Z",
        },
        {
            "entry": "Webinar XYZ",
            "datetime_start": f"{fake_today}T16:00:00",
            "datetime_end": f"{fake_today}T17:00:00Z",
        },
    ]


class ContratosSchema(BaseModel):
    empresa: Optional[str] = None
    status: Optional[Literal["open", "pending", "canceled", "closed"]] = None
    date_created: Optional[str] = Field(
        description="datetime YYYY-MM-DDThh:mm:ssZ", default=None
    )
    date_updated: Optional[str] = Field(
        description="datetime YYYY-MM-DDThh:mm:ssZ", default=None
    )


@tool("contratos", args_schema=ContratosSchema)
def contract(
    empresa: Optional[str] = None,
    status: Optional[str] = None,
    date_created: Optional[str] = None,
    date_updated: Optional[str] = None,
) -> List[dict]:
    """Pesquisar contratos por empresa, ou por status, ou por data de criação ou por data de atualização. Datas no formato YYYY-MM-DD"""
    return [
        {
            "contract:": "Contrato X",
            "empresa": "X",
            "status": "pending",
            "created_at": f"{fake_today}T09:35:00Z",
            "updated_at": f"{fake_today}T15:55:00Z",
        },
        {
            "contract:": "Contrato XY",
            "empresa": "XY",
            "status": "canceled",
            "created_at": f"{fake_today}T09:35:00Z",
            "updated_at": f"{fake_today}T15:55:00Z",
        },
        {
            "contract:": "Contrato LoremIpsum",
            "empresa": "LoremIpsum",
            "status": "pending",
            "created_at": f"{fake_today}T09:35:00Z",
            "updated_at": f"{fake_today}T15:55:00Z",
        },
        {
            "contract:": "Contrato Fantastic",
            "empresa": "Fantastic",
            "status": "closed",
            "created_at": f"{fake_today}T09:35:00Z",
            "updated_at": f"{fake_today}T15:55:00Z",
        },
        {
            "contract:": "Contrato Emblemático",
            "empresa": "Amber",
            "status": "open",
            "created_at": f"{fake_today}T09:35:00Z",
            "updated_at": f"{fake_today}T15:55:00Z",
        },
    ]


tools_list = [contatos, calendar, contract]
