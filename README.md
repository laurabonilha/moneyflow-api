# MoneyFlow API 💸

**MoneyFlow API** é o backend do sistema MoneyFlow, uma aplicação voltada para o controle financeiro pessoal. Desenvolvida em **Python** utilizando o microframework **Flask** com **flask_openapi3** e **Pydantic**, esta API fornece todos os endpoints necessários para o gerenciamento de transações (receitas e despesas), organização por categorias personalizadas e visualização de resumos financeiros.

---

## 🚀 Funcionalidades Principais

- **Transações:** Cadastro, listagem, exclusão e busca de receitas e despesas.
- **Categorias:** Criação de categorias personalizadas (com ícone e cor) para organização das finanças.
- **Resumos:** Cálculo automático de saldos totais, controle de despesas agrupadas por categorias e possibilidade de buscar relatórios por mês específico.
- **Documentação Interativa (Swagger):** API totalmente documentada via OpenAPI 3.1, com suporte a Swagger, Redoc e RapiDoc.
- **Validação Automática:** Validação dos dados de entrada via Pydantic Schemas.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Flask** (Microframework Web)
- **flask_openapi3** (Geração automática da documentação OpenAPI/Swagger)
- **Pydantic** (Validação de dados e definição de schemas)
- **Flask-SQLAlchemy** (ORM para integração com banco de dados)
- **SQLite3** (Banco de Dados relacional)
- **Flask-CORS** (Integração e permissão de acesso com o Front-end)

---

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de ter o [Python](https://www.python.org/downloads/) (versão 3.8 ou superior) instalado na sua máquina.

---

## 💻 Instruções de Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto localmente:

### 1. Clonar o repositório

Caso ainda não o tenha feito, clone o repositório ou navegue até a pasta do projeto:

```bash
cd moneyflow-api
```

### 2. Criar e Ativar um Ambiente Virtual (Recomendado)

O ambiente virtual (venv) evita conflitos de versão entre as bibliotecas desta API e de outros projetos Python.

- **No Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **No macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias que estão listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Inicializar a Aplicação

A inicialização criará automaticamente o banco de dados SQLite (`moneyflow.db`) caso não exista. Para rodar o servidor, execute:

```bash
python app.py
```

*A API estará rodando por padrão em `http://127.0.0.1:5000`.*

---

## 🗺️ Principais Rotas da API

Nesta API web, você tem as seguintes capacidades divididas por entidades de negócios:

**Transações:**
- `GET /transacoes` - Lista todas as transações de receitas e despesas.
- `POST /transacoes` - Cadastra uma nova transação (validada via `TransacaoSchema`).
- `GET /transacoes/<id>` - Busca uma transação específica pelo ID.
- `GET /transacoes/mes/<ano>/<mes>` - Filtra o extrato de transações de um mês e ano específicos.
- `DELETE /transacoes/<id>` - Estorna/Exclui um registro.

**Categorias:**
- `GET /categorias` - Lista todas as categorias (Ex: Moradia, Alimentação, Lazer).
- `POST /categorias` - Cria uma categoria com ícone e cores customizados (validada via `CategoriaSchema`).
- `GET /categorias/<id>` - Busca uma categoria específica pelo ID.
- `DELETE /categorias/<id>` - Remove uma categoria do sistema.

**Resumos (Dashboards):**
- `GET /resumo` - Exibe os totais de receitas, despesas e o saldo atual disponível.
- `GET /resumo/categorias` - Soma todas as despesas e as agrupa por categoria (ideal para gráficos).

---

## 📚 Documentação da API (Swagger/OpenAPI)

A documentação completa dos endpoints é gerada automaticamente a partir dos **Pydantic Schemas** e pode ser acessada de forma interativa pelo navegador.

Com a aplicação rodando (etapa 4), acesse o seguinte endereço no seu navegador:

👉 **[http://127.0.0.1:5000/openapi](http://127.0.0.1:5000/openapi)**

Você poderá escolher entre três estilos de documentação:
- **Swagger** — Interface interativa clássica para testar endpoints
- **Redoc** — Documentação legível e organizada
- **RapiDoc** — Interface moderna e customizável

Lá você encontrará a descrição de cada rota da API, os métodos HTTP permitidos (GET, POST, DELETE), além da estrutura exata esperada (schemas) em cada requisição e resposta!

---

## 📂 Estrutura do Projeto

```
moneyflow-api/
│
├── app.py                  # Arquivo principal – inicializa o OpenAPI, CORS e registra os APIBlueprints
├── database.py             # Conexão do SQLAlchemy com o banco de dados SQLite
├── requirements.txt        # Lista de dependências do projeto (pip)
├── moneyflow.db            # Banco de dados SQLite (criado automaticamente na 1ª execução)
├── .gitignore              # Regras de arquivos ignorados pelo Git
├── README.md               # Documentação do projeto (este arquivo)
│
├── models/                 # Camada de modelos – definição das tabelas do banco de dados
│   ├── __init__.py         # Inicializador do pacote models
│   ├── categoria.py        # Modelo SQLAlchemy da tabela Categoria
│   └── transacao.py        # Modelo SQLAlchemy da tabela Transação
│
├── schemas/                # Camada de schemas – validação e formatação de dados (Pydantic)
│   ├── __init__.py         # Exporta todos os schemas para uso nas rotas
│   ├── categoria.py        # Schemas de entrada, saída e busca de Categorias
│   ├── transacao.py        # Schemas de entrada, saída e busca de Transações
│   ├── resumo.py           # Schemas de resposta dos resumos financeiros
│   └── error.py            # Schema padrão para respostas de erro
│
└── routes/                 # Camada de rotas – APIBlueprints Flask (endpoints da API)
    ├── __init__.py          # Inicializador do pacote routes
    ├── categorias.py        # Rotas de Categorias   (GET, POST, DELETE)
    ├── transacoes.py        # Rotas de Transações   (GET, POST, DELETE)
    └── resumo.py            # Rotas de Resumo/Dashboard (GET)
```

### Descrição das Camadas

| Camada | Responsabilidade |
|--------|-----------------|
| **`app.py`** | Ponto de entrada da aplicação. Configura o `OpenAPI` (flask_openapi3), habilita o CORS e registra os APIBlueprints de rotas. |
| **`database.py`** | Gerencia a conexão do Flask-SQLAlchemy com o banco SQLite (`moneyflow.db`) e cria as tabelas automaticamente. |
| **`models/`** | Define a estrutura das tabelas do banco de dados (colunas, tipos e relacionamentos) usando SQLAlchemy. |
| **`schemas/`** | Define os formatos de entrada e saída da API usando Pydantic. Responsável pela validação automática dos dados e geração da documentação OpenAPI. |
| **`routes/`** | Define os endpoints REST da API organizados por domínio, utilizando o padrão de **APIBlueprints** do flask_openapi3. |

---
Feito com ❤️ para o controle eficiente do seu dinheiro.
