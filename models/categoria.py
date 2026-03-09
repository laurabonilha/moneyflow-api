from database import get_connection


def inserir_categoria(nome, icone, cor):
    """
    Insere uma nova categoria no banco.
    Equivale ao Categoria.objects.create() do Django.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO categorias (nome, icone, cor)
        VALUES (?, ?, ?)
    """, (nome, icone, cor))
    # Os '?' são placeholders — equivalem ao %s do Django raw SQL
    # NUNCA concatene strings SQL diretamente, isso causa SQL Injection!

    conn.commit()

    # cursor.lastrowid retorna o id do registro recém criado
    # Equivale ao objeto.pk após o .save() do Django
    novo_id = cursor.lastrowid

    conn.close()
    return novo_id


def listar_categorias():
    """
    Retorna todas as categorias.
    Equivale ao Categoria.objects.all() do Django.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categorias ORDER BY nome")
    categorias = cursor.fetchall()
    # fetchall() retorna uma lista de sqlite3.Row
    # Como definimos row_factory no database.py, podemos acessar como dicionário

    conn.close()

    # Convertemos para lista de dicionários para poder serializar em JSON depois
    return [dict(c) for c in categorias]


def buscar_categoria(id):
    """
    Retorna uma categoria pelo id.
    Equivale ao Categoria.objects.get(id=id) do Django.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
    categoria = cursor.fetchone()
    # fetchone() retorna apenas um registro ou None se não encontrar

    conn.close()

    if categoria is None:
        return None  # A rota vai tratar isso como 404

    return dict(categoria)


def deletar_categoria(id):
    """
    Deleta uma categoria pelo id.
    Equivale ao Categoria.objects.get(id=id).delete() do Django.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Primeiro verificamos se existe
    cursor.execute("SELECT id FROM categorias WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        return False  # Não encontrou — a rota retornará 404

    cursor.execute("DELETE FROM categorias WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return True  # Deletou com sucesso — a rota retornará 200