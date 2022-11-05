import requests
from utils.constants import *


def make_post_request_to_AI(list_papers):
    AI_response = requests.post(AI_URL + ':' + str(AI_PORT), json = list_papers)

    return AI_response.json()