from flask import request, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from models import db, User
from extensions import bcrypt


class Users(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        response_dict = [user.to_dict() for user in users]
        return make_response(response_dict, 200)


class UserById(Resource):
    @jwt_required()
    def get(self, id):
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404
        response_dict = user.to_dict()
        return make_response(response_dict, 200)

    @jwt_required()
    def patch(self, id):
        try:
            user = User.query.get(id)
            if not user:
                return {"error": "User not found"}, 404

            data = request.get_json()

            if "name" in data:
                user.name = data["name"]
            if "email" in data:
                user.email = data["email"]
            if "password" in data:
                user.password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
            if "image" in data:
                user.image = data["image"]

            db.session.commit()

            return {"message": "User updated successfully", "user": user.to_dict()}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    @jwt_required()
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200


def register(api):
    api.add_resource(Users, '/users')
    api.add_resource(UserById, '/userById/<int:id>')
