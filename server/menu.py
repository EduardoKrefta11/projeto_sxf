from flask import jsonify, session, request
from db import query_db

def register_menu_routes(app):
    @app.route('/api/meus_pacientes', methods=['GET'])
    def buscar_pacientes():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        pacientes = query_db(
            "SELECT nome, sexo, dataNascimento, ultimoTeste, dataCriacao FROM paciente WHERE idPesquisador = %s",
            (user_id,)
        )
        return jsonify(pacientes or [])

    @app.route('/api/stats', methods=['GET'])
    def obter_estatisticas():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        organizacao = request.args.get('organizacao', 'genero')
        
        if organizacao == 'genero':
            stats = query_db("""
                SELECT sexo as label, COUNT(*) as valor
                FROM paciente 
                WHERE idPesquisador = %s 
                GROUP BY sexo
            """, (user_id,))
            
        elif organizacao == 'data':
            stats = query_db("""
                SELECT DATE(dataHora) as label, COUNT(*) as valor
                FROM consulta c
                INNER JOIN paciente p ON c.idPaciente = p.id
                WHERE p.idPesquisador = %s
                GROUP BY DATE(c.dataHora)
                ORDER BY label
            """, (user_id,))
            
        elif organizacao == 'sintoma':
            stats = query_db("""
                SELECT s.nome as label, COUNT(*) as valor
                FROM consultasintoma cs
                INNER JOIN sintoma s ON cs.idSintoma = s.id
                INNER JOIN consulta c ON cs.idConsulta = c.id
                INNER JOIN paciente p ON c.idPaciente = p.id
                WHERE p.idPesquisador = %s
                GROUP BY s.id, s.nome
            """, (user_id,))
            
        elif organizacao == 'peso':
            stats = query_db("""
                SELECT s.nome as label, 
                    CASE 
                        WHEN p.sexo = 'Masculino' THEN s.pesoMasculino
                        WHEN p.sexo = 'Feminino' THEN s.pesoFeminino
                    END as valor
                FROM consultasintoma cs
                INNER JOIN sintoma s ON cs.idSintoma = s.id
                INNER JOIN consulta c ON cs.idConsulta = c.id
                INNER JOIN paciente p ON c.idPaciente = p.id
                WHERE p.idPesquisador = %s
                GROUP BY s.id, s.nome, p.sexo
            """, (user_id,))
        else:
            return jsonify({"error": "Organização inválida"}), 400
        
        if stats is None:
            return jsonify({"error": "Erro ao buscar dados"}), 500
        
        return jsonify({
            "labels": [item['label'] for item in stats],
            "valores": [float(item['valor']) for item in stats]
        })
