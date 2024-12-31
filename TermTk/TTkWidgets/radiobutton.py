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

__all__ = ['TTkRadioButton']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkWidgets.widget import TTkWidget

class TTkRadioButton(TTkWidget):
    '''
    **Checked**
    ::

        (X)radioButton

    **Unchecked**
    ::

        ( )RadioButton

    Demo: `formwidgets.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/formwidgets.py>`_

    '''

    clicked:pyTTkSignal
    '''
    This signal is emitted when the button is activated
    '''

    classStyle = {
                'default':     {'color': TTkColor.RST,
                                'borderColor':TTkColor.RST,
                                'rbContentColor': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'borderColor':TTkColor.fg('#888888'),
                                'rbContentColor': TTkColor.fg('#888888')},
                'focus':       {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")+TTkColor.BOLD,
                                'borderColor': TTkColor.fg("#ffff00") + TTkColor.BOLD,
                                'rbContentColor': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")+TTkColor.BOLD},
            }

    _radioLists = {}
    __slots__ = (
        '_checked', '_text', '_radiogroup',
        # Signals
        'clicked', 'toggled'
        )
    def __init__(self, *,
                 radiogroup:str='DefaultGroup',
                 checked:bool=False,
                 checkStatus:TTkK.CheckState = None,
                 text:TTkString='',
                 **kwargs) -> None:
        '''
        :param str text: the text shown on the radio button, defaults to ""
        :type text: str, optional
        :param str radiogroup: the text used to group the RadioButtons, only one checked status is allowed in between all the radio buttons with the same radiogroup, defaults to "DefaultGroup"
        :type radiogroup: str, optional
        :param bool checked: Checked status, defaults to "False"
        :type checked: bool, optional
        :param checkStatus: If defined, override the option defined in the 'checked' field otherwise defaults to :py:class:`TTkK.CheckState.Checked` or :py:class:`TTkK.CheckState.Unchecked` based on the checked status
        :type checkStatus: :py:class:`TTkK.CheckState` , optional
        '''

        # Define Signals
        self.clicked = pyTTkSignal()
        self.toggled = pyTTkSignal(bool)
        # use name if radiogroup is not available for retrocompatibility
        self._radiogroup = radiogroup
        # self.checked = pyTTkSignal()
        self._checked = checked
        if checkStatus != None :
            self._checked = checkStatus==TTkK.Checked
        else:
            self._checked = checked
        self._text = TTkString(text)

        TTkWidget.__init__(self, **kwargs)

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

        :return: :py:class:`TTkString`
        '''
        return self._text

    def setText(self, text):
        ''' This property holds the text shown on the checkhox

        :param text:
        :type text: :py:class:`TTkString`
        '''
        if self._text.sameAs(text): return
        self._text = TTkString(text)
        self.setMinimumSize(3 + len(self._text), 1)
        self.update()

    def isChecked(self):
        ''' This property holds whether the radiobutton is checked

        :return: bool - True if :py:class:`~TermTk.TTkCore.constant.TTkConstant.CheckState.Checked` or :py:class:`~TermTk.TTkCore.constant.TTkConstant.CheckState.PartiallyChecked`
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

        :return: :py:class:`TTkConstant.CheckState` : the checkbox status
        '''
        if self._checked:
            return TTkK.Checked
        else:
            return TTkK.Unchecked

    def setCheckState(self, state):
        ''' Sets the radiobutton's check state.

        :param state: state of the checkbox
        :type state: :py:class:`TTkConstant.CheckState`
        '''
        if not self._checked and state == TTkK.Unchecked: return
        if self._checked and state != TTkK.Unchecked: return
        if self._checked and state == TTkK.Unchecked:
            self._checked = False
        else:
            self._checkEvent()
        self.toggled.emit(self._checked)
        self.update()

    def paintEvent(self, canvas):
        style = self.currentStyle()

        borderColor = style['borderColor']
        textColor   = style['color']
        xColor = style['rbContentColor']

        canvas.drawText(pos=(0,0), color=borderColor ,text="( )")
        canvas.drawText(pos=(3,0), color=textColor ,text=self._text)
        if self._checked:
            canvas.drawText(pos=(1,0), color=xColor ,text="X")
        else:
            canvas.drawText(pos=(1,0), color=xColor ,text=" ")

    def _checkEvent(self):
        # Uncheck the radio already checked;
        for radio in TTkRadioButton._radioLists[self._radiogroup]:
            if self != radio != None:
                if radio.isChecked():
                    radio.setCheckState(TTkK.Unchecked)
        self._checked = True

    def _pressEvent(self):
        self._checkEvent()
        self.clicked.emit()
        self.update()

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        self.setCheckState(TTkK.Checked)
        self.clicked.emit()
        return True

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._pressEvent()
            return True
        return False

