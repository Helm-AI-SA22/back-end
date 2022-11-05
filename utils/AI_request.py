import requests
from utils.constants import *
import json


def make_post_request_to_AI(list_papers, type):
    # AI_response = requests.post(AI_URL + ':' + str(AI_PORT) + f'&type={type}', json = list_papers)

    # return AI_response.json()

    with open("lda_response_example.json") as f:
        ai_mock = json.load(f)

    return ai_mock