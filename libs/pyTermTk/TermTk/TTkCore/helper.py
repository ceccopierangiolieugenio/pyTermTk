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

from __future__ import annotations

__all__ = ['TTkHelper']

from typing import TYPE_CHECKING, Set, Optional, Tuple, Callable
from dataclasses import dataclass

from TermTk.TTkCore.TTkTerm.term import TTkTerm
from TermTk.TTkCore.cfg import TTkCfg, TTkGlbl
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

if TYPE_CHECKING:
    from TermTk.TTkGui.drag import TTkDnDEvent, TTkDrag
    from TermTk.TTkCore.ttk import TTk
    from TermTk.TTkCore.canvas import TTkCanvas
    from TermTk.TTkCore.string import TTkString
    from TermTk.TTkWidgets.widget import TTkWidget
    from TermTk.TTkWidgets.container import TTkContainer

class TTkHelper:
    '''TTkHelper

    This is a collection of helper utilities to be used all around TermTk
    '''
    _rootCanvas: Optional[TTkCanvas] = None
    _rootWidget: Optional[TTk] = None
    _updateWidget:Set[TTkWidget] = set()
    _updateBuffer:Set[TTkWidget]  = set()
    _mousePos: Tuple[int, int] = (0,0)
    _cursorPos: Tuple[int, int] = (0,0)
    _cursor: bool = False
    _cursorType: str = TTkTerm.Cursor.BLINKING_BLOCK
    _cursorWidget: Optional[TTkWidget] = None

    @staticmethod
    def updateAll() -> None:
        if TTkHelper._rootWidget:
            TTkHelper._rootWidget.update(repaint=True, updateLayout=True)
            for w in TTkHelper._rootWidget.layout().iterWidgets():
                w.update(repaint=True, updateLayout=True)

    @staticmethod
    def unlockPaint() -> None:
        if rw := TTkHelper._rootWidget:
            rw._paintEvent.set()

    @staticmethod
    def addUpdateWidget(widget: TTkWidget) -> None:
        # if not widget.isVisibleAndParent(): return
        if widget not in TTkHelper._updateWidget:
            TTkHelper._updateWidget.add(widget)
            TTkHelper.unlockPaint()

    @staticmethod
    def addUpdateBuffer(widget: TTkWidget) -> None:
        TTkHelper._updateBuffer.add(widget)

    @staticmethod
    def registerRootWidget(widget: TTk) -> None:
        TTkHelper._rootCanvas = widget.getCanvas()
        TTkHelper._rootWidget = widget
        TTkHelper._rootCanvas.enableDoubleBuffer()

    @staticmethod
    def cleanRootWidget() -> None:
        TTkHelper._rootCanvas = None
        TTkHelper._rootWidget = None

    quitEvent: pyTTkSignal = pyTTkSignal()

    @staticmethod
    @pyTTkSlot()
    def quit() -> None:
        '''Quit TermTk'''
        TTkHelper.quitEvent.emit()
        if TTkHelper._rootWidget:
            TTkHelper._rootWidget._quit()

    @staticmethod
    @pyTTkSlot()
    def aboutTermTk() -> None:
        '''
        Displays a simple message box about `pyTermTk <https://github.com/ceccopierangiolieugenio/pyTermTk>`__.
        The message includes the version number of TermTk being used by the application.

        This is useful for inclusion in the Help menu of an application, as shown in the Menus example.

        This function is a convenience slot for :py:meth:`TTk.aboutTermTk`.
        '''
        if TTkHelper._rootWidget:
            TTkHelper._rootWidget.aboutTermTk()

    @staticmethod
    def getTerminalSize() -> Tuple[int, int]:
        return TTkGlbl.term_w, TTkGlbl.term_h

    @staticmethod
    def checkModalOverlay(widget: TTkWidget) -> bool:
        if not TTkHelper._rootWidget:
            return False
        return TTkHelper._rootWidget._checkModalOverlay(widget)

    @staticmethod
    def overlay(caller: Optional[TTkWidget], widget: TTkWidget, x:int, y:int, modal:bool=False, forceBoundaries:bool=True, toolWindow:bool=False) -> None:
        '''overlay'''
        if not TTkHelper._rootWidget:
            return
        TTkHelper._rootWidget.overlay(
            caller=caller,
            widget=widget,
            pos=(x,y),
            modal=modal,
            forceBoundaries=forceBoundaries,
            toolWindow=toolWindow
        )

    @staticmethod
    def removeOverlay() -> None:
        if not TTkHelper._rootWidget:
            return
        return TTkHelper._rootWidget._removeOverlay()

    @staticmethod
    def removeOverlayAndChild(widget: Optional[TTkWidget]) -> None:
        if not TTkHelper._rootWidget:
            return
        return TTkHelper._rootWidget._removeOverlayAndChild(widget=widget)

    @staticmethod
    def removeOverlayChild(widget: TTkWidget) -> None:
        if not TTkHelper._rootWidget:
            return
        return TTkHelper._rootWidget._removeOverlayChild(widget=widget)

    @staticmethod
    def setMousePos(pos: Tuple[int, int]) -> None:
        TTkHelper._mousePos = pos
        # update the position of the Drag and Drop Widget
        if TTkHelper._dnd:
            hsx, hsy = TTkHelper._dnd.d.hotSpot()
            TTkHelper._dnd.d.pixmap().move(pos[0]-hsx, pos[1]-hsy)

    @staticmethod
    def mousePos() -> Tuple[int, int]:
        return TTkHelper._mousePos

    @staticmethod
    def paintAll() -> None:
        '''
            _updateBuffer = list widgets that require a repaint [paintEvent]
            _updateWidget = list widgets that need to be pushed below
        '''
        if TTkHelper._rootCanvas is None:
            return

        # Build a list of buffers to be repainted
        updateWidgetsBk = TTkHelper._updateWidget.copy()
        updateBuffers = TTkHelper._updateBuffer.copy()
        TTkHelper._updateWidget.clear()
        TTkHelper._updateBuffer.clear()
        updateWidgets = set()

        # TTkLog.debug(f"{len(TTkHelper._updateBuffer)} {len(TTkHelper._updateWidget)}")
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
    def rePaintAll() -> None:
        if TTkHelper._rootCanvas and  TTkHelper._rootWidget:
            TTkTerm.push(TTkTerm.CLEAR)
            TTkHelper._rootCanvas.cleanBuffers()
            TTkHelper._rootWidget.update()

    @staticmethod
    def widgetDepth(widget: TTkWidget) -> int:
        if widget is None:
            return 0
        return 1 + TTkHelper.widgetDepth(widget.parentWidget())

    @staticmethod
    def isParent(widget: TTkWidget, parent: TTkWidget) -> bool:
        if p := widget.parentWidget():
            if p == parent:
                return True
            return TTkHelper.isParent(p, parent)
        return False

    @staticmethod
    def widgetAt(x: int, y: int, layout=None) -> Optional[TTkWidget]:
        if not TTkHelper._rootWidget:
            return None
        layout = layout if layout else TTkHelper._rootWidget.rootLayout()
        lx,ly,lw,lh =layout.geometry()
        lox, loy = layout.offset()
        lx,ly,lw,lh = lx+lox, ly+loy, lw-lox, lh-loy
        if x<lx or x>=lx+lw or y<ly or y>=lh+ly: return None
        x-=lx
        y-=ly
        for item in reversed(layout.zSortedItems):
            if item.layoutItemType() == TTkK.WidgetItem and not item.isEmpty():
                widget = item.widget()
                if not widget._visible: continue
                wx,wy,ww,wh = widget.geometry()

                if wx <= x < wx+ww and wy <= y < wy+wh:
                    if hasattr(widget,'rootLayout'):
                        return TTkHelper.widgetAt(x-wx, y-wy, widget.rootLayout())
                    else:
                        return widget
                continue

            elif item.layoutItemType() == TTkK.LayoutItem:
                if (wid:=TTkHelper.widgetAt(x, y, item)):
                    return wid
        return layout.parentWidget()

    @staticmethod
    def absPos(widget: TTkWidget) -> Tuple[int,int]:
        wx, wy = 0,0
        layout = widget.widgetItem()
        while layout:
            px, py = layout.pos()
            ox, oy = layout.offset()
            wx, wy = wx+px+ox, wy+py+oy
            layout = layout.parent()
        return (wx, wy)

    @staticmethod
    def showCursor(cursorType: int = TTkK.Cursor_Blinking_Block) -> None:
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

    @staticmethod
    def hideCursor() -> None:
        TTkTerm.Cursor.hide()
        TTkHelper._cursorType = TTkTerm.Cursor.BLINKING_BLOCK
        TTkHelper._cursor = False
        # TTkHelper._cursorWidget = None

    @staticmethod
    def moveCursor(widget: TTkWidget, x: int, y: int) -> None:
        TTkHelper._cursorWidget = widget
        xx, yy = TTkHelper.absPos(widget)
        pos = (xx+x,yy+y)
        if TTkHelper._cursorPos == pos:
            return
        TTkHelper._cursorPos = pos
        TTkTerm.push(TTkTerm.Cursor.moveTo(yy+y+1,xx+x+1))

    @staticmethod
    def cursorWidget() -> Optional[TTkWidget]:
        return TTkHelper._cursorWidget

    @dataclass(frozen=False)
    class _DnD():
        d:  TTkDrag
        w:  Optional[TTkWidget] = None

    # Drag and Drop related helper routines
    _dnd: Optional[TTkHelper._DnD] = None

    @staticmethod
    def dndInit(drag:TTkDrag) -> None:
        if not TTkHelper._rootWidget:
            return
        TTkHelper._dnd = TTkHelper._DnD(d=drag, w=None)
        TTkHelper._rootWidget.rootLayout().addWidget(drag.pixmap())
        drag.pixmap().raiseWidget()

    @staticmethod
    def dndGetDnd() -> Optional[_DnD]:
        return TTkHelper._dnd

    @staticmethod
    def dndGetDrag() -> Optional[TTkDrag]:
        return TTkHelper._dnd.d if TTkHelper._dnd else None

    @staticmethod
    def dndWidget() -> Optional[TTkWidget]:
        return TTkHelper._dnd.w if TTkHelper._dnd else None

    @staticmethod
    def dndEnter(widget:TTkWidget) -> None:
        if not TTkHelper._dnd:
            return
        TTkHelper._dnd.w = widget

    @staticmethod
    def isDnD() -> bool:
        return TTkHelper._dnd is not None

    @staticmethod
    def dndEnd() -> None:
        if not TTkHelper._rootWidget:
            return
        if TTkHelper._dnd:
            TTkHelper._rootWidget.rootLayout().removeWidget(TTkHelper._dnd.d.pixmap())
        TTkHelper._dnd = None
        TTkHelper._rootWidget.update()

    # ToolTip Helper Methods
    toolTipWidget: Optional[TTkWidget] = None
    toolTipTrigger: Callable[[TTkString], None] = lambda _: None
    toolTipReset:   Callable[[], None] = lambda  : None

    @staticmethod
    def toolTipShow(tt: TTkWidget) -> None:
        TTkHelper.toolTipClose()
        if not TTkHelper._rootWidget:
            return
        TTkHelper.toolTipWidget = tt
        rw = TTkHelper._rootWidget.width()
        tw,th = tt.size()
        mx,my =  TTkHelper._mousePos
        x = max(0, min(mx-(tw//2),rw-tw))
        if my <= th: # Draw below the Mouse
            y = my+1
        else: # Draw above the Mouse
            y = max(0,my-th)
        wi = tt.widgetItem()
        wi.setLayer(wi.LAYER3)
        tt.move(x,y)
        TTkHelper._rootWidget.rootLayout().addWidget(tt)
        tt.raiseWidget()

    @staticmethod
    def toolTipClose() -> None:
        if not TTkHelper._rootWidget:
            return
        TTkHelper.toolTipReset()
        if TTkHelper.toolTipWidget:
            TTkHelper._rootWidget.rootLayout().removeWidget(TTkHelper.toolTipWidget)
            TTkHelper.toolTipWidget = None
