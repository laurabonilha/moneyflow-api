from flask import Flask
from flask_cors import CORS
from database import init_db

app = Flask(__name__)
CORS(app)

# Cria as tabelas ao iniciar o servidor
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)