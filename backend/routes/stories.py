from flask import Blueprint, request, jsonify
from database import get_db
from utils import token_required
from datetime import datetime, timedelta

stories = Blueprint('stories', __name__)

@stories.route('/api/stories', methods=['POST'])
@token_required
def create_story(current_user):
    data = request.json
    conn = get_db()
    conn.execute(
        """INSERT INTO stories (user_id,media_type,media_path,expires_at)
           VALUES (?,?,?,?)""",
        (current_user['id'], data['type'], data['path'],
         datetime.now()+timedelta(hours=24))
    )
    conn.commit()
    return jsonify({'message':'story added'})

@stories.route('/api/stories', methods=['GET'])
def get_stories():
    conn = get_db()
    rows = conn.execute("""
        SELECT stories.*, users.username, users.avatar
        FROM stories JOIN users ON stories.user_id=users.id
        WHERE expires_at > CURRENT_TIMESTAMP
    """).fetchall()

    return jsonify([dict(r) for r in rows])
