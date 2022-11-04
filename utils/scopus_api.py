import requests
from utils.constants import *


def compose_scopus_request(q_str):
    return SCOPUS_SITE + '?query=' + q_str + '&' + SCOPUS_HEADERS


def make_scopus_request(q_str):
    scopus_request = compose_scopus_request(q_str)
    scopus_response = requests.get(scopus_request).json()
    return scopus_response