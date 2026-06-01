from flask import jsonify, request, session
from db import query_db
import bcrypt

def register_admin_routes(app):
    @app.route('/api/usuarios', methods=['GET', 'POST'])
    def manage_usuarios():
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'GET':
            usuarios = query_db("SELECT id, user, nome, permissao, dataNascimento FROM usuario")
            return jsonify(usuarios)
        
        if request.method == 'POST':
            data = request.get_json()
            hashed_pw = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            query_db("INSERT INTO usuario (user, nome, senha, permissao, dataNascimento) VALUES (%s, %s, %s, %s, %s)", 
                     (data['user'], data['nome'], hashed_pw, data['permissao'], data['dataNascimento']))
            return jsonify({"success": True}), 201

    @app.route('/api/usuarios/<int:id>', methods=['DELETE'])
    def delete_usuario(id):
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        query_db("DELETE FROM usuario WHERE id = %s", (id,))
        return jsonify({"success": True})

    @app.route('/api/pacientes', methods=['GET', 'POST'])
    def manage_pacientes():
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        if request.method == 'GET':
            pacientes = query_db("SELECT id, nome, cpf, sexo, dataNascimento FROM paciente")
            return jsonify(pacientes)
        if request.method == 'POST':
            data = request.get_json()
            query_db("INSERT INTO paciente (nome, cpf, sexo, dataNascimento, idPesquisador, idCriador) VALUES (%s, %s, %s, %s, %s, %s)", 
                     (data['nome'], data['cpf'], data['sexo'], data['dataNascimento'], data['idPesquisador'], session['user_id']))
            return jsonify({"success": True}), 201

    @app.route('/api/pacientes/<int:id>', methods=['DELETE'])
    def delete_paciente(id):
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        query_db("DELETE FROM paciente WHERE id = %s", (id,))
        return jsonify({"success": True})

    @app.route('/api/sintomas', methods=['GET', 'POST'])
    def manage_sintomas():
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        if request.method == 'GET':
            sintomas = query_db("SELECT id, nome, pesoMasculino, pesoFeminino FROM sintoma")
            return jsonify(sintomas)
        if request.method == 'POST':
            data = request.get_json()
            query_db("INSERT INTO sintoma (nome, pesoMasculino, pesoFeminino) VALUES (%s, %s, %s)", 
                     (data['nome'], data['pesoMasculino'], data['pesoFeminino']))
            return jsonify({"success": True}), 201

    @app.route('/api/sintomas/<int:id>', methods=['DELETE'])
    def delete_sintoma(id):
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        query_db("DELETE FROM sintoma WHERE id = %s", (id,))
        return jsonify({"success": True})
