# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import json

from pygments import highlight
from pygments.lexers import PythonLexer, JavascriptLexer
from pygments.formatters import TerminalFormatter, Terminal256Formatter, TerminalTrueColorFormatter

import TermTk as ttk

import tlogg

class JsonViewer(ttk.TTkTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLineWrapMode(ttk.TTkK.WidgetWidth)
        self.setWordWrapMode(ttk.TTkK.WordWrap)
        tlogg.tloggProxy.lineSelected.connect(self._showLine)

    ttk.pyTTkSlot(str)
    def _showLine(self, text):
        try:
            text = json.loads(text)
            text = json.dumps(text, indent=4)
            text = highlight(text, JavascriptLexer(), TerminalTrueColorFormatter(style='material'))

        except ValueError as e:
            pass
        self.setText(text)

tlogg.TloggPlugin(
    name="Json Viewer",
    position=ttk.TTkK.RIGHT,
    menu=True,
    visible=False,
    widget=JsonViewer(lineNumber=True, readOnly=False, ))
