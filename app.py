from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from database import init_db

app = Flask(__name__)
CORS(app)  # Libera o front-end acessar a API
Swagger(app, template={
    "info": {
        "title": "MoneyFlow API",
        "description": "API para o aplicativo de controle financeiro MoneyFlow",
        "version": "1.0.0"
    }
})

# Cria as tabelas ao iniciar conectando o SQLAlchemy no App
init_db(app)

from routes.categorias import categorias_bp
from routes.transacoes import transacoes_bp
from routes.resumo import resumo_bp

# Registra os blueprints — equivale ao include() do urls.py do Django
app.register_blueprint(categorias_bp)
app.register_blueprint(transacoes_bp)
app.register_blueprint(resumo_bp)

if __name__ == '__main__':
    app.run(debug=True)