from utils.constants import *
import requests
from utils.utils import remove_uncompleted_papers, error_log


def clear_author(author_paper):
    res_authors = list()

    for aut in author_paper["authors"]:
        if "full_name" in aut.keys():
            res_authors.append(aut["full_name"])

    return ";".join(res_authors)


def clear_access_type(access_type):
    return 1 if access_type in ["OPEN_ACCESS", "EPHEMERA"] else 0


def clear_features(list_papers):
    for paper in list_papers:
        paper["authors"] = clear_author(paper["authors"])
        paper["access_type"] = clear_access_type(paper["access_type"])

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
    
    try:
        ieee_request = compose_ieee_request(query_string)
        ieee_response = requests.get(ieee_request).json()

        results = ieee_response["articles"]
    except:
        error_log("IEEE retrieving error")
        return []

    results = clear_features(results)

    return remove_uncompleted_papers(results, "ieee")