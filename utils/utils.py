from constants import AGGREGATION_FEATURES
import logging
from flask_log_request_id import current_request_id


# --- LOGGING

def info_log(message):
    logging.info(f'{current_request_id()} - {message}')


def debug_log(message):
    logging.debug(f'{current_request_id()} - {message}')


def error_log(message):
    logging.error(f'{current_request_id()} - {message}')


def warning_log(message):
    logging.warning(f'{current_request_id()} - {message}')


def remove_uncompleted_papers(list_papers, source):
    features = AGGREGATION_FEATURES[source]

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