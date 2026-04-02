from pydantic import BaseModel
from typing import Optional, List


class ResumoViewSchema(BaseModel):
    """Define como o resumo financeiro será retornado."""
    total_receitas: float = 5000.00
    total_despesas: float = 1500.50
    saldo: float = 3499.50


class ResumoCategoriaSchema(BaseModel):
    """Define como o resumo por categoria será retornado."""
    categoria: str = "Alimentação"
    cor: Optional[str] = "#ff0000"
    icone: Optional[str] = "🍔"
    total: float = 450.00


class ListagemResumoCategoriaSchema(BaseModel):
    """Define como a listagem do resumo por categorias será retornada."""
    resumo_categorias: List[ResumoCategoriaSchema]
