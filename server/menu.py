from flask import jsonify
from main import app, query_db

@app.route('/api/pacientes', methods=['GET'])
def buscar_pacientes():
    pacientes = query_db(
        "SELECT nome, sexo, dataNascimento, ultimoTeste, dataCriacao FROM paciente"
    )
    return jsonify(pacientes or [])
