from database import db

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    icone = db.Column(db.String(50))
    cor = db.Column(db.String(50))
    
    # Opcional: serialize método útil para jsonify
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "icone": self.icone,
            "cor": self.cor
        }

def inserir_categoria(nome, icone, cor):
    nova_categoria = Categoria(nome=nome, icone=icone, cor=cor)
    db.session.add(nova_categoria)
    db.session.commit()
    return nova_categoria.id

def listar_categorias():
    return [c.to_dict() for c in Categoria.query.order_by(Categoria.nome).all()]

def buscar_categoria(id):
    categoria = Categoria.query.get(id)
    return categoria.to_dict() if categoria else None

def deletar_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return False
    db.session.delete(categoria)
    db.session.commit()
    return True