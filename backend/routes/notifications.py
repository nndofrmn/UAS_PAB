from flask import Blueprint, request, jsonify
from database import get_db
from utils import token_required

notifications = Blueprint('notifications', __name__)

@notifications.route('/api/notifications', methods=['GET'])
@token_required
def get_notifications(current_user):
    conn = get_db()
    
    # Get likes on user's posts
    likes = conn.execute('''
        SELECT l.*, p.text_content, u.username as liker_username
        FROM likes l
        JOIN posts p ON l.post_id = p.id
        JOIN users u ON l.user_id = u.id
        WHERE p.user_id = ?
        ORDER BY l.rowid DESC
        LIMIT 20
    ''', (current_user['id'],)).fetchall()
    
    # Get comments on user's posts
    comments = conn.execute('''
        SELECT c.*, p.text_content, u.username as commenter_username
        FROM comments c
        JOIN posts p ON c.post_id = p.id
        JOIN users u ON c.user_id = u.id
        WHERE p.user_id = ?
        ORDER BY c.created_at DESC
        LIMIT 20
    ''', (current_user['id'],)).fetchall()
    
    # Get follows
    follows = conn.execute('''
        SELECT f.*, u.username as follower_username
        FROM follows f
        JOIN users u ON f.follower_id = u.id
        WHERE f.following_id = ?
        ORDER BY f.rowid DESC
        LIMIT 20
    ''', (current_user['id'],)).fetchall()
    
    notifications_list = []
    for like in likes:
        notifications_list.append({
            'id': f"like_{like['user_id']}_{like['post_id']}",
            'type': 'like',
            'message': f'{like["liker_username"]} liked your post',
            'post_preview': like["text_content"][:50] + '...' if len(like["text_content"]) > 50 else like["text_content"],
            'from_user': like["liker_username"],
            'created_at': 'recent'  # likes table has no timestamp
        })
    
    for comment in comments:
        notifications_list.append({
            'id': f"comment_{comment['id']}",
            'type': 'comment',
            'message': f'{comment["commenter_username"]} commented: "{comment["comment_text"]}"',
            'post_preview': comment["text_content"][:50] + '...' if len(comment["text_content"]) > 50 else comment["text_content"],
            'from_user': comment["commenter_username"],
            'created_at': comment['created_at']
        })
    
    for follow in follows:
        notifications_list.append({
            'id': f"follow_{follow['follower_id']}_{follow['following_id']}",
            'type': 'follow',
            'message': f'{follow["follower_username"]} started following you',
            'from_user': follow["follower_username"],
            'created_at': 'recent'
        })
    
    # Sort notifications by type priority or something, but for now return as is
    return jsonify(notifications_list)
