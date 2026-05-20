## pip install mysql_connector
## pip install flask_cors

from flask import Flask, jsonify, request
from flask_cors import CORS 
import html
import mysql.connector
import bcrypt

app = Flask(__name__)
cors = CORS(app, origins='*')

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='prototype'
    )

def query_db(query, args=(), one=False):
    con = get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute(query, args)
    result = cursor.fetchone() if one else cursor.fetchall()
    cursor.close()
    con.close()
    return result

@app.route('/api/login', methods=['POST'])

def login():
    data = request.get_json()
    user = html.escape(data.get('user'))
    inputSenha = html.escape(data.get('senha'))
    permissao = data.get('permissao')
    permissao_mapa = {'ADM': 1, 'COM': 0}

    verify = query_db("SELECT nome, senha, permissao FROM usuario WHERE nome = %s", (user,))
    
    if not verify:
      return jsonify({
            "message" : f"Falha no Login, tente novamente"
        })

    if not bcrypt.checkpw(inputSenha.encode('utf-8'), 
                          verify['senha'].encode('utf-8')):
        return jsonify({
            "message" : f"Falha no Login, tente novamente"
        })

    if permissao_mapa.get(verify['permissao']) != permissao:
        return jsonify({
            "message" : f"Acesso negado, permissão insuficiente"
        })

    return jsonify({
        "message" : f"Login efetuado com sucesso. Bem-vindo, {verify['nome']}"
    })

if __name__ == "__main__":
    app.run(debug=True)