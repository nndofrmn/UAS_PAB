from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY

auth = Blueprint('auth', __name__)

@auth.route('/api/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username,password,email) VALUES (?,?,?)",
            (data['username'], generate_password_hash(data['password']), data['email'])
        )
        conn.commit()
        return jsonify({'message':'Registered'}), 201
    except:
        return jsonify({'message':'User exists'}), 400

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=?", (data['username'],)
    ).fetchone()

    if user and check_password_hash(user['password'], data['password']):
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.utcnow()+timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token, 'user': dict(user)})
    return jsonify({'message':'Invalid'}), 401
