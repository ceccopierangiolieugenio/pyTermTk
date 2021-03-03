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
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.constant import *

class TTkHelper:
    # TODO: Add Setter/Getter
    _focusWidget = None
    _rootCanvas = None
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

    _overlay = None

    @staticmethod
    def addUpdateWidget(widget):
        if widget not in TTkHelper._updateWidget:
            TTkHelper._updateWidget.append(widget)

    @staticmethod
    def addUpdateBuffer(canvas):
        if canvas is not TTkHelper._rootCanvas:
            if canvas not in TTkHelper._updateBuffer:
                TTkHelper._updateBuffer.append(canvas)

    @staticmethod
    def registerRootCanvas(canvas):
        TTkHelper._rootCanvas = canvas
        TTkHelper._updateBuffer = []
        TTkHelper._updateWidget = []

    @staticmethod
    def isOverlay(widget):
        if widget is None:
            return False
        if TTkHelper._overlay is None:
            return False
        while widget is not None:
            if widget == TTkHelper._overlay._widget:
                return True
            widget = widget.parentWidget()
        return False

    @staticmethod
    def overlay(caller, widget, x, y):
        wx, wy = TTkHelper.absPos(caller)
        TTkHelper._overlay = TTkHelper._Overlay(wx+x,wy+y,widget)
        # widget.setFocus()

    @staticmethod
    def getOverlay():
        if TTkHelper._overlay is not None:
            return TTkHelper._overlay._widget
        return None

    @staticmethod
    def removeOverlay():
        if TTkHelper._overlay is not None:
            TTkHelper._overlay = None

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

        if TTkHelper._overlay is not None:
            TTkHelper._rootCanvas.clean()
            TTkHelper._rootCanvas.getWidget().paintChildCanvas()
            lx,ly,lw,lh = (0, 0, TTkGlbl.term_w, TTkGlbl.term_h)
            child =TTkHelper._overlay._widget
            cx,cy,cw,ch = child.geometry()
            TTkHelper._rootCanvas.paintCanvas(
                                child.getCanvas(),
                                (cx,  cy,  cw, ch),
                                (0,0,cw,ch),
                                (lx, ly, lw, lh))

        if pushToTerminal:
            if TTkHelper._cursor:
                lbt.Term.hideCursor()
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
        ppos = TTkHelper.absParentPos(widget)
        wpos = widget.pos()
        return (wpos[0]+ppos[0], wpos[1]+ppos[1])

    @staticmethod
    def absParentPos(widget) -> (int,int):
        if widget is None or widget.parentWidget() is None:
            return (0, 0)
        return TTkHelper.absPos(widget.parentWidget())

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
