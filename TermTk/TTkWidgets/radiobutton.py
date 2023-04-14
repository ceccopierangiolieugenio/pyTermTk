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
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkWidgets.widget import *

class TTkRadioButton(TTkWidget):
    '''
    **Checked**
    ::

        (X)radioButton

    **Unchecked**
    ::

        ( )RadioButton

    Demo: `formwidgets.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/formwidgets.py>`_

    :param str text: the text shown on the radio button, defaults to ""
    :type text: str, optional
    :param str radiogroup: the text used to group the RadioButtons, only one checked status is allowed in between all the radio buttons with the same radiogroup, defaults to "DefaultGroup"
    :type radiogroup: str, optional
    :param bool checked: Checked status, defaults to "False"
    :type checked: bool, optional

    +-----------------------------------------------------------------------------------------------+
    | `Signals <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_ |
    +-----------------------------------------------------------------------------------------------+

        .. py:method:: clicked()
            :signal:

            This signal is emitted when the button is activated

     '''

    _radioLists = {}
    __slots__ = (
        '_checked', '_text', '_radiogroup'
        # Signals
        'clicked'
        )
    def __init__(self, *args, **kwargs):
        # Define Signals
        self.clicked = pyTTkSignal()
        # use name if radiogroup is not available for retrocompatibility
        self._radiogroup = kwargs.get('name', 'DefaultGroup' )
        self._radiogroup = kwargs.get('radiogroup', self._radiogroup )
        TTkWidget.__init__(self, *args, **kwargs)
        # self.checked = pyTTkSignal()
        self._checked = kwargs.get('checked', False )
        self._text = TTkString(kwargs.get('text', '' ))
        self.setMinimumSize(3 + len(self._text), 1)
        self.setMaximumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        if self._radiogroup not in TTkRadioButton._radioLists:
            TTkRadioButton._radioLists[self._radiogroup] = [self]
        else:
            TTkRadioButton._radioLists[self._radiogroup].append(self)

    def radioGroup(self):
        return self._radiogroup

    def text(self):
        ''' This property holds the text shown on the checkhox

        :return: :class:`~TermTk.TTkCore.string.TTkString`
        '''
        return self._text

    def setText(self, text):
        ''' This property holds the text shown on the checkhox

        :param text:
        :type text: :class:`~TermTk.TTkCore.string.TTkString`
        '''
        if self._text.sameAs(text): return
        self._text = TTkString(text)
        self.setMinimumSize(3 + len(self._text), 1)
        self.update()

    def isChecked(self):
        ''' This property holds whether the radiobutton is checked

        :return: bool - True if :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState.Checked` or :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState.PartiallyChecked`
        '''
        return self._checked

    def setChecked(self, state):
        ''' Set the check status

        :param state:
        :type tate: bool
        '''
        self.setCheckState(TTkK.Checked if state else TTkK.Unchecked)

    def checkState(self):
        ''' Retrieve the state of the radiobutton

        :return: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState` : the checkbox status
        '''
        if self._checked:
            return TTkK.Checked
        else:
            return TTkK.Unchecked

    def setCheckState(self, state):
        ''' Sets the radiobutton's check state.

        :param state: state of the checkbox
        :type state: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState`
        '''
        if not self._checked and state == TTkK.Unchecked: return
        if self._checked and state != TTkK.Unchecked: return
        if self._checked and state == TTkK.Unchecked:
            self._checked = False
        else:
            self._checkEvent()
        self.update()

    def paintEvent(self):
        if self.hasFocus():
            borderColor = TTkCfg.theme.radioButtonBorderColorFocus
            textColor   = TTkCfg.theme.radioButtonTextColorFocus
            xColor      = TTkCfg.theme.radioButtonContentColorFocus
        else:
            borderColor = TTkCfg.theme.radioButtonBorderColor
            textColor   = TTkCfg.theme.radioButtonTextColor
            xColor      = TTkCfg.theme.radioButtonContentColor
        self._canvas.drawText(pos=(0,0), color=borderColor ,text="( )")
        self._canvas.drawText(pos=(3,0), color=textColor ,text=self._text)
        if self._checked:
            self._canvas.drawText(pos=(1,0), color=xColor ,text="X")
        else:
            self._canvas.drawText(pos=(1,0), color=xColor ,text=" ")

    def _checkEvent(self):
        # Uncheck the radio already checked;
        for radio in TTkRadioButton._radioLists[self._radiogroup]:
            if self != radio != None:
                if radio._checked:
                    radio._checked = False
                    radio.update()
        self._checked = True

    def _pressEvent(self):
        self._checkEvent()
        self.clicked.emit()
        self.update()

    def mousePressEvent(self, evt):
        self._pressEvent()
        return True

    def keyEvent(self, evt):
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._pressEvent()
            return True
        return False

