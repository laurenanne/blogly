from unittest import TestCase

from app import app
from flask import session

from models import db, User


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()


class UserTestCase(TestCase):

    def setUp(self):
        """Tests for views for Users"""
        with app.app_context():
            User.query.delete()

            user = User(first_name="TestUserFirst", last_name="TestUserLast")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        """clean up"""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUserFirst', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>TestUserFirst TestUserLast</p>', html)

    def test_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_new_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUserFirst2", "last_name": "TestUserLast2",
                 "image_url": "https://www.google.com/logos/doodles/2022/seasonal-holidays-2022-6753651837109831.4-s.png"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUserFirst TestUserLast", html)

    def test_no_first_name_user(self):
        with app.test_client() as client:
            d = {"first_name": "", "last_name": "TestUserLast3", "image_url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(('message', 'Must submit full name'),
                          session['_flashes'])
