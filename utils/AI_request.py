import requests
from constants import *
import json
import os


def make_post_request_to_AI(keywords, list_papers, type):

    if 'DEPLOY' in os.environ and os.environ['DEPLOY'].lower() == "true":
        url = AI_URL_DEPLOY
        port = AI_PORT_DEPLOY
    else:
        url = AI_URL
        port = AI_PORT

    AI_response = requests.post(url + ':' + str(port) + f"/{type}", json = {"documents" : list_papers, "keywords": keywords})

    return AI_response.json()

    # with open("lda_response_example.json") as f:
    #     ai_mock = json.load(f)

    # return ai_mock