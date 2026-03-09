from flask import Blueprint, jsonify, request
from models.transacao import (
    inserir_transacao,
    listar_transacoes,
    buscar_transacao,
    listar_por_mes,
    deletar_transacao
)

transacoes_bp = Blueprint('transacoes', __name__)


@transacoes_bp.route('/transacoes', methods=['POST'])
def criar_transacao():
    dados = request.get_json()

    # Validação dos campos obrigatórios
    campos = ['descricao', 'valor', 'tipo', 'data']
    for campo in campos:
        if not dados or not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400

    if dados['tipo'] not in ['receita', 'despesa']:
        return jsonify({'erro': 'Tipo deve ser receita ou despesa'}), 400

    novo_id = inserir_transacao(
        descricao=dados['descricao'],
        valor=float(dados['valor']),
        tipo=dados['tipo'],
        categoria_id=dados.get('categoria_id'),
        data=dados['data']
    )

    return jsonify({
        'mensagem': 'Transação criada com sucesso!',
        'id': novo_id
    }), 201


@transacoes_bp.route('/transacoes', methods=['GET'])
def get_transacoes():
    transacoes = listar_transacoes()
    return jsonify(transacoes), 200


@transacoes_bp.route('/transacoes/<int:id>', methods=['GET'])
def get_transacao(id):
    transacao = buscar_transacao(id)

    if transacao is None:
        return jsonify({'erro': 'Transação não encontrada'}), 404

    return jsonify(transacao), 200


@transacoes_bp.route('/transacoes/mes/<int:ano>/<int:mes>', methods=['GET'])
def get_transacoes_mes(ano, mes):
    if mes < 1 or mes > 12:
        return jsonify({'erro': 'Mês inválido'}), 400

    transacoes = listar_por_mes(ano, mes)
    return jsonify(transacoes), 200


@transacoes_bp.route('/transacoes/<int:id>', methods=['DELETE'])
def delete_transacao(id):
    deletado = deletar_transacao(id)

    if not deletado:
        return jsonify({'erro': 'Transação não encontrada'}), 404

    return jsonify({'mensagem': 'Transação deletada com sucesso!'}), 200