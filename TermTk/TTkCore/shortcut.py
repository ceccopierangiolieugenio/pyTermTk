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

__all__ = ['TTkShortcut']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent

class TTkStandardKey():
    pass

class TTkKeySequence():
    __slots__ = ('_key')
    def __init__(self, key:int):
        self._key = key
        mod = (
            ( TTkK.ControlModifier if key & TTkK.CTRL  else 0 ) |
            ( TTkK.AltModifier     if key & TTkK.ALT   else 0 ) |
            ( TTkK.ShiftModifier   if key & TTkK.SHIFT else 0 ) )
        key &= ~(TTkK.CTRL|TTkK.ALT|TTkK.SHIFT|TTkK.META)
        t = TTkK.SpecialKey if mod else TTkK.Character
        self._key = TTkKeyEvent(type=t, key=key, mod=mod, code="")

    def __hash__(self) -> int:
        return self._key.__hash__()

    def __eq__(self, __value: object) -> bool:
        pass

class TTkShortcut():
    _shortcuts = {}
    __slots__ = (
        '_key', '_parent', '_shortcutContext',
        # Signals
        'activated')
    def __init__(self,
                 key:int|TTkKeySequence, parent=None,
                 shortcutContext: TTkK.ShortcutContext = TTkK.ShortcutContext.WindowShortcut):
        if type(key) == int:
            key = TTkKeySequence(key)._key
        self._key = key
        self._parent = parent
        self._shortcutContext = shortcutContext
        # Signals
        self.activated = pyTTkSignal()
        if key not in TTkShortcut._shortcuts:
            TTkShortcut._shortcuts[key] = []
        TTkShortcut._shortcuts[key].append(self)

    @staticmethod
    def processKey(key, focusWidget):
        if key in TTkShortcut._shortcuts:
            for sc in TTkShortcut._shortcuts[key]:
                if ( (   sc._shortcutContext == TTkK.WidgetShortcut
                       and focusWidget == sc._parent )
                  or ( sc._shortcutContext == TTkK.WidgetWithChildrenShortcut
                        and (  focusWidget == sc._parent
                            or TTkHelper.isParent(sc._parent,focusWidget) ) )
                  or ( sc._shortcutContext == TTkK.WindowShortcut )
                  or ( sc._shortcutContext == TTkK.ApplicationShortcut )):
                    if sc.activated._connected_slots:
                        sc.activated.emit()
                        return True
        return False
