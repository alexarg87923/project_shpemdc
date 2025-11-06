"""
This module contains helper funcs so they're not mixed in with the routes
"""
import logging
import sys


def process_event_data(event_list) -> dict:
    """ Prepares data to be sent to front-end

    Args:
        event_list (list of events): output from sql DB

    Returns:
        dictionary: turns it into a JSON-formatted dictionary ready to be used
    """
    event_dict = {
        "occasion": event_list[1],
        "startTime": event_list[2],
        "endTime": event_list[3],
        "year": event_list[4],
        "month": event_list[5],
        "day": event_list[6],
        "cancelled": bool(event_list[7])
    }
    return event_dict


def create_logger() -> logging:
    """ Makes a logger to be used throughout app

    Returns:
        logger: logger that takes a string to be saved in log file
    """
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s - %(clientip)s'
                    ' - %(url)s - %(method)s%(input)s'
                    )

    # uncomment if you want logs to be saved to file.
    # file_handler = logging.FileHandler('app.log')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def create_extra_dict(request, input_data=None) -> dict:
    """_summary_

    Args:
        request (request obj): request from user
        input_data (list, optional): input data from user. Defaults to None.

    Returns:
        dictionary: dictionary formatted to be used in logger
    """
    extra_dict = {
        'clientip': request.clientip,
        'url': request.url,
        'method': request.method,
        'input': ' - ' + input_data if input_data else ''
    }
    return extra_dict