from flask import Blueprint, jsonify
from database import get_db
from utils import token_required

bookmarks = Blueprint('bookmarks', __name__)

@bookmarks.route('/api/bookmark/<int:post_id>', methods=['POST'])
@token_required
def bookmark(current_user, post_id):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO bookmarks (user_id,post_id) VALUES (?,?)",
            (current_user['id'], post_id)
        )
        conn.commit()
        return jsonify({'message':'saved'})
    except:
        return jsonify({'message':'already saved'}), 400

@bookmarks.route('/api/bookmarks', methods=['GET'])
@token_required
def my_bookmarks(current_user):
    conn = get_db()
    rows = conn.execute("""
        SELECT posts.* FROM bookmarks
        JOIN posts ON bookmarks.post_id=posts.id
        WHERE bookmarks.user_id=?
    """,(current_user['id'],)).fetchall()

    return jsonify([dict(r) for r in rows])
