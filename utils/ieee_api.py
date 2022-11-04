from utils.constants import *
import requests


# define ieee request for api
def compose_ieee_request(q_str):
    return IEEE_SITE + '?querytext=' + q_str + '&' + IEEE_HEADERS

# execute request
def make_ieee_request(q_str):
    ieee_request = compose_ieee_request(q_str)
    ieee_response = requests.get(ieee_request).json()
    return ieee_response