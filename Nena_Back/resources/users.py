from flask import request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
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
        # Any authenticated user may look up any other user's public profile
        # (name/email) -- SideBar and mode-tile attribution need this. Only
        # write access below is restricted to the owner.
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404
        response_dict = user.to_dict()
        return make_response(response_dict, 200)

    @jwt_required()
    def patch(self, id):
        if str(get_jwt_identity()) != str(id):
            return {"error": "Forbidden"}, 403

        try:
            user = User.query.get(id)
            if not user:
                return {"error": "User not found"}, 404

            data = request.get_json()
            if not data:
                return {"error": "Missing data in request"}, 400

            if "name" in data:
                user.name = data["name"]
            if "email" in data:
                user.email = data["email"]
            if "password" in data or "newpassword" in data:
                current_password = data.get("current_password") or data.get("current")
                new_password = data.get("password") or data.get("newpassword")

                if not current_password:
                    return {"error": "Current password is required"}, 400
                if not bcrypt.check_password_hash(user.password, current_password):
                    return {"error": "Current password is incorrect"}, 401

                user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
            if "image" in data:
                user.image = data["image"]

            db.session.commit()

            return {"message": "User updated successfully", "user": user.to_dict()}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500

        except AssertionError as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    @jwt_required()
    def delete(self, id):
        if str(get_jwt_identity()) != str(id):
            return {"error": "Forbidden"}, 403

        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200


def register(api):
    api.add_resource(Users, '/users')
    api.add_resource(UserById, '/userById/<int:id>')
