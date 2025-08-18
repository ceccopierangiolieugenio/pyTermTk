# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os, io
import logging
import pytest
from typing import Union, Optional

sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import TermTk as ttk


class FakeStderr():
    value = []

def message_handler(mode, context, message):
    FakeStderr.value.append(message)
    msgType = "NONE"
    if   mode == ttk.TTkLog.InfoMsg:     msgType = "[INFO]"
    elif mode == ttk.TTkLog.WarningMsg:  msgType = "[WARNING]"
    elif mode == ttk.TTkLog.CriticalMsg: msgType = "[CRITICAL]"
    elif mode == ttk.TTkLog.FatalMsg:    msgType = "[FATAL]"
    elif mode == ttk.TTkLog.ErrorMsg:    msgType = "[ERROR]"
    print(f"{msgType} {context.file} {message}")

def test_stderr_01():
    ttk.TTkLog.installMessageHandler(message_handler)

    print('Test',file=sys.stderr)
    with ttk.ttk_capture_stderr():
        print('XXXXX Test',file=sys.stderr)
        with open('pippo','r') as f:
            f.read()
        raise ValueError('YYYYY Test')
    print('After Test')

def test_ttk_capture_stderr():
    ttk.TTkLog.installMessageHandler(message_handler)
    with ttk.ttk_capture_stderr() as fake_stderr:
        print("This is an error message", file=sys.stderr)
    output = FakeStderr.value
    assert "This is an error message" in output

def test_ttk_capture_stderr_exception_handling():
    ttk.TTkLog.installMessageHandler(message_handler)
    with ttk.ttk_capture_stderr() as fake_stderr:
        raise ValueError("Test exception")
    # After the exception, sys.stderr should be restored
    output = FakeStderr.value
    assert any("Test exception" in _o for _o in output)
    assert isinstance(sys.stderr, io.TextIOWrapper) or sys.stderr is sys.__stderr__
