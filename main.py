import datetime
from multiprocessing import Event
from sre_constants import SUCCESS
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api, abort

from src.models import *

app = Flask(__name__)
CORS(app)
api = Api(app)
setup_db(app)
# db_drop_and_create_all()

@app.route("/")
def health():
  return { "success": True }

@app.errorhandler(500)
def error():
  return { "success": False }

@app.route("/events")
def events():
  try:
    events = Event.query.order_by(Event.start_date).all()
    event = [evt.title for evt in events] 
    return { "events": event }
  except:
    abort(500)

@app.route("/login/<user_name>")
def login(user_name):
  return { "response": "Hello " + user_name }

@app.route("/sign_up")
def sign_up():
  return { "response": "success"}

@app.route("/register_event")
def register_event():
  try:
    event = Event("Secret Saturday", datetime.datetime.now())
    event.insert()
    return {"message": "event created"}
  except:
    abort(500)
    
@app.route("/rsvp")
def rsvp():
  return { "response": "success"}

if __name__ == "__main__":
  app.run(debug=True)
