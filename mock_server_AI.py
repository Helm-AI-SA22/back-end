from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json

def run_server_mock_AI(host, port):
    class BackendServer(Resource):

        def get(self):
            return {'prova AI': 'prova get'}
            


        def post(self):
            req_json = request.get_json()
            print('Json arrived to AI:', req_json)

            return_json = {'prova AI': 'prova prova prova vnslofnsw'}

            return jsonify(return_json)




    app = Flask(__name__)
    api = Api(app)
    api.add_resource(BackendServer, "/")
    app.run(host = host, port = port)

