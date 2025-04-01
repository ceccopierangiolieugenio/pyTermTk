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

__all__ = ['TTkButton']

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkWidgets.widget import TTkWidget

class TTkButton(TTkWidget):
    ''' TTkButton:

    Border = True
    ::

         ┌────────┐
         │  Text  │
         ╘════════╛

    Border = False
    ::

         [  Text  ]

         ╿ Text 2 ╿
         ╽New line╽

         ╿ Text 3 ╿
         │  New   │
         ╽  Line  ╽

    Demo: `formwidgets.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/formwidgets.py>`_
    '''

    clicked:pyTTkSignal
    '''
    This signal is emitted when the button is activated
    '''

    toggled:pyTTkSignal
    '''
    This signal is emitted whenever the button state changes if checkeable,
    i.e., whenever the user checks or unchecks it.

    :param checked: True if checked otherwise False
    :type checked: bool
    '''

    classStyle = {
                'default':     {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044"),
                                'borderColor': TTkColor.RST,
                                'grid':1},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'borderColor':TTkColor.fg('#888888'),
                                'grid':0},
                'hover':       {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000050")+TTkColor.BOLD,
                                'borderColor': TTkColor.fg("#FFFFCC")+TTkColor.BOLD,
                                'grid':1},
                'checked':     {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#004488"),
                                'borderColor': TTkColor.fg("#FFFFFF"),
                                'grid':0},
                'unchecked':   {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044"),
                                'borderColor': TTkColor.RST,
                                'grid':3},
                'clicked':     {'color': TTkColor.fg("#FFFFDD")+TTkColor.BOLD,
                                'borderColor': TTkColor.fg("#DDDDDD")+TTkColor.BOLD,
                                'grid':0},
                'focus':       {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")+TTkColor.BOLD,
                                'borderColor': TTkColor.fg("#ffff00") + TTkColor.BOLD,
                                'grid':1},
            }

    __slots__ = (
        '_text', '_border',
        '_checkable', '_checked',
        # Signals
        'clicked', 'toggled'
        )
    def __init__(self, *,
                 text:TTkString="",
                 border:bool=False,
                 checked:bool=False,
                 checkable:bool=False,
                 **kwargs) -> None:
        '''
        :param str text: the text shown on the button, defaults to ""
        :type text: str, optional

        :param bool border: the border of the button, defaults to "False"
        :type border: bool, optional

        :param bool checked: checked status if the button is checkable, defaults to "False"
        :type checked: bool, optional
        :param bool checkable: define if the button is checkable, defaults to "False"
        :type checkable: bool, optional
        '''
        self._text = TTkString(text).split('\n')
        textWidth = max(t.termWidth() for t in self._text)
        self._border = border
        if self._border:
            self.setDefaultSize(kwargs, textWidth+2, len(self._text)+2)
        else:
            self.setDefaultSize(kwargs, textWidth+2, len(self._text))

        super().__init__(**kwargs)
        # Define Signals
        self.clicked = pyTTkSignal()
        self.toggled = pyTTkSignal(bool)

        self._checked = checked
        self._checkable = checkable

        if self._border:
            if 'minSize' not in kwargs:
                if 'minWidth' not in kwargs:
                    self.setMinimumWidth(textWidth+2)
                if 'minHeight' not in kwargs:
                    self.setMinimumHeight(len(self._text)+2)
        else:
            if 'minSize' not in kwargs:
                if 'minWidth' not in kwargs:
                    self.setMinimumWidth(textWidth+2)
                if 'minHeight' not in kwargs:
                    self.setMinimumHeight(len(self._text))
            if 'maxSize' not in kwargs:
                if 'maxHeight' not in kwargs:
                    self.setMaximumHeight(len(self._text))

        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def border(self) -> bool:
        ''' This property holds whether the button has a border

        :return: bool
        '''
        return self._border

    def isCheckable(self) -> bool:
        ''' This property holds whether the button is checkable

        :return: bool
        '''
        return self._checkable

    def setCheckable(self, ch:bool) -> None:
        ''' Enable/Disable the checkable property

        :param ch: Checkable
        :type ch: bool
        '''
        self._checkable = ch
        self.update()

    def isChecked(self) -> bool:
        ''' This property holds whether the button is checked

        Only checkable buttons can be checked. By default, the button is unchecked.

        :return: bool
        '''
        return self._checked

    def setChecked(self, ch:bool) -> None:
        ''' Set the checked status

        :param ch: Checked
        :type ch: bool
        '''
        self._checked = ch
        self.toggled.emit(self._checked)
        self.update()

    def text(self) -> TTkString:
        ''' This property holds the text shown on the button

        :return: :py:class:`TTkString`
        '''
        return TTkString('\n').join(self._text)

    def setText(self, text:TTkString) -> None:
        ''' This property holds the text shown on the button

        :param text:
        :type text: :py:class:`TTkString`
        '''
        if self._text and self._text[0] == text: return
        self._text = TTkString(text).split('\n')
        textWidth = max(t.termWidth() for t in self._text)
        if self._border:
            self.setMinimumSize(textWidth+2, len(self._text)+2)
        else:
            self.setMinimumSize(textWidth+2, len(self._text))
            self.setMaximumHeight(len(self._text))
        self.update()


    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        # TTkLog.debug(f"{self._text} Test Mouse {evt}")
        self.update()
        return True

    def mouseReleaseEvent(self, evt:TTkMouseEvent) -> bool:
        # TTkLog.debug(f"{self._text} Test Mouse {evt}")
        if self._checkable:
            self._checked = not self._checked
            self.toggled.emit(self._checked)
        self.update()
        self.clicked.emit()
        return True

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            if self._checkable:
                self._checked = not self._checked
                self.toggled.emit(self._checked)
            self.update()
            self.clicked.emit()
            return True
        return False

    def paintEvent(self, canvas:TTkCanvas) -> None:
        if self.isEnabled() and self._checkable:
            if self._checked:
                style = self.style()['checked']
            else:
                style = self.style()['unchecked']
            if self.hasFocus():
                borderColor = self.style()['focus']['borderColor']
            else:
                borderColor = style['borderColor']
        else:
            style = self.currentStyle()
            borderColor = style['borderColor']
        textColor   = style['color']
        grid = style['grid']

        w,h = self.size()

        # Draw the border and bgcolor
        if not self._border or (self._border and ( h==1 or ( h>1 and len(self._text)>h-2 and len(self._text[0])!=0 ))):
            canvas.fill(pos=(1,0), size=(w-2,h), color=textColor)
            if h<=1:
                canvas.drawChar(pos=(0  ,0), color=borderColor ,char='[')
                canvas.drawChar(pos=(w-1,0), color=borderColor ,char=']')
            else: # No border multiline button
                canvas.drawChar(pos=(0,  0),  char='╿', color=borderColor)
                canvas.drawChar(pos=(w-1,0),  char='╿', color=borderColor)
                canvas.drawChar(pos=(w-1,h-1),char='╽', color=borderColor)
                canvas.drawChar(pos=(0,  h-1),char='╽', color=borderColor)
                for y in range(1,h-1):
                    canvas.drawChar(pos=(0,  y),char='│', color=borderColor)
                    canvas.drawChar(pos=(w-1,y),char='│', color=borderColor)
        else:
            canvas.fill(pos=(1,1), size=(w-2,h-2), color=textColor)
            canvas.drawButtonBox(pos=(0,0),size=(self._width,self._height),color=borderColor, grid=grid)
        # Print the text strings
        off = 1 if self._border else 0
        for i,t in enumerate(self._text, (h-len(self._text))//2):
            if t!='':
                canvas.drawText(pos=(1,i) ,text=t.completeColor(textColor), color=textColor, width=w-2, alignment=TTkK.CENTER_ALIGN)
