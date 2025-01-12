import os
import unittest
from common.log import logger, Logger
from tools.path_tool import root_dir
from tools.time_tool import get_current_time_string


class TestLogger(unittest.TestCase):

    def test_singleton_instance(self):
        # 测试单例模式，确保只有一个实例被创建
        logger1 = Logger()
        logger2 = Logger()
        self.assertEqual(logger1, logger2)

    def test_logging_methods(self):
        # 测试日志记录方法
        logger.info("Test info message")
        logger.debug("Test debug message")
        logger.warning("Test warning message")
        logger.error("Test error message")

    def test_log_path_creation(self):
        # 测试日志路径的创建
        expected_log_path = os.path.join(root_dir, "log/{}.log".format(get_current_time_string()))
        self.assertTrue(os.path.exists(os.path.dirname(expected_log_path)))

    def test_logger_initialization(self):
        # 测试日志记录器的初始化
        self.assertTrue(hasattr(logger, "logger"))
        self.assertTrue(logger.logger.handlers)


if __name__ == '__main__':
    unittest.main()
