import datetime
import os
from sqlalchemy import Column, ForeignKey, String, Integer, exists
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, column_property

db = SQLAlchemy()

def setup_db(app):
    database_name = 'python_getting_started'
    default_detabase_path = 'postgresql://{}:{}@{}/{}'.format('postgres', 'password', 'localhost:5432', database_name)
    database_path = os.getenv('DATABASE_URL', default_detabase_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

# Mixins
class MixinAsDict:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class RSVP(MixinAsDict, db.Model):
    __tablename__ = 'rsvp'
    id = Column(Integer, primary_key=True)
    state = Column(String(50))
    event_id = Column(Integer, ForeignKey('event.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    signed_up_at = Column(db.DateTime)

    def __init__(self, state, event_id, user_id):
        self.firstname = state
        self.event_id = event_id
        self.user_id = user_id
        self.signed_up_at = datetime.datetime.now()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

# The Event table to store events that represents games on the calendar. A User can register to one or more Events.
class Event(MixinAsDict, db.Model):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    description = Column(String(250))
    start_date = Column(db.DateTime)
    rsvp = relationship(RSVP, backref='event')
    has_rsvp = column_property(
        exists().where(RSVP.event_id == id)
    )

    def __init__(self, title, description, start_date):
        self.title = title
        self.description = description
        self.start_date = start_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

# Mixins
class MixinGetByEmail:
    email = Column(String(100), unique=True)

    @classmethod
    def get_by_email(cls, email):
        return db.session.query(cls).filter(cls.email == email).first()

# The User table to store users which represents playes that can register to events.
class User(MixinAsDict, MixinGetByEmail, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    password = Column(String(100))
    fullname = Column(String(50))
    last_login = Column(db.DateTime)
    rsvp = relationship(RSVP, backref='user')

    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.last_login = datetime.datetime.now()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
