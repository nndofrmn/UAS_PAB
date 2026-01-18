from flask import Blueprint, jsonify
from database import get_db
from utils import token_required

users = Blueprint('users', __name__)

@users.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify(current_user)

@users.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    user = conn.execute(
        "SELECT id,username,bio,avatar,cover_photo,is_verified FROM users WHERE id=?",
        (user_id,)
    ).fetchone()
    return jsonify(dict(user)) if user else ('',404)

@users.route('/api/follow/<int:user_id>', methods=['POST'])
@token_required
def follow(current_user, user_id):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO follows (follower_id,following_id) VALUES (?,?)",
            (current_user['id'], user_id)
        )
        conn.commit()
        return jsonify({'message':'followed'})
    except:
        return jsonify({'message':'already followed'}), 400

@users.route('/api/unfollow/<int:user_id>', methods=['POST'])
@token_required
def unfollow(current_user, user_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM follows WHERE follower_id=? AND following_id=?",
        (current_user['id'], user_id)
    )
    conn.commit()
    return jsonify({'message':'unfollowed'})
