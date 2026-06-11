from flask import jsonify, session, request, send_file, send_from_directory
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from io import BytesIO
import os
import textwrap
import base64
from werkzeug.utils import secure_filename
from db import query_db, execute_db

def montar_filtros(user_id, dados=None):

    if dados is None:
        dados = {}

    filtros = ["p.idPesquisador = %s"]
    parametros = [user_id]

    def obter_param(nome):
        valor = dados.get(nome)
        if valor is None or valor == "":
            valor = request.args.get(nome)
        return valor

    sexo = obter_param("sexo")

    if sexo:
        filtros.append("p.sexo = %s")
        parametros.append(sexo)

    nascimento_min = obter_param("nascimentoMin")

    if nascimento_min:
        filtros.append("p.dataNascimento >= %s")
        parametros.append(nascimento_min)

    nascimento_max = request.args.get("nascimentoMax")

    if nascimento_max:
        filtros.append("p.dataNascimento <= %s")
        parametros.append(nascimento_max)

    sintoma = request.args.get("sintoma")

    if sintoma:
        filtros.append("s.nome = %s")
        parametros.append(sintoma)

    pontuacao_min = request.args.get("pontuacaoMin")

    if pontuacao_min:
        filtros.append("c.pontuacao >= %s")
        parametros.append(pontuacao_min)

    pontuacao_max = request.args.get("pontuacaoMax")

    if pontuacao_max:
        filtros.append("c.pontuacao <= %s")
        parametros.append(pontuacao_max)

    return filtros, parametros

def register_menu_routes(app):

    @app.route('/api/meu_perfil', methods=['GET'])
    def buscar_perfil():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error" : "Não autorizado"}), 401
        
        perfil = query_db(
            "SELECT user, nome, dataNascimento, dataCriacao, fotoPerfil FROM usuario WHERE id = %s", (user_id,), one=True
            )

        if perfil is None:
            return jsonify({"error" : "Erro na busca do usuário"}), 404

        return jsonify(perfil)
    
    @app.route('/api/user_pfp', methods=['POST'])
    def atualizarPfp():

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error" : "Não autorizado"}), 401
        
        if 'foto' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        arquivo = request.files['foto']

        if arquivo.filename == '':
            return jsonify({"error": "Arquivo inválido"}), 400

        extensao = arquivo.filename.rsplit('.', 1)[1].lower()

        nome_arquivo = f"user_{user_id}.{extensao}"

        pasta_upload = os.path.join('uploads', 'perfis')

        os.makedirs(pasta_upload, exist_ok=True)

        caminho_fisico = os.path.join(
            pasta_upload,
            secure_filename(nome_arquivo)
        )

        arquivo.save(caminho_fisico)

        caminho_banco = f"/uploads/perfis/{nome_arquivo}"

        execute_db(
            """
            UPDATE usuario
            SET fotoPerfil = %s
            WHERE id = %s
            """,
            (caminho_banco, user_id)
        )

        return jsonify({
            "message": "Foto enviada com sucesso",
            "fotoPerfil": caminho_banco
        })
    
    @app.route('/api/paciente_pfp', methods=['POST'])
    def pacientePfp():
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        id_paciente = request.form.get('idPaciente')

        if not id_paciente:
            return jsonify({"error": "Paciente não informado"}), 400

        if 'foto' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        arquivo = request.files['foto']

        if arquivo.filename == '':
            return jsonify({"error": "Arquivo inválido"}), 400

        extensao = arquivo.filename.rsplit('.', 1)[1].lower()

        nome_arquivo = f"paciente_{id_paciente}.{extensao}"

        pasta_upload = os.path.join('uploads', 'pacientes')

        os.makedirs(pasta_upload, exist_ok=True)

        caminho_fisico = os.path.join(
            pasta_upload,
            secure_filename(nome_arquivo)
        )

        arquivo.save(caminho_fisico)

        caminho_banco = f"/uploads/pacientes/{nome_arquivo}"

        linhas_afetadas = execute_db(
            """
            UPDATE paciente
            SET fotoPerfil = %s
            WHERE id = %s
            AND idPesquisador = %s
            """,
            (caminho_banco, id_paciente, user_id)
        )

        return jsonify({
            "message": "Foto enviada com sucesso",
            "fotoPerfil": caminho_banco
        })

    @app.route('/uploads/pacientes/<filename>')
    def servir_paciente_pfp(filename):
        return send_from_directory(
            'uploads/pacientes',
            filename
        )
    
    @app.route('/uploads/perfis/<filename>')
    def servir_pfp(filename):
        return send_from_directory(
            'uploads/perfis',
            filename
        )

    @app.route('/api/meus_pacientes', methods=['GET', 'POST'])
    def meus_pacientes():

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        if request.method == 'POST':
            data = request.get_json() or {}
            nome = data.get('nome')
            cpf = data.get('cpf')
            sexo = data.get('sexo')
            data_nascimento = data.get('dataNascimento')

            if not nome or not cpf or not sexo or not data_nascimento:
                return jsonify({"error": "Dados incompletos"}), 400

            execute_db(
                """INSERT INTO
                paciente 
                (nome, cpf, sexo, dataNascimento, idPesquisador, idCriador) 
                VALUES 
                (%s, %s, %s, %s, %s, %s)""",
                (nome, cpf, sexo, data_nascimento, user_id, user_id)
            )
            return jsonify({"success": True}), 201

        pacientes = query_db("""
            SELECT
                p.id,
                p.nome,
                p.sexo,
                p.dataNascimento,
                p.ultimoTeste,
                p.dataCriacao,
                p.fotoPerfil,
                c.pontuacao,
                c.encaminhamento
            FROM paciente p
            LEFT JOIN consulta c
                ON c.id = (
                    SELECT id
                    FROM consulta
                    WHERE idPaciente = p.id
                    ORDER BY dataHora DESC
                    LIMIT 1
                ) WHERE p.idPesquisador = %s""", (user_id,))
        
        return jsonify(pacientes or [])

    @app.route('/api/paciente_nova_consulta', methods=['POST'])
    def nova_consulta():
        data = request.get_json()

        user_id = session.get('user_id')
        id_paciente = data['idPaciente']
        sintomas = data['sintomas']
        tipo_exame = data.get('tipoExame')
        observacao = data.get('observacao')

        paciente = query_db("""
            SELECT sexo
            FROM paciente
            WHERE id = %s
        """, (id_paciente,), one=True)

        ids = ','.join(['%s'] * len(sintomas))

        rows = query_db(f"""
            SELECT id, pesoMasculino, pesoFeminino
            FROM sintoma
            WHERE id IN ({ids})
        """, tuple(sintomas))

        score = 0

        for s in rows:
            if paciente['sexo'] == 'Masculino':
                score += float(s['pesoMasculino'] or 0)
            else:
                score += float(s['pesoFeminino'] or 0)

        score = round(score, 2)

        limite = 0.56 if paciente['sexo'] == 'Masculino' else 0.55

        encaminhamento = (
            "Encaminhar para teste genético confirmatório"
            if score >= limite
            else "Sem necessidade de encaminhamento"
        )

        resultado_exame = (
            "Positivo"
            if score >= limite
            else "Negativo"
        )

        consulta_id = execute_db("""
            INSERT INTO consulta (
                idPaciente,
                idPesquisador,
                dataHora,
                tipoExame,
                resultadoExame,
                pontuacao,
                encaminhamento,
                observacao
            )
            VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s)
        """, (
            id_paciente,
            user_id,
            tipo_exame,
            resultado_exame,
            score,
            encaminhamento,
            observacao
        ), return_lastrowid=True)

        for sintoma_id in sintomas:
            execute_db("""
                INSERT INTO consultasintoma (
                    idConsulta,
                    idSintoma
                )
                VALUES (%s, %s)
            """, (
                consulta_id,
                sintoma_id
            ))

        return jsonify({
            "success": True,
            "score": score,
            "resultadoExame": resultado_exame,
            "encaminhamento": encaminhamento
        }), 201

    @app.route('/api/pdf/paciente/<int:paciente_id>', methods=['GET'])
    def gerar_pdf_paciente(paciente_id):
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        paciente = query_db(
            """
            SELECT nome,
                sexo,
                dataNascimento,
                ultimoTeste,
                dataCriacao,
                fotoPerfil
            FROM paciente
            WHERE id = %s
            AND idPesquisador = %s
            """,
            (paciente_id, user_id),
            one=True
        )

        consultas = query_db("""
            SELECT
                c.id,
                c.dataHora,
                c.tipoExame,
                c.resultadoExame,
                c.pontuacao,
                c.encaminhamento,
                c.observacao,
                GROUP_CONCAT(
                    s.nome
                    SEPARATOR ', '
                ) as sintomas
            FROM consulta c
            LEFT JOIN consultasintoma cs
                ON c.id = cs.idConsulta
            LEFT JOIN sintoma s
                ON cs.idSintoma = s.id
            WHERE c.idPaciente = %s
            GROUP BY c.id
            ORDER BY c.dataHora ASC
        """, (paciente_id,))

        if not paciente:
            return jsonify({"error": "Paciente não encontrado"}), 404

        buffer = BytesIO()

        pdf = canvas.Canvas(buffer, pagesize=A4)

        logo_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "sxf_pjbl",
            "src",
            "assets",
            "buko_kaesemodel.webp"
        )

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
            logo_path,
            150,
            730,
            width=300,
            height=110,
            mask='auto'
        )

        pdf.line(50, 715, 550, 715)

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(
            300,
            690,
            f"RELATÓRIO CLÍNICO - {paciente['nome']}"
        )

        pdf.line(50, 670, 550, 670)

        y = 650

        pdf.setFont("Helvetica", 12)

        pdf.drawString(50, y, f"Nome: {paciente['nome']}")
        y -= 25

        pdf.drawString(50, y, f"Sexo: {paciente['sexo']}")
        y -= 25

        pdf.drawString(
            50,
            y,
            f"Data de Nascimento: {paciente['dataNascimento']}"
        )
        y -= 25

        pdf.drawString(
            50,
            y,
            f"Último Teste: {paciente['ultimoTeste']}"
        )
        y -= 25

        pdf.drawString(
            50,
            y,
            f"Data de Criação: {paciente['dataCriacao']}"
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

            if y < 100:
                pdf.showPage()
                y = 800

            pdf.setFont("Helvetica-Bold", 12)

            pdf.drawString(
                50,
                y,
                f"Consulta - {consulta['dataHora']}"
            )

            y -= 20

            pdf.setFont("Helvetica", 11)

            pdf.drawString(
                70,
                y,
                f"Tipo de exame: {consulta['tipoExame']}"
            )

            y -= 18

            pdf.drawString(
                70,
                y,
                f"Resultado: {consulta['resultadoExame']}"
            )

            y -= 18

            pdf.drawString(
                70,
                y,
                f"Pontuação: {consulta['pontuacao']}"
            )

            y -= 18

            pdf.drawString(
                70,
                y,
                f"Encaminhamento: {consulta['encaminhamento']}"
            )

            y -= 18

            linhas = textwrap.wrap(
                f"Observação: {consulta['observacao'] or 'Nenhuma'}",
                width=80
            )

            for linha in linhas:
                pdf.drawString(70, y, linha)
                y -= 15

            y -= 10

            linhas = textwrap.wrap(
                f"Sintomas: {consulta['sintomas'] or 'Nenhum'}",
                width=80
            )

            for linha in linhas:
                pdf.drawString(70, y, linha)
                y -= 15

            y -= 25

            pdf.line(50, y, 550, y)

            y -= 25

        pdf.save()

        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Relatorio_paciente.pdf",
            mimetype="application/pdf"
        )
    
    @app.route('/api/buscar_sintomas', methods=['GET'])
    def listar_sintomas():

        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        sintomas = query_db("""
            SELECT
                id,
                nome
            FROM sintoma
            ORDER BY nome
        """)

        return jsonify(sintomas)

    @app.route('/api/stats', methods=['GET'])
    def obter_estatisticas():

        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        organizacao = request.args.get('organizacao', 'genero')

        filtros, parametros = montar_filtros(user_id)

        where_clause = " AND ".join(filtros)

        if organizacao == 'genero':

            query = f"""
                SELECT
                    p.sexo as label,
                    COUNT(DISTINCT p.id) as valor
                FROM paciente p
                LEFT JOIN consulta c
                    ON c.idPaciente = p.id
                LEFT JOIN consultaSintoma cs
                    ON cs.idConsulta = c.id
                LEFT JOIN sintoma s
                    ON s.id = cs.idSintoma
                WHERE {where_clause}
                GROUP BY p.sexo
            """

        elif organizacao == 'sintoma':

            query = f"""
                SELECT
                    s.nome as label,
                    COUNT(*) as valor
                FROM consultaSintoma cs
                INNER JOIN sintoma s
                    ON cs.idSintoma = s.id
                INNER JOIN consulta c
                    ON cs.idConsulta = c.id
                INNER JOIN paciente p
                    ON c.idPaciente = p.id
                WHERE {where_clause}
                GROUP BY s.id, s.nome
            """

        elif organizacao == 'peso':

            query = f"""
                SELECT
                    s.nome as label,
                    AVG(
                        CASE
                            WHEN p.sexo = 'Masculino'
                                THEN s.pesoMasculino
                            WHEN p.sexo = 'Feminino'
                                THEN s.pesoFeminino
                        END
                    ) as valor
                FROM consultaSintoma cs
                INNER JOIN sintoma s
                    ON cs.idSintoma = s.id
                INNER JOIN consulta c
                    ON cs.idConsulta = c.id
                INNER JOIN paciente p
                    ON c.idPaciente = p.id
                WHERE {where_clause}
                GROUP BY s.id, s.nome
            """

        else:
            return jsonify({"error": "Organização inválida"}), 400

        stats = query_db(query, tuple(parametros))

        if stats is None:
            return jsonify({"error": "Erro ao buscar dados"}), 500

        return jsonify({
            "labels": [item["label"] for item in stats],
            "valores": [float(item["valor"]) for item in stats]
        })

    @app.route('/api/pdf/stats', methods=['GET', 'POST'])
    def gerarPdfEstatisticas():
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        dados_json = request.get_json(silent=True) or {}
        organizacao = dados_json.get('organizacao', request.args.get('organizacao', 'genero'))
        tipoGrafico = dados_json.get('tipoGrafico', request.args.get('tipoGrafico', 'colunas'))

        filtros, parametros = montar_filtros(user_id, dados_json)
        where_clause = " AND ".join(filtros)

        if organizacao == 'genero':
            query = f"""
                SELECT
                    p.sexo as label,
                    COUNT(DISTINCT p.id) as valor
                FROM paciente p
                LEFT JOIN consulta c
                    ON c.idPaciente = p.id

                LEFT JOIN consultaSintoma cs
                    ON cs.idConsulta = c.id

                LEFT JOIN sintoma s
                    ON s.id = cs.idSintoma
                WHERE {where_clause}
                GROUP BY p.sexo
            """

        elif organizacao == 'data':
            query = f"""
                SELECT
                    DATE(c.dataHora) as label,
                    COUNT(DISTINCT p.id) as valor
                FROM consulta c
                INNER JOIN paciente p
                    ON c.idPaciente = p.id
                LEFT JOIN consultaSintoma cs
                    ON cs.idConsulta = c.id
                LEFT JOIN sintoma s
                    ON s.id = cs.idSintoma
                WHERE {where_clause}
                GROUP BY DATE(c.dataHora)
                ORDER BY label
            """

        elif organizacao == 'sintoma':
            query = f"""
                SELECT
                    s.nome as label,
                    COUNT(*) as valor
                FROM consultaSintoma cs
                INNER JOIN sintoma s
                    ON cs.idSintoma = s.id
                INNER JOIN consulta c
                    ON cs.idConsulta = c.id
                INNER JOIN paciente p
                    ON c.idPaciente = p.id
                WHERE {where_clause}
                GROUP BY s.id, s.nome
            """

        elif organizacao == 'peso':
            query = f"""
                SELECT
                    s.nome as label,

                    AVG(
                        CASE
                            WHEN p.sexo = 'Masculino'
                                THEN s.pesoMasculino
                            WHEN p.sexo = 'Feminino'
                                THEN s.pesoFeminino
                        END
                    ) as valor
                FROM consultaSintoma cs
                INNER JOIN sintoma s
                    ON cs.idSintoma = s.id
                INNER JOIN consulta c
                    ON cs.idConsulta = c.id
                INNER JOIN paciente p
                    ON c.idPaciente = p.id
                WHERE {where_clause}
                GROUP BY s.id, s.nome
            """

        else:
            return jsonify({"error": "Organização inválida"}), 400

        dadosEstatisticos = query_db(query, tuple(parametros))  

        if dadosEstatisticos is None:
            return jsonify({"error": "Erro ao buscar dados"}), 500

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)

        logo_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "sxf_pjbl",
            "src",
            "assets",
            "buko_kaesemodel.webp"
        )

        pdf.drawImage(
            logo_path,
            150,
            730,
            width=300,
            height=110,
            mask='auto'
        )

        pdf.line(50, 715, 550, 715)

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(
            300,
            690,
            f"RELATÓRIO ESTATÍSTICO"
        )

        pdf.line(50, 670, 550, 670)

        y = 650
        pdf.setFont("Helvetica", 12)

        def wrap_text(start_y, text, max_chars=70, line_height=16):
            for line in textwrap.wrap(text, width=max_chars):
                pdf.drawString(50, start_y, line)
                start_y -= line_height
            return start_y

        filtrosAplicados = []
        if request.args.get('sexo'):
            filtrosAplicados.append(f"Sexo: {request.args.get('sexo')}")
        if request.args.get('nascimentoMin'):
            filtrosAplicados.append(f"Nascimento mínimo: {request.args.get('nascimentoMin')}")
        if request.args.get('nascimentoMax'):
            filtrosAplicados.append(f"Nascimento máximo: {request.args.get('nascimentoMax')}")
        if request.args.get('sintoma'):
            filtrosAplicados.append(f"Sintoma: {request.args.get('sintoma')}")
        if request.args.get('pontuacaoMin'):
            filtrosAplicados.append(f"Pontuação mínima: {request.args.get('pontuacaoMin')}")
        if request.args.get('pontuacaoMax'):
            filtrosAplicados.append(f"Pontuação máxima: {request.args.get('pontuacaoMax')}")

        filtrosTexto = "; ".join(filtrosAplicados) if filtrosAplicados else "Nenhum filtro aplicado"

        y -= 20

        imagem_grafico_base64 = dados_json.get('imagemGraficoBase64')
        if imagem_grafico_base64:
            if ',' in imagem_grafico_base64:
                imagem_grafico_base64 = imagem_grafico_base64.split(',', 1)[1]
            try:
                imagem_bytes = base64.b64decode(imagem_grafico_base64)
                imagem = ImageReader(BytesIO(imagem_bytes))
                if y < 280:
                    pdf.showPage()
                    y = 800
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(50, y, "Gráfico")
                y -= 20
                pdf.drawImage(imagem, 50, y - 240, width=500, height=240, preserveAspectRatio=True, mask='auto')
                y -= 260
            except Exception:
                pdf.setFont("Helvetica-Italic", 12)
                pdf.drawString(50, y, "Não foi possível incluir a imagem do gráfico.")
                y -= 20

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Dados do gráfico")
        y -= 24
        pdf.setFont("Helvetica", 12)

        if not dadosEstatisticos:
            pdf.drawString(50, y, "Nenhum dado disponível para os filtros selecionados.")
        else:
            for item in dadosEstatisticos:
                label = item.get('label') or 'Sem rótulo'
                valor = item.get('valor')
                y = wrap_text(y, f"{label}: {valor}")
                y -= 10

                if y < 100:
                    pdf.showPage()
                    y = 800
                    pdf.setFont("Helvetica", 12)

        pdf.save()
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Relatorio_estatisticas.pdf",
            mimetype="application/pdf"
        )