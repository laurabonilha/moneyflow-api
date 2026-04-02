from pydantic import BaseModel
from typing import Optional, List


class CategoriaSchema(BaseModel):
    """Define como uma nova categoria a ser inserida deve ser representada."""
    nome: str = "Alimentação"
    icone: Optional[str] = "🍔"
    cor: Optional[str] = "#ff0000"


class CategoriaBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca por ID."""
    id: int = 1


class CategoriaViewSchema(BaseModel):
    """Define como uma categoria será retornada."""
    id: int = 1
    nome: str = "Alimentação"
    icone: Optional[str] = "🍔"
    cor: Optional[str] = "#ff0000"


class ListagemCategoriasSchema(BaseModel):
    """Define como uma listagem de categorias será retornada."""
    categorias: List[CategoriaViewSchema]


class CategoriaDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma remoção."""
    mensagem: str
    id: int


def apresenta_categoria(categoria) -> dict:
    """Retorna uma representação da categoria seguindo o schema definido
    em CategoriaViewSchema.
    """
    return {
        "id": categoria.id,
        "nome": categoria.nome,
        "icone": categoria.icone,
        "cor": categoria.cor,
    }


def apresenta_categorias(categorias) -> dict:
    """Retorna uma representação da listagem de categorias seguindo o schema
    definido em ListagemCategoriasSchema.
    """
    result = []
    for categoria in categorias:
        result.append({
            "id": categoria.id,
            "nome": categoria.nome,
            "icone": categoria.icone,
            "cor": categoria.cor,
        })

    return {"categorias": result}
