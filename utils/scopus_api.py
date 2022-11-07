import requests
from utils.constants import *
import json


def remove_nodoi(list_papers):
    return_list = list()

    for paper in list_papers:
        if "prism:doi" in paper.keys():
            return_list.append(paper)

    return return_list


def clear_author(author_paper):
    res_authors = list()

    for aut in author_paper:
        if "authname" in aut.keys():
            res_authors.append(aut["authname"])

    return ";".join(res_authors)


def clear_link(link_paper):
    return link_paper[1]["@href"]


def clear_features(list_papers):
    for paper in list_papers:
        paper["author"] = clear_author(paper["author"])
        paper["link"] = clear_author(paper["link"])

    return list_papers

def compose_scopus_request(q_str, start=0):
    return SCOPUS_SITE + '?query=' + q_str + '&' + SCOPUS_HEADERS + f"&start={start}"


def make_scopus_request(q_str):
    
    result = list()

    while len(result) < 20:
        try:

            scopus_request = compose_scopus_request(q_str, len(result))

            scopus_response = requests.get(scopus_request).json()

            print(scopus_response)

            scopus_response = scopus_response["search-results"]

            scopus_entries = scopus_response["entry"]

            if "error" in scopus_entries[0].keys():
                break
            
            result += scopus_entries

        except Exception as e:
            raise e

        
    return remove_nodoi(result)

    """
    with open("mocks/scopus_try.json") as f:
        result = json.load(f)

    result = result["search-results"]["entry"]
    
    # clear features to make them consistent with other sources
    result = clear_features(result)

    return remove_nodoi(result)
    """