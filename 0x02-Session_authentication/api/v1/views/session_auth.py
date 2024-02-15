#!/usr/bin/env python3
""" Module of Session Authentication view
"""
from flask import jsonify, abort, request
import os
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """ Function that retrieve the login info (Email, Password)
        from request form
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
        if not users:
            return jsonify({"error": "no user found for this email"}), 404
        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                response = jsonify(user.to_json())
                cookie_name = os.environ.get('SESSION_NAME')
                response.set_cookie(cookie_name, session_id)
                return jsonify(response)
            else:
                return jsonify({"error": "wrong password"}), 401
        return jsonify({"error": "no user found for this email"}), 404
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
