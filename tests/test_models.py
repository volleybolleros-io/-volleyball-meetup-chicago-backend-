import datetime
import unittest
from main import app

from src.models import *

class DBTestCase(unittest.TestCase):

    def setUp(self) -> None:
        setup_db(app)
        db.session.close()
        db.drop_all()
        db.create_all()

        user = User(firstname="first_name", lastname="last_name", email="test@test.com", password="test_password")
        db.session.add(user)
        db.session.commit()

        event = Event(title="test_title", start_date=datetime.datetime.now())
        db.session.add(event)
        db.session.commit()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_user_model(self):
        user = User.query.filter(User.email == "test@test.com").first()
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.firstname, "first_name")
        self.assertEqual(user.lastname, "last_name")

    def test_event_model(self):
        event = Event.query.order_by(Event.id).first()
        self.assertIsNotNone(event)
        self.assertIsNotNone(event.id)
        self.assertEqual(event.title, "test_title")

    def test_get_by_email(self):
        user = User.get_by_email("test@test.com")
        self.assertIsNotNone(user)
        user = User.get_by_email("hacker")
        self.assertIsNone(user)

    def test_mixin_as_dict(self):
        user = User.query.order_by(User.id).first()
        user_as_dict = user.as_dict()
        self.assertIsNotNone(user_as_dict)
        self.assertEqual(user_as_dict["email"], "test@test.com")
        self.assertEqual(user_as_dict["id"], 1)
        self.assertEqual(user_as_dict["firstname"], "first_name")
        self.assertEqual(user_as_dict["lastname"], "last_name")
        self.assertEqual(user_as_dict["password"], "test_password")

        event = Event.query.order_by(Event.id).first()
        event_as_dict = event.as_dict()
        self.assertIsNotNone(event_as_dict)
        self.assertEqual(event_as_dict["title"], "test_title")

    def test_has_event(self):
        user = User.query.filter(User.email == "test@test.com").first()
        event = Event.query.filter(Event.title == "test_title").first()

        self.assertIsNotNone(user)
        self.assertIsNotNone(event)

        self.assertEqual(user.id, 1)
        self.assertEqual(event.id, 1)

        rsvp = RSVP(state="pending", event_id=1, user_id=1)
        db.session.add(rsvp)
        db.session.commit()

        self.assertTrue(event.has_rsvp)
