from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ProdutoBase(BaseModel):
    nome: str
    preco_unitario: float = Field(gt=0, description="Preço unitário deve ser maior que zero")

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True

class ItemVendaBase(BaseModel):
    nome: str
    quantidade: int = Field(gt=0)
    preco_unitario: float = Field(gt=0)

class VendaCreate(BaseModel):
    id_venda: int
    data: str
    produtos: List[ItemVendaBase]
    valor_total: float

class VendaResponse(BaseModel):
    id: int
    id_venda_original: int
    data: datetime
    valor_total: float

    class Config:
        from_attributes = True
