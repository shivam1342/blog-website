from flask import Blueprint
from controllers import user_controller

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    return user_controller.register()

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    return user_controller.login()

@user_bp.route('/profile', methods=['GET'])
def view_profile():
    return user_controller.view_profile()

@user_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    return user_controller.edit_profile()

@user_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return user_controller.forgot_password()

@user_bp.route('/logout')
def logout():
    return user_controller.logout()

@user_bp.route('/profile/change-password', methods=['GET', 'POST'])
def change_password():
    return user_controller.change_password()