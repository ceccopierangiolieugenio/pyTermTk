# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TextDocumentHighlight']

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkGui import TTkTextDocument

class TextDocumentHighlight(TTkTextDocument):
    __slots__ = (
        #Signals
        'highlightUpdate')
    def __init__(self, *args, **kwargs):
        self.highlightUpdate = pyTTkSignal()
        super().__init__(*args, **kwargs)
        TTkLog.warn("Pygments not found!!!")

    @staticmethod
    def getStyles() -> list[str]:
        return []

    @staticmethod
    def getLexers() -> list[str]:
        return []

    @pyTTkSlot(str)
    def setStyle(self, alias:str) -> None:
        pass

    @pyTTkSlot(str)
    def setLexer(self, alias:str) -> None:
        pass

    @pyTTkSlot(str)
    def guessLexerFromFilename(self, fileName:str) -> None:
        pass

