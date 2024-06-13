#!/usr/bin/env python3
""" app module
Implements Flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Registers a user
    POST /users
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        user = AUTH.register_user(email, password)
        response = {"email": user.email, "message": "user created"}
        return jsonify(response), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """POST /sessions
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """DELETE /sessions
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        abort(403)
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """GET /profile
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        abort(403)
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """POST /reset_password
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        response = {"email": email, "reset_token": reset_token}
        return jsonify(response), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
