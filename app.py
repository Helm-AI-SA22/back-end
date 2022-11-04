from crypt import methods
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from utils.scopus_api import make_scopus_request
from utils.AI_request import make_post_request_to_AI
import os


class MockAI(Resource):

    def get(self):
        return {'prova AI': 'prova get'}
        

    def post(self):
        req_json = request.get_json()
        print('Json arrived to AI:', req_json)
        return_json = {'prova AI': 'riuscita'}
        return jsonify(return_json)


class Aggregator(Resource):

    def get(self):
        query_string = request.args.get("query_string")
        
        scopus_response = make_request(query_string)

        print(scopus_response)

        # search query_string on Scopus and return the results in a JSON format

        # elaborate front-end request

        # make request to scopus / ieee and merge
        # make post to ai server

        return make_post_request_to_AI(scopus_response)

    def post(self):
        # Non serve
        pass


class Home(Resource):

    def get(self):
        
        return "HOME in GET"

    def post(self):

        return "HOME in POST"

class FrontEndRequest(Resource):

    def get(self):
        
        with open('BE_respto_FE.json', "r") as json_file:
            data = json.load(json_file)
        
        json_file.close()

        return data


    def post(self):

        with open('BE_respto_FE.json', "r") as json_file:
            data = json.load(json_file)
        
        json_file.close()
        return data

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)

    # routes
    api.add_resource(Home, "/")
    api.add_resource(MockAI, "/mock_ai")
    api.add_resource(Aggregator, "/aggregator")
    api.add_resource(FrontEndRequest, "/front_end_request")
    
    # set host to gateway to handle route
    app.run(host = "0.0.0.0")
