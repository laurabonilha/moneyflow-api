from flask_openapi3 import APIBlueprint, Tag

from database import db
from logger import logger
from models.transacao import Transacao

from schemas import (
    TransacaoSchema,
    TransacaoViewSchema,
    TransacaoBuscaSchema,
    TransacaoMesSchema,
    TransacaoDelSchema,
    ListagemTransacoesSchema,
    ErrorSchema,
    apresenta_transacao,
    apresenta_transacoes,
)

transacao_tag = Tag(name="Transação", description="Adição, visualização e remoção de transações à base")
transacoes_bp = APIBlueprint('transacoes', __name__)


@transacoes_bp.post('/transacoes', tags=[transacao_tag],
                    responses={"201": TransacaoViewSchema, "400": ErrorSchema})
def criar_transacao(body: TransacaoSchema):
    """Adiciona uma nova Transação à base de dados

    Retorna uma representação da transação criada.
    """
    if body.tipo not in ['receita', 'despesa']:
        logger.warning(f"Erro ao adicionar transação: Tipo '{body.tipo}' inválido")
        return {"erro": "Tipo deve ser receita ou despesa"}, 400

    transacao = Transacao(
        descricao=body.descricao,
        valor=body.valor,
        tipo=body.tipo,
        categoria_id=body.categoria_id,
        data=body.data
    )
    logger.debug(f"Adicionando transação: '{transacao.descricao}'")
    db.session.add(transacao)
    db.session.commit()
    logger.debug(f"Adicionada transação: '{transacao.descricao}'")

    return apresenta_transacao(transacao), 201


@transacoes_bp.get('/transacoes', tags=[transacao_tag],
                   responses={"200": ListagemTransacoesSchema})
def get_transacoes():
    """Faz a busca por todas as Transações cadastradas

    Retorna uma representação da listagem de transações.
    """
    logger.debug("Coletando transações")
    transacoes = Transacao.query.order_by(
        Transacao.data.desc(), Transacao.criado_em.desc()
    ).all()

    if not transacoes:
        return {"transacoes": []}, 200

    logger.debug(f"{len(transacoes)} transações encontradas")
    return apresenta_transacoes(transacoes), 200


@transacoes_bp.get('/transacoes/<int:id>', tags=[transacao_tag],
                   responses={"200": TransacaoViewSchema, "404": ErrorSchema})
def get_transacao(path: TransacaoBuscaSchema):
    """Faz a busca por uma Transação a partir do id

    Retorna uma representação da transação.
    """
    logger.debug(f"Coletando dados sobre transação #{path.id}")
    transacao = Transacao.query.get(path.id)

    if not transacao:
        error_msg = "Transação não encontrada"
        logger.warning(f"Erro ao buscar transação '{path.id}', {error_msg}")
        return {"erro": error_msg}, 404

    logger.debug(f"Transação encontrada: '{transacao.descricao}'")
    return apresenta_transacao(transacao), 200


@transacoes_bp.get('/transacoes/mes/<int:ano>/<int:mes>', tags=[transacao_tag],
                   responses={"200": ListagemTransacoesSchema, "400": ErrorSchema})
def get_transacoes_mes(path: TransacaoMesSchema):
    """Faz a busca por Transações de um mês e ano específicos

    Retorna uma representação da listagem de transações do período.
    """
    logger.debug(f"Coletando transações do mês {path.mes}/{path.ano}")
    if path.mes < 1 or path.mes > 12:
        logger.warning(f"Erro ao buscar transações: Mês {path.mes} inválido")
        return {"erro": "Mês inválido"}, 400

    mes_str = str(path.mes).zfill(2)
    ano_str = str(path.ano)

    transacoes = Transacao.query.filter(
        db.func.strftime('%Y', Transacao.data) == ano_str,
        db.func.strftime('%m', Transacao.data) == mes_str
    ).order_by(Transacao.data.desc()).all()

    if not transacoes:
        return {"transacoes": []}, 200

    logger.debug(f"{len(transacoes)} transações encontradas neste mês")
    return apresenta_transacoes(transacoes), 200


@transacoes_bp.delete('/transacoes/<int:id>', tags=[transacao_tag],
                      responses={"200": TransacaoDelSchema, "404": ErrorSchema})
def delete_transacao(path: TransacaoBuscaSchema):
    """Deleta uma Transação a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    logger.debug(f"Deletando dados sobre transação #{path.id}")
    transacao = Transacao.query.get(path.id)

    if not transacao:
        error_msg = "Transação não encontrada"
        logger.warning(f"Erro ao deletar transação #'{path.id}', {error_msg}")
        return {"erro": error_msg}, 404

    db.session.delete(transacao)
    db.session.commit()
    logger.debug(f"Deletada transação #{path.id}")

    return {"mensagem": "Transação deletada com sucesso!", "id": path.id}, 200