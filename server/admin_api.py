from flask import jsonify, request, session, send_file
from db import query_db, execute_db
import bcrypt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
import textwrap

def register_admin_routes(app):

    @app.route('/api/usuarios', methods=['GET', 'POST'])
    def manage_usuarios():
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'GET':
            usuarios = query_db("SELECT id, user, nome, permissao, dataNascimento, status FROM usuario")
            return jsonify(usuarios)
        
        if request.method == 'POST':
            data = request.get_json()
            hashed_pw = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            execute_db("INSERT INTO usuario (user, nome, senha, permissao, dataNascimento, status) VALUES (%s, %s, %s, %s, %s, 'Ativo')", 
                (data['user'], data['nome'], hashed_pw, data['permissao'], data['dataNascimento']))
            return jsonify({"success": True}), 201

    @app.route('/api/usuarios/<int:id>', methods=['PUT', 'DELETE'])
    def handle_usuario(id):
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'PUT':
            data = request.get_json()
            if data.get('senha'):
                hashed_pw = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                execute_db("UPDATE usuario SET user=%s, nome=%s, senha=%s, permissao=%s, dataNascimento=%s, status=%s WHERE id=%s",
                           (data['user'], data['nome'], hashed_pw, data['permissao'], data['dataNascimento'], data['status'], id))
            else:
                execute_db("UPDATE usuario SET user=%s, nome=%s, permissao=%s, dataNascimento=%s, status=%s WHERE id=%s",
                           (data['user'], data['nome'], data['permissao'], data['dataNascimento'], data['status'], id))
            return jsonify({"success": True})

        if request.method == 'DELETE':
            execute_db("UPDATE usuario SET status = 'Inativo' WHERE id = %s", (id,))
            return jsonify({"success": True})

    @app.route('/api/pacientes', methods=['GET', 'POST'])
    def manage_pacientes():
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'GET':
            pacientes = query_db("SELECT p.id, p.nome, p.cpf, p.sexo, p.dataNascimento, p.idPesquisador, p.fotoPerfil, u.nome as nomePesquisador FROM paciente p LEFT JOIN usuario u ON p.idPesquisador = u.id")
            return jsonify(pacientes)
        
        if request.method == 'POST':
            data = request.get_json()
            execute_db("INSERT INTO paciente (nome, cpf, sexo, dataNascimento, idPesquisador, idCriador) VALUES (%s, %s, %s, %s, %s, %s)", 
                (data['nome'], data['cpf'], data['sexo'], data['dataNascimento'], data['idPesquisador'], session['user_id']))
            return jsonify({"success": True}), 201

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
            execute_db("DELETE FROM paciente WHERE id = %s", (id,))
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
            execute_db("INSERT INTO sintoma (nome, pesoMasculino, pesoFeminino) VALUES (%s, %s, %s)", 
                     (data['nome'], data['pesoMasculino'], data['pesoFeminino']))
            return jsonify({"success": True}), 201

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
            execute_db("DELETE FROM sintoma WHERE id = %s", (id,))
            return jsonify({"success": True})

    @app.route('/api/admin/consultas', methods=['GET', 'POST'])
    def manage_admin_consultas():
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'GET':
            consultas = query_db("SELECT c.id, c.dataHora, c.tipoExame, c.resultadoExame, c.pontuacao, c.encaminhamento, c.observacao, p.nome as nomePaciente, u.nome as nomePesquisador, c.idPaciente, (SELECT GROUP_CONCAT(cs.idSintoma SEPARATOR ',') FROM consultasintoma cs WHERE cs.idConsulta = c.id) as idsSintomas, (SELECT GROUP_CONCAT(s.nome SEPARATOR ', ') FROM consultasintoma cs JOIN sintoma s ON cs.idSintoma = s.id WHERE cs.idConsulta = c.id) as sintomas FROM consulta c JOIN paciente p ON c.idPaciente = p.id LEFT JOIN usuario u ON p.idPesquisador = u.id ORDER BY c.dataHora DESC")
            return jsonify(consultas)

        if request.method == 'POST':
            data = request.get_json()
            paciente = query_db("SELECT sexo FROM paciente WHERE id = %s", (data['idPaciente'],), one=True)
            if not paciente: return jsonify({"message": "Paciente não encontrado"}), 404
            
            sintomas_ids = ",".join(map(str, data['sintomas']))
            sintomas_selecionados = query_db(f"SELECT id, pesoMasculino, pesoFeminino FROM sintoma WHERE id IN ({sintomas_ids})")
            
            score = 0
            for s in sintomas_selecionados:
                score += s['pesoMasculino'] if paciente['sexo'] == 'Masculino' else s['pesoFeminino']
            
            resultado = "Positivo" if score >= 3.0 else "Negativo"
            encaminhamento = "Encaminhar para teste genético confirmatório" if score >= 3.0 else "Monitorar sintomas e reavaliar em 6 meses"

            execute_db("INSERT INTO consulta (idPaciente, dataHora, tipoExame, resultadoExame, pontuacao, encaminhamento, observacao) VALUES (%s, NOW(), %s, %s, %s, %s, %s)",
                       (data['idPaciente'], data['tipoExame'], resultado, score, encaminhamento, data['observacao']))
            
            last_id = query_db("SELECT LAST_INSERT_ID() as id", one=True)['id']
            for s_id in data['sintomas']:
                execute_db("INSERT INTO consultasintoma (idConsulta, idSintoma) VALUES (%s, %s)", (last_id, s_id))
            return jsonify({"success": True}), 201

    @app.route('/api/admin/consultas/<int:id>', methods=['PUT', 'DELETE'])
    def handle_admin_consulta(id):
        if session.get('permissao') != 'ADM':
            return jsonify({"message": "Não autorizado"}), 401
        
        if request.method == 'PUT':
            data = request.get_json()
            paciente = query_db("SELECT sexo FROM paciente WHERE id = %s", (data['idPaciente'],), one=True)
            if not paciente: return jsonify({"message": "Paciente não encontrado"}), 404
            
            sintomas_ids = ",".join(map(str, data['sintomas']))
            sintomas_selecionados = query_db(f"SELECT id, pesoMasculino, pesoFeminino FROM sintoma WHERE id IN ({sintomas_ids})")
            
            score = 0
            for s in sintomas_selecionados:
                score += s['pesoMasculino'] if paciente['sexo'] == 'Masculino' else s['pesoFeminino']
            
            resultado = "Positivo" if score >= 3.0 else "Negativo"
            encaminhamento = "Encaminhar para teste genético confirmatório" if score >= 3.0 else "Monitorar sintomas e reavaliar em 6 meses"

            execute_db("UPDATE consulta SET tipoExame=%s, resultadoExame=%s, pontuacao=%s, encaminhamento=%s, observacao=%s WHERE id=%s",
                       (data['tipoExame'], resultado, score, encaminhamento, data['observacao'], id))
            
            execute_db("DELETE FROM consultasintoma WHERE idConsulta = %s", (id,))
            for s_id in data['sintomas']:
                execute_db("INSERT INTO consultasintoma (idConsulta, idSintoma) VALUES (%s, %s)", (id, s_id))
            return jsonify({"success": True})

        if request.method == 'DELETE':
            execute_db("DELETE FROM consultasintoma WHERE idConsulta = %s", (id,))
            execute_db("DELETE FROM consulta WHERE id = %s", (id,))
            return jsonify({"success": True})

    @app.route('/api/admin/pdf/paciente/<int:paciente_id>', methods=['GET'])
    def gerar_pdf_admin(paciente_id):
        if session.get('permissao') != 'ADM':
            return jsonify({"error": "Não autorizado"}), 401

        paciente = query_db("SELECT nome, sexo, dataNascimento, ultimoTeste, dataCriacao, fotoPerfil FROM paciente WHERE id = %s", (paciente_id,), one=True)
        consultas = query_db("SELECT c.id, c.dataHora, c.tipoExame, c.resultadoExame, c.pontuacao, c.encaminhamento, c.observacao, (SELECT GROUP_CONCAT(s.nome SEPARATOR ', ') FROM consultasintoma cs JOIN sintoma s ON cs.idSintoma = s.id WHERE cs.idConsulta = c.id) as sintomas FROM consulta c WHERE c.idPaciente = %s ORDER BY c.dataHora ASC", (paciente_id,))

        if not paciente:
            return jsonify({"error": "Paciente não encontrado"}), 404

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        logo_path = os.path.join(os.path.dirname(__file__), "..", "sxf_pjbl", "src", "assets", "buko_kaesemodel.webp")
        if os.path.exists(logo_path):
            pdf.drawImage(logo_path, 150, 730, width=300, height=110, mask='auto')

        pdf.line(50, 715, 550, 715)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(300, 690, f"RELATÓRIO CLÍNICO - {paciente['nome']}")
        pdf.line(50, 670, 550, 670)

        y = 650
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y, f"Nome: {paciente['nome']}")
        y -= 25
        pdf.drawString(50, y, f"Sexo: {paciente['sexo']}")
        y -= 25
        pdf.drawString(50, y, f"Data de Nascimento: {paciente['dataNascimento']}")
        y -= 25
        pdf.drawString(50, y, f"Último Teste: {paciente['ultimoTeste']}")
        y -= 25
        pdf.drawString(50, y, f"Data de Criação: {paciente['dataCriacao']}")

        if paciente['fotoPerfil']:
            foto_path = os.path.join(
                os.path.dirname(__file__),
                paciente['fotoPerfil'].lstrip('/')
            )
        else:
            foto_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "sxf_pjbl",
                "src",
                "assets",
                "default.png"
            )

        pdf.drawImage(
            foto_path,
            420,
            550,
            width=100,
            height=100,
            preserveAspectRatio=True,
            mask='auto'
        )

        y -= 40
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "HISTÓRICO DE CONSULTAS")
        y -= 30

        for consulta in consultas:
            if y < 150:
                pdf.showPage()
                y = 800
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, y, f"Consulta - {consulta['dataHora']}")
            y -= 20
            pdf.setFont("Helvetica", 11)
            pdf.drawString(70, y, f"Tipo de exame: {consulta['tipoExame']}")
            y -= 18
            pdf.drawString(70, y, f"Resultado: {consulta['resultadoExame']}")
            y -= 18
            pdf.drawString(70, y, f"Pontuação: {consulta['pontuacao']}")
            y -= 18
            pdf.drawString(70, y, f"Encaminhamento: {consulta['encaminhamento']}")
            y -= 18
            
            obs_texto = f"Observação: {consulta['observacao'] or 'Nenhuma'}"
            linhas_obs = textwrap.wrap(obs_texto, width=85)
            for linha in linhas_obs:
                pdf.drawString(70, y, linha)
                y -= 18
            
            sintomas_texto = f"Sintomas: {consulta['sintomas'] or 'Nenhum'}"
            linhas_sintomas = textwrap.wrap(sintomas_texto, width=85)
            for linha in linhas_sintomas:
                pdf.drawString(70, y, linha)
                y -= 18

            y -= 10
            pdf.line(50, y, 550, y)
            y -= 25

        pdf.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"Relatorio_{paciente['nome']}.pdf", mimetype="application/pdf")