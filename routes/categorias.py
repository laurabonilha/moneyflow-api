from flask import Blueprint, jsonify, request
from models.categoria import (
    inserir_categoria,
    listar_categorias,
    buscar_categoria,
    deletar_categoria
)

categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route('/categorias', methods=['POST'])
def criar_categoria():
    dados = request.get_json()

    # Validação dos campos obrigatórios
    if not dados or not dados.get('nome'):
        return jsonify({'erro': 'Campo nome é obrigatório'}), 400

    novo_id = inserir_categoria(
        nome=dados.get('nome'),
        icone=dados.get('icone', '📦'),
        cor=dados.get('cor', '#CCCCCC')
    )

    return jsonify({
        'mensagem': 'Categoria criada com sucesso!',
        'id': novo_id
    }), 201


@categorias_bp.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = listar_categorias()
    return jsonify(categorias), 200


@categorias_bp.route('/categorias/<int:id>', methods=['GET'])
def get_categoria(id):
    categoria = buscar_categoria(id)

    if categoria is None:
        return jsonify({'erro': 'Categoria não encontrada'}), 404

    return jsonify(categoria), 200


@categorias_bp.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    deletado = deletar_categoria(id)

    if not deletado:
        return jsonify({'erro': 'Categoria não encontrada'}), 404

    return jsonify({'mensagem': 'Categoria deletada com sucesso!'}), 200