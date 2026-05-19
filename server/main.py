from flask import Flask, jsonify, request
from flask_cors import CORS 
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
    user = data.get('user')
    inputSenha = data.get('senha')
    permissao = data.get('permissao')

    if permissao == 1:

        verify = query_db('SELECT nome, senha, permissao FROM usuario WHERE nome = %s', (user))

        if not verify:
            return jsonify({
                "message" : f"Falha no Login, tente novamente"
            })
    
        else:
            return jsonify({
                "message" : f"Usuário registrado no banco de dados!"
            })
        
    if permissao == 0:

        verify = query_db('SELECT nome, senha, permissao FROM usuario WHERE nome = %s', (user))

        if not verify:
            return jsonify({
                "message" : f"Falha no Login, tente novamente"
            })
        
        else:
            return jsonify({
                "message" : f"Usuário registrado no banco de dados!"
            })


if __name__ == "__main__":
    app.run(debug=True)