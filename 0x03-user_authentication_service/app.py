#!/usr/bin/env python3
""" Basic Flask app """
from flask import Flask, jsonify, request, abort, redirect
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
    if not AUTH.valid_login(email=email, password=password):
        abort(401)
    session_id = AUTH.create_session(email=email)
    response = jsonify({"email": f'{email}', "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ Route function that logs the users out """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


if __name__ == '__main__':
    """ Entry point of the back-end program """
    app.run(host='0.0.0.0', port='5000')
