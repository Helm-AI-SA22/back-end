import logging
from flask_log_request_id import current_request_id


# --- LOGGING

def info_log(message):
    logging.info(f'{current_request_id()} - {message}')


def debug_log(message):
    logging.debug(f'{current_request_id()} - {message}')


def error_log(message):
    logging.error(f'{current_request_id()} - {message}')


def error_log(message):
    logging.warning(f'{current_request_id()} - {message}')