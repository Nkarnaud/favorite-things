import logging
import os
from flask import has_request_context, request
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


# setting logging
def init_logs(log_name):
    #setting the log dir
    log_dir = os.getcwd() + '/log'
    log_file = log_dir + '/' + log_name + '.log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # Instantiating logging class
    global log
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    ch = RotatingFileHandler(log_file, maxBytes=5000000, backupCount=3)
    # Definig formatte
    formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(logging.INFO)
    return log