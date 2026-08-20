from flask import make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from constants.frameworks import FRAMEWORKS


class FrameworksResource(Resource):
    @jwt_required()
    def get(self):
        return make_response({"frameworks": FRAMEWORKS}, 200)


def register(api):
    api.add_resource(FrameworksResource, '/frameworks')
