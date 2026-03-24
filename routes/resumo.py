from flask import Blueprint, jsonify
from database import db
from models.transacao import Transacao
from models.categoria import Categoria
from sqlalchemy import func

resumo_bp = Blueprint('resumo', __name__)

@resumo_bp.route('/resumo', methods=['GET'])
def get_resumo():
    """
    Retorna o resumo financeiro atual
    ---
    tags:
      - Resumo
    responses:
      200:
        description: Resumo financeiro retornado com sucesso
        schema:
          type: object
          properties:
            total_receitas:
              type: number
              example: 5000.00
            total_despesas:
              type: number
              example: 1500.50
            saldo:
              type: number
              example: 3499.50
    """
    total_receitas = db.session.query(func.coalesce(func.sum(Transacao.valor), 0)).filter(Transacao.tipo == 'receita').scalar()
    total_despesas = db.session.query(func.coalesce(func.sum(Transacao.valor), 0)).filter(Transacao.tipo == 'despesa').scalar()
    
    saldo = total_receitas - total_despesas

    return jsonify({
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo
    }), 200

@resumo_bp.route('/resumo/categorias', methods=['GET'])
def get_resumo_categorias():
    """
    Retorna o total de despesas agrupado por categoria
    ---
    tags:
      - Resumo
    responses:
      200:
        description: Resumo por categoria retornado com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              categoria:
                type: string
                example: "Alimentação"
              cor:
                type: string
                example: "#ff0000"
              icone:
                type: string
                example: "🍔"
              total:
                type: number
                example: 450.00
    """
    resultados = db.session.query(
        Categoria.nome.label('categoria'),
        Categoria.cor.label('cor'),
        Categoria.icone.label('icone'),
        func.coalesce(func.sum(Transacao.valor), 0).label('total')
    ).outerjoin(Transacao, (Categoria.id == Transacao.categoria_id) & (Transacao.tipo == 'despesa')) \
     .group_by(Categoria.id) \
     .order_by(func.coalesce(func.sum(Transacao.valor), 0).desc()).all()

    dados = [
        {
            "categoria": r.categoria,
            "cor": r.cor,
            "icone": r.icone,
            "total": r.total
        } for r in resultados
    ]

    return jsonify(dados), 200