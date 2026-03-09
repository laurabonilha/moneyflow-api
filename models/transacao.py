from database import get_connection


def inserir_transacao(descricao, valor, tipo, categoria_id, data):
    """
    Insere uma nova transação no banco.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transacoes (descricao, valor, tipo, categoria_id, data)
        VALUES (?, ?, ?, ?, ?)
    """, (descricao, valor, tipo, categoria_id, data))

    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id


def listar_transacoes():
    """
    Retorna todas as transações com o nome da categoria junto.
    Aqui usamos JOIN — equivale ao select_related() do Django.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # O JOIN traz os dados da categoria junto com a transação
    # Assim o front-end recebe tudo em uma única chamada
    cursor.execute("""
        SELECT
            t.id,
            t.descricao,
            t.valor,
            t.tipo,
            t.data,
            t.criado_em,
            t.categoria_id,
            c.nome  AS categoria_nome,
            c.icone AS categoria_icone,
            c.cor   AS categoria_cor
        FROM transacoes t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        ORDER BY t.data DESC, t.criado_em DESC
    """)

    transacoes = cursor.fetchall()
    conn.close()
    return [dict(t) for t in transacoes]


def buscar_transacao(id):
    """
    Retorna uma transação pelo id, com dados da categoria.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.id,
            t.descricao,
            t.valor,
            t.tipo,
            t.data,
            t.criado_em,
            t.categoria_id,
            c.nome  AS categoria_nome,
            c.icone AS categoria_icone,
            c.cor   AS categoria_cor
        FROM transacoes t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        WHERE t.id = ?
    """, (id,))

    transacao = cursor.fetchone()
    conn.close()

    if transacao is None:
        return None

    return dict(transacao)


def listar_por_mes(ano, mes):
    """
    Filtra transações por mês e ano.
    Usa strftime do SQLite para extrair mês e ano do campo data.
    Equivale ao filter(data__year=ano, data__month=mes) do Django.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.id,
            t.descricao,
            t.valor,
            t.tipo,
            t.data,
            t.criado_em,
            t.categoria_id,
            c.nome  AS categoria_nome,
            c.icone AS categoria_icone,
            c.cor   AS categoria_cor
        FROM transacoes t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        WHERE strftime('%Y', t.data) = ?
          AND strftime('%m', t.data) = ?
        ORDER BY t.data DESC
    """, (str(ano), str(mes).zfill(2)))
    # zfill(2) garante que o mês tenha 2 dígitos: 3 → "03"

    transacoes = cursor.fetchall()
    conn.close()
    return [dict(t) for t in transacoes]


def deletar_transacao(id):
    """
    Deleta uma transação pelo id.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM transacoes WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        return False

    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return True