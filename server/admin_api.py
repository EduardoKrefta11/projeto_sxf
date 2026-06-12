from flask import jsonify, request, session
from db import query_db, execute_db
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
            result = execute_db("INSERT INTO usuario (user, nome, senha, permissao, dataNascimento) VALUES "
                "(%s, %s, %s, %s, %s)", 
                (data['user'], data['nome'], hashed_pw, data['permissao'], data['dataNascimento']))
            
            return jsonify(result), 201

    @app.route('/api/usuarios/<int:id>', methods=['PUT', 'DELETE'])
    def handle_usuario(id):
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'PUT':
            data = request.get_json()
            if data.get('senha'):
                hashed_pw = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                execute_db("UPDATE usuario SET user=%s, nome=%s, senha=%s, permissao=%s, dataNascimento=%s WHERE id=%s",
                           (data['user'], data['nome'], hashed_pw, data['permissao'], data['dataNascimento'], id))
            else:
                execute_db("UPDATE usuario SET user=%s, nome=%s, permissao=%s, dataNascimento=%s WHERE id=%s",
                           (data['user'], data['nome'], data['permissao'], data['dataNascimento'], id))
            return jsonify({"success": True})

        if request.method == 'DELETE':
            execute_db("DELETE FROM usuario WHERE id = %s", (id,))
            return jsonify({"success": True})

    @app.route('/api/pacientes', methods=['GET', 'POST'])
    def manage_pacientes():
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'GET':
            pacientes = query_db("""
                SELECT p.id, p.nome, p.cpf, p.sexo, p.dataNascimento, p.idPesquisador, u.nome as nomePesquisador 
                FROM paciente p 
                LEFT JOIN usuario u ON p.idPesquisador = u.id
            """)
            return jsonify(pacientes)
        
        if request.method == 'POST':
            data = request.get_json()
            result = execute_db("INSERT INTO paciente (nome, cpf, sexo, dataNascimento, idPesquisador, idCriador) " \
                "VALUES (%s, %s, %s, %s, %s, %s)", 
                (data['nome'], data['cpf'], data['sexo'], data['dataNascimento'], data['idPesquisador'], session['user_id']))
            return jsonify(result), 201

    @app.route('/api/pacientes/<int:id>', methods=['PUT', 'DELETE'])
    def handle_paciente(id):
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'PUT':
            data = request.get_json()
            execute_db("UPDATE paciente SET nome=%s, cpf=%s, sexo=%s, dataNascimento=%s, idPesquisador=%s WHERE id=%s",
                       (data['nome'], data['cpf'], data['sexo'], data['dataNascimento'], data['idPesquisador'], id))
            return jsonify({"success": True})

        if request.method == 'DELETE':
            result = execute_db("DELETE FROM paciente WHERE id = %s", (id,))
            return jsonify(result)

    @app.route('/api/sintomas', methods=['GET', 'POST'])
    def manage_sintomas():
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'GET':
            sintomas = query_db("SELECT id, nome, pesoMasculino, pesoFeminino FROM sintoma")
            return jsonify(sintomas)
        
        if request.method == 'POST':
            data = request.get_json()
            result = execute_db("INSERT INTO sintoma (nome, pesoMasculino, pesoFeminino) VALUES (%s, %s, %s)", 
                     (data['nome'], data['pesoMasculino'], data['pesoFeminino']))
            
            return jsonify(result), 201

    @app.route('/api/sintomas/<int:id>', methods=['PUT', 'DELETE'])
    def handle_sintoma(id):
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'PUT':
            data = request.get_json()
            execute_db("UPDATE sintoma SET nome=%s, pesoMasculino=%s, pesoFeminino=%s WHERE id=%s",
                       (data['nome'], data['pesoMasculino'], data['pesoFeminino'], id))
            return jsonify({"success": True})

        if request.method == 'DELETE':
            result = execute_db("DELETE FROM sintoma WHERE id = %s", (id,))
            return jsonify(result)

    @app.route('/api/admin/consultas', methods=['GET', 'POST'])
    def manage_admin_consultas():
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'GET':
            consultas = query_db("""
                SELECT c.id, c.dataHora, c.tipoExame, c.resultadoExame, c.pontuacao, c.encaminhamento, c.observacao,
                       c.idPaciente, p.nome as nomePaciente, p.sexo as sexoPaciente, u.nome as nomePesquisador,
                       (SELECT GROUP_CONCAT(s.id SEPARATOR ',') 
                        FROM consultasintoma cs 
                        JOIN sintoma s ON cs.idSintoma = s.id 
                        WHERE cs.idConsulta = c.id) as idsSintomas,
                       (SELECT GROUP_CONCAT(s.nome SEPARATOR ', ') 
                        FROM consultasintoma cs 
                        JOIN sintoma s ON cs.idSintoma = s.id 
                        WHERE cs.idConsulta = c.id) as sintomas
                FROM consulta c
                JOIN paciente p ON c.idPaciente = p.id
                JOIN usuario u ON p.idPesquisador = u.id
                ORDER BY c.dataHora DESC
            """)
            return jsonify(consultas)

        if request.method == 'POST':
            data = request.get_json()
            id_paciente = data['idPaciente']
            sintomas_ids = data['sintomas']
            tipo_exame = data.get('tipoExame', '')
            observacao = data.get('observacao', '')

            paciente = query_db("SELECT sexo, idPesquisador FROM paciente WHERE id = %s", (id_paciente,), one=True)
            if not paciente:
                return jsonify({"message": "Paciente não encontrado"}), 404

            sintomas_data = query_db(f"SELECT pesoMasculino, pesoFeminino FROM sintoma WHERE id IN ({','.join(['%s']*len(sintomas_ids))})", tuple(sintomas_ids))
            
            score = 0
            for s in sintomas_data:
                if paciente['sexo'] == 'Masculino':
                    score += float(s['pesoMasculino'] or 0)
                else:
                    score += float(s['pesoFeminino'] or 0)
            score = round(score, 2)
            
            limite = 0.56 if paciente['sexo'] == 'Masculino' else 0.55
            encaminhamento = "Encaminhar para teste genético confirmatório" if score >= limite else "Sem necessidade de encaminhamento"
            resultado_exame = "Positivo" if score >= limite else "Negativo"

            consulta_id = execute_db("""
                INSERT INTO consulta (idPaciente, idPesquisador, dataHora, tipoExame, resultadoExame, pontuacao, encaminhamento, observacao)
                VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s)
            """, (id_paciente, paciente['idPesquisador'], tipo_exame, resultado_exame, score, encaminhamento, observacao), return_lastrowid=True)

            for s_id in sintomas_ids:
                execute_db("INSERT INTO consultasintoma (idConsulta, idSintoma) VALUES (%s, %s)", (consulta_id, s_id))

            return jsonify({"success": True, "id": consulta_id}), 201

    @app.route('/api/admin/consultas/<int:id>', methods=['PUT', 'DELETE'])
    def handle_admin_consulta(id):
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401

        if request.method == 'PUT':
            data = request.get_json()
            id_paciente = data['idPaciente']
            sintomas_ids = data['sintomas']
            tipo_exame = data.get('tipoExame', '')
            observacao = data.get('observacao', '')

            paciente = query_db("SELECT sexo FROM paciente WHERE id = %s", (id_paciente,), one=True)
            sintomas_data = query_db(f"SELECT pesoMasculino, pesoFeminino FROM sintoma WHERE id IN ({','.join(['%s']*len(sintomas_ids))})", tuple(sintomas_ids))
            
            score = 0
            for s in sintomas_data:
                if paciente['sexo'] == 'Masculino':
                    score += float(s['pesoMasculino'] or 0)
                else:
                    score += float(s['pesoFeminino'] or 0)
            score = round(score, 2)
            
            limite = 0.56 if paciente['sexo'] == 'Masculino' else 0.55
            encaminhamento = "Encaminhar para teste genético confirmatório" if score >= limite else "Sem necessidade de encaminhamento"
            resultado_exame = "Positivo" if score >= limite else "Negativo"

            execute_db("""
                UPDATE consulta SET idPaciente=%s, tipoExame=%s, resultadoExame=%s, pontuacao=%s, encaminhamento=%s, observacao=%s
                WHERE id=%s
            """, (id_paciente, tipo_exame, resultado_exame, score, encaminhamento, observacao, id))

            execute_db("DELETE FROM consultasintoma WHERE idConsulta = %s", (id,))
            for s_id in sintomas_ids:
                execute_db("INSERT INTO consultasintoma (idConsulta, idSintoma) VALUES (%s, %s)", (id, s_id))

            return jsonify({"success": True})

        if request.method == 'DELETE':
            execute_db("DELETE FROM consultasintoma WHERE idConsulta = %s", (id,))
            execute_db("DELETE FROM consulta WHERE id = %s", (id,))
            return jsonify({"success": True})
