from flask import request, jsonify
from psycopg2 import IntegrityError
from app.models.class_models import db, Carro


def carro_rotas(app):
    @app.route('/carros', methods=['POST'])
    def criar_carro():
        data = request.json
        modelo = data.get('modelo')
        cor = data.get('cor')

        cores_validas = ['amarelo', 'azul', 'cinza']
        if cor not in cores_validas:
            return jsonify({'mensagem': 'Cor inválida. As cores permitidas são: amarelo, azul, cinza.'}), 400

        modelos_validos = ['hatch', 'sedã', 'conversível']
        if modelo not in modelos_validos:
            return jsonify({'mensagem': 'Modelo inválido. Os modelos permitidos são: hatch, sedã, cinza.'}), 400

        novo_carro = Carro(modelo=modelo, cor=cor)
        db.session.add(novo_carro)

        try:
            db.session.commit()
            return jsonify(novo_carro.formatar()), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'mensagem': 'Erro ao adicionar carro. Verifique os dados fornecidos.'}), 400

    @app.route('/carros/<int:carro_id>', methods=['GET'])
    def obter_carro(carro_id):
        carro = Carro.query.get(carro_id)
        if carro:
            return jsonify(carro.formatar())
        return jsonify({'mensagem': 'Carro não encontrado.'}), 404

    @app.route('/carros/<int:carro_id>', methods=['PUT'])
    def atualizar_carro(carro_id):
        carro = Carro.query.get(carro_id)
        if not carro:
            return jsonify({'mensagem': 'Carro não encontrado.'}), 404

        data = request.json
        modelo = data.get('modelo')
        cor = data.get('cor')

        # Verificando se a cor é válida
        cores_validas = ['amarelo', 'azul', 'cinza']
        if cor not in cores_validas:
            return jsonify({'mensagem': 'Cor inválida. As cores permitidas são: amarelo, azul, cinza.'}), 400

        # Verificando se o modelo é válido
        modelos_validos = ['hatch', 'sedã', 'cinza']
        if modelo not in modelos_validos:
            return jsonify({'mensagem': 'Modelo inválido. Os modelos permitidos são: hatch, sedã, cinza.'}), 400

        carro.modelo = modelo
        carro.cor = cor

        try:
            db.session.commit()
            return jsonify(carro.formatar())
        except IntegrityError:
            db.session.rollback()
            return jsonify({'mensagem': 'Erro ao atualizar carro. Verifique os dados fornecidos.'}), 400

    @app.route('/carros/<int:carro_id>', methods=['DELETE'])
    def deletar_carro(carro_id):
        carro = Carro.query.get(carro_id)
        if carro:
            db.session.delete(carro)
            db.session.commit()
            return jsonify({'mensagem': 'Carro deletado com sucesso.'})
        return jsonify({'mensagem': 'Carro não encontrado.'}), 404