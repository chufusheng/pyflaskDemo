import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_name = os.path.join(log_dir, 'app.log')
    log_handler = RotatingFileHandler(log_file_name, maxBytes=1024 * 1024, backupCount=5)
    log_handler.setLevel(logging.INFO)
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(log_format)

    logger = logging.getLogger('appLogger')
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    return logger
