from pydantic import BaseModel, EmailStr #Classe mãe das validações e EmailStr para conferir se é um email valido.
from typing import Optional, List # para campos nao obrigatorios de preencher
from enum import Enum
from datetime import date

class UsuariosBase(BaseModel):
    telefone : str
    nome : str
    email: EmailStr #Usa o EmailStr para validação de email.
    cpf : str
    data_nascimento: date
    cargo: Optional[str] = "Cliente" #Caso não enviem nada o padrão é cliente

class UsuarioCreate(UsuariosBase):
    senha: str
    confirma_senha: str

class UsuarioOut(UsuariosBase):
    pass

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class LoginOut(BaseModel):
    nome: str
    cargo: str
    mensagem: str

class CanaisAtendimento(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class StatusPagamento(str, Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGAMENTO_APROVADO = "PAGAMENTO_APROVADO"
    PAGAMENTO_RECUSADO = "PAGAMENTO_RECUSADO"

class ItemPedido(BaseModel):
    cardapio_id: int
    quantidade: int

class PedidoCreate(BaseModel):
    canalPedido: CanaisAtendimento
    unidade_id : int
    cliente_telefone: str
    itens: List[ItemPedido]

class PedidoOut(BaseModel):
    id: int
    cliente_telefone: str
    status_pedido: str

class PedidoUpdate(BaseModel):
    status_pedido: str
    status_pagamento: StatusPagamento = "AGUARDANDO_PAGAMENTO"

class CardapioBase(BaseModel):
    id: int
    prato: str
    preco: float

class CardapioCreate (BaseModel):
    prato: str
    preco: float

class CardapioOut(CardapioBase):
    pass

class CardapioUpdate(BaseModel):
    preco: float

class EstoqueBase(BaseModel):
    unidade_id: int
    cardapio_id: int
    quantidade: int

class EstoqueCreate(EstoqueBase):
    pass

class EstoqueOut(BaseModel):
    id: int
    prato: str
    preco: float
    quantidade: int

class EstoqueUpdate (EstoqueBase):
    pass 

class UnidadeBase(BaseModel):
    id: int
    nome: str
    gerente : str

class UnidadeCreate(BaseModel):
    nome: str
    gerente: str

class UnidadeOut(UnidadeBase):
    pass
