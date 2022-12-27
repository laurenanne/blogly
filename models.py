"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String,)

    posts = db.relationship("Post", backref="user")

    def __repr__(self):
        p = self
        return f"<User id ={p.id} name = {p.first_name} {p.last_name}>"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    user_key = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # post_tag = db.relationship('PostTag',
    #    backref = 'post')

    post_t = db.relationship('Tag', secondary="post_tags", backref="post")

    def __repr__(self):
        p = self
        return f"<Post id ={p.id} name = {p.title}>"


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    p = db.relationship('PostTag', backref='t')


class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), nullable=False, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), nullable=False, primary_key=True)
