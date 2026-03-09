from flask import Flask
from flask_cors import CORS
from database import init_db
from routes.categorias import categorias_bp
from routes.transacoes import transacoes_bp
from routes.resumo import resumo_bp

app = Flask(__name__)
CORS(app)  # Libera o front-end acessar a API

# Registra os blueprints — equivale ao include() do urls.py do Django
app.register_blueprint(categorias_bp)
app.register_blueprint(transacoes_bp)
app.register_blueprint(resumo_bp)

# Cria as tabelas ao iniciar
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)