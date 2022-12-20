import json
from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from utils.utils import debug_log
from utils.aggregator import execute_aggregation_topic_modeling, add_topic_ratio
from utils.filtering import filtering
from utils.ranking import rank
from flask_cors import CORS
from flask_log_request_id import RequestID
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s : %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default',
    }},
# TODO: understand how doesn't works
#    'filters': {
#        'myfilter': {
#            '()': RequestIDLogFilter,
#        }
#    },
    'root': {
        'level': 'NOTSET',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
RequestID(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)


class Aggregator(Resource):

    #TODO rimuovere get?
    def get(self):

        keywords = request.args.get("keywords").split(";")

        topic_modeling = request.args.get("type")
        
        return jsonify(execute_aggregation_topic_modeling(keywords, topic_modeling))


    def post(self):

        data = request.get_json()
        keywords = data["keywords"].split(";")
        topic_modeling = data["type"]
        return jsonify(execute_aggregation_topic_modeling(keywords, topic_modeling))


class RankRequest(Resource):

    def get(self):

        criteria = request.args["criteria"]
        ascending = request.args["ascending"]

        debug_log(f"starting mock sorting request type : {criteria}")

        with open('mocks/aggregated_fast.json', "r") as json_file:
            data = json.load(json_file)

        documents_list = data["documents"]
        return jsonify({"documents": rank(documents_list, criteria, ascending)})

    def post(self):

        data = request.get_json()

        criteria = data["criteria"]
        ascending = data["ascending"]

        debug_log(f"starting sorting request type : {criteria}")

        documents_list = data["documents"]
        return jsonify({"documents": rank(documents_list, criteria, ascending)})


def mock_retrieving(topic_modeling):
    if topic_modeling == "slow":

        with open('mocks/aggregated_slow.json', "r") as json_file:
            data = json.load(json_file)

        debug_log("retrieved slow mock data")

    elif topic_modeling == "fast":

        with open('mocks/aggregated_fast.json', "r") as json_file:
            data = json.load(json_file)

        debug_log("retrieved fast mock data")

    else:
        raise Exception("type key not valid (slow | fast)")

            
    return data


class FrontEndRequest(Resource):

    def get(self):

        topic_modeling = request.args.get("type")

        debug_log(f"starting get mock request type : {topic_modeling}")

        return jsonify(mock_retrieving(topic_modeling))

    def post(self):
    
        data = request.get_json()

        topic_modeling = data["type"]

        debug_log(f"starting post mock request type : {topic_modeling}")

        return jsonify(mock_retrieving(topic_modeling))


class FilteringRequest(Resource):

    def post(self):

        return jsonify(filtering(request.get_json()))


class Prova(Resource):

    def post(self):
        return jsonify(add_topic_ratio(request.get_json())) 


if __name__ == "__main__":
    # routes
    api.add_resource(Aggregator, "/aggregator")
    api.add_resource(FrontEndRequest, "/mock")
    api.add_resource(FilteringRequest, "/filtering")
    api.add_resource(RankRequest, "/ranking")

    api.add_resource(Prova, "/prova")

    # set host to gateway to handle route
    app.run(host = "0.0.0.0")