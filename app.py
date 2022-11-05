import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from utils.scopus_api import make_scopus_request
from utils.ieee_api import make_ieee_request
from utils.AI_request import make_post_request_to_AI
from flask_cors import CORS


def add_topic_paper(topics, papers, doi):
    for paper in papers:
        if paper["doi"] == str(doi):
            paper["topics"] = topics

    return papers


def process_ai_result(ai_result, list_papers):
    documents_result_ai = ai_result.pop("documents")

    for doc in documents_result_ai:
        doi = doc["id"]
        list_papers = add_topic_paper(doc["topics"], list_papers, doi)

    ai_result["documents"] = list_papers

    return ai_result


def format_data_ai(list_papers, return_keys):
    return_list = list()
    
    for paper in list_papers:

        formatted_paper = dict()

        for k in return_keys:
            formatted_paper[k] = paper[k]

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


class MockAI(Resource):

    def get(self):
        return {'prova AI': 'prova get'}
        

    def post(self):
        req_json = request.get_json()
        print('Json arrived to AI:', req_json)
        return_json = {'prova AI': 'riuscita'}
        return jsonify(return_json)


def execute_aggregation_topic_modeling(query_string, topic_modeling):
    ieee_results = make_ieee_request(query_string)

    scopus_results = make_scopus_request(query_string)

    aggregated_results = aggregator(ieee_results, scopus_results)

    with open("aggregation_features.json") as f:
        aggregation_features = json.load(f)

    # call AI module
    data_to_ai = format_data_ai(aggregated_results, [aggregation_features["aggregated_key"], aggregation_features["aggregated_abstract"]])

    ai_result = make_post_request_to_AI(data_to_ai, topic_modeling)

    processed_result = process_ai_result(ai_result, aggregated_results)

    return jsonify(processed_result)


class Aggregator(Resource):

    def get(self):

        keywords = request.args.get("keywords").split(";")

        topic_modeling = request.args.get("type")

        query_string = " AND ".join(keywords)
        
        return execute_aggregation_topic_modeling(query_string, topic_modeling)

    def post(self):

        data = request.get_json()

        keywords = data["keywords"]

        topic_modeling = data["type"]

        query_string = " AND ".join(keywords)
        
        return execute_aggregation_topic_modeling(query_string, topic_modeling)


class Home(Resource):

    def get(self):
        
        return "HOME in GET"

    def post(self):

        return "HOME in POST"

class FrontEndRequest(Resource):

    def get(self):
        
        with open('mocks/BE_respto_FE.json', "r") as json_file:
            data = json.load(json_file)
        
        json_file.close()

        return data


    def post(self):

        with open('mocks/BE_respto_FE.json', "r") as json_file:
            data = json.load(json_file)
        
        json_file.close()
        return data

if __name__ == "__main__":
    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    api = Api(app)

    # routes
    api.add_resource(Home, "/")
    api.add_resource(MockAI, "/mock_ai")
    api.add_resource(Aggregator, "/aggregator")
    api.add_resource(FrontEndRequest, "/front_end_request")
    
    # set host to gateway to handle route
    app.run(host = "0.0.0.0")