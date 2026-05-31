from flask import jsonify
from main import app
from flask import session
from db import query_db

@app.route('/api/pacientes', methods=['GET'])
def buscar_pacientes():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Não autorizado"}), 401

    pacientes = query_db(
        "SELECT nome, sexo, dataNascimento, ultimoTeste, dataCriacao FROM paciente WHERE pesquisador_id = %s",
        (user_id,)
    )
    return jsonify(pacientes or [])
