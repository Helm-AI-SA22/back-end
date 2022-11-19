import requests
from constants import *
import json
from utils.utils import remove_uncompleted_papers, error_log


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
        paper["link"] = clear_link(paper["link"])

    return list_papers

def compose_scopus_request(q_str, start=0):
    return SCOPUS_SITE + '?query=' + q_str + '&' + SCOPUS_HEADERS + f"&start={start}"


def make_scopus_request(keywords):
    
    result = list()

    query_string = STARTING_STRING_SCOPUS
    query_string += "+AND+".join(keywords)
    query_string += ENDING_STRING_SCOPUS

    try:
        while len(result) < SCOPUS_MAX_COUNT:

                scopus_request = compose_scopus_request(query_string, len(result))

                scopus_response = requests.get(scopus_request).json()

                scopus_response = scopus_response["search-results"]

                if not "entry" in scopus_response.keys():
                    break

                scopus_entries = scopus_response["entry"]

                if "error" in scopus_entries[0].keys():
                    break
                
                result += scopus_entries

    except Exception as e:
        error_log("Scopus retrieving error")
        return []
    
    # clear features to make them consistent with other sources
    result = clear_features(result)

    return remove_uncompleted_papers(result, "scopus")