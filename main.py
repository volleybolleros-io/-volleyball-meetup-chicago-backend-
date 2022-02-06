from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route("/")
def health():
  return { "success": True }

@app.errorhandler(500)
def error():
  return { "success": False }

@app.route("/events")
def events():
  return { "response": "success"}

@app.route("/login/<user_name>")
def login(user_name):
  return { "response": "Hello " + user_name }

@app.route("/sign_up")
def sign_up():
  return { "response": "success"}

@app.route("/register_event")
def register_event():
  return { "response": "success"}

@app.route("/rsvp")
def rsvp():
  return { "response": "success"}


if __name__ == "__main__":
  app.run(debug=True)