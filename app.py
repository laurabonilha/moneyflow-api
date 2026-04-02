from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS
from database import init_db

info = Info(title="MoneyFlow API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Cria as tabelas ao iniciar conectando o SQLAlchemy no App
init_db(app)

# Importa e registra os blueprints (APIBlueprint)
from routes.categorias import categorias_bp
from routes.transacoes import transacoes_bp
from routes.resumo import resumo_bp

app.register_api(categorias_bp)
app.register_api(transacoes_bp)
app.register_api(resumo_bp)

# definindo tag da home
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


if __name__ == '__main__':
    app.run(debug=True)