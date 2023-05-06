#!/usr/bin/python3
"""views for session authentication"""
from flask import request, jsonify, abort
from os import getenv
from . import app_views, User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login form for session authentication"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(getenv('SESSION_NAME'), user[0].id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def destroy_session():
    """logout user"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
