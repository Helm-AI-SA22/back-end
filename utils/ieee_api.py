from utils.constants import *
import requests
import json
from collections import defaultdict

def remove_uncompleted_papers(list_papers):

    with open("aggregation_features.json", "r") as f:
        aggregated_features = json.load(f)

    features = aggregated_features["ieee"]

    return_list = list()

    for paper in list_papers:
        accepted_paper = True

        for feature in features:
            if not feature in paper.keys():
                accepted_paper = False
                break
            else: 
                if paper[feature] is None:
                    accepted_paper = False
                    break

        if accepted_paper:
            return_list.append(paper)        

    return return_list


def clear_author(author_paper):
    res_authors = list()

    for aut in author_paper["authors"]:
        if "full_name" in aut.keys():
            res_authors.append(aut["full_name"])

    return ";".join(res_authors)


def clear_features(list_papers):
    for paper in list_papers:
        paper["authors"] = clear_author(paper["authors"])

    return list_papers


# define ieee request for api
def compose_ieee_request(q_str):
    return IEEE_SITE + '?querytext=' + q_str + '&' + IEEE_HEADERS

# execute request
def make_ieee_request(keywords):
    key = []
    for keyword in keywords:
        key.append(QUOTES_IEEE + keyword.replace(' ', SPACE_IEEE) + QUOTES_IEEE)
    keys_conj = SPACE_IEEE + "AND" + SPACE_IEEE
    query_string = keys_conj.join(key)
    
    ieee_request = compose_ieee_request(query_string)
    ieee_response = requests.get(ieee_request).json()

    results = ieee_response["articles"]

    results = clear_features(results)

    return remove_uncompleted_papers(results)