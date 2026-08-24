from flask import make_response
from flask_restful import Resource

from models import Mode


class Modes(Resource):
    def get(self):
        modes = Mode.query.all()
        # Opt back into a shallow recordings list; the frontend's stat boxes read
        # mode.recordings.length. Recording's own rules keep it from nesting further.
        response_dict = [mode.to_dict(rules=('recordings',)) for mode in modes]
        return make_response(response_dict, 200)


def register(api):
    api.add_resource(Modes, '/modes')
