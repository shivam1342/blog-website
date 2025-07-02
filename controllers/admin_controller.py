from flask import render_template, request, session, redirect, url_for, abort
from models.login_info import LoginInfo
from models.user_profile import UserProfile
from models.post import Post
from models import db
from flask_mailman import EmailMessage


def admin_only():
    if session.get('role') != 'admin':
        abort(403)



def view_users():
    admin_only()
    users = LoginInfo.query.join(UserProfile).filter(UserProfile.is_deleted == False).all()
    return render_template('admin/users.html', users=users)

def delete_user(user_id):
    admin_only()

    user = LoginInfo.query.get(user_id)
    if user and user.role == 'admin':
        return "Cannot delete admin users.", 403

    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if profile:
        profile.is_deleted = True
        db.session.commit()

    return redirect(url_for('admin.view_users'))


def edit_user(user_id):
    admin_only()
    user = LoginInfo.query.get_or_404(user_id)

    if request.method == 'POST':
        new_role = request.form['role']
        new_password = request.form['password']
        if new_role in ['admin', 'publisher', 'visitor']:
            user.role = new_role
        if new_password:
            user.password = new_password
        db.session.commit()
        return redirect(url_for('admin.view_users'))

    return render_template('admin/edit_user.html', user=user)



def view_all_posts():
    admin_only()
    posts = Post.query.filter(Post.is_deleted == False).order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

def delete_post(post_id):
    admin_only()
    post = Post.query.get_or_404(post_id)
    post.is_deleted = True
    db.session.commit()
    return redirect(url_for('admin.view_all_posts'))



def pending_posts():
    admin_only()
    posts = Post.query.filter(Post.is_published == True, Post.is_approved == False, Post.is_deleted == False).order_by(Post.created_at.desc()).all()
    return render_template('admin/approvals.html', posts=posts)

def approve_post(post_id):
    admin_only()
    post = Post.query.get_or_404(post_id)

    author = post.author
    if not author:
        return "Author not found", 404

    post.is_approved = True
    db.session.commit()


    subject = "Your Post Approved"
    message = f"Hello {author.username},\n\nYour post titled \"{post.title}\" has been approved by the admin."
    email = EmailMessage(subject, message, to=[author.profile.email])
    email.send()

    return redirect(url_for('admin.pending_posts'))

def disapprove_post(post_id):
    admin_only()
    post = Post.query.get_or_404(post_id)

    author = post.author
    if not author or not author.profile:
        return "Author profile not found", 404

    post.is_deleted = True
    db.session.commit()

    subject = "Your Post Has Been Disapproved"
    message = f"Hello {author.username},\n\nUnfortunately, your post titled \"{post.title}\" has been disapproved by the admin."
    email = EmailMessage(subject, message, to=[author.profile.email])
    email.send()

    return redirect(url_for('admin.pending_posts'))