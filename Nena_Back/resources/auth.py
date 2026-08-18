from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, create_refresh_token
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
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return {'access_token': access_token}, 200
        except Exception as e:
            return jsonify(error=str(e)), 500


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
