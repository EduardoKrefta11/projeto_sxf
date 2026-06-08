from flask import jsonify, session, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from db import query_db, execute_db

def montar_filtros(user_id):

    filtros = ["p.idPesquisador = %s"]
    parametros = [user_id]

    sexo = request.args.get("sexo")

    if sexo:
        filtros.append("p.sexo = %s")
        parametros.append(sexo)

    nascimento_min = request.args.get("nascimentoMin")

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

    @app.route('/api/meus_pacientes', methods=['GET'])
    def buscar_pacientes():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        pacientes = query_db(
            "SELECT id, nome, sexo, dataNascimento, ultimoTeste, dataCriacao, fotoPerfil FROM paciente WHERE idPesquisador = %s",
            (user_id,)
        )
        return jsonify(pacientes or [])

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
                dataCriacao
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

            pdf.drawString(
                70,
                y,
                f"Observação: {consulta['observacao'] or 'Nenhuma'}"
            )

            y -= 25

            pdf.drawString(
                70,
                y,
                f"Sintomas: {consulta['sintomas'] or 'Nenhum'}"
            )

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

        stats = query_db(query, tuple(parametros))

        if stats is None:
            return jsonify({"error": "Erro ao buscar dados"}), 500

        return jsonify({
            "labels": [item["label"] for item in stats],
            "valores": [float(item["valor"]) for item in stats]
        })

    @app.route('/api/pdf/stats', methods=['GET'])
    def gerar_pdf_stats():
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"error": "Não autorizado"}), 401

        organizacao = request.args.get('organizacao', 'genero')