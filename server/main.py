## cd 'PASTA DO main.py'
## python -m venv .venv
## .venv\Scripts\activate
## pip install Flask
## pip install mysql_connector
## pip install flask_cors
## pip install bcrypt

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
    result = cursor.fetchone()
    cursor.close()
    con.close()
    return result

@app.route('/api/login', methods=['POST'])

def login():
    data = request.get_json()
    user = data.get('user')
    inputSenha = data.get('senha')
    permissao = data.get('permissao')
    permissao_mapa = {'ADM': True, 'COM': False}

    verify = query_db("SELECT user, senha, permissao FROM usuario WHERE user = %s", (user, ), one=True)
    
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
        "message" : f"Login efetuado com sucesso. Bem-vindo, {verify['user']}"
    })

@app.route('/', methods=['GET'])

def test():
    return jsonify({
      "message" : "Teste realizado com sucesso."
    })

if __name__ == "__main__":
    app.run(debug=True)