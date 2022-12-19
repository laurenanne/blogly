"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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


def __repr__(self):
    p = self
    return f"<User id ={p.id} name = {p.first_name} {p.last_name}>"
