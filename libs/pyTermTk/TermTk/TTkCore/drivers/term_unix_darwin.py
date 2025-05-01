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

__all__ = ['TTkTerm']

import sys

try: import termios
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

from ..TTkTerm.term_base import TTkTermBase
from .term_unix_common import _TTkTerm

class TTkTerm(_TTkTerm):
    @staticmethod
    def _setSigmask(mask, value=True):
        attr = termios.tcgetattr(sys.stdin)
        if mask & TTkTerm.Sigmask.CTRL_C:
            attr[6][termios.VINTR]=  b'\x03' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_S:
            attr[6][termios.VSTOP]=  b'\x13' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_Z:
            attr[6][termios.VSUSP]=  b'\x1a' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_Q:
            attr[6][termios.VSTART]= b'\x11' if value else 0
        if mask & TTkTerm.Sigmask.CTRL_Y:
            attr[6][termios.VDSUSP]= b'\x19' if value else 0
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, attr)
    TTkTermBase.setSigmask = _setSigmask

    @staticmethod
    def _getSigmask():
        mask = 0x00
        attr = termios.tcgetattr(sys.stdin)
        mask |= TTkTerm.Sigmask.CTRL_C if attr[6][termios.VINTR]  else 0
        mask |= TTkTerm.Sigmask.CTRL_S if attr[6][termios.VSTOP]  else 0
        mask |= TTkTerm.Sigmask.CTRL_Z if attr[6][termios.VSUSP]  else 0
        mask |= TTkTerm.Sigmask.CTRL_Q if attr[6][termios.VSTART] else 0
        mask |= TTkTerm.Sigmask.CTRL_Y if attr[6][termios.VDSUSP] else 0
        return mask
    TTkTermBase.getSigmask = _getSigmask
