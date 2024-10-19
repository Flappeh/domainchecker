from time import time
import os
import logging
import sys
from datetime import datetime, timedelta
from typing import List


dir_path = os.path.dirname(os.path.realpath(__file__))
loggers = {}

def get_logger(name=None):
    global loggers
    if not name:
        name = __name__
    if loggers.get(name):
        return loggers.get(name)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger
