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

__all__ = ['About']

import TermTk as ttk
from .. import __version__

_DPT_image = ttk.TTkUtil.base64_deflate_2_obj(
    "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")

class About(ttk.TTkWindow):
    def __init__(self, **kwargs):
        image = ttk.TTkLabel(text=_DPT_image)
        super().__init__(**kwargs)
        self.setTitle('About the Dumb Paint Tool...')
        self.resize(65+2,12+4)
        self.layout().addWidgets([
            ttk.TTkLabel(text=_DPT_image),
            ttk.TTkLabel(pos=(38,7), text=ttk.TTkString(f"  Version: {__version__}", ttk.TTkColor.fg('#AAAAFF'))),
            ttk.TTkLabel(pos=(38,9), text=ttk.TTkString("Powered By, Eugenio Parodi",ttk.TTkColor.fg("#FF00FF"))),
            ttk.TTkLabel(pos=(13,11),text=ttk.TTkString("https://github.com/ceccopierangiolieugenio/pyTermTk", ttk.TTkColor.fg('#44FFFF', link="https://github.com/ceccopierangiolieugenio/pyTermTk")))
            ])
