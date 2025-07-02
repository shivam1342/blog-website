from flask import Blueprint
from controllers.publisher_controller import (dashboard as dashboard_controller, create_post as create, edit_post as edit, delete_post as delete, publish_post as publish, get_post)
from controllers.publisher_controller import like_post as like, comment_post as comment


publisher_bp = Blueprint('publisher', __name__, url_prefix='/publisher')

@publisher_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return dashboard_controller()

@publisher_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    return create()

@publisher_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    return edit(post_id)

@publisher_bp.route('/delete/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    return delete(post_id)

@publisher_bp.route('/publish/<int:post_id>', methods=['GET'])
def publish_post(post_id):
    return publish(post_id)

@publisher_bp.route('/post/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    return like(post_id)

@publisher_bp.route('/post/<int:post_id>/comment', methods=['POST'])
def comment_post(post_id):
    return comment(post_id)

@publisher_bp.route('/post/<int:post_id>', methods=['GET'])
def show_post(post_id):
    return get_post(post_id)