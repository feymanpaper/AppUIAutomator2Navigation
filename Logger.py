import logging
import sys
from logging import StreamHandler
from logging import FileHandler
import os
from Config import *
from StatRecorder import *

class Logger:
    def __new__(cls, *args, **kwargs):
        if not hasattr(Logger, "_instance"):
            Logger._instance = object.__new__(cls)
        return Logger._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(Logger, '_instance'):
            Logger._instance = Logger(*args, **kwargs)
        return Logger._instance

    def __init__(self):
        self.file_path = ""
        self.logger = logging.getLogger(__name__)
        # self.rewrite_print = print

    def __create_dir(self):
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))

    def __add_stream_handler(self):
        # 标准流处理器，设置的级别为WARAING
        stream_handler = StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(logging.INFO)
        format = logging.Formatter('%(message)s')
        stream_handler.setFormatter(format)
        self.logger.addHandler(stream_handler)

    def __add_file_handler(self):
        file_handler = FileHandler(filename=self.file_path)
        file_handler.setLevel(logging.INFO)
        format = logging.Formatter('%(message)s')
        file_handler.setFormatter(format)
        self.logger.addHandler(file_handler)

    def __set_logger(self):
        self.__add_stream_handler()
        self.__add_file_handler()
        self.logger.setLevel(logging.DEBUG)

    def setup(self, file_path = "./Log/test.log"):
        self.file_path = file_path
        self.__create_dir()
        self.__set_logger()

    def log_info(self, msg):
        self.logger.info(msg)

    def log_error(self, msg):
        self.logger.error(msg)

    def print(self, *args):
        # self.rewrite_print(*args)
        self.log_info(*args)




