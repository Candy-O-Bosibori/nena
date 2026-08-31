import os
from datetime import timedelta

from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, create_refresh_token,
    decode_token
)
from flask_restful import Resource
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from models import db, User
from models.user import validate_password_strength
from extensions import bcrypt

# "Remember me" unchecked still needs to survive a page refresh (the client
# holds it in sessionStorage rather than localStorage for that case), just
# not indefinitely. This bounds that unremembered session server-side too,
# independent of the client-side storage choice.
NOT_REMEMBERED_REFRESH_TOKEN_EXPIRES = timedelta(hours=12)


class SignIn(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        email = data.get('email')
        password = data.get('password')
        remember_me = bool(data.get('remember_me'))

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"error": "User does not exist"}, 401

        if not user.password or not bcrypt.check_password_hash(user.password, password):
            return {"error": "Incorrect password"}, 401

        access_token = create_access_token(identity=str(user.id))
        refresh_expires = None if remember_me else NOT_REMEMBERED_REFRESH_TOKEN_EXPIRES
        refresh_token = create_refresh_token(identity=str(user.id), expires_delta=refresh_expires)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200


class TokenRefresh(Resource):
    """Exchange a refresh token for a fresh access token.

    Accepts the refresh token either as `Authorization: Bearer <token>` or in the
    JSON body as {"token": ...} / {"refresh_token": ...}, so any client shape works.

    Returns the new access token under several key names for the same reason, and
    rotates the refresh token so a user who keeps using the app never expires.
    """

    def post(self):
        identity = None

        # 1. Authorization header (standard flask-jwt-extended form)
        auth_header = request.headers.get("Authorization", "")
        raw_token = None
        if auth_header.startswith("Bearer "):
            raw_token = auth_header.split(" ", 1)[1].strip()

        # 2. JSON body fallback
        if not raw_token:
            body = request.get_json(silent=True) or {}
            raw_token = body.get("token") or body.get("refresh_token")

        if not raw_token:
            return {"error": "Missing refresh token"}, 401

        try:
            decoded = decode_token(raw_token)
        except Exception:
            return {"error": "Invalid or expired refresh token"}, 401

        if decoded.get("type") != "refresh":
            return {"error": "Expected a refresh token"}, 401

        identity = decoded.get("sub")
        if not identity:
            return {"error": "Invalid refresh token"}, 401

        # Confirm the account still exists before minting anything.
        if not User.query.get(int(identity)):
            return {"error": "User no longer exists"}, 401

        access_token = create_access_token(identity=str(identity))
        new_refresh_token = create_refresh_token(identity=str(identity))

        return {
            "access_token": access_token,
            "accessToken": access_token,
            "refresh_token": new_refresh_token,
            "refreshToken": new_refresh_token,
        }, 200


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        image = data.get('image', None)  # optional

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            validate_password_strength(password)
        except AssertionError as e:
            return {"error": str(e)}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            image=image
        )

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=str(new_user.id))
        refresh_token = create_refresh_token(identity=str(new_user.id))

        return {"access_token": access_token, "refresh_token": refresh_token}, 200


class GoogleSignIn(Resource):
    """Exchange a Google Identity Services ID token for our own JWTs.

    Verifies the token against Google's public keys (audience-checked against
    our own client ID) rather than trusting anything the client claims about
    the user. Links to an existing account by email on first Google sign-in
    so a user who already registered with a password doesn't get a duplicate.
    """

    def post(self):
        data = request.get_json(silent=True) or {}
        credential = data.get('credential')
        if not credential:
            return {"error": "Missing credential"}, 400

        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        if not client_id:
            return {"error": "Google sign-in is not configured"}, 500

        try:
            payload = google_id_token.verify_oauth2_token(
                credential, google_requests.Request(), client_id
            )
        except ValueError:
            return {"error": "Invalid Google credential"}, 401

        google_id = payload.get('sub')
        email = payload.get('email')
        if not google_id or not email:
            return {"error": "Google credential missing required fields"}, 401

        user = User.query.filter_by(google_id=google_id).first()

        if not user:
            user = User.query.filter_by(email=email).first()
            if user:
                user.google_id = google_id
            else:
                user = User(
                    name=payload.get('name') or email.split('@')[0],
                    email=email,
                    password=None,
                    image=payload.get('picture'),
                    google_id=google_id,
                )
                db.session.add(user)
            db.session.commit()

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return {"access_token": access_token, "refresh_token": refresh_token}, 200


def register(api):
    api.add_resource(SignIn, '/signin')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(SignUp, '/signup')
    api.add_resource(GoogleSignIn, '/auth/google')
