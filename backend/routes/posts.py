from flask import Blueprint, request, jsonify
from database import get_db
from utils import token_required
import json

posts = Blueprint('posts', __name__)

@posts.route('/api/posts', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO posts (user_id,text_content,images) VALUES (?,?,?)",
        (current_user['id'], data.get('text'), json.dumps(data.get('images',[])))
    )
    conn.commit()
    return jsonify({'message':'post created'})

@posts.route('/api/posts', methods=['GET'])
def feed():
    conn = get_db()
    rows = conn.execute("""
        SELECT posts.*, users.username, users.avatar, users.is_verified
        FROM posts JOIN users ON posts.user_id=users.id
        ORDER BY posts.created_at DESC
    """).fetchall()

    return jsonify([dict(r) for r in rows])

@posts.route('/api/posts/<int:post_id>/like', methods=['POST'])
@token_required
def like(current_user, post_id):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO likes (user_id,post_id) VALUES (?,?)",
            (current_user['id'], post_id)
        )
        conn.commit()
        return jsonify({'message':'liked'})
    except:
        return jsonify({'message':'already liked'}), 400

@posts.route('/api/posts/<int:post_id>/comment', methods=['POST'])
@token_required
def comment(current_user, post_id):
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO comments (user_id,post_id,comment_text) VALUES (?,?,?)",
        (current_user['id'], post_id, data['comment'])
    )
    conn.commit()
    return jsonify({'message':'commented'})
