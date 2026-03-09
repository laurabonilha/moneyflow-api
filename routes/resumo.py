from flask import Blueprint, jsonify
from database import get_connection

resumo_bp = Blueprint('resumo', __name__)


@resumo_bp.route('/resumo', methods=['GET'])
def get_resumo():
    conn = get_connection()
    cursor = conn.cursor()

    # Calcula receitas, despesas e saldo em uma única query
    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END), 0) AS total_receitas,
            COALESCE(SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END), 0) AS total_despesas,
            COALESCE(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE -valor END), 0) AS saldo
        FROM transacoes
    """)
    # COALESCE garante que retorna 0 ao invés de NULL quando não há transações

    resultado = dict(cursor.fetchone())
    conn.close()
    return jsonify(resultado), 200


@resumo_bp.route('/resumo/categorias', methods=['GET'])
def get_resumo_categorias():
    conn = get_connection()
    cursor = conn.cursor()

    # Agrupa total de despesas por categoria — para o gráfico de pizza
    cursor.execute("""
        SELECT
            c.nome  AS categoria,
            c.cor   AS cor,
            c.icone AS icone,
            COALESCE(SUM(t.valor), 0) AS total
        FROM categorias c
        LEFT JOIN transacoes t
            ON c.id = t.categoria_id AND t.tipo = 'despesa'
        GROUP BY c.id, c.nome, c.cor, c.icone
        ORDER BY total DESC
    """)

    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(resultado), 200