from flask_openapi3 import APIBlueprint, Tag

from database import db
from models.categoria import Categoria
from schemas import (
    CategoriaSchema,
    CategoriaViewSchema,
    CategoriaBuscaSchema,
    CategoriaDelSchema,
    ListagemCategoriasSchema,
    ErrorSchema,
    apresenta_categoria,
    apresenta_categorias,
)

categoria_tag = Tag(name="Categoria", description="Adição, visualização e remoção de categorias à base")
categorias_bp = APIBlueprint('categorias', __name__)


@categorias_bp.post('/categorias', tags=[categoria_tag],
                    responses={"201": CategoriaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def criar_categoria(body: CategoriaSchema):
    """Adiciona uma nova Categoria à base de dados

    Retorna uma representação da categoria criada.
    """
    nome = body.nome.strip()

    if not nome:
        return {"erro": "Campo nome é obrigatório e não pode conter apenas espaços"}, 400

    # Verifica se já existe uma categoria com o mesmo nome (case-insensitive)
    categoria_existente = Categoria.query.filter(
        db.func.lower(Categoria.nome) == nome.lower()
    ).first()

    if categoria_existente:
        return {"erro": f"A categoria '{nome}' já está cadastrada"}, 409

    categoria = Categoria(
        nome=nome,
        icone=body.icone or "📦",
        cor=body.cor or "#CCCCCC"
    )
    db.session.add(categoria)
    db.session.commit()

    return apresenta_categoria(categoria), 201


@categorias_bp.get('/categorias', tags=[categoria_tag],
                   responses={"200": ListagemCategoriasSchema})
def get_categorias():
    """Faz a busca por todas as Categorias cadastradas

    Retorna uma representação da listagem de categorias.
    """
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if not categorias:
        return {"categorias": []}, 200

    return apresenta_categorias(categorias), 200


@categorias_bp.get('/categorias/<int:id>', tags=[categoria_tag],
                   responses={"200": CategoriaViewSchema, "404": ErrorSchema})
def get_categoria(path: CategoriaBuscaSchema):
    """Faz a busca por uma Categoria a partir do id

    Retorna uma representação da categoria.
    """
    categoria = Categoria.query.get(path.id)

    if not categoria:
        return {"erro": "Categoria não encontrada"}, 404

    return apresenta_categoria(categoria), 200


@categorias_bp.delete('/categorias/<int:id>', tags=[categoria_tag],
                      responses={"200": CategoriaDelSchema, "404": ErrorSchema})
def delete_categoria(path: CategoriaBuscaSchema):
    """Deleta uma Categoria a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    categoria = Categoria.query.get(path.id)

    if not categoria:
        return {"erro": "Categoria não encontrada"}, 404

    db.session.delete(categoria)
    db.session.commit()

    return {"mensagem": "Categoria deletada com sucesso!", "id": path.id}, 200