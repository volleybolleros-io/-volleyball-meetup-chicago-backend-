import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):
    database_name = 'python_getting_started'
    default_detabase_path = 'postgres://{}:{}@{}/{}'.format('postgres', 'password', 'localhost:5432', database_name)
    database_path = os.getenv('DATABASE_URL', default_detabase_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Event(db.Model):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=False)
    start_date = Column(db.DateTime)

    def __init__(self, title, start_date):
        self.title = title
        self.start_date = start_date

    def details(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_date': self.start_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()