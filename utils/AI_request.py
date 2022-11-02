import requests
from utils.constants import *

def make_post_request_to_AI(my_json):
    AI_response = requests.post(AI_URL + ':' + str(AI_PORT), json = my_json)

    print('suca')

    return AI_response.json()