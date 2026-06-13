from flask import Flask, jsonify, request, session
from flask_cors import CORS 
import bcrypt
import os
from db import query_db
from admin_api import register_admin_routes
from menu import register_menu_routes

app = Flask(__name__)
register_admin_routes(app)
register_menu_routes(app)
app.secret_key = os.environ.get('FLASK_SECRET', '123')
cors = CORS(app, supports_credentials=True, origins=['http://localhost:5173'], allow_headers=['Content-Type'] )
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('user')
    inputSenha = data.get('senha')

    verify = query_db("SELECT id, user, senha, permissao, status FROM usuario WHERE user = %s", (user, ), one=True)
    
    if not verify:
      return jsonify({
            "success" : False,
            "message" : "Falha no Login, tente novamente"
        })

    if verify.get('status') == 'Inativo':
        return jsonify({
            "success" : False,
            "message" : "Esta conta foi desativada. Entre em contato com o administrador."
        })

    if not bcrypt.checkpw(inputSenha.encode('utf-8'), 
                          verify['senha'].encode('utf-8')):
        return jsonify({
            "success" : False,
            "message" : "Senha incorreta, favor tentar novamente"
        })

    session['user_id'] = verify.get('id')
    session['permissao'] = verify.get('permissao')

    response = jsonify({
        "success" : True,
        "permissao": verify.get('permissao'),
        "message" : f"Login efetuado com sucesso. Bem-vindo, {verify['user']}"
    })
    return response

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Desconectado com sucesso"}), 200

import menu

if __name__ == "__main__":
    app.run(debug=True)
