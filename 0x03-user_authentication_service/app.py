#!/usr/bin/env python3
"""Entry file for app"""
from flask import Flask, jsonify, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
