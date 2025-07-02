from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .login_info import LoginInfo
from .post import Post, Like, Comment
from .user_profile import UserProfile