from models.post import Post
from flask import flash, redirect, url_for, abort
from models import db
from flask_login import current_user


def list_posts(published=True):
    """
    Return list of posts filtered by published status.
    """
    return Post.query.filter_by(isPublished=published).order_by(Post.date_created.desc()).all()


def get_post(post_id):
    """
    Retrieve a post by its ID or abort with 404 if not found.
    """
    post = Post.query.get_or_404(post_id)
    if not post.isPublished and post.author != current_user:
        abort(403)
    return post


def create_post(form):
    """
    Create a new post using form data.
    """
    title = form.get('title', '').strip()
    content = form.get('content', '').strip()
    is_published = bool(form.get('isPublished'))

    # Validation
    if not title or not content:
        flash("Title and content are required.", "error")
        return redirect(url_for('posts.new_post'))

    # Create post
    post = Post(
        title=title,
        content=content,
        isPublished=is_published,
        user_id=current_user.id
    )

    db.session.add(post)
    db.session.commit()

    flash("Post created successfully!", "success")
    return redirect(url_for('posts.show_posts'))


def update_post(post_id, form):
    """
    Update an existing post using form data.
    """
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    title = form.get('title', '').strip()
    content = form.get('content', '').strip()
    is_published = bool(form.get('isPublished'))

    if not title or not content:
        flash("Title and content cannot be empty.", "error")
        return redirect(url_for('posts.edit_post', post_id=post_id))

    post.title = title
    post.content = content
    post.isPublished = is_published

    db.session.commit()

    flash("Post updated successfully!", "success")
    return redirect(url_for('posts.edit_post', post_id=post.id))


def list_drafts():
    """
    Return list of unpublished posts.
    """
    return list_posts(published=False)
