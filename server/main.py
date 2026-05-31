## cd 'PASTA DO main.py'
## python -m venv .venv
## .venv\Scripts\activate
## pip install Flask
## pip install PyMySQL
## pip install flask_cors
## pip install bcrypt

from flask import Flask, jsonify, request, session
from flask_cors import CORS 
import bcrypt
import os
from db import query_db

app = Flask(__name__)
# python -c "import secrets; print(secrets.token_urlsafe(48))"
app.secret_key = os.environ.get('FLASK_SECRET', '123')
cors = CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.route('/api/login', methods=['POST'])

def login():
    data = request.get_json()
    user = data.get('user')
    inputSenha = data.get('senha')

    verify = query_db("SELECT id, user, senha, permissao FROM usuario WHERE user = %s", (user, ), one=True)
    
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

    session['user_id'] = verify.get('id')
    session['permissao'] = verify.get('permissao')

    return jsonify({
        "success" : True,
        "permissao": verify.get('permissao'),
        "message" : f"Login efetuado com sucesso. Bem-vindo, {verify['user']}"
    })

# importa menu para registrar as rotas de paciente
import menu

if __name__ == "__main__":
    app.run(debug=True)