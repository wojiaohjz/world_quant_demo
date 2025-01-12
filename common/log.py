import logging
import os.path
from tools.path_tool import root_dir

from tools.time_tool import get_current_date_string


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
            cls._instance.__logger = logging.getLogger()
        return cls._instance

    def __init__(self):
        current_date_string = get_current_date_string()
        log_path = os.path.join(root_dir, "log/{}.log".format(current_date_string))
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))

        self.__logger.setLevel(logging.DEBUG)
        if not self.__logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s [%(name)s] [%(levelname)s] - %(message)s')

            file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self.__logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.__logger.addHandler(console_handler)

    def info(self, message):
        self.__logger.info(message)

    def debug(self, message):
        self.__logger.debug(message)

    def warning(self, message):
        self.__logger.warning(message)

    def error(self, message):
        self.__logger.error(message)


logger = Logger()
