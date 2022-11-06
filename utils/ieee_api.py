from utils.constants import *
import requests
import json
from collections import defaultdict


def remove_nodoi(list_papers):
    return_list = list()

    for paper in list_papers:
        if not paper["DOI"] is None:
            return_list.append(paper)

    return return_list

# define ieee request for api
def compose_ieee_request(q_str):
    return IEEE_SITE + '?querytext=' + q_str + '&' + IEEE_HEADERS

# execute request
def make_ieee_request(q_str):
    # ieee_request = compose_ieee_request(q_str)
    # ieee_response = requests.get(ieee_request).json()

    with open("mocks/ieee.json") as f:
        ieee_response = json.load(f)

    # transform ieee response in a list of papers, with relative infoes

    transfomed_ieee_response = defaultdict(dict)

    for feature_key, feature_values_dict in ieee_response.items():
        for key, value in feature_values_dict.items():
            transfomed_ieee_response[key][feature_key] = value

    transfomed_ieee_response = list(transfomed_ieee_response.values())


    return remove_nodoi(transfomed_ieee_response)