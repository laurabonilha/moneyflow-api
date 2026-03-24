from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    """
    Cria a conexão inicial do SQLAlchemy com a integração do Flask.
    """
    # Define o path do sqlite na mesma pasta que já estava
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'moneyflow.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        # Import models inside so that they are registered on the metadata
        from models.categoria import Categoria
        from models.transacao import Transacao
        
        db.create_all()
        print("✅ Banco de dados inicializado via SQLAlchemy com sucesso!")