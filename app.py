"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secrets7"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()


@app.route('/')
def home():
    return redirect('/users')


"""routes for useres"""


@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def display_form():

    return render_template('form.html')


@app.route('/users/new', methods=['POST'])
def new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if (first_name == "" or last_name == ""):
        flash('Must submit full name')
        return redirect('/users/new')

    else:
        new_user = User(first_name=first_name,
                        last_name=last_name, image_url=image_url)

        with app.app_context():
            db.session.add(new_user)
            db.session.commit()

            return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    with app.app_context():
        user = User.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


"""routes for posts"""


@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post-form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
    title = request.form['title']
    content = request.form['content']

    if (title == ""):
        flash('Your post must have a title')
        return redirect(f'/users/{user_id}/posts/new')

    if (content == ""):
        flash('Your post must have content')
        return redirect(f'/users/{user_id}/posts/new')

    else:
        new_post = Post(title=title,
                        content=content, user_key=user_id)

        with app.app_context():
            db.session.add(new_post)
            db.session.commit()

            return redirect(f'/posts/{new_post.id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('edit-post.html', post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    with app.app_context():
        post = Post.query.get_or_404(post_id)

        db.session.delete(post)
        db.session.commit()

    return redirect(f'/users/{post.user_key}')


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


"""routes for tags """


@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tag.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def new_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-details.html', tag=tag)


@app.route('/tags/new')
def display_tag_form():

    return render_template('tag-form.html')


@app.route('/tags/new', methods=['POST'])
def show_tag():
    name = request.form['name']

    if (name == ""):
        flash('Your tag cannot be blank')
        return redirect(f'/tags/new')

    else:
        new_tag = Tag(name=name)

        db.session.add(new_tag)
        db.session.commit()

        return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit-tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    with app.app_context():
        tag = Tag.query.get_or_404(tag_id)

        db.session.delete(tag)
        db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag_id}')
