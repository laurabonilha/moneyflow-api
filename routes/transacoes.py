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
    """
    Cria uma nova transação
    ---
    tags:
      - Transações
    parameters:
      - in: body
        name: body
        description: Dados da nova transação
        required: true
        schema:
          type: object
          required:
            - descricao
            - valor
            - tipo
            - data
          properties:
            descricao:
              type: string
              example: "Compra no mercado"
            valor:
              type: number
              example: 150.50
            tipo:
              type: string
              enum: [receita, despesa]
              example: "despesa"
            categoria_id:
              type: integer
              example: 1
            data:
              type: string
              format: date
              example: "2023-10-15"
    responses:
      201:
        description: Transação criada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Transação criada com sucesso!"
            id:
              type: integer
              example: 1
      400:
        description: Dados inválidos
    """
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
    """
    Lista todas as transações
    ---
    tags:
      - Transações
    responses:
      200:
        description: Lista de transações retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              descricao:
                type: string
                example: "Salário"
              valor:
                type: number
                example: 5000.00
              tipo:
                type: string
                example: "receita"
              data:
                type: string
                example: "2023-10-01"
              categoria_id:
                type: integer
                example: 2
    """
    transacoes = listar_transacoes()
    return jsonify(transacoes), 200


@transacoes_bp.route('/transacoes/<int:id>', methods=['GET'])
def get_transacao(id):
    """
    Busca uma transação específica pelo ID
    ---
    tags:
      - Transações
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da transação
    responses:
      200:
        description: Detalhes da transação retornados com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            descricao:
              type: string
              example: "Salário"
            valor:
              type: number
              example: 5000.00
            tipo:
              type: string
              example: "receita"
            data:
              type: string
              example: "2023-10-01"
            categoria_id:
              type: integer
              example: 2
      404:
        description: Transação não encontrada
    """
    transacao = buscar_transacao(id)

    if transacao is None:
        return jsonify({'erro': 'Transação não encontrada'}), 404

    return jsonify(transacao), 200


@transacoes_bp.route('/transacoes/mes/<int:ano>/<int:mes>', methods=['GET'])
def get_transacoes_mes(ano, mes):
    """
    Lista transações de um mês e ano específicos
    ---
    tags:
      - Transações
    parameters:
      - in: path
        name: ano
        type: integer
        required: true
        description: Ano (exemplo 2023)
      - in: path
        name: mes
        type: integer
        required: true
        description: Mês (1-12)
    responses:
      200:
        description: Transações do mês retornadas com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              descricao:
                type: string
              valor:
                type: number
              tipo:
                type: string
              data:
                type: string
              categoria_id:
                type: integer
      400:
        description: Mês inválido
    """
    if mes < 1 or mes > 12:
        return jsonify({'erro': 'Mês inválido'}), 400

    transacoes = listar_por_mes(ano, mes)
    return jsonify(transacoes), 200


@transacoes_bp.route('/transacoes/<int:id>', methods=['DELETE'])
def delete_transacao(id):
    """
    Deleta uma transação existente
    ---
    tags:
      - Transações
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da transação a ser deletada
    responses:
      200:
        description: Transação deletada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Transação deletada com sucesso!"
      404:
        description: Transação não encontrada
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Transação não encontrada"
    """
    deletado = deletar_transacao(id)

    if not deletado:
        return jsonify({'erro': 'Transação não encontrada'}), 404

    return jsonify({'mensagem': 'Transação deletada com sucesso!'}), 200