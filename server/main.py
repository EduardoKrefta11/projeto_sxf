## cd 'PASTA DO main.py'
## python -m venv .venv
## .venv\Scripts\activate
## pip install Flask
## pip install PyMySQL
## pip install flask_cors
## pip install bcrypt

from flask import Flask, jsonify, request
from flask_cors import CORS 
import html
import pymysql
import bcrypt

app = Flask(__name__)
cors = CORS(app, origins='*')

def get_connection():

    try:
        return pymysql.connect(
            host='localhost',
            user='flaskuser',
            password='123flask',
            database='db_sxf',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as err:
        print(f"Erro MySQL: {err}")
        return None

def query_db(query, args=(), one=False):

    try:
        con = get_connection()
        if con is None:
            return None
        cursor = con.cursor()
        cursor.execute(query, args)
        result = cursor.fetchone() if one else cursor.fetchall()
        cursor.close()
        con.close()
        return result
    
    except Exception as e:
        print(f"ERRO MYSQL: {e}")
        return None

@app.route('/api/login', methods=['POST'])

def login():
    data = request.get_json()
    user = data.get('user')
    inputSenha = data.get('senha')

    verify = query_db("SELECT user, senha, permissao FROM usuario WHERE user = %s", (user, ), one=True)
    
    if not verify:
      return jsonify({
            "success" : False,
            "message" : f"Falha no Login, tente novamente"
        })

    if not bcrypt.checkpw(inputSenha.encode('utf-8'), 
                          verify['senha'].encode('utf-8')):
        return jsonify({
            "success" : False,
            "message" : f"Senha incorreta, favor tentar novamente"
        })

    return jsonify({
        "success" : True,
        "permissao": verify.get('permissao'),
        "message" : f"Login efetuado com sucesso. Bem-vindo, {verify['user']}"
    })

@app.route('/', methods=['GET'])

def test():
    return jsonify({
      "message" : "Teste de conn Flask"
    })

if __name__ == "__main__":
    app.run(debug=True)