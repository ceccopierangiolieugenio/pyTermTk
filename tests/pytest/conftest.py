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
# SOFTWARE.import sys

# Thanks to: https://stackoverflow.com/questions/43162722/mocking-a-module-import-in-pytest

import sys

from mock_term  import Mock_TTkTerm
from mock_input import Mock_TTkInput

moduleTerm = type(sys)('TermTk.TTkCore.drivers.term_unix_common')
moduleTerm._TTkTerm = Mock_TTkTerm

moduleInput = type(sys)('TermTk.TTkCore.TTkTerm.input')
moduleInput.TTkInput = Mock_TTkInput

sys.modules['TermTk.TTkCore.drivers.term_unix_common']  = moduleTerm
sys.modules['TermTk.TTkCore.TTkTerm.input'] = moduleInput


# ---------------------------------------------------------------------------
# Pytest fixtures and helpers for common test utilities
# ---------------------------------------------------------------------------

import pytest
from typing import Callable
import TermTk as ttk


class _FakeCanvas(ttk.TTkCanvas):
    '''Lightweight test canvas with text-search convenience helpers.'''

    def text_in_line(self, line:int, text:str) -> bool:
        '''Check whether ``text`` appears in a specific canvas line.

        :param line: target line index in the internal canvas buffer
        :type line: int
        :param text: substring to search for
        :type text: str
        :return: ``True`` if the text is found in the selected line, otherwise ``False``
        :rtype: bool
        '''
        if 0 < line < len(self._data):
            return text in ''.join(self._data[line])
        return False
    
    def text_in_canvas(self, text:str) -> bool:
        '''Check whether ``text`` appears in any line of the canvas.

        :param text: substring to search for
        :type text: str
        :return: ``True`` if the text is found in at least one line, otherwise ``False``
        :rtype: bool
        '''
        for data_line in self._data:
            if text in ''.join(data_line):
                return True
        return False
    
    def canvas_to_string(self) -> str:
        return '\n'.join([''.join(line) for line in self._data])

@pytest.fixture
def fake_canvas() -> Callable[[int, int], _FakeCanvas]:
    '''Factory fixture that creates _FakeCanvas instances for testing.
    
    Usage:
        def test_something(fake_canvas):
            canvas = fake_canvas(10, 5)  # Create 10x5 canvas
            # Use canvas in test
    
    Returns:
        A callable that creates _FakeCanvas instances with specified width and height.
    '''
    def _create_canvas(width: int = 10, height: int = 5) -> _FakeCanvas:
        '''Create a TTkCanvas with the specified dimensions.
        
        :param width: canvas width in terminal cells, defaults to 10
        :type width: int
        :param height: canvas height in terminal cells, defaults to 5
        :type height: int
        :return: initialized TTkCanvas instance
        :rtype: ttk.TTkCanvas
        '''
        return _FakeCanvas(width=width, height=height)

    return _create_canvas