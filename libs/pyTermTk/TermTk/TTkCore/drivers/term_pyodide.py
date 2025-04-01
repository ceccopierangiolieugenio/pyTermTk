# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkTerm']

import pyodideProxy

from ..TTkTerm.term_base import TTkTermBase

class TTkTerm(TTkTermBase):
    @staticmethod
    def _push(*args):
        pyodideProxy.termPush(str(*args))
    TTkTermBase.push = _push

    @staticmethod
    def _getTerminalSize():
        return pyodideProxy.termSize()
    TTkTermBase.getTerminalSize = _getTerminalSize

    @staticmethod
    def _registerResizeCb(callback):
        TTkTerm._sigWinChCb = callback
        # Dummy call to retrieve the terminal size
        TTkTerm.width, TTkTerm.height = TTkTerm.getTerminalSize()
        callback(TTkTerm.width, TTkTerm.height)
    TTkTermBase.registerResizeCb = _registerResizeCb
