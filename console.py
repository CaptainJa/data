# -*- coding: utf-8 -*-
'''
用于向屏幕上输出log信息

基本用法：
import console

console.debug('this is the debug message')
console.info('this is the info message')
console.warning('this is the warning message')
console.error('this is the error message')
console.log('this is the log message')

输出显示示例：
2018-07-16 00:43:52 - [func_name]: DEBUG -> hello, world
2018-07-16 00:43:52 - [func_name]: INFO -> hello, world
2018-07-16 00:43:52 - [func_name]: WARNING -> hello, world
2018-07-16 00:43:52 - [func_name]: ERROR -> hello, world
'''

import logging

_FORMAT = '%(asctime)s - [%(funcName)s]: %(levelname)s -> %(message)s'
_DATEFMT = '%Y-%m-%d %H:%M:%S'

_LOGGING_LEVEL = logging.DEBUG  # 设置默认显示级别为DEBUG
logging.basicConfig(format=_FORMAT, datefmt=_DATEFMT)
_console = logging.getLogger('console')
_console.setLevel(_LOGGING_LEVEL)

debug = _console.debug
info = _console.info
warn = _console.warn
warning = _console.warning
error = _console.error
log = _console.info  # 模仿JS里的console.log


LEVEL_DEBUG = logging.DEBUG
LEVEL_INFO = logging.INFO
LEVEL_WARN = logging.WARN
LEVEL_ERROR = logging.ERROR


def set_level(level):
    _console.setLevel(level)
