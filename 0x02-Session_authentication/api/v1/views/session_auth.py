#!/usr/bin/env python3
"""session_auth
Handles all routes for the Session authentication.
"""
import os
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve User instance based on email
    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth

            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            cookie_name = os.getenv("SESSION_NAME")
            response.set_cookie(cookie_name, session_id)

            return response

    return jsonify({"error": "wrong password"}), 401


@app_views.route("/api/v1/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logs out a user
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
