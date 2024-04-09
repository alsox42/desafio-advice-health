from flask import request, jsonify
from app.models.class_models import db, Proprietario, Carro

def proprietario_rotas(app):

    @app.route('/proprietarios', methods=['POST'])
    def criar_proprietario():
        dados = request.json
        nome = dados['nome']
        
        if 'carros' in dados and len(dados['carros']) > 3:
            return jsonify({'erro': 'Um proprietário não pode ter mais do que 3 carros'}), 400
        
        novo_proprietario = Proprietario(nome=nome)
        
        if 'carros' in dados:
            for carro_dados in dados['carros']:
                modelo = carro_dados['modelo']
                cor = carro_dados['cor']
                carro = Carro(modelo=modelo, cor=cor, proprietario=novo_proprietario)
                db.session.add(carro)
        
        db.session.add(novo_proprietario)
        db.session.commit()
        return jsonify({'mensagem': 'Proprietário criado com sucesso'}), 201
    
    @app.route('/proprietarios', methods=['GET'])
    def listar_proprietarios():
         proprietarios = Proprietario.query.all()
         resultado = []
         for p in proprietarios:
             carros_proprietario = [car.formatar() for car in p.carros]
             total_carros = p.calcular_total_carros()
             resultado.append({"id": p.id, "nome": p.nome, "carros": carros_proprietario, "total_carros": total_carros})
         return jsonify(resultado), 200


    @app.route('/proprietarios/<int:id>', methods=['GET'])
    def obter_proprietario(id):
        proprietario = Proprietario.query.get(id)

        if not proprietario:
            return jsonify({'erro': 'Proprietário não encontrado'}), 404

        carros_proprietario = [car.formatar() for car in proprietario.carros]
        total_carros = proprietario.calcular_total_carros()

        resultado = {
            "id": proprietario.id,
            "nome": proprietario.nome,
            "carros": carros_proprietario,
            "total_carros": total_carros
        }

        return jsonify(resultado), 200

    @app.route('/proprietarios/<int:id>', methods=['PUT'])
    def atualizar_proprietario(id):
        proprietario = Proprietario.query.get_or_404(id)
        dados = request.json
        proprietario.nome = dados['nome']
        db.session.commit()
        return jsonify({'mensagem': 'Proprietário atualizado com sucesso'}), 200

    @app.route('/proprietarios/<int:id>', methods=['DELETE'])
    def deletar_proprietario(id):
        proprietario = Proprietario.query.get_or_404(id)
        db.session.delete(proprietario)
        db.session.commit()
        return jsonify({'mensagem': 'Proprietário deletado com sucesso'}), 200
