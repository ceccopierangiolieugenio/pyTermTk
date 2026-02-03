# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTKodeCommandPaletteListItem', 'TTKodeCommandPaletteListItemFile']

from pathlib import Path

import TermTk as ttk

class TTKodeCommandPaletteListItem():
    def toTTkString(self, width:int) -> ttk.TTkString:
        return ttk.TTkString()

_colorDirectory = ttk.TTkColor.fg('#AAAAAA')

class TTKodeCommandPaletteListItemFile():
    __slots__ = ('_file')
    _file:Path
    def __init__(self, file:Path):
        self._file = file

    def toTTkString(self, width:int) -> ttk.TTkString:
        file = self._file
        fileName = file.name
        folder = file.parent

        text = (
            ttk.TTkString(ttk.TTkCfg.theme.fileIcon.getIcon(fileName), ttk.TTkCfg.theme.fileIconColor) +
            ttk.TTkString(" " + fileName + " ") + ttk.TTkString( folder, _colorDirectory )
        )

        if len(text) > width:
            text = text.substring(to=width-3) + '...'

        return text
