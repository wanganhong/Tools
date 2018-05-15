#!/usr/bin/env python
# -*- coding:utf-8 -*-  

"""
-------------------------------------------------
   Author:       CrackM5
   FileName:     logger.py  
   Time:         2018/05/14 16:34
   Description:   
-------------------------------------------------
   Change Activity:
                  2018/05/14: 
-------------------------------------------------
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler

PROD_LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
DEBUG_LOG_FORMAT = (
    '-' * 100 + '\n' +
    '%(asctime)s[%(levelname)s][%(pathname)s:%(lineno)d]:\n' +
    '%(message)s\n' +
    '-' * 100
)

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'Log')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


# LOG_FILE_PATH = os.path.join(LOG_PATH, 'main.log')


class LoggerManager(object):
    def __init__(self, name, config=None, logger_type=None):
        """
        参数config和logger_type至少设置一个
        :param name: logger name
        :param config: 配置类，形如:
                        1、class ProductionConfig(object):
                                TYPE = 'Production'  #类型为生产环境
                        2、class DevelopmentConfig(object):
                                TYPE = 'Development' #类型为开发环境
        :param logger_type:日志类型，1、Production 2、Development

        :return:带有StreamHandler和TimedRotatingFileHandler的日志对象
        """
        self.__name = name
        # logger with name already exists
        if self.__name in logging.Logger.manager.loggerDict:
            self.__logger = logging.getLogger(self.__name)
        else:
            # Set logging level and format
            self.__log_level = logging.DEBUG
            self.__log_format = DEBUG_LOG_FORMAT
            if config is None and logger_type is None:
                raise Exception('config and logger_type can not be None at the same time!')

            if hasattr(config, 'TYPE'):
                logger_type = config.TYPE

            if logger_type == 'Production':
                self.__log_level = logging.INFO
                self.__log_format = PROD_LOG_FORMAT
            self.__logger = self._create_logger()

    def _handlers(self):
        handlers = list()
        # Create stream handler
        stream_handler = logging.StreamHandler()
        handlers.append(stream_handler)
        # Create file handler
        log_file = os.path.join(LOG_PATH, '{0}.log'.format(self.__name))
        file_handler = TimedRotatingFileHandler(filename=log_file, when='midnight',
                                                interval=1, backupCount=5)
        handlers.append(file_handler)
        return handlers

    def _create_logger(self):
        # Create logger
        logger = logging.getLogger(self.__name)
        logger.setLevel(self.__log_level)
        # Set handlers
        for handler in self._handlers():
            handler.setLevel(self.__log_level)
            handler.setFormatter(logging.Formatter(self.__log_format))
            # Add
            logger.addHandler(handler)
        return logger

    @property
    def logger(self):
        return self.__logger


class Logger(logging.Logger):
    def __init__(self, name, config=None, logger_type=None):
        """
        参数config和logger_type至少设置一个
        :param name: logger name
        :param config: 配置类，形如:
                        1、class ProductionConfig(object):
                                TYPE = 'Production'  #类型为生产环境
                        2、class DevelopmentConfig(object):
                                TYPE = 'Development' #类型为开发环境
        :param logger_type:日志类型，1、Production 2、Development

        :return:带有StreamHandler和TimedRotatingFileHandler的日志对象
        """
        self.__name = name
        # logger with name already exists
        if self.__name not in logging.Logger.manager.loggerDict:
            # Set logging level and format
            self.__log_level = logging.DEBUG
            self.__log_format = DEBUG_LOG_FORMAT
            if config is None and logger_type is None:
                raise Exception('config and logger_type can not be None at the same time!')

            if hasattr(config, 'TYPE'):
                logger_type = config.TYPE

            if logger_type == 'Production':
                self.__log_level = logging.INFO
                self.__log_format = PROD_LOG_FORMAT
            super(Logger, self).__init__(name, level=self.__log_level)
            self._set_handlers()
        else:
            self = logging.getLogger(self.__name)

    def _handlers(self):
        handlers = list()
        # Create stream handler
        stream_handler = logging.StreamHandler()
        handlers.append(stream_handler)
        # Create file handler
        log_file = os.path.join(LOG_PATH, '{0}.log'.format(self.__name))
        file_handler = TimedRotatingFileHandler(filename=log_file, when='midnight',
                                                interval=1, backupCount=5)
        handlers.append(file_handler)
        return handlers

    def _set_handlers(self):
        for handler in self._handlers():
            handler.setLevel(self.__log_level)
            handler.setFormatter(logging.Formatter(self.__log_format))
            # Add
            self.addHandler(handler)


def create_logger(name, config=None, logger_type=None):
    """
    日志对象创建，参数config和logger_type至少设置一个
    :param name: logger name
    :param config: 配置类，形如:
                    1、class ProductionConfig(object):
                            TYPE = 'Production'  #类型为生产环境
                    2、class DevelopmentConfig(object):
                            TYPE = 'Development' #类型为开发环境
    :param logger_type:日志类型，1、Production 2、Development

    :return:带有StreamHandler和TimedRotatingFileHandler的日志对象
    """
    # logger with name already exists
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)
    # Set logging level and format
    log_level = logging.DEBUG
    log_format = DEBUG_LOG_FORMAT
    if config is None and logger_type is None:
        raise Exception('config and logger_type can not be None at the same time!')

    if hasattr(config, 'TYPE'):
        logger_type = config.TYPE

    if logger_type == 'Production':
        log_level = logging.INFO
        log_format = PROD_LOG_FORMAT

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Set handlers
    def _handlers():
        handlers = list()
        # Create stream handler
        stream_handler = logging.StreamHandler()
        handlers.append(stream_handler)
        # Create file handler
        log_file = os.path.join(LOG_PATH, '{0}.log'.format(name))
        file_handler = TimedRotatingFileHandler(filename=log_file, when='midnight',
                                                interval=1, backupCount=5)
        handlers.append(file_handler)
        return handlers

    for handler in _handlers():
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter(log_format))
        # Add
        logger.addHandler(handler)
    return logger


if __name__ == '__main__':
    class ProductionConfig(object):
        TYPE = 'Production'


    cfg = ProductionConfig()

    log1 = create_logger('test', config=cfg)
    log1.info('This is a test msg:1')

    log2 = create_logger('test', logger_type='Production')
    log2.info('This is a test msg:2')

    log = Logger('test', config=cfg)
    log.info('test')
