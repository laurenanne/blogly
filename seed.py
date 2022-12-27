"""Seed file to make sample data for blogly db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

# If table isn't empty, empty it
    User.query.delete()
    Post.query.delete()
    Tag.query.delete()
    PostTag.query.delete()

# Add users
santa = User(first_name="Santa", last_name="Claus",
             image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Jonathan_G_Meath_portrays_Santa_Claus.jpg/1200px-Jonathan_G_Meath_portrays_Santa_Claus.jpg")
elf = User(first_name="Betty", last_name="Elf",
           image_url="https://img.freepik.com/premium-vector/happy-cute-little-kid-boy-girl-wearing-green-elf-christmas-costume_97632-3315.jpg?w=2000")
snow = User(first_name="Frosty", last_name="Snowman",
            image_url="https://i.etsystatic.com/37674354/r/il/693b1f/4348260065/il_794xN.4348260065_8jz3.jpg")
rudy = User(first_name="Rudolph", last_name="Reindeer",
            image_url="https://st.depositphotos.com/1033654/1283/v/600/depositphotos_12832389-stock-illustration-rudolph-reindeer-red-nose.jpg")


# Add new objects to session, so they'll persist
with app.app_context():
    db.session.add(santa)
    db.session.add(elf)
    db.session.add(snow)
    db.session.add(rudy)

# Commit--otherwise, this never gets saved!
    db.session.commit()
