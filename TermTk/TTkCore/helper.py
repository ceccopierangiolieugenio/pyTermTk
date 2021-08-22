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

import TermTk.libbpytop as lbt
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg, TTkGlbl
from TermTk.TTkCore.constant import TTkK

class TTkHelper:
    # TODO: Add Setter/Getter
    _focusWidget = None
    _rootCanvas = None
    _rootWidget = None
    _updateWidget = []
    _updateBuffer  = []
    _cursorPos = [0,0]
    _cursor = False
    _cursorType = lbt.Term.cursor_blinking_block
    class _Overlay():
        __slots__ = ('_widget','_x','_y')
        def __init__(self,x,y,widget):
            self._widget = widget
            widget.move(x,y)
    _savedFocus = None
    _overlay = []

    class _Shortcut():
        __slots__ = ('_letter','_widget')
        def __init__(self, letter, widget):
            self._letter = letter.lower()
            self._widget = widget
    _shortcut = []

    @staticmethod
    def addShortcut(widget, letter):
        TTkHelper._shortcut.append(TTkHelper._Shortcut(letter, widget))

    @staticmethod
    def isParent(parent, widget):
        if parent==widget: return True
        if widget.parentWidget() is None: return False
        return TTkHelper.isParent(parent,widget.parentWidget())

    @staticmethod
    def execShortcut(letter, widget=None):
        if not isinstance(letter, str): return
        for sc in TTkHelper._shortcut:
            if sc._letter == letter.lower() and sc._widget.isVisible():
                if not widget or TTkHelper.isParent(widget, sc._widget):
                    sc._widget.shortcutEvent()
                    return

    @staticmethod
    def updateAll():
        if TTkHelper._rootWidget:
            TTkHelper._rootWidget.update(repaint=True, updateLayout=True)

    @staticmethod
    def addUpdateWidget(widget):
        if not widget.isVisible(): return
        if widget not in TTkHelper._updateWidget:
            TTkHelper._updateWidget.append(widget)

    @staticmethod
    def addUpdateBuffer(canvas):
        if canvas is not TTkHelper._rootCanvas:
            if canvas not in TTkHelper._updateBuffer:
                TTkHelper._updateBuffer.append(canvas)

    @staticmethod
    def registerRootWidget(widget):
        TTkHelper._rootCanvas = widget.getCanvas()
        TTkHelper._rootWidget = widget
        TTkHelper._rootCanvas.enableDoubleBuffer()
        TTkHelper._updateBuffer = []
        TTkHelper._updateWidget = []

    @staticmethod
    def rootOverlay(widget):
        if widget is None:
            return None
        if not TTkHelper._overlay:
            return None
        overlayWidgets = [o._widget for o in TTkHelper._overlay]
        while widget is not None:
            if widget in overlayWidgets:
                return widget
            widget = widget.parentWidget()
        return None

    @staticmethod
    def isOverlay(widget):
         return TTkHelper.rootOverlay(widget) is not None

    @staticmethod
    def overlay(caller, widget, x, y):
        wx, wy = TTkHelper.absPos(caller)
        w,h = widget.size()
        if not TTkHelper._savedFocus and \
           not TTkHelper.isOverlay(TTkHelper._focusWidget):
            TTkHelper._savedFocus = TTkHelper._focusWidget
        # Try to keep the overlay widget inside the terminal
        wx = max(0, wx+x if wx+x+w < TTkGlbl.term_w else TTkGlbl.term_w-w )
        wy = max(0, wy+y if wy+y+h < TTkGlbl.term_h else TTkGlbl.term_h-h )
        TTkHelper._overlay.append(TTkHelper._Overlay(wx,wy,widget))
        TTkHelper._rootWidget.rootLayout().addWidget(widget)
        widget.setFocus()
        widget.raiseWidget()

    @staticmethod
    def getOverlay():
        if TTkHelper._overlay:
            return TTkHelper._overlay[-1]._widget
        return None

    @staticmethod
    def removeOverlay(refocus=True):
        for widget in TTkHelper._overlay:
            TTkHelper._rootWidget.rootLayout().removeWidget(widget._widget)
        TTkHelper._overlay = []
        if TTkHelper._focusWidget:
            TTkHelper._focusWidget.clearFocus()
        if TTkHelper._savedFocus:
            bk = TTkHelper._savedFocus
            TTkHelper._savedFocus = None
            if refocus:
                bk.setFocus()

    @staticmethod
    def removeSingleOverlay(widget):
        if len(TTkHelper._overlay) <= 1:
            return TTkHelper.removeOverlay()
        rootWidget = TTkHelper.rootOverlay(widget)
        rootWidget
        for o in TTkHelper._overlay:
            if o._widget == rootWidget:
                TTkHelper._overlay.remove(o)
        TTkHelper._rootWidget.rootLayout().removeWidget(rootWidget)
        TTkHelper._overlay[-1]._widget.setFocus()

    @staticmethod
    def paintAll():
        '''
            _updateBuffer = list widgets that require a repaint [paintEvent]
            _updateWidget = list widgets that need to be pushed below
        '''
        if TTkHelper._rootCanvas is None:
            return

        # Build a list of buffers to be repainted
        updateBuffers = TTkHelper._updateBuffer.copy()
        updateWidgets = TTkHelper._updateWidget.copy()

        # TTkLog.debug(f"{len(TTkHelper._updateBuffer)} {len(TTkHelper._updateWidget)}")
        for widget in TTkHelper._updateWidget:
            if not widget.isVisible(): continue
            parent = widget.parentWidget()
            while parent is not None:
                if parent not in updateBuffers:
                    updateBuffers.append(parent)
                if parent not in updateWidgets:
                    updateWidgets.append(parent)
                parent = parent.parentWidget()

        TTkHelper._updateBuffer = []
        TTkHelper._updateWidget = []

        # Paint all the canvas
        for widget in updateBuffers:
            if not widget.isVisible(): continue
            # Resize the canvas just before the paintEvent
            # to avoid too many allocations
            widget.getCanvas().updateSize()
            widget.getCanvas().clean()
            widget.paintEvent()

        # Compose all the canvas to the parents
        # From the deepest childs to the bottom
        pushToTerminal = False
        sortedUpdateWidget = [ (w, TTkHelper.widgetDepth(w)) for w in updateWidgets]
        sortedUpdateWidget = sorted(sortedUpdateWidget, key=lambda w: -w[1])
        for w in sortedUpdateWidget:
            widget = w[0]
            if not widget.isVisible(): continue
            pushToTerminal = True
            widget.paintChildCanvas()

        if pushToTerminal:
            if TTkHelper._cursor:
                lbt.Term.hideCursor()
            if TTkCfg.doubleBuffer:
                TTkHelper._rootCanvas.pushToTerminalBuffered(0, 0, TTkGlbl.term_w, TTkGlbl.term_h)
            else:
                TTkHelper._rootCanvas.pushToTerminal(0, 0, TTkGlbl.term_w, TTkGlbl.term_h)
            if TTkHelper._cursor:
                x,y = TTkHelper._cursorPos
                lbt.Term.push(lbt.Mv.to(y+1,x+1))
                lbt.Term.showCursor(TTkHelper._cursorType)

    @staticmethod
    def widgetDepth(widget) -> int:
        if widget is None:
            return 0
        return 1 + TTkHelper.widgetDepth(widget.parentWidget())

    @staticmethod
    def absPos(widget) -> (int,int):
        wx, wy = 0,0
        layout = widget.widgetItem()
        while layout:
            px, py = layout.pos()
            wx, wy = wx+px, wy+py
            layout = layout.parent()
        return (wx, wy)

    def nextFocus(widget):
        rootWidget = TTkHelper.rootOverlay(widget)
        if not rootWidget:
            rootWidget =  TTkHelper._rootWidget
        if widget == rootWidget:
            widget = None
        first = None
        for w in rootWidget.rootLayout().iterWidgets():
            if not first and w.focusPolicy() & TTkK.TabFocus == TTkK.TabFocus:
                first = w
            # TTkLog.debug(f"{w._name} {widget}")
            if widget:
                if w == widget:
                    widget=None
                continue
            if w.focusPolicy() & TTkK.TabFocus == TTkK.TabFocus:
                w.setFocus()
                w.update()
                return
        if first:
            first.setFocus()
            first.update()

    def prevFocus(widget):
        rootWidget = TTkHelper.rootOverlay(widget)
        if not rootWidget:
            rootWidget = TTkHelper._rootWidget
        if widget == rootWidget:
            widget = None
        prev = None
        for w in rootWidget.rootLayout().iterWidgets():
            # TTkLog.debug(f"{w._name} {widget}")
            if w == widget:
                widget=None
                if prev:
                    break
            if w.focusPolicy() & TTkK.TabFocus == TTkK.TabFocus:
                prev = w
        if prev:
            prev.setFocus()
            prev.update()

    @staticmethod
    def setFocus(widget):
        TTkHelper._focusWidget = widget

    @staticmethod
    def getFocus():
        return TTkHelper._focusWidget

    @staticmethod
    def clearFocus():
        TTkHelper._focusWidget = None

    @staticmethod
    def showCursor(cursorType = TTkK.Cursor_Blinking_Block):
        if   cursorType == TTkK.Cursor_Blinking_Block      : TTkHelper._cursorType = lbt.Term.cursor_blinking_block
        elif cursorType == TTkK.Cursor_Blinking_Block_Also : TTkHelper._cursorType = lbt.Term.cursor_blinking_block_also
        elif cursorType == TTkK.Cursor_Steady_Block        : TTkHelper._cursorType = lbt.Term.cursor_steady_block
        elif cursorType == TTkK.Cursor_Blinking_Underline  : TTkHelper._cursorType = lbt.Term.cursor_blinking_underline
        elif cursorType == TTkK.Cursor_Steady_Underline    : TTkHelper._cursorType = lbt.Term.cursor_steady_underline
        elif cursorType == TTkK.Cursor_Blinking_Bar        : TTkHelper._cursorType = lbt.Term.cursor_blinking_bar
        elif cursorType == TTkK.Cursor_Steady_Bar          : TTkHelper._cursorType = lbt.Term.cursor_steady_bar
        lbt.Term.showCursor(TTkHelper._cursorType)
        TTkHelper._cursor = True
    @staticmethod
    def hideCursor():
        lbt.Term.hideCursor()
        TTkHelper._cursorType = lbt.Term.cursor_blinking_block
        TTkHelper._cursor = False
    @staticmethod
    def moveCursor(widget, x, y):
        xx, yy = TTkHelper.absPos(widget)
        TTkHelper._cursorPos = [xx+x,yy+y]
        lbt.Term.push(lbt.Mv.to(yy+y+1,xx+x+1))


    class Color(lbt.Color): pass
    class Mv(lbt.Mv): pass
