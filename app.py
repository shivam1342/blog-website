from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import db
from models.login_info import LoginInfo as User 
from flask_migrate import Migrate
from routes.user_routes import user_bp
from routes.post_routes import publisher_bp
from routes.home_routes import public_bp
from routes.admin_routes import admin_bp
from flask_mailman import Mail
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.secret_key = 'sa;foibhnmrsdfig'


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL").replace("postgres://", "postgresql+pg8000://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = 'zerdragneel400@gmail.com',
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
)

mail = Mail(app)


db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login' 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(user_bp)
app.register_blueprint(publisher_bp)
app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def index():
    return redirect(url_for('public.home')) 

if __name__ == '__main__':
    # from models import *
    # from models.login_info import LoginInfo
    # from models.post import Post, Like, Comment
    # from models.user_profile import UserProfile
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
