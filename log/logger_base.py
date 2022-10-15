# -*- coding: utf-8 -*-
"""
@editor: PyCharm
@project: python_snippet
@file: logger_base.py
@author: tanxin
@create_time: 2022/10/15 17:43
@version: 1.0
@description: 继承该类，可以使用日志

字段/属性名称	使用格式	描述
asctime	%(asctime)s	日志事件发生的时间--人类可读时间，如：2003-07-08 16:49:45,896
created	%(created)f	日志事件发生的时间--时间戳，就是当时调用time.time()函数返回的值
relativeCreated	%(relativeCreated)d	日志事件发生的时间相对于logging模块加载时间的相对毫秒数（目前还不知道干嘛用的）
msecs	%(msecs)d	日志事件发生事件的毫秒部分
levelname	%(levelname)s	该日志记录的文字形式的日志级别（'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'）
levelno	%(levelno)s	该日志记录的数字形式的日志级别（10, 20, 30, 40, 50）
name	%(name)s	所使用的日志器名称，默认是'root'，因为默认使用的是 rootLogger
message	%(message)s	日志记录的文本内容，通过 msg % args计算得到的
pathname	%(pathname)s	调用日志记录函数的源码文件的全路径
filename	%(filename)s	pathname的文件名部分，包含文件后缀
module	%(module)s	filename的名称部分，不包含后缀
lineno	%(lineno)d	调用日志记录函数的源代码所在的行号
funcName	%(funcName)s	调用日志记录函数的函数名
process	%(process)d	进程ID
processName	%(processName)s	进程名称，Python 3.1新增
thread	%(thread)d	线程ID
threadName	%(thread)s	线程名称
"""
import re
import os
import logging
from logging.handlers import TimedRotatingFileHandler


class LoggerBase:
    def __init__(self, name: str = None, format_string: str = None, default_level: int = logging.INFO):
        self.default_level = default_level
        if format_string is None:
            format_string = '%(asctime)s [%(name)s.%(funcName)s] %(levelname)s: %(message)s'
        else:
            format_string = format_string
        # 创建Formatter类
        self.formatter = logging.Formatter(format_string)
        # 创建日志类
        if name is None:
            name = self.__class__.__name__
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.default_level)

    def _add_console_handler(self, level: int = None) -> None:
        handler = logging.StreamHandler()
        self.__set_format_and_level_to_handler(handler, level)
        self.logger.addHandler(handler)

    def _add_file_handler(self, file_path: str, level: int = None) -> None:
        handler = logging.FileHandler(file_path)
        self.__set_format_and_level_to_handler(handler, level)
        self.logger.addHandler(handler)

    def _add_time_rotate_file_handler(self,
                                      directory_path: str,
                                      interval_by_hours: int = None,
                                      backup_count: int = None,
                                      file_name_prefix: str = None,
                                      level: int = None) -> None:
        """
        file_name：日志文件名的prefix；

            when：是一个字符串，用于描述滚动周期的基本单位，字符串的值及意义如下：
            “S”: Seconds
            “M”: Minutes
            “H”: Hours
            “D”: Days
            “W”: Week day (0=Monday)
            “midnight”: Roll over at midnight

            interval: 滚动周期，单位有when指定，比如：when=’D’,interval=1，表示每天产生一个日志文件；

            backupCount: 表示日志文件的保留个数；
        :param directory_path: 文件保存路径
        :param interval_by_hours: 每多少小时生成一个新的日志
        :param backup_count: 保留的日志数量
        :param file_name_prefix: 文件名前缀
        :param level: 打印日志级别
        :return: 无返回
        """
        if interval_by_hours is None:
            interval_by_hours = 24
        if backup_count is None:
            backup_count = 20
        if file_name_prefix is None:
            file_name_prefix = 'log_'
        handler = TimedRotatingFileHandler(os.path.join(directory_path, file_name_prefix)
                                           , when='H'
                                           , interval=interval_by_hours
                                           , backupCount=backup_count
                                           )
        # 不设置下面两个值，会自动根据when设置默认值
        # handler.suffix = "%Y-%m-%d_%H-%M.log"
        # handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
        self.__set_format_and_level_to_handler(handler, level)
        self.logger.addHandler(handler)

    def __set_format_and_level_to_handler(self, handler: logging.Handler, level: int = None):
        if level is None:
            handler.setLevel(self.default_level)
        else:
            handler.setLevel(level)
        handler.setFormatter(self.formatter)


class LoggerBaseTest(LoggerBase):
    def __init__(self):
        super().__init__()
        self._add_console_handler()
        self.logger.info('abcd')


if __name__ == '__main__':
    LoggerBaseTest()