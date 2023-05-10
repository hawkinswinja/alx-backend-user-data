#!/usr/bin/env/python3
"""Entry file for app"""
from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """home index"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """registers new users to the system"""
    data = request.form
    email = data.get("'email")
    if email:
        pw = data.get("'password")
    else:
        email = data.get('email')
        pw = data.get('password')
    try:
        AUTH.register_user(email, pw)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
