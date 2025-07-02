from flask import render_template, request, redirect, url_for, session, abort
from models.post import Post
from models import db
from datetime import datetime
from models.post import Like, Comment
from models.login_info import LoginInfo


def home():
    page = request.args.get('page', 1, type=int)
    per_page = 5 
    posts = Post.query.filter(
        Post.is_published == True,
        Post.is_approved == True,
        Post.is_deleted == False
    ).order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template('home.html', posts=posts)


def search_post():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    query = request.args.get('q', '').strip()
    tag_filter = request.args.get('tag', '').strip()
    publisher_filter = request.args.get('publisher', '').strip()

    posts_query = Post.query.filter(
        Post.is_published == True,
        Post.is_approved == True,
        Post.is_deleted == False
    )

    if query:
        posts_query = posts_query.filter(Post.title.ilike(f"%{query}%"))

    if tag_filter:
        posts_query = posts_query.filter(Post.tags.ilike(f"%{tag_filter}%"))

    if publisher_filter.isdigit():
        posts_query = posts_query.filter(Post.user_id == int(publisher_filter))

    posts = posts_query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page)

    publishers = LoginInfo.query.filter_by(role='publisher').all()

    return render_template(
        'home.html',
        posts=posts,
        publishers=publishers,
        query=query,
        tag_filter=tag_filter,
        publisher_filter=publisher_filter
    )




def dashboard():
    if session.get('role') != 'publisher':
        return "You are not authorized to perform this action.", 403

    user_id = session.get('user_id')
    posts = Post.query.filter_by(user_id=user_id, is_deleted=False).order_by(Post.created_at.desc()).all()
    return render_template('publisher_dashboard.html', posts=posts)

def create_post():
    if session.get('role') != 'publisher':
        return "You are not allowed to perform this action."

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form['tags']
        is_published = request.form.get('isPublished') == 'on'

        new_post = Post(
            title=title,
            content=content,
            tags=tags,
            is_published=is_published,
            is_approved=False,
            is_deleted=False,
            user_id=session['user_id'],
            created_at=datetime.now()
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect('/publisher/dashboard')

    return render_template('create_post.html')

def edit_post(post_id):
    if session.get('role') != 'publisher':
        return "You are not authorized to perform this action.", 403

    post = Post.query.get_or_404(post_id)
    if post.user_id != session.get('user_id'):
        abort(403)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.tags = request.form['tags']
        post.is_published = request.form.get('isPublished') == 'on'
        db.session.commit()
        return redirect(url_for('publisher.dashboard'))

    return render_template('create_post.html', post=post)

def get_post(post_id):
    user_id = session.get('user_id')
    # if not user_id:
    #     return redirect(url_for('user.login'))
    post = Post.query.get_or_404(post_id)
    has_liked = False

    if user_id:
        has_liked = Like.query.filter_by(user_id=user_id, post_id=post_id).first() is not None

    if not post.is_published or not post.is_approved or post.is_deleted:
        if session.get('user_id') != post.user_id and session.get('role') != 'admin':
            abort(403)

    return render_template('view_post.html', post=post, Comment=Comment, has_liked=has_liked)


def delete_post(post_id):
    if session.get('role') != 'publisher':
        return "You are not authorized to perform this action.", 403

    post = Post.query.get_or_404(post_id)
    if post.user_id != session.get('user_id'):
        abort(403)

    post.is_deleted = True
    db.session.commit()
    return redirect(url_for('publisher.dashboard'))


def publish_post(post_id):
    if session.get('role') != 'publisher':
        return "You are not authorized to perform this action.", 403

    post = Post.query.get_or_404(post_id)
    if post.user_id != session.get('user_id'):
        abort(403)

    post.is_published = True
    db.session.commit()
    return redirect(url_for('publisher.dashboard'))



def like_post(post_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('user.login'))

    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if like:
        db.session.delete(like)
    else:
        db.session.add(Like(user_id=user_id, post_id=post_id))
    db.session.commit()
    return redirect(url_for('publisher.show_post', post_id=post_id))


def comment_post(post_id):
    user_id = session.get('user_id')
    content = request.form.get('comment')

    if content:
        comment = Comment(user_id=user_id, post_id=post_id, content=content)
        db.session.add(comment)
        db.session.commit()

    return redirect(url_for('publisher.show_post', post_id=post_id))