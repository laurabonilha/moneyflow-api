from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify

from database import db
from models.transacao import Transacao
from models.categoria import Categoria
from sqlalchemy import func
from schemas.resumo import (
    ResumoViewSchema,
    ListagemResumoCategoriaSchema,
)

resumo_tag = Tag(name="Resumo", description="Visualização de resumos financeiros e por categoria")
resumo_bp = APIBlueprint('resumo', __name__)


@resumo_bp.get('/resumo', tags=[resumo_tag],
               responses={"200": ResumoViewSchema})
def get_resumo():
    """Retorna o resumo financeiro atual

    Retorna o total de receitas, despesas e o saldo.
    """
    total_receitas = db.session.query(
        func.coalesce(func.sum(Transacao.valor), 0)
    ).filter(Transacao.tipo == 'receita').scalar()

    total_despesas = db.session.query(
        func.coalesce(func.sum(Transacao.valor), 0)
    ).filter(Transacao.tipo == 'despesa').scalar()

    saldo = total_receitas - total_despesas

    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo
    }, 200


@resumo_bp.get('/resumo/categorias', tags=[resumo_tag],
               responses={"200": ListagemResumoCategoriaSchema})
def get_resumo_categorias():
    """Retorna o total de despesas agrupado por categoria

    Retorna uma listagem com categoria, cor, ícone e total de despesas.
    """
    resultados = db.session.query(
        Categoria.nome.label('categoria'),
        Categoria.cor.label('cor'),
        Categoria.icone.label('icone'),
        func.coalesce(func.sum(Transacao.valor), 0).label('total')
    ).outerjoin(
        Transacao,
        (Categoria.id == Transacao.categoria_id) & (Transacao.tipo == 'despesa')
    ).group_by(Categoria.id).order_by(
        func.coalesce(func.sum(Transacao.valor), 0).desc()
    ).all()

    dados = [
        {
            "categoria": r.categoria,
            "cor": r.cor,
            "icone": r.icone,
            "total": r.total
        } for r in resultados
    ]

    return jsonify(dados), 200