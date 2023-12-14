from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import post_bp
from .. import db
from .forms import PostForm
from .models import Post

@post_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            text=form.text.data,
            type=form.type.data,
            user_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post added', 'success')
        return redirect(url_for('post_bp.posts'))

    return render_template('create_post.html', form=form)

@post_bp.route('/post', methods=['GET'])
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

@post_bp.route('/post/<int:id>', methods=['GET'])
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template('view_post.html', post=post)

@post_bp.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        db.session.commit()
        flash('Post updated', 'success')
        return redirect(url_for('post_bp.view_post', id=post.id))

    return render_template('update_post.html', form=form, post=post)

@post_bp.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('post_bp.posts'))
