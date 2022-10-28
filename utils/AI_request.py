import requests

def make_post_request_to_AI(my_json):
    url = "http://127.0.0.1"
    port = 4567

    AI_response = requests.post(url + ':' + str(port), json = my_json)

    print('suca')

    return AI_response.json()