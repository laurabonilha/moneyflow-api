from database import db
from datetime import datetime
from sqlalchemy import func

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

    def to_dict(self):
        # Mapeia os dados do JOIN igual era feito manualmente no dict() do fetchall()
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "tipo": self.tipo,
            "data": self.data,
            "criado_em": self.criado_em.strftime('%Y-%m-%d %H:%M:%S') if self.criado_em else None,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "categoria_icone": self.categoria.icone if self.categoria else None,
            "categoria_cor": self.categoria.cor if self.categoria else None
        }

def inserir_transacao(descricao, valor, tipo, categoria_id, data):
    nova_transacao = Transacao(
        descricao=descricao,
        valor=valor,
        tipo=tipo,
        categoria_id=categoria_id,
        data=data
    )
    db.session.add(nova_transacao)
    db.session.commit()
    return nova_transacao.id

def listar_transacoes():
    transacoes = Transacao.query.order_by(Transacao.data.desc(), Transacao.criado_em.desc()).all()
    return [t.to_dict() for t in transacoes]

def buscar_transacao(id):
    t = Transacao.query.get(id)
    return t.to_dict() if t else None

def listar_por_mes(ano, mes):
    # strftime com sqlite funciona convertendo a coluna p/ ano e mes
    mes_str = str(mes).zfill(2)
    ano_str = str(ano)

    transacoes = Transacao.query.filter(
        func.strftime('%Y', Transacao.data) == ano_str,
        func.strftime('%m', Transacao.data) == mes_str
    ).order_by(Transacao.data.desc()).all()
    
    return [t.to_dict() for t in transacoes]

def deletar_transacao(id):
    t = Transacao.query.get(id)
    if not t:
        return False
    db.session.delete(t)
    db.session.commit()
    return True