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

__all__ = ['TTkCheckbox']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkWidgets.widget import *

class TTkCheckbox(TTkWidget):
    '''
    **Checked**
    ::

        [X]CheckBox

    **Unchecked**
    ::

        [ ]CheckBox

    **Partially Checked**
    ::

        [/]CheckBox

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

        .. py:method:: toggled(checked)
            :signal:

            This signal is emitted whenever the checkbox's state changes, i.e., whenever the user checks or unchecks it.

            :param checked: True if checked otherwise False
            :type checked: bool

     '''

    classStyle = {
                'default':     {'color': TTkColor.RST,
                                'borderColor':TTkColor.RST,
                                'cbContentColor': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'borderColor':TTkColor.fg('#888888'),
                                'cbContentColor': TTkColor.fg('#888888')},
                'focus':       {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")+TTkColor.BOLD,
                                'borderColor': TTkColor.fg("#ffff00") + TTkColor.BOLD,
                                'cbContentColor': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")+TTkColor.BOLD},
            }

    __slots__ = (
        '_checkStatus', '_text', '_tristate',
        # Signals
        'clicked', 'stateChanged', 'toggled'
        )
    def __init__(self, *args, **kwargs):
        # Define Signals
        self.stateChanged = pyTTkSignal(TTkK.CheckState)
        self.clicked = pyTTkSignal(bool)
        self.toggled = pyTTkSignal(bool)

        TTkWidget.__init__(self, *args, **kwargs)

        if 'checkStatus' in kwargs:
            self._checkStatus = kwargs.get('checkStatus', TTkK.Unchecked )
        else:
            self._checkStatus = TTkK.Checked if kwargs.get('checked', False ) else TTkK.Unchecked
        self._tristate = kwargs.get('tristate', False)
        self._text = TTkString(kwargs.get('text', '' ))
        self.setMinimumSize(3 + len(self._text), 1)
        self.setMaximumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def text(self):
        ''' This property holds the text shown on the checkhox

        :return: :class:`~TermTk.TTkCore.string.TTkString`
        '''
        return self._text

    pyTTkSlot(str)
    def setText(self, text):
        ''' This property holds the text shown on the checkhox

        :param text:
        :type text: :class:`~TermTk.TTkCore.string.TTkString`
        '''
        if self._text.sameAs(text): return
        self._text = TTkString(text)
        self.setMinimumSize(3 + len(self._text), 1)
        self.update()

    def isTristate(self):
        ''' This property holds whether the checkbox is a tri-state checkbox

        :return: bool
        '''
        return self._tristate

    def setTristate(self, tristate):
        ''' Enable/Disable the tristate property

        :param tristate:
        :type tristate: bool
        '''
        if tristate == self._tristate: return
        self._tristate = tristate
        self.update()

    def isChecked(self):
        ''' This property holds whether the checkbox is checked

        :return: bool - True if :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState.Checked` or :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState.PartiallyChecked`
        '''
        return self._checkStatus != TTkK.Unchecked

    @pyTTkSlot(bool)
    def setChecked(self, state):
        ''' Set the check status

        :param state:
        :type state: bool
        '''
        self.setCheckState(TTkK.Checked if state else TTkK.Unchecked)

    def checkState(self):
        ''' Retrieve the state of the checkbox

        :return: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState` : the checkbox status
        '''
        return self._checkStatus

    @pyTTkSlot(TTkK.CheckState)
    def setCheckState(self, state):
        ''' Sets the checkbox's check state.

        :param state: state of the checkbox
        :type state: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState`
        '''
        if self._checkStatus == state: return
        if state==TTkK.PartiallyChecked and not self._tristate: return
        self._checkStatus = state
        self.update()

    def paintEvent(self, canvas):
        style = self.currentStyle()

        borderColor = style['borderColor']
        textColor   = style['color']
        xColor = style['cbContentColor']

        canvas.drawText(pos=(0,0), color=borderColor ,text="[ ]")
        canvas.drawText(pos=(3,0), color=textColor ,text=self._text)
        text = {
            TTkK.Checked :   "X",
            TTkK.Unchecked : " ",
            TTkK.PartiallyChecked: "/"}.get(self._checkStatus, " ")
        canvas.drawText(pos=(1,0), color=xColor ,text=text)

    def _pressEvent(self):
        self._checkStatus = {
            TTkK.Unchecked:        TTkK.PartiallyChecked,
            TTkK.PartiallyChecked: TTkK.Checked,
            TTkK.Checked:          TTkK.Unchecked,
        }.get(self._checkStatus,TTkK.Unchecked)
        if not self._tristate and self._checkStatus == TTkK.PartiallyChecked:
            self._checkStatus = TTkK.Checked
        self.clicked.emit(self._checkStatus!=TTkK.Unchecked)
        self.toggled.emit(self._checkStatus!=TTkK.Unchecked)
        self.stateChanged.emit(self._checkStatus)
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
