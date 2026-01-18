from flask import Blueprint, request, jsonify
from database import get_db
from utils import token_required

messages = Blueprint('messages', __name__)

@messages.route('/api/messages/<int:user_id>', methods=['POST'])
@token_required
def send_message(current_user, user_id):
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO messages (sender_id,receiver_id,message_text) VALUES (?,?,?)",
        (current_user['id'], user_id, data['message'])
    )
    conn.commit()
    return jsonify({'message':'sent'})

@messages.route('/api/messages/<int:user_id>', methods=['GET'])
@token_required
def get_messages(current_user, user_id):
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM messages
        WHERE (sender_id=? AND receiver_id=?)
           OR (sender_id=? AND receiver_id=?)
        ORDER BY created_at
    """,(current_user['id'],user_id,user_id,current_user['id'])).fetchall()

    return jsonify([dict(r) for r in rows])
