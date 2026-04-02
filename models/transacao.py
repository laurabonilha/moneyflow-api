from database import db
from datetime import datetime

class Transacao(db.Model):
    __tablename__ = 'transacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(20), nullable=False) # 'receita' ou 'despesa'
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    data = db.Column(db.String(20), nullable=False) # YYYY-MM-DD
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento automático com a tabela Categoria
    categoria = db.relationship('Categoria', backref='transacoes')