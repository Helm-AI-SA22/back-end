from constants import *
import requests


def compose_request(q_str):
    return SCOPUS_SITE + '?query=' + q_str + '&' + SCOPUS_HEADERS


def make_request(q_str):
    scopus_request = compose_request(q_str)
    scopus_response = requests.get(scopus_request).json()
    return scopus_response