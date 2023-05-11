#!/usr/bin/env python3
"""Entry file for app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """home index"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def new_user() -> str:
    """registers new users to the system"""
    try:
        email = request.form['email']
        pw = request.form['password']
        user = AUTH.register_user(email, pw)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """validate user and create session id"""
    email = request.form.get('email')
    pw = request.form.get('password')
    if not AUTH.valid_login(email, pw):
        abort(401)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie('session_id', AUTH.create_session(email))
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """logout current user and remove their session id"""
    id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """request session user data"""
    id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """user reset password token"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """update the user's password using reset_token"""
    email = request.form.get('email')
    reset = request.form.get('reset_token')
    pw = request.form.token('new_password')

    try:
        AUTH.update_password(reset, pw)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
