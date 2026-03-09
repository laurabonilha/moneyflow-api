import sqlite3

# Nome do arquivo do banco de dados
DATABASE = 'moneyflow.db'


def get_connection():
    """
    Abre e retorna uma conexão com o banco SQLite.
    """
    conn = sqlite3.connect(DATABASE)

    # Isso faz o SQLite retornar as linhas como dicionários
    # ex: {"id": 1, "nome": "Alimentação"} ao invés de (1, "Alimentação")
    # Equivale ao cursor_factory=RealDictCursor do Django/Postgres
    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    """
    Cria as tabelas no banco se elas ainda não existirem.
    Equivale ao 'migrate' do Django.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de categorias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT NOT NULL,
            icone     TEXT,
            cor       TEXT
        )
    """)

    # Tabela de transações — note o FOREIGN KEY referenciando categorias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao    TEXT NOT NULL,
            valor        REAL NOT NULL,
            tipo         TEXT NOT NULL CHECK(tipo IN ('receita', 'despesa')),
            categoria_id INTEGER,
            data         TEXT NOT NULL,
            criado_em    TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso!")