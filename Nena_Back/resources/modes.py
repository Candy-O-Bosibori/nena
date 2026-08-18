from flask import make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models import Mode


class Modes(Resource):
    @jwt_required()
    def get(self):
        modes = Mode.query.all()
        response_dict = [mode.to_dict() for mode in modes]
        return make_response(response_dict, 200)


def register(api):
    api.add_resource(Modes, '/modes')
