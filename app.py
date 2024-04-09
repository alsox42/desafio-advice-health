# app.py
from flask import Flask
from app.config.config import Config
from app.models.class_models import db
from app.routes.proprietario import proprietario_rotas
from app.routes.carro import carro_rotas

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
proprietario_rotas(app)
carro_rotas(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
