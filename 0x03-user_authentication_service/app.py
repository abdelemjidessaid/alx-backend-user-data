#!/usr/bin/env python3
""" Basic Flask app """
from flask import Flask, jsonify, request, abort, redirect, make_response
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def main_page() -> str:
    """ Welcome page """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ Function route that registers users """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Route function that log the users in """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_auth = AUTH.valid_login(email=email, password=password)
    if valid_auth:
        session_id = AUTH.create_session(email=email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return make_response(response)
    abort(401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
