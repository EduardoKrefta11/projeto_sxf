from flask import Flask, jsonify, request
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('id')
    senha = data.get('senha')

    return jsonify({
        "message" : f"Backend recebeu {user_id} e {senha}"
    })

if __name__ == "__main__":
    app.run(debug=True)