import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'your-secret-key-change-this'

UPLOAD_FOLDER = 'uploads'
AVATAR_FOLDER = 'avatars'
STORY_FOLDER = 'stories'
VIDEO_FOLDER = 'videos'
COVER_FOLDER = 'covers'

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

FOLDERS = [
    UPLOAD_FOLDER,
    AVATAR_FOLDER,
    STORY_FOLDER,
    VIDEO_FOLDER,
    COVER_FOLDER
]
