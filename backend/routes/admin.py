from flask import Blueprint, jsonify
from database import get_db
from utils import token_required

admin = Blueprint('admin', __name__)

@admin.route('/api/admin/users', methods=['GET'])
@token_required
def users_list(current_user):
    if not current_user['is_admin']:
        return ('',403)

    conn = get_db()
    rows = conn.execute("SELECT id,username,email,is_verified FROM users").fetchall()
    return jsonify([dict(r) for r in rows])
