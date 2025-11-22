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

__all__ = ['_TTkRootContainer']

from typing import Optional

from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.shortcut import TTkShortcut
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.widget import TTkWidget

class _TTkRootContainer(TTkContainer):
    ''' _TTkRootContainer:

    Internal root container class that manages the application's root widget hierarchy and focus navigation.

    This class is not meant to be used directly by application code. It is instantiated internally by :py:class:`TTk`
    to provide the top-level container for all widgets and handle keyboard-based focus traversal.

    The root container manages focus cycling when Tab/Shift+Tab or arrow keys are pressed and no widget
    consumes the event, ensuring focus loops back to the first/last focusable widget.
    '''
    __slots__ = (
        '_focusWidget')

    _focusWidget:Optional[TTkWidget]

    def __init__(self, **kwargs) -> None:
        self._focusWidget = None
        super().__init__(**kwargs)

    def _getFocusWidget(self) -> Optional[TTkWidget]:
        '''
        Returns the currently focused widget.

        :return: the widget with focus, or None if no widget has focus
        :rtype: :py:class:`TTkWidget` or None
        '''
        return self._focusWidget

    def _setFocusWidget(self, widget:Optional[TTkWidget]) -> None:
        '''
        Sets the currently focused widget and triggers a repaint.

        :param widget: the widget to receive focus, or None to clear focus
        :type widget: :py:class:`TTkWidget` or None
        '''
        if self._focusWidget is widget:
            return
        self._focusWidget = widget
        self.update()

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        '''
        Handles keyboard events for focus navigation.

        Implements focus cycling behavior when Tab/Shift+Tab or arrow keys are pressed
        and no child widget consumes the event. When the last focusable widget is reached,
        focus cycles back to the first widget (and vice versa).

        :param evt: the keyboard event
        :type evt: :py:class:`TTkKeyEvent`

        :return: True if the event was handled, False otherwise
        :rtype: bool
        '''
        if super().keyEvent(evt=evt):
            return True

        # If this is reached after a tab focus event, it means that either
        # no focus widgets are defined
        # or the last/first focus is reached - the focus need to go to start from the opposite side
        if ( (evt.key == TTkK.Key_Tab and evt.mod == TTkK.NoModifier) or
             (evt.key in (TTkK.Key_Right, TTkK.Key_Down ) ) ) :
            if _nfw:=self._getFirstFocus(widget=None,focusPolicy=TTkK.FocusPolicy.TabFocus,reverse=False):
                _nfw.setFocus()
                return True
        if ( (evt.key == TTkK.Key_Tab and evt.mod == TTkK.ShiftModifier) or
             (evt.key in ( TTkK.Key_Left, TTkK.Key_Up ) ) ) :
            if _pfw:=self._getFirstFocus(widget=None,focusPolicy=TTkK.FocusPolicy.TabFocus,reverse=True):
                _pfw.setFocus()
                return True
        return False