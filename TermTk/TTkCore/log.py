#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This code is inspired by
# https://github.com/ceccopierangiolieugenio/pyCuT/blob/master/cupy/CuTCore/CuDebug.py

import inspect
import logging
from collections.abc import Callable, Set

class _TTkContext:
    __slots__ = ['file', 'line', 'function']
    def __init__(self, cf):
        self.file = cf[1]
        self.line = cf[2]
        self.function = cf[3]
    def __str__(self):
        return f"{self.file}:{self.line} [{self.function}]"

class TTkLog:
    DebugMsg    = 0x0001
    InfoMsg     = 0x0002
    ErrorMsg    = 0x0004
    WarningMsg  = 0x0008
    CriticalMsg = 0x0010
    FatalMsg    = 0x0020
    SystemMsg   = CriticalMsg

    # TypeHandlers = list[Callable]
    _messageHandler: Set = []

    @staticmethod
    def _logging_message_handler(mode, context, message):
        log = logging.debug
        if mode == TTkLog.InfoMsg:       log = logging.info
        elif mode == TTkLog.WarningMsg:  log = logging.warning
        elif mode == TTkLog.CriticalMsg: log = logging.critical
        elif mode == TTkLog.FatalMsg:    log = logging.fatal
        elif mode == TTkLog.ErrorMsg:    log = logging.error
        log(f"{context.file}:{context.line} {message}")

    @staticmethod
    def use_default_file_logging(file="session.log"):
        logging.basicConfig(level=logging.DEBUG,
                    filename='session.log',
                    format='%(levelname)s:(%(threadName)-9s) %(message)s',)
        TTkLog.installMessageHandler(TTkLog._logging_message_handler)

    @staticmethod
    def use_default_stdout_logging():
        logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s:(%(threadName)-9s) %(message)s',)
        TTkLog.installMessageHandler(TTkLog._logging_message_handler)


    @staticmethod
    def _process_msg(mode: int, msg: str):
        for cb in TTkLog._messageHandler:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe,1)
            if len(calframe) > 2:
                ctx = _TTkContext(calframe[2])
                cb(mode, ctx, msg)

    @staticmethod
    def debug(msg):
        TTkLog._process_msg(TTkLog.DebugMsg, msg)

    @staticmethod
    def info(msg):
        TTkLog._process_msg(TTkLog.InfoMsg, msg)

    @staticmethod
    def error(msg):
        TTkLog._process_msg(TTkLog.ErrorMsg, msg)

    @staticmethod
    def warn(msg):
        TTkLog._process_msg(TTkLog.WarningMsg, msg)

    @staticmethod
    def critical(msg):
        TTkLog._process_msg(TTkLog.CriticalMsg, msg)

    @staticmethod
    def fatal(msg):
        TTkLog._process_msg(TTkLog.FatalMsg, msg)

    @staticmethod
    def installMessageHandler(mh: Callable):
        TTkLog._messageHandler.append(mh)
