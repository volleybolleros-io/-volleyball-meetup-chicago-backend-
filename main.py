from multiprocessing import Event
from sre_constants import SUCCESS
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, abort
from werkzeug.security import generate_password_hash, check_password_hash

from src.models import *

app = Flask(__name__)
CORS(app)
api = Api(app)
setup_db(app)

# TODO
is_prod = False
if is_prod:
  db_drop_and_create_all()

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

@app.route("/login", methods=["POST"])
def login():
  email = request.form.get("email")
  password = request.form.get("password")

  user = User.query.filter_by(email=email).first()

  if not user or not check_password_hash(user.password, password):
    return {"message": "User does not exist or wrong credentials!"}

  user.last_login = datetime.datetime.now()
  user.update()

  return {"message": f"Welcome back {user.firstname} {user.lastname}! Last login: {user.last_login:%Y-%m-%d %H:%M}"}

@app.route("/signup", methods=["POST"])
def signup_post():
  firstname = request.form.get("firstname")
  lastname = request.form.get("lastname")
  email = request.form.get("email")
  password = request.form.get("password")

  user = User.query.filter_by(email=email).first()

  if user:
    return { "message": f"ERROR: user already exists."}

  try:
    new_user = User(firstname=firstname, lastname=lastname, email=email, password=generate_password_hash(password, method="sha256"))
    new_user.insert()

    return { "message": f"Welcome {new_user.firstname} {new_user.lastname}!" }
  except:
    abort(500)

@app.route("/register_event")
def register_event():
  try:
    event = Event("Secret Saturday", datetime.datetime.now())
    event.insert()
    return {"message": f"Event {event.title} created!"}
  except:
    abort(500)

@app.route("/rsvp")
def rsvp():
  return { "response": "success"}

if __name__ == "__main__":
  app.run(debug=True)
