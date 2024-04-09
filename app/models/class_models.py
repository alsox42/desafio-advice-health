from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Proprietario(db.Model):
    __tablename__ = 'proprietarios'
    id = db.Column(Integer, primary_key=True)
    nome = db.Column(String)
    carros = relationship("Carro", back_populates="proprietario")

    def __repr__(self):
       return f'<Modelo {self.modelo} Cor {self.cor}  '
    
    def calcular_total_carros(self):
        return len(self.carros)


class Carro(db.Model):
    __tablename__ = 'carros'
    id = db.Column(Integer, primary_key=True)
    modelo = db.Column(String)
    cor = db.Column(String)
    proprietario_id = db.Column(Integer, ForeignKey('proprietarios.id'))
    proprietario = relationship("Proprietario", back_populates="carros")

    def __repr__(self):
        return f'<Nome {self.nome}>'
    
    def formatar(self):
        return {'modelo': self.modelo, 'cor': self.cor}

