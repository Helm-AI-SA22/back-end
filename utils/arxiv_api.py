from utils.constants import *
import requests
import json
from collections import defaultdict
import xmltodict
from functools import reduce
import pandas as pd
from utils.utils import info_log


def remove_uncompleted_papers(list_papers):

    with open("aggregation_features.json", "r") as f:
        aggregated_features = json.load(f)

    features = aggregated_features["arxiv"]

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
    

def clear_link(paper):
    # get pdf link
    link = None
    if "link" in paper:
        # if link is a list
        if type(paper["link"]) == list:
            for link in paper["link"]:
                if "@title" in link and link["@title"] == "pdf":
                    link = link["@href"]
        # if is not a list
        elif "@title" in link and link["@title"] == "pdf":
            link = link["@href"]
        
        paper["openaccess"] = 1
    
    paper["link"] = link

    return paper


def clear_authors(paper):
    # get the authors
    authors = []

    if "author" in paper:
        if type(paper["author"]) == list:
            for author in paper["author"]:
                if "name" in author:
                    authors.append(author["name"])
        else:
            if "name" in paper["author"]:
                authors.append(paper["author"]["name"])
    
    if authors == []:
        authors = None
    else:
        authors = ";".join(authors)

    paper["author"] = authors

    return paper



def clear_features(list_papers):
    for paper in list_papers:
        paper["citationCount"] = -1

        if "arxiv:doi" in paper:
            doi = paper["arxiv:doi"]["#text"]
        elif "id" in paper:
            doi = paper["id"]
        else:
            doi = None
        paper["id"] = doi

        paper = clear_link(paper)

        # get abstract
        paper["summary"] = None if "summary" not in paper else paper["summary"].replace("\n", " ").replace("\\", " ")

        # get publication date
        paper["published"] = None if "published" not in paper else paper["published"]

        # get date
        paper["title"] = None if "title" not in paper else paper["title"].replace("\n", " ").replace("\\", " ")

        paper = clear_authors(paper)

    return list_papers


def compose_arxiv_request(q_str):
    return f"{ARXIV_SITE}?search_query={q_str}&start=0&max_results={ARXIV_MAX_RESULTS}"


def make_arxiv_request(keywords):
    query_text = ""
    for keyword in keywords:
        query_text += f"all:{keyword}+AND+"

    query_text = query_text[:-5]

    request_text = compose_arxiv_request(query_text)

    response = requests.get(request_text)
    
    data_dict = xmltodict.parse(response.text)
    
    # json_data = json.dumps(data_dict)

    results = data_dict["feed"]["entry"]

    results = clear_features(results)

    return remove_uncompleted_papers(results)

    