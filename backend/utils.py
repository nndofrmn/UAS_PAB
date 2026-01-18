import jwt, io, os
from functools import wraps
from datetime import datetime
from flask import request, jsonify
from PIL import Image
from config import SECRET_KEY, ALLOWED_EXTENSIONS, STORY_FOLDER
from database import get_db

def token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        try:
            token = token.split()[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = get_db().execute(
                'SELECT * FROM users WHERE id=?', (data['user_id'],)
            ).fetchone()
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(dict(user), *args, **kwargs)
    return wrap

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def optimize_image(file, size=(1200,1200)):
    img = Image.open(file)
    img.thumbnail(size)
    out = io.BytesIO()
    img.save(out, format='JPEG', quality=85)
    out.seek(0)
    return out

def cleanup_expired_stories():
    conn = get_db()
    expired = conn.execute(
        "SELECT media_path FROM stories WHERE expires_at <= ?",
        (datetime.now(),)
    ).fetchall()
    for s in expired:
        try:
            os.remove(os.path.join(STORY_FOLDER, s['media_path']))
        except:
            pass
    conn.execute("DELETE FROM stories WHERE expires_at <= ?", (datetime.now(),))
    conn.commit()
    conn.close()
