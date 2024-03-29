#!/usr/bin/env python3
""" Module of Session Authentication view
"""
from flask import jsonify, abort, request
from os import getenv
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """ Function that retrieve the login info (Email, Password)
        from request form
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
        return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ Funtion that called when a request of logout sent
    """
    from api.v1.app import auth
    result = auth.destroy_session(request)
    if not result:
        abort(404)
    return jsonify({}), 200
