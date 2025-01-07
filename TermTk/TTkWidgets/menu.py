# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkMenuButton', 'TTkMenu']

from TermTk.TTkCore.cfg import TTkK
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent

from TermTk.TTkLayouts.gridlayout import TTkGridLayout

from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.scrollarea import TTkScrollArea
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame

from TermTk.TTkAbstract.abstractscrollview import TTkAbstractScrollView

class _TTkMenuSpacer(TTkWidget):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def paintEvent(self, canvas):
        canvas.drawText(pos=(0,0), text="-"*self.width())

class TTkMenuButton(TTkWidget):
    '''TTkMenuButton'''
    classStyle = TTkWidget.classStyle | {
                'default':     {'color': TTkColor.RST},
                'highlighted': {'color': TTkColor.fg('#00FF00')+TTkColor.bg('#0055FF')},
                'hover':       {'color': TTkColor.fg('#00FF00')+TTkColor.bg('#0077FF')},
                'checked':     {'color': TTkColor.fg('#00FF00')+TTkColor.bg('#00FFFF')},
                'clicked':     {'color': TTkColor.fg('#FFFF00')},
                'disabled':    {'color': TTkColor.fg('#888888')},
            }

    __slots__ = (
        '_data','_text', '_checkable', '_checked', '_submenu', '_shortcuts', '_highlighted',
        # Signals
        'menuButtonClicked', 'triggered', 'toggled', 'dataChanged', 'textChanged')
    def __init__(self, *,
            text:TTkString=TTkString(),
            data:object=None,
            checked:bool=False,
            checkable:bool=False,
            **kwargs) -> None:
        self.dataChanged = pyTTkSignal(object)
        self.textChanged = pyTTkSignal(TTkString)
        self.menuButtonClicked = pyTTkSignal(TTkMenuButton)
        self.triggered = pyTTkSignal(bool)
        self.toggled = pyTTkSignal(bool)
        self._submenu = []
        self._text = text if type(text) == TTkString else TTkString(text)
        self._data = data
        self._checked = checked
        self._checkable = checkable
        self._shortcuts = []
        self._highlighted = False
        super().__init__(**kwargs)
        width = self._text.termWidth() + (3 if self._checkable else 1)
        self.setMinimumWidth(width)
        # self.setStyle(self.classStyle)

    # Forward Focus Method
    def setFocus(self):
        return self.parentWidget().setFocus()

    def data(self):
        ''' Returns the user data as set in the constructor or :py:class:`setData`.'''
        return self._data

    def setData(self, data):
        ''' Sets the Menu Button's internal data to the given userData.

        :param data: the user data
        '''
        if self._data == data: return
        self._data = data
        self.dataChanged.emit(self._data)
        self.update()

    def setHighlight(self, hl):
        if self._highlighted == hl: return
        self._highlighted = hl
        self.update()

    def isCheckable(self):
        ''' This property holds whether the button is checkable

        :return: bool
        '''
        return self._checkable

    def setCheckable(self, ch):
        ''' Enable/Disable the checkable property

        :param ch: Checkable
        :type ch: bool
        '''
        self._checkable = ch
        self.update()

    def isChecked(self):
        ''' This property holds whether the button is checked

        Only checkable buttons can be checked. By default, the button is unchecked.

        :return: bool
        '''
        return self._checked

    def setChecked(self, ch):
        ''' Set the checked status

        :param ch: Checked
        :type ch: bool
        '''
        self._checked = ch
        self.toggled.emit(self._checked)
        self.update()

    def text(self):
        ''' This property holds the text shown

        :return: :py:class:`TTkString`
        '''
        return self._text

    def setText(self, text):
        ''' This property holds the text shown

        :param text:
        :type text: :py:class:`TTkString`
        '''
        if self._text == text: return
        self._text = TTkString(text)
        self.textChanged.emit(self._text)
        self.update()

    @pyTTkSlot()
    def shortcutEvent(self):
        self._triggerButton()

    def _triggerSubmenu(self):
        if not self._submenu: return
        width = 2+max(smb.minimumWidth() for smb in self._submenu if type(smb) is TTkMenuButton)
        height = len(self._submenu)+2
        subMenu = TTkMenu(pos=(8,6), size=(width,height), caller=self)
        for smb  in self._submenu:
            subMenu.addMenuItem(smb)
        x,y = self.pos()
        if issubclass(type(_p := self.parentWidget()),TTkAbstractScrollView):
            wid = _p
            w,h = _p.size()
            _,voy = _p.getViewOffsets()
            ox,oy = w, y-voy-1
        else:
            subMenu.setTitle(self.text())
            subMenu.setTitleAlign(TTkK.LEFT_ALIGN)
            wid = self
            ox,oy = -1,0
        # Highlight the first entry in the submenu
        if btns := [b for b in self._submenu if type(b)==TTkMenuButton]:
            btns[0].setHighlight(True)
        TTkHelper.overlay(wid, subMenu, ox,oy)

    def _triggerButton(self):
        if not self._submenu and issubclass(type(_p := self.parentWidget()),TTkAbstractScrollView):
            _p._closeAll()
        if self._checkable:
            self._checked = not self._checked
            self.toggled.emit(self._checked)
        self.menuButtonClicked.emit(self)
        self.triggered.emit(self._checked)
        self._triggerSubmenu()
        if issubclass(type(_p := self.parentWidget()),TTkAbstractScrollView):
            _p._cleanHighlight()
        self.setHighlight(True)
        self.update()

    def mouseReleaseEvent(self, evt:TTkMouseEvent) -> bool:
        self._triggerButton()
        return True

    def _menuButtonEvent(self):
        self.menuButtonClicked.emit(self)

    def removeMenuItem(self, item):
        self._submenu.pop(self._submenu.index(item))

    def addMenu(self, text:TTkString, data:object=None, checkable:bool=False, checked:bool=False):
        '''addMenu'''
        text = text if issubclass(type(text),TTkString) else TTkString(text)
        text, shortcuts = text.extractShortcuts()
        button = TTkMenuButton(text=text, data=data, checkable=checkable, checked=checked)
        button._shortcuts = [ch.upper() for ch in shortcuts]
        self._submenu.append(button)
        return button

    def addSpacer(self):
        self._submenu.append(_TTkMenuSpacer())

    def paintEvent(self, canvas: TTkCanvas):
        if self._highlighted:
            style = self.style()['highlighted']
        else:
            style = self.currentStyle()

        # '▶','□','▣'
        w = self.width()
        if self._checkable:
            canvas.drawText(width=w, color=style['color'] ,text=('▣ ' if self._checked else '□ ')+self._text)
        else:
            canvas.drawText(width=w, color=style['color'] ,text=self._text)
        if self._submenu:
            canvas._set(0, w-1, '▶', style['color'])
        off = 0

class _TTkMenuAreaWidget(TTkAbstractScrollView):
    __slots__ = ('_submenu','_minWith','_caller')
    def __init__(self, *,
                 caller=None,
                 **kwargs) -> None:
        self._submenu = []
        self._minWidth = 0
        self._caller = caller
        super().__init__(**kwargs)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)
        self.viewChanged.connect(self._viewChangedHandler)

    def _resizeEvent(self):
        w,h = self.size()
        # w = w-1 if (h<len(self._submenu)) else w
        w = max(w,self._minWidth)
        for i,wid in enumerate(self._submenu):
            wid.setGeometry(0,i,w,1)
        # self.viewChanged.emit()

    def _closeAll(self):
        c = self
        while c._caller and type(c._caller) is TTkMenuButton:
            c = c._caller.parentWidget()
            TTkHelper.removeOverlayAndChild(c)
        TTkHelper.removeOverlayAndChild(self)

    def _cleanHighlight(self):
        [b.setHighlight(False) for b in self._submenu if type(b)==TTkMenuButton]


    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        if not self._submenu: return False
        btns = [b for b in self._submenu if type(b)==TTkMenuButton]
        if evt.type == TTkK.SpecialKey:
            # Retrieve the current highlighted button
            curBtn = _b[0] if (_b := [b for b in btns if b._highlighted]) else None
            if evt.key == TTkK.Key_Up:
                self._cleanHighlight()
                if not curBtn:
                    curBtn = btns[0]
                else:
                    curBtn = btns[(btns.index(curBtn)-1)%len(btns)]
                curBtn.setHighlight(True)
                return True
            elif evt.key == TTkK.Key_Down:
                self._cleanHighlight()
                if not curBtn:
                    curBtn = btns[0]
                else:
                    curBtn = btns[(btns.index(curBtn)+1)%len(btns)]
                curBtn.setHighlight(True)
                return True
            elif evt.key == TTkK.Key_Left:
                TTkHelper.removeOverlayAndChild(self)
                if self._caller:
                    self._caller.setFocus()
                return True
            elif evt.key == TTkK.Key_Right:
                if curBtn:
                    curBtn._triggerSubmenu()
                return True
            elif evt.key == TTkK.Key_Enter:
                if curBtn:
                    curBtn.shortcutEvent()
                    return True
        else:
            # Handle shortcuts
            if evt.key == " ":
                curBtn = _b[0] if (_b := [b for b in btns if b._highlighted]) else None
                if curBtn:
                    curBtn.shortcutEvent()
                    return True
            ch = evt.key.upper()
            for btn in btns:
                if ch in btn._shortcuts:
                    btn.shortcutEvent()
                    return True
        return super().keyEvent(evt)

    def resizeEvent(self, w, h):
        self._resizeEvent()

    def addMenuItem(self, item):
        if type(item) is TTkMenuButton:
            item.setHighlight(False)
        self._submenu.append(item)
        self.layout().addWidget(item)
        self._minWidth = max(self._minWidth,item.minimumWidth())
        self._resizeEvent()

    def addMenu(self, text:TTkString, data:object=None, checkable:bool=False, checked:bool=False):
        '''addMenu'''
        button = TTkMenuButton(text=text, data=data, checkable=checkable, checked=checked)
        self.addMenuItem(button)
        return button

    def addSpacer(self):
        self.addMenuItem(_TTkMenuSpacer())

    @pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def maximumWidth(self):   return 0x10000
    def maximumHeight(self):  return 0x10000
    def minimumWidth(self):   return 0
    def minimumHeight(self):  return 0


class TTkMenu(TTkResizableFrame):
    __slots__ = ('_scrollView',
                 #Forwarded Methods
                 'addSpacer','addMenuItem')
    def __init__(self,
                 caller=None,
                 **kwargs) -> None:
        super().__init__(**kwargs|{'layout':TTkGridLayout()})
        sa =TTkScrollArea(parent=self)
        self._scrollView = _TTkMenuAreaWidget(caller=caller)
        sa.setViewport(self._scrollView)

        # Forwarded Methods
        # self.addMenu     = self._scrollView.addMenu
        self.addSpacer   = self._scrollView.addSpacer
        self.addMenuItem = self._scrollView.addMenuItem

    def addMenu(self, *args, **kwargs) -> None:
        ret = self._scrollView.addMenu(*args, **kwargs)
        w,h = self._scrollView.viewFullAreaSize()
        self.resize(w+3,h+2)
        return ret

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        return self._scrollView.keyEvent(evt)
    # # Forward Focus Method
    # def setFocus(self):
    #     return self._scrollView.setFocus()
