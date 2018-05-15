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
LOG_FILE_PATH = os.path.join(LOG_PATH, 'main.log')


def _handlers():
    handlers = list()
    # Create stream handler
    stream_handler = logging.StreamHandler()
    handlers.append(stream_handler)
    # Create file handler
    file_handler = TimedRotatingFileHandler(filename=LOG_FILE_PATH, when='midnight',
                                            interval=1, backupCount=5)
    handlers.append(file_handler)
    return handlers


def create_logger(config=None, logger_type=None):
    """
    日志对象创建，参数config和logger_type至少设置一个
    :param config: 配置类，形如:
                    1、class ProductionConfig(object):
                            TYPE = 'Production'  #类型为生产环境
                    2、class DevelopmentConfig(object):
                            TYPE = 'Development' #类型为开发环境
    :param logger_type:日志类型，1、Production 2、Development

    :return:带有StreamHandler和TimedRotatingFileHandler的日志对象
    """
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
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    # Set handlers
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

    log1 = create_logger(config=cfg)
    log1.info('This is a test msg:1')

    log2 = create_logger(logger_type='Production')
    log2.info('This is a test msg:2')
