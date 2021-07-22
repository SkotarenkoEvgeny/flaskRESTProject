from flask_restful import Resource

from src import api


class Smoke(Resource):
    def get(self):
        return {"message": "OK"}, 200


api.add_resource(Smoke, "/smoke/")
