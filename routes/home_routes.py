from flask import Blueprint
from controllers.publisher_controller import ( home as home_controller, search_post)

public_bp = Blueprint('public', __name__)

@public_bp.route('/', methods=['GET'])
def home():
    return home_controller()

@public_bp.route('/search', methods=['GET'])
def search():
    return search_post()
