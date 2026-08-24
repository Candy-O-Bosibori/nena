from flask import make_response
from flask_restful import Resource

from constants.frameworks import FRAMEWORKS


class FrameworksResource(Resource):
    def get(self):
        return make_response({"frameworks": FRAMEWORKS}, 200)


def register(api):
    api.add_resource(FrameworksResource, '/frameworks')
