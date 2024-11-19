import os
import logging
from logging.handlers import RotatingFileHandler


class CustomLogger:
    _logger = None

    @classmethod
    def setup_logging(cls):
        if cls._logger is not None:
            return cls._logger

        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_name = os.path.join(log_dir, 'app.log')
        log_handler = RotatingFileHandler(log_file_name, maxBytes=1024 * 1024, backupCount=5)
        log_handler.setLevel(logging.INFO)
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_handler.setFormatter(log_format)

        cls._logger = logging.getLogger('appLogger')
        cls._logger.setLevel(logging.INFO)
        cls._logger.addHandler(log_handler)

        return cls._logger

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls.setup_logging().info(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls.setup_logging().error(msg, *args, **kwargs)

    # 可以根据需要继续添加其他日志级别方法，如debug、warning等
    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls.setup_logging().debug(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls.setup_logging().warning(msg, *args, **kwargs)