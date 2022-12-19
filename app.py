"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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

    if (first_name is "" or last_name is ""):
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


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    with app.app_context():
        user = User.query.filter(User.id == user_id)
        user.delete()

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

    # @app.route("/<int:pet_id>")
    # def show_pet(pet_id):
    #     """Show details about a single pet"""
    #     pet = Pet.query.get_or_404(pet_id)
    #     return render_template("details.html", pet=pet)

    # @app.route("/species/<species_id>")
    # def show_pets_by_species(species_id):
    #     pets = Pet.get_by_species(species_id)
    #     return render_template("species.html", pets=pets, species=species_id)
