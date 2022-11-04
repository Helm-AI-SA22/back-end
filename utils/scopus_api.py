import requests
from utils.constants import *


def compose_scopus_request(q_str, start=0):
    return SCOPUS_SITE + '?query=' + q_str + '&' + SCOPUS_HEADERS + f"&start={start}"


def make_scopus_request(q_str):

    result = list()

    while len(result) < 20:
        try:
            scopus_request = compose_scopus_request(q_str, len(result))

            scopus_response = requests.get(scopus_request).json()

            scopus_response = scopus_response["search-results"]

            scopus_entries = scopus_response["entry"]

            if "error" in scopus_entries[0].keys():
                break
            
            result += scopus_entries

        except Exception as e:
            return e.message()

    return result