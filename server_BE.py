from flask import Flask, request
from flask_restful import Resource, Api
from AI_request import make_post_request_to_AI
import requests


SITE = 'https://api.elsevier.com/content/search/scopus'
API_KEY = '3e68f6817fc5ecd448df31067d4bd08a'
HEADERS = 'apiKey=' + API_KEY + '&httpAccept=application/json'

def compose_request(q_str):
    return SITE + '?query=' + q_str + '&' + HEADERS


def run_server_BE(host, port):
    class BackendServer(Resource):

        def get(self):
            query_string = request.args.get("query_string")
            
            scopus_request = compose_request(query_string)
            scopus_response = requests.get(scopus_request).json()

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

