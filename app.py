import json
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, reqparse
from utils.scopus_api import make_scopus_request
from utils.ieee_api import make_ieee_request
from utils.utils import debug_log
from utils.AI_request import make_post_request_to_AI
from utils.filtering import filtering
from flask_cors import CORS
from flask_log_request_id import RequestID

import sys
from logging.config import dictConfig
import logging

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
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


def add_topic_paper(topics, papers, doi):
    for paper in papers:
        if paper["id"] == str(doi):
            paper["topics"] = topics

    return papers


def process_ai_result(ai_result, list_papers):
    documents_result_ai = ai_result.pop("documents")

    for doc in documents_result_ai:
        doi = doc["id"]
        list_papers = add_topic_paper(doc["topics"], list_papers, doi)

    ai_result["documents"] = list_papers

    return ai_result


def format_data_ai(list_papers, key_doi, key_abstract):
    return_list = list()
    
    for paper in list_papers:
        if not paper[key_abstract] is None:

            formatted_paper = dict()

            formatted_paper[key_doi] = paper[key_doi]
            formatted_paper[key_abstract] = paper[key_abstract]

            return_list.append(formatted_paper)
    
    return return_list


def remove_duplicated(results, key):
    memo = set()
    transformed_results = list()
    
    for res in results:
        if not res[key] in memo:
            transformed_results.append(res)
            memo.add(res[key])

    return transformed_results


def mapping_feature_names(results, start_features, end_features):

    transformed_results = list()

    for res in results:
        transformed_results.append({end_features[i]: res[k] for i, k in enumerate(start_features)})
    
    return transformed_results


def aggregator(ieee_results, scopus_results):

    with open("aggregation_features.json") as f:
        aggregation_features = json.load(f)

    ieee_transformed_results = mapping_feature_names(ieee_results, aggregation_features["ieee"], aggregation_features["aggregated"])
    scopus_transformed_results = mapping_feature_names(scopus_results, aggregation_features["scopus"], aggregation_features["aggregated"])

    results = ieee_transformed_results + scopus_transformed_results

    # remove duplicate
    transformed_results = remove_duplicated(results, aggregation_features["aggregated_key"])

    return transformed_results


def execute_aggregation_topic_modeling(keywords, topic_modeling):
    
    ieee_results = make_ieee_request(keywords)

    debug_log("ieee done")

    scopus_results = make_scopus_request(keywords)

    debug_log("scopus done")

    aggregated_results = aggregator(ieee_results, scopus_results)

    debug_log("aggregation done")

    # take simple subset, to be fast
    # aggregated_results = aggregated_results[:200]

    with open("aggregation_features.json") as f:
        aggregation_features = json.load(f)

    # apply filtering

    # apply ranking, parallelizable wrt call AI module

    # call AI module
    data_to_ai = format_data_ai(aggregated_results, aggregation_features["aggregated_key"], aggregation_features["aggregated_abstract"])

    debug_log("formatted to ai done")

    ai_result = make_post_request_to_AI(data_to_ai, topic_modeling)

    debug_log("ai done")

    processed_result = process_ai_result(ai_result, aggregated_results)

    debug_log("processed ai results done")

    return jsonify(processed_result)


class Aggregator(Resource):

    #TODO rimuovere get?
    def get(self):

        keywords = request.args.get("keywords").split(";")

        topic_modeling = request.args.get("type")
        
        return execute_aggregation_topic_modeling(keywords, topic_modeling)

    def post(self):

        data = request.get_json()
        keywords = data["keywords"]
        topic_modeling = data["type"]

        return execute_aggregation_topic_modeling(keywords, topic_modeling)


def mock_retrieving(topic_modeling):
    if topic_modeling == "slow":

        with open('mocks/slow_be_fe.json', "r") as json_file:
            data = json.load(json_file)

        debug_log("retrieved slow mock data")

    elif topic_modeling == "fast":

        with open('mocks/fast_be_fe.json', "r") as json_file:
            data = json.load(json_file)

        debug_log("retrieved fast mock data")

    else:
        raise Exception("type key not valid (slow | fast)")

            
    return data


class FrontEndRequest(Resource):

    def get(self):

        topic_modeling = request.args.get("type")

        debug_log(f"starting get mock request type : {topic_modeling}")

        return mock_retrieving(topic_modeling)

    def post(self):

        data = request.get_json()

        topic_modeling = data["type"]

        debug_log(f"starting post mock request type : {topic_modeling}")

        return mock_retrieving(topic_modeling)

class FilteringRequest(Resource):

    def post(self):

        return filtering(request.get_json())


if __name__ == "__main__":
    # routes
    api.add_resource(Aggregator, "/aggregator")
    api.add_resource(FrontEndRequest, "/mock")
    api.add_resource(FilteringRequest, "/filtering")

    # set host to gateway to handle route
    app.run(host = "0.0.0.0")