#!/usr/bin/env python3

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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import *

class TTkCheckbox(TTkWidget):
    '''
    **Checked**
    ::

        [X]CheckBox

    **Unchecked**
    ::

        [ ]CheckBox

    :Demo: `formwidgets.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/formwidgets.py>`_

    :param str text: the text shown on the checkbox, defaults to ""
    :type text: str, optional
    :param bool checked: Checked status, defaults to "False"
    :type checked: bool, optional

    +-----------------------------------------------------------------------------------------------+
    | `Signals <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_ |
    +-----------------------------------------------------------------------------------------------+

        .. py:method:: clicked(checked)
            :signal:

            This signal is emitted when the button is activated

            :param checked: True if checked otherwise False
            :type checked: bool

        .. py:method:: stateChanged(state)
            :signal:

            This signal is emitted whenever the checkbox's state changes, i.e., whenever the user checks or unchecks it.

            :param state: state of the checkbox
            :type state: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState`

     '''
    __slots__ = (
        '_checked', '_text',
        # Signals
        'clicked', 'stateChanged'
        )
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkCheckbox' )
        # Define Signals
        self.stateChanged = pyTTkSignal(int)
        self.clicked = pyTTkSignal(bool)
        self._checked = kwargs.get('checked', False )
        self._text = kwargs.get('text', '' )
        self.setMinimumSize(3 + len(self._text), 1)
        self.setMaximumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def checkState(self):
        ''' Retrieve the state of the checkbox

        :return: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState` : the checkbox status
        '''
        if self._checked:
            return TTkK.Checked
        else:
            return TTkK.Unchecked

    def setCheckState(self, state):
        ''' Sets the checkbox's check state.

        :param state: state of the checkbox
        :type state: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState`
        '''


        self._checked = state == TTkK.Checked
        self.update()

    def paintEvent(self):
        if self.hasFocus():
            borderColor = TTkCfg.theme.checkboxBorderColorFocus
            textColor   = TTkCfg.theme.checkboxTextColorFocus
            xColor      = TTkCfg.theme.checkboxContentColorFocus
        else:
            borderColor = TTkCfg.theme.checkboxBorderColor
            textColor   = TTkCfg.theme.checkboxTextColor
            xColor      = TTkCfg.theme.checkboxContentColor
        self._canvas.drawText(pos=(0,0), color=borderColor ,text="[ ]")
        self._canvas.drawText(pos=(3,0), color=textColor ,text=self._text)
        if self._checked:
            self._canvas.drawText(pos=(1,0), color=xColor ,text="X")
        else:
            self._canvas.drawText(pos=(1,0), color=xColor ,text=" ")

    def _pressEvent(self):
        self._checked = not self._checked
        self.clicked.emit(self._checked)
        self.stateChanged.emit(self.checkState())
        self.update()
        return True

    def mousePressEvent(self, evt):
        self._pressEvent()
        return True

    def keyEvent(self, evt):
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._pressEvent()
            return True
        return False
