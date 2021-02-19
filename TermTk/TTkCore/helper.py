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

class TTkHelper:
    # TODO: Add Setter/Getter
    _rootCanvas = None
    _updateWidget = []
    _paintBuffer  = []

    @staticmethod
    def addUpdateWidget(widget):
        if widget not in TTkHelper._updateWidget:
            TTkHelper._updateWidget.append(widget)

    @staticmethod
    def addPaintBuffer(canvas):
        if canvas is not TTkHelper._rootCanvas:
            if canvas not in TTkHelper._paintBuffer:
                TTkHelper._paintBuffer.append(canvas)

    @staticmethod
    def registerRootCanvas(canvas):
        TTkHelper._rootCanvas = canvas
        TTkHelper._paintBuffer = []
        TTkHelper._updateWidget = []

    @staticmethod
    def execPaint(cw, ch):
        if TTkHelper._rootCanvas is None :
            return
        for canvas in TTkHelper._paintBuffer:
            widget = canvas.getWidget()
            x = widget.getX()
            y = widget.getY()
            w = widget.getWidth()
            h = widget.getHeight()
            TTkHelper._rootCanvas.paintCanvas(canvas, x, y, w, h)
        TTkHelper._paintBuffer = []

    @staticmethod
    def paintAll():
        if TTkHelper._rootCanvas is None:
            return
        for widget in TTkHelper._updateWidget:
            widget.paintEvent()
        TTkHelper._updateWidget = []
        TTkHelper.execPaint(TTkGlbl.term_w,TTkGlbl.term_h)
        TTkHelper._rootCanvas.pushToTerminal(0, 0, TTkGlbl.term_w, TTkGlbl.term_h)

        # curses.panel.update_panels()
        # TTkGlbl.GLBL['screen'].refresh()

    @staticmethod
    def absPos(widget) -> (int,int):
        pos = TTkHelper.absParentPos(widget)
        return widget.pos() + pos

    @staticmethod
    def absParentPos(widget) -> (int,int):
        if widget is None or widget.parentWidget() is None:
            return (0, 0)
        return TTkHelper.absPos(widget.parentWidget())