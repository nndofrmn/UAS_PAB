from flask import Blueprint, request, jsonify
from database import get_db
from utils import token_required

verification = Blueprint('verification', __name__)

@verification.route('/api/verify/request', methods=['POST'])
@token_required
def request_verification(current_user):
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO verification_requests (user_id,reason) VALUES (?,?)",
        (current_user['id'], data['reason'])
    )
    conn.commit()
    return jsonify({'message':'requested'})

@verification.route('/api/admin/verify/<int:user_id>', methods=['POST'])
@token_required
def approve_verification(current_user, user_id):
    if not current_user['is_admin']:
        return ('',403)

    conn = get_db()
    conn.execute("UPDATE users SET is_verified=1 WHERE id=?", (user_id,))
    conn.commit()
    return jsonify({'message':'verified'})
