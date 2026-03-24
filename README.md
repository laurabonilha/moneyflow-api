# MoneyFlow API 💸

**MoneyFlow API** é o backend do sistema MoneyFlow, uma aplicação voltada para o controle financeiro pessoal. Desenvolvida em **Python** utilizando o microframework **Flask**, esta API fornece todos os endpoints necessários para o gerenciamento de transações (receitas e despesas), organização por categorias personalizadas e visualização de resumos financeiros.

---

## 🚀 Funcionalidades Principais

- **Transações:** Cadastro, listagem, exclusão e busca de receitas e despesas.
- **Categorias:** Criação de categorias personalizadas (com ícone e cor) para organização das finanças.
- **Resumos:** Cálculo automático de saldos totais, controle de despesas agrupadas por categorias e possibilidade de buscar relatórios por mês específico.
- **Documentação Interativa (Swagger):** API totalmente documentada via Swagger/OpenAPI.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Flask** (Microframework Web)
- **SQLite3** (Banco de Dados relacional nativo)
- **Flasgger** (Geração da documentação Swagger)
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
- `POST /transacoes` - Cadastra uma nova transação.
- `GET /transacoes/mes/<ano>/<mes>` - Filtra o extrato de transações de um mês e ano específicos.
- `DELETE /transacoes/<id>` - Estorna/Exclui um registro.

**Categorias:**
- `GET /categorias` - Lista todas as categorias (Ex: Moradia, Alimentação, Lazer).
- `POST /categorias` - Cria uma categoria com ícone e cores customizados.
- `DELETE /categorias/<id>` - Remove uma categoria do sistema.

**Resumos (Dashboards):**
- `GET /resumo` - Exibe os totais de receitas, despesas e o saldo atual disponível.
- `GET /resumo/categorias` - Soma todas as despesas e as agrupa por categoria (ideal para gráficos).

---

## 📚 Documentação da API (Swagger/OpenAPI)

A demonstração e documentação completas dos endpoints podem ser acessadas de forma interativa diretamente pelo navegador através da interface do Swagger. 

Com a aplicação rodando (etapa 4), acesse o seguinte endereço no seu navegador:

👉 **[http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/)**

Lá você encontrará a descrição de cada rota da API, os métodos HTTP permitidos (GET, POST, DELETE), além da estrutura exata esperada em cada requisição e cada resposta!

---

## 📌 Organização do Código

- `app.py`: Arquivo principal que inicia a aplicação Flask e as configurações do Swagger e do contexto.
- `database.py`: Funções responsáveis pela conexão com o SQLite.
- `models/`: Contém arquivos de regras de negócios e escopo da persistência de dados.
- `routes/`: Contém os "Blueprints" (rotas separadas) organizados por área (`categorias.py`, `transacoes.py`, `resumo.py`).

---
Feito com ❤️ para o controle eficiente do seu dinheiro.
