from pydantic import BaseModel
from typing import Optional, List


class TransacaoSchema(BaseModel):
    """Define como uma nova transação a ser inserida deve ser representada."""
    descricao: str = "Compra no mercado"
    valor: float = 150.50
    tipo: str = "despesa"
    categoria_id: Optional[int] = 1
    data: str = "2023-10-15"


class TransacaoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca por ID."""
    id: int = 1


class TransacaoMesSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca por mês."""
    ano: int = 2023
    mes: int = 10


class TransacaoViewSchema(BaseModel):
    """Define como uma transação será retornada."""
    id: int = 1
    descricao: str = "Compra no mercado"
    valor: float = 150.50
    tipo: str = "despesa"
    data: str = "2023-10-15"
    criado_em: Optional[str] = "2023-10-15 14:30:00"
    categoria_id: Optional[int] = 1
    categoria_nome: Optional[str] = "Alimentação"
    categoria_icone: Optional[str] = "🍔"
    categoria_cor: Optional[str] = "#ff0000"


class ListagemTransacoesSchema(BaseModel):
    """Define como uma listagem de transações será retornada."""
    transacoes: List[TransacaoViewSchema]


class TransacaoDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma remoção."""
    mensagem: str
    id: int


def apresenta_transacao(transacao) -> dict:
    """Retorna uma representação da transação seguindo o schema definido
    em TransacaoViewSchema.
    """
    return {
        "id": transacao.id,
        "descricao": transacao.descricao,
        "valor": transacao.valor,
        "tipo": transacao.tipo,
        "data": transacao.data,
        "criado_em": transacao.criado_em.strftime('%Y-%m-%d %H:%M:%S') if transacao.criado_em else None,
        "categoria_id": transacao.categoria_id,
        "categoria_nome": transacao.categoria.nome if transacao.categoria else None,
        "categoria_icone": transacao.categoria.icone if transacao.categoria else None,
        "categoria_cor": transacao.categoria.cor if transacao.categoria else None,
    }


def apresenta_transacoes(transacoes) -> dict:
    """Retorna uma representação da listagem de transações seguindo o schema
    definido em ListagemTransacoesSchema.
    """
    result = []
    for t in transacoes:
        result.append({
            "id": t.id,
            "descricao": t.descricao,
            "valor": t.valor,
            "tipo": t.tipo,
            "data": t.data,
            "criado_em": t.criado_em.strftime('%Y-%m-%d %H:%M:%S') if t.criado_em else None,
            "categoria_id": t.categoria_id,
            "categoria_nome": t.categoria.nome if t.categoria else None,
            "categoria_icone": t.categoria.icone if t.categoria else None,
            "categoria_cor": t.categoria.cor if t.categoria else None,
        })

    return {"transacoes": result}
