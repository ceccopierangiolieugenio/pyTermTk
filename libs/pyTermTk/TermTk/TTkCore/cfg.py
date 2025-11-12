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
from __future__ import annotations

__all__ = ['TTkCfg', 'TTkGlbl']

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from TermTk.TTkTheme.theme import TTkTheme

from TermTk import __version__
from TermTk.TTkCore.constant import TTkK

class _TTkCfg:
    version:str = __version__
    name:str = "pyTermTk"

    color_depth: int = TTkK.DEP_24

    maxFps:int = 65
    doubleBuffer:bool = True
    doubleBufferNew:bool = False

    scrollDelta:int = 5

    _theme:Optional[TTkTheme] = None
    @property
    def theme(self) -> TTkTheme:
        if not TTkCfg._theme:
            from TermTk.TTkTheme.theme import TTkTheme
            TTkCfg._theme = TTkTheme()
        return TTkCfg._theme

TTkCfg = _TTkCfg()

class TTkGlbl:
    term_w: int = 0
    term_h: int = 0


