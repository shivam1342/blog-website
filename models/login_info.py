from models import db
import enum


class UserRole(enum.Enum):
    admin = 'admin'
    publisher = 'publisher'
    visitor = 'visitor'


class LoginInfo(db.Model):
    __tablename__ = 'login_info'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.Enum(UserRole), nullable=False)

    profile = db.relationship('UserProfile', backref='login', uselist=False)
    posts = db.relationship('Post', backref='author', lazy=True)
