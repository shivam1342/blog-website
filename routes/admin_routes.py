from flask import Blueprint
from controllers import admin_controller

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/users', methods=['GET'])
def view_users():
    return admin_controller.view_users()

@admin_bp.route('/user/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    return admin_controller.delete_user(user_id)

@admin_bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    return admin_controller.edit_user(user_id)

@admin_bp.route('/posts', methods=['GET'])
def view_all_posts():
    return admin_controller.view_all_posts()

@admin_bp.route('/post/delete/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    return admin_controller.delete_post(post_id)


@admin_bp.route('/approvals', methods=['GET'])
def pending_posts():
    return admin_controller.pending_posts()

@admin_bp.route('/approve/<int:post_id>', methods=['GET'])
def approve_post(post_id):
    return admin_controller.approve_post(post_id)

@admin_bp.route('/disapprove/<int:post_id>', methods=['GET'])
def disapprove_post(post_id):
    return admin_controller.disapprove_post(post_id)
