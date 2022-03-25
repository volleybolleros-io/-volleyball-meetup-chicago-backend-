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

is_prod = False # FIXME
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
    events_as_dict = [evt.as_dict() for evt in events]
    return { "events": events_as_dict }
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

  return {"message": user.as_dict()}

@app.route("/signup", methods=["POST"])
def signup_post():
  fullname = request.form.get("name")
  email = request.form.get("email")
  password = request.form.get("password")

  user = User.query.filter_by(email=email).first()

  if user:
    return { "message": "ERROR: user already exists."}

  try:
    new_user = User(fullname=fullname, email=email, password=generate_password_hash(password, method="sha256"))
    new_user.insert()

    return { "message": new_user.as_dict() }
  except:
    abort(500)

@app.route("/register-event", methods=["POST"])
def register_event():
  title = request.form.get("title")
  description = request.form.get("description")
  start_date = request.form.get("start_date") # Assuming this is ISO 8601 example: '2018-06-29 08:15:27.243860'
  date_time_object = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S.%f')
  try:
    event = Event(title, description, date_time_object)
    event.insert()
    return {"message": event.as_dict()}
  except:
    abort(500)

@app.route("/rsvp")
def rsvp():
  try:
    rsvps = RSVP.query.order_by(RSVP.signed_up_at).all()
    rsvps_as_dict = [evt.as_dict() for evt in rsvps]
    return { "rsvps": rsvps_as_dict }
  except:
    abort(500)

if __name__ == "__main__":
  app.run(debug=True)
