from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, create_refresh_token,
    decode_token
)
from flask_restful import Resource

from models import db, User
from extensions import bcrypt


class SignIn(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"error": "User does not exist"}, 401

        if not bcrypt.check_password_hash(user.password, password):
            return {"error": "Incorrect password"}, 401

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
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


def register(api):
    api.add_resource(SignIn, '/signin')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(SignUp, '/signup')
