from flask import Flask, request
from flask_restful import Resource, Api

from utils.scopus_api import make_request
from utils.AI_request import make_post_request_to_AI
import requests


def run_server_BE(host, port):
    class BackendServer(Resource):

        def get(self):
            query_string = request.args.get("query_string")
            
            scopus_response = make_request(query_string)

            # search query_string on Scopus and return the results in a JSON format

            # elaborate front-end request

            # make request to scopus / ieee and merge
            # make post to ai server

            return make_post_request_to_AI(scopus_response)
           
            # elaborate response from ai server


        def post(self):
            # Non serve
            pass


    app = Flask(__name__)
    api = Api(app)
    api.add_resource(BackendServer, "/")
    app.run(host = host, port = port)
