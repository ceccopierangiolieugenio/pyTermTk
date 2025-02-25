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

__all__ = ['TTkHelperDraw']

from .helper import TTkHelper
from TermTk.TTkCore.drivers import TTkAsyncio
from TermTk.TTkCore.TTkTerm.term import TTkTerm
from TermTk.TTkCore.cfg import TTkCfg, TTkGlbl
from TermTk.TTkCore.constant import TTkK

class TTkHelperDraw:
    '''TTkHelperDraw

    This is a collection of helper utilities to be used all around TermTk
    '''

    _updateWidget = set()
    _updateBuffer  = set()

    @staticmethod
    def updateAll():
        if TTkHelper._rootWidget:
            TTkHelper._rootWidget.update(repaint=True, updateLayout=True)
            for w in TTkHelper._rootWidget.layout().iterWidgets():
                w.update(repaint=True, updateLayout=True)

    @staticmethod
    def unlockPaint():
        if rw := TTkHelper._rootWidget:
            async def _set():
                rw._paintEvent.set()
            # TTkAsyncio.create_task(rw._paintEvent.set   )
            # rw._paintEvent.set()
            TTkAsyncio.create_task(_set())

    @staticmethod
    def addUpdateWidget(widget):
        # if not widget.isVisibleAndParent(): return
        if widget not in TTkHelperDraw._updateWidget:
            TTkHelperDraw._updateWidget.add(widget)
            TTkHelperDraw.unlockPaint()

    @staticmethod
    def addUpdateBuffer(canvas):
        if canvas is not TTkHelper._rootCanvas:
            TTkHelperDraw._updateBuffer.add(canvas)

    @staticmethod
    def paintAll():
        '''
            _updateBuffer = list widgets that require a repaint [paintEvent]
            _updateWidget = list widgets that need to be pushed below
        '''
        if TTkHelper._rootCanvas is None:
            return

        # Build a list of buffers to be repainted
        updateWidgetsBk = TTkHelperDraw._updateWidget.copy()
        updateBuffers = TTkHelperDraw._updateBuffer.copy()
        TTkHelperDraw._updateWidget.clear()
        TTkHelperDraw._updateBuffer.clear()
        updateWidgets = set()

        # TTkLog.debug(f"{len(TTkHelperDraw._updateBuffer)} {len(TTkHelperDraw._updateWidget)}")
        for widget in updateWidgetsBk:
            if not widget.isVisibleAndParent(): continue
            updateBuffers.add(widget)
            updateWidgets.add(widget)
            parent = widget.parentWidget()
            while parent is not None:
                updateBuffers.add(parent)
                updateWidgets.add(parent)
                parent = parent.parentWidget()

        # Paint all the canvas
        for widget in updateBuffers:
            if not widget.isVisibleAndParent(): continue
            # Resize the canvas just before the paintEvent
            # to avoid too many allocations
            canvas = widget.getCanvas()
            canvas.updateSize()
            canvas.clean()
            widget.paintEvent(canvas)

        # Compose all the canvas to the parents
        # From the deepest children to the bottom
        pushToTerminal = False
        sortedUpdateWidget = sorted(updateWidgets, key=lambda w: -TTkHelper.widgetDepth(w))
        for widget in sortedUpdateWidget:
            if not widget.isVisibleAndParent(): continue
            pushToTerminal = True
            widget.paintChildCanvas()

        if pushToTerminal:
            if TTkHelper._cursor:
                TTkTerm.Cursor.hide()
            if TTkCfg.doubleBuffer:
                TTkHelper._rootCanvas.pushToTerminalBuffered(0, 0, TTkGlbl.term_w, TTkGlbl.term_h)
            elif TTkCfg.doubleBufferNew:
                TTkHelper._rootCanvas.pushToTerminalBufferedNew(0, 0, TTkGlbl.term_w, TTkGlbl.term_h)
            else:
                TTkHelper._rootCanvas.pushToTerminal(0, 0, TTkGlbl.term_w, TTkGlbl.term_h)
            if TTkHelper._cursor:
                x,y = TTkHelper._cursorPos
                TTkTerm.push(TTkTerm.Cursor.moveTo(y+1,x+1))
                TTkTerm.Cursor.show(TTkHelper._cursorType)

    @staticmethod
    def rePaintAll():
        if TTkHelper._rootCanvas and  TTkHelper._rootWidget:
            TTkTerm.push(TTkTerm.CLEAR)
            TTkHelper._rootCanvas.cleanBuffers()
            TTkHelper._rootWidget.update()

    @staticmethod
    def showCursor(cursorType = TTkK.Cursor_Blinking_Block):
        newType = {
            TTkK.Cursor_Blinking_Block      : TTkTerm.Cursor.BLINKING_BLOCK,
            TTkK.Cursor_Blinking_Block_Also : TTkTerm.Cursor.BLINKING_BLOCK_ALSO,
            TTkK.Cursor_Steady_Block        : TTkTerm.Cursor.STEADY_BLOCK,
            TTkK.Cursor_Blinking_Underline  : TTkTerm.Cursor.BLINKING_UNDERLINE,
            TTkK.Cursor_Steady_Underline    : TTkTerm.Cursor.STEADY_UNDERLINE,
            TTkK.Cursor_Blinking_Bar        : TTkTerm.Cursor.BLINKING_BAR,
            TTkK.Cursor_Steady_Bar          : TTkTerm.Cursor.STEADY_BAR,
        }.get(cursorType, TTkTerm.Cursor.BLINKING_BAR)
        if not TTkHelper._cursor or TTkHelper._cursorType != newType:
            TTkHelper._cursorType = newType
            TTkTerm.Cursor.show(TTkHelper._cursorType)
        TTkHelper._cursor = True
