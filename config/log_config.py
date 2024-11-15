import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging():
    log_dir = '../logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # 根据当前时间生成日志文件名称
    current_time = datetime.now()
    log_file_name = os.path.join(log_dir, f'app_{current_time.strftime("%Y%m%d%H%M")}.log')
    log_handler = RotatingFileHandler(log_file_name, maxBytes=1024 * 1024, backupCount=5)
    log_handler.setLevel(logging.INFO)
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(log_format)

    logger = logging.getLogger('appLogger')
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    return logger
