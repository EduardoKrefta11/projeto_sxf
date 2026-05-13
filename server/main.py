from flask import Flask, jsonify, request
from flask_cors import CORS 
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
cors = CORS(app, origins='*')

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='prototype'
    )

@app.route('/api/debug/tables', methods=['GET'])

def getTables_debug():
    con = get_connection()
    cursor=con.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    cursor.close()
    con.close()
    table_names=[table[0] for table in tables]
    return jsonify({"Tables: ", table_names}), 200

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
    senha = data.get('senha')

    verify = query_db('SELECT nome, senha FROM pesquisador WHERE nome = %s', (user,))

    if not verify:
        return jsonify({
            "message" : f"Usuário não registrado no banco de dados"
        })
    else:
        return jsonify({
            "message" : f"Usuário registrado no banco de dados, com Nome = {user} e SENHA = {senha}"
        })

if __name__ == "__main__":
    app.run(debug=True)