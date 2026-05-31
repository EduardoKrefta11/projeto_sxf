## cd 'PASTA DO main.py'
## python -m venv .venv
## .venv\Scripts\activate
## pip install Flask
## pip install PyMySQL
## pip install flask_cors
## pip install bcrypt

from flask import Flask, jsonify, request
from flask_cors import CORS 
import bcrypt
from db import query_db

app = Flask(__name__)
cors = CORS(app, origins='*')

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

# importa menu para registrar as rotas de paciente
import menu

if __name__ == "__main__":
    app.run(debug=True)