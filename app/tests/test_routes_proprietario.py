import json
from flask import Flask
from app.models.class_models import db, Proprietario
import pytest


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:postgres@127.0.0.1/db_nork_town'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_criar_proprietario(client):
    # Teste para criar um novo proprietário
    novo_proprietario = {'nome': 'João', 'carros': [{'modelo': 'hatch', 'cor': 'azul'}]}
    response = client.post('/proprietarios', json=novo_proprietario)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['mensagem'] == 'Proprietário criado com sucesso'


def test_criar_proprietario_com_mais_de_tres_carros(client):
    # Teste para criar um proprietário com mais de três carros
    novo_proprietario = {'nome': 'Maria', 'carros': [{'modelo': 'hatch', 'cor': 'azul'}] * 4}
    response = client.post('/proprietarios', json=novo_proprietario)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['erro'] == 'Um proprietário não pode ter mais do que 3 carros'


def test_listar_proprietarios(client):
    # Teste para listar todos os proprietários
    novo_proprietario1 = Proprietario(nome='João')
    novo_proprietario2 = Proprietario(nome='Maria')
    db.session.add_all([novo_proprietario1, novo_proprietario2])
    db.session.commit()
    response = client.get('/proprietarios')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2


def test_obter_proprietario(client):
    # Teste para obter um proprietário existente
    novo_proprietario = Proprietario(nome='João')
    db.session.add(novo_proprietario)
    db.session.commit()
    response = client.get(f"/proprietarios/{novo_proprietario.id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['nome'] == 'João'


def test_obter_proprietario_inexistente(client):
    # Teste para tentar obter um proprietário que não existe
    response = client.get('/proprietarios/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['erro'] == 'Proprietário não encontrado'


def test_atualizar_proprietario(client):
    # Teste para atualizar um proprietário existente
    novo_proprietario = Proprietario(nome='João')
    db.session.add(novo_proprietario)
    db.session.commit()
    dados_atualizados = {'nome': 'Pedro'}
    response = client.put(f"/proprietarios/{novo_proprietario.id}", json=dados_atualizados)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['mensagem'] == 'Proprietário atualizado com sucesso'


def test_atualizar_proprietario_inexistente(client):
    # Teste para tentar atualizar um proprietário que não existe
    dados_atualizados = {'nome': 'Pedro'}
    response = client.put('/proprietarios/999', json=dados_atualizados)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['erro'] == 'Proprietário não encontrado'


def test_deletar_proprietario(client):
    # Teste para deletar um proprietário existente
    novo_proprietario = Proprietario(nome='João')
    db.session.add(novo_proprietario)
    db.session.commit()
    response = client.delete(f"/proprietarios/{novo_proprietario.id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['mensagem'] == 'Proprietário deletado com sucesso'


def test_deletar_proprietario_inexistente(client):
    # Teste para tentar deletar um proprietário que não existe
    response = client.delete('/proprietarios/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['erro'] == 'Proprietário não encontrado'
