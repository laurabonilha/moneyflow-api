from flask import Blueprint, jsonify, request
from models.categoria import (
    inserir_categoria,
    listar_categorias,
    buscar_categoria,
    deletar_categoria,
    buscar_categoria_por_nome
)

categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route('/categorias', methods=['POST'])
def criar_categoria():
    """
    Cria uma nova categoria
    ---
    tags:
      - Categorias
    parameters:
      - in: body
        name: body
        description: Dados da nova categoria
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              example: "Lazer"
            icone:
              type: string
              example: "🏖️"
            cor:
              type: string
              example: "#ff5733"
    responses:
      201:
        description: Categoria criada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Categoria criada com sucesso!"
            id:
              type: integer
              example: 1
      400:
        description: Dados inválidos
      409:
        description: Categoria já existente
    """
    dados = request.get_json()

    # Validação dos campos obrigatórios
    if not dados or not dados.get('nome'):
        return jsonify({'erro': 'Campo nome é obrigatório'}), 400

    nome = dados.get('nome').strip()
    
    if not nome:
        return jsonify({'erro': 'Campo nome é obrigatório e não pode conter apenas espaços'}), 400

    # Verifica se já existe uma categoria com o mesmo nome
    if buscar_categoria_por_nome(nome):
        return jsonify({'erro': f"A categoria '{nome}' já está cadastrada"}), 409

    novo_id = inserir_categoria(
        nome=nome,
        icone=dados.get('icone', '📦'),
        cor=dados.get('cor', '#CCCCCC')
    )

    return jsonify({
        'mensagem': 'Categoria criada com sucesso!',
        'id': novo_id
    }), 201


@categorias_bp.route('/categorias', methods=['GET'])
def get_categorias():
    """
    Lista todas as categorias
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: "Alimentação"
              icone:
                type: string
                example: "🍔"
              cor:
                type: string
                example: "#ff0000"
    """
    categorias = listar_categorias()
    return jsonify(categorias), 200


@categorias_bp.route('/categorias/<int:id>', methods=['GET'])
def get_categoria(id):
    """
    Busca uma categoria específica pelo ID
    ---
    tags:
      - Categorias
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da categoria
    responses:
      200:
        description: Detalhes da categoria retornados com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: "Alimentação"
            icone:
              type: string
              example: "🍔"
            cor:
              type: string
              example: "#ff0000"
      404:
        description: Categoria não encontrada
    """
    categoria = buscar_categoria(id)

    if categoria is None:
        return jsonify({'erro': 'Categoria não encontrada'}), 404

    return jsonify(categoria), 200


@categorias_bp.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    """
    Deleta uma categoria existente
    ---
    tags:
      - Categorias
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da categoria a ser deletada
    responses:
      200:
        description: Categoria deletada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Categoria deletada com sucesso!"
      404:
        description: Categoria não encontrada
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Categoria não encontrada"
    """
    deletado = deletar_categoria(id)

    if not deletado:
        return jsonify({'erro': 'Categoria não encontrada'}), 404

    return jsonify({'mensagem': 'Categoria deletada com sucesso!'}), 200