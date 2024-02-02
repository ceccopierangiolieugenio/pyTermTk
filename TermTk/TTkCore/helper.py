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

__all__ = ['TTkHelper']

from TermTk.TTkCore.TTkTerm.colors import TTkTermColor
from TermTk.TTkCore.TTkTerm.term import TTkTerm
from TermTk.TTkCore.cfg import TTkCfg, TTkGlbl
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot

class TTkHelper:
    '''TTkHelper

    This is a collection of helper utilities to be used all around TermTk
    '''
    # TODO: Add Setter/Getter
    _focusWidget = None
    _rootCanvas = None
    _rootWidget = None
    _updateWidget = set()
    _updateBuffer  = set()
    _mousePos = (0,0)
    _cursorPos = (0,0)
    _cursor = False
    _cursorType = TTkTerm.Cursor.BLINKING_BLOCK
    _cursorWidget = None
    class _Overlay():
        __slots__ = ('_widget','_prevFocus','_x','_y','_modal')
        def __init__(self,x,y,widget,prevFocus,modal):
            self._widget = widget
            self._prevFocus = prevFocus
            self._modal = modal
            widget.move(x,y)
    _overlay = []

    @staticmethod
    def updateAll():
        if TTkHelper._rootWidget:
            TTkHelper._rootWidget.update(repaint=True, updateLayout=True)
            for w in TTkHelper._rootWidget.layout().iterWidgets():
                w.update(repaint=True, updateLayout=True)

    @staticmethod
    def unlockPaint():
        if rw := TTkHelper._rootWidget:
            rw._paintEvent.set()

    @staticmethod
    def addUpdateWidget(widget):
        # if not widget.isVisibleAndParent(): return
        if widget not in TTkHelper._updateWidget:
            TTkHelper._updateWidget.add(widget)
            TTkHelper.unlockPaint()

    @staticmethod
    def addUpdateBuffer(canvas):
        if canvas is not TTkHelper._rootCanvas:
            TTkHelper._updateBuffer.add(canvas)

    @staticmethod
    def registerRootWidget(widget):
        TTkHelper._rootCanvas = widget.getCanvas()
        TTkHelper._rootWidget = widget
        TTkHelper._rootCanvas.enableDoubleBuffer()

    quitEvent = pyTTkSignal()

    @staticmethod
    @pyTTkSlot()
    def quit():
        '''Quit TermTk'''
        TTkHelper.quitEvent.emit()
        if TTkHelper._rootWidget:
            TTkHelper._rootWidget._quit()

    @staticmethod
    def getTerminalSize():
        return TTkGlbl.term_w, TTkGlbl.term_h

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
    def focusLastModal():
        if modal := TTkHelper.getLastModal():
            modal._widget.setFocus()

    @staticmethod
    def getLastModal():
        modal = None
        for o in TTkHelper._overlay:
            if o._modal:
                modal = o
        return modal

    @staticmethod
    def checkModalOverlay(widget):
        #if not TTkHelper._overlay:
        #    # There are no Overlays
        #    return True

        if not (lastModal := TTkHelper.getLastModal()):
            return True

        # if not TTkHelper._overlay[-1]._modal:
        #     # The last window is not modal
        #     return True
        if not (rootWidget := TTkHelper.rootOverlay(widget)):
            # This widget is not overlay
            return False
        if rootWidget in [ o._widget for o in TTkHelper._overlay[TTkHelper._overlay.index(lastModal):]]:
            return True
        # if TTkHelper._overlay[-1]._widget == rootWidget:
        #     return True
        return False

    @staticmethod
    def isOverlay(widget):
        return TTkHelper.rootOverlay(widget) is not None

    @staticmethod
    def overlay(caller, widget, x:int, y:int, modal:bool=False, forceBoundaries:bool=True, toolWindow:bool=False):
        '''overlay'''
        if not caller:
            caller = TTkHelper._rootWidget
        wx, wy = TTkHelper.absPos(caller)
        w,h = widget.size()

        # Try to keep the overlay widget inside the terminal
        if forceBoundaries:
            wx = max(0, wx+x if wx+x+w < TTkGlbl.term_w else TTkGlbl.term_w-w )
            wy = max(0, wy+y if wy+y+h < TTkGlbl.term_h else TTkGlbl.term_h-h )
            mw,mh = widget.minimumSize()
            ww = min(w,max(mw, TTkGlbl.term_w))
            wh = min(h,max(mh, TTkGlbl.term_h))
            widget.resize(ww,wh)
        else:
            wx += x
            wy += y

        if  toolWindow:
            # Forcing the layer to:
            # TTkLayoutItem.LAYER1    =  0x40000000
            widget.move(wx,wy)
            wi = widget.widgetItem()
            wi.setLayer(wi.LAYER1)
        else:
            TTkHelper._overlay.append(TTkHelper._Overlay(wx,wy,widget,TTkHelper._focusWidget,modal))
        TTkHelper._rootWidget.rootLayout().addWidget(widget)
        widget.setFocus()
        widget.raiseWidget()
        if hasattr(widget,'rootLayout'):
            for w in widget.rootLayout().iterWidgets(onlyVisible=True):
                w.update()

    @staticmethod
    def getOverlay():
        if TTkHelper._overlay:
            return TTkHelper._overlay[-1]._widget
        return None

    @staticmethod
    def removeOverlay():
        if not TTkHelper._overlay:
            return
        bkFocus = None
        # Remove the first element also if it is modal
        TTkHelper._overlay[-1]._modal = False
        while TTkHelper._overlay:
            if TTkHelper._overlay[-1]._modal:
                break
            owidget = TTkHelper._overlay.pop()
            bkFocus = owidget._prevFocus
            TTkHelper._rootWidget.rootLayout().removeWidget(owidget._widget)
        if TTkHelper._focusWidget:
            TTkHelper._focusWidget.clearFocus()
        if bkFocus:
            bkFocus.setFocus()

    @staticmethod
    def removeOverlayAndChild(widget):
        if not TTkHelper.isOverlay(widget): return
        if len(TTkHelper._overlay) <= 1:
            return TTkHelper.removeOverlay()
        rootWidget = TTkHelper.rootOverlay(widget)
        bkFocus = None
        found = False
        newOverlay = []
        for o in TTkHelper._overlay:
            if o._widget == rootWidget:
                found = True
                bkFocus = o._prevFocus
            if not found:
                newOverlay.append(o)
            else:
                TTkHelper._rootWidget.rootLayout().removeWidget(o._widget)
        TTkHelper._overlay = newOverlay
        if bkFocus:
            bkFocus.setFocus()
        if not found:
            TTkHelper.removeOverlay()

    @staticmethod
    def removeOverlayChild(widget):
        rootWidget = TTkHelper.rootOverlay(widget)
        found = False
        newOverlay = []
        for o in TTkHelper._overlay:
            if o._widget == rootWidget:
                found = True
                newOverlay.append(o)
                continue
            if not found:
                newOverlay.append(o)
            else:
                TTkHelper._rootWidget.rootLayout().removeWidget(o._widget)
        TTkHelper._overlay = newOverlay
        if not found:
            TTkHelper.removeOverlay()

    @staticmethod
    def setMousePos(pos):
        TTkHelper._mousePos = pos
        # update the position of the Drag and Drop Widget
        if TTkHelper._dnd:
            hsx, hsy = TTkHelper._dnd['d'].hotSpot()
            TTkHelper._dnd['d'].pixmap().move(pos[0]-hsx, pos[1]-hsy)

    @staticmethod
    def mousePos():
        return TTkHelper._mousePos

    @staticmethod
    def paintAll():
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
    def rePaintAll():
        if TTkHelper._rootCanvas and  TTkHelper._rootWidget:
            TTkTerm.push(TTkTerm.CLEAR)
            TTkHelper._rootCanvas.cleanBuffers()
            TTkHelper._rootWidget.update()

    @staticmethod
    def widgetDepth(widget) -> int:
        if widget is None:
            return 0
        return 1 + TTkHelper.widgetDepth(widget.parentWidget())

    @staticmethod
    def isParent(widget, parent):
        if p := widget.parentWidget():
            if p == parent:
                return True
            return TTkHelper.isParent(p, parent)
        return False

    @staticmethod
    def widgetAt(x, y, layout=None):
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
    def absPos(widget) -> (int,int):
        wx, wy = 0,0
        layout = widget.widgetItem()
        while layout:
            px, py = layout.pos()
            ox, oy = layout.offset()
            wx, wy = wx+px+ox, wy+py+oy
            layout = layout.parent()
        return (wx, wy)

    @staticmethod
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
            if w.isEnabled() and w.focusPolicy() & TTkK.TabFocus == TTkK.TabFocus:
                w.setFocus()
                w.update()
                return
        if first:
            first.setFocus()
            first.update()

    @staticmethod
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
            if w.isEnabled() and w.focusPolicy() & TTkK.TabFocus == TTkK.TabFocus:
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
    def hideCursor():
        TTkTerm.Cursor.hide()
        TTkHelper._cursorType = TTkTerm.Cursor.BLINKING_BLOCK
        TTkHelper._cursor = False
        # TTkHelper._cursorWidget = None

    @staticmethod
    def moveCursor(widget, x, y):
        TTkHelper._cursorWidget = widget
        xx, yy = TTkHelper.absPos(widget)
        pos = (xx+x,yy+y)
        if TTkHelper._cursorPos == pos:
            return
        TTkHelper._cursorPos = pos
        TTkTerm.push(TTkTerm.Cursor.moveTo(yy+y+1,xx+x+1))

    @staticmethod
    def cursorWidget():
        return TTkHelper._cursorWidget

    class Color(TTkTermColor): pass

    # Drag and Drop related helper routines
    _dnd = None

    @staticmethod
    def dndInit(drag):
        TTkHelper._dnd = {
                'd' : drag,
                'w' : None
            }
        TTkHelper._rootWidget.rootLayout().addWidget(drag.pixmap())
        drag.pixmap().raiseWidget()

    @staticmethod
    def dndGetDrag():
        return TTkHelper._dnd['d'] if TTkHelper._dnd else None

    @staticmethod
    def dndWidget():
        return TTkHelper._dnd['w'] if TTkHelper._dnd else None

    @staticmethod
    def dndEnter(widget):
        TTkHelper._dnd['w'] = widget

    @staticmethod
    def isDnD():
        return TTkHelper._dnd is not None

    @staticmethod
    def dndEnd():
        if TTkHelper._dnd:
            TTkHelper._rootWidget.rootLayout().removeWidget(TTkHelper._dnd['d'].pixmap())
        TTkHelper._dnd = None
        TTkHelper._rootWidget.update()

    # ToolTip Helper Methods
    toolTipWidget = None
    toolTipTrigger = lambda _: True
    toolTipReset   = lambda  : True

    @staticmethod
    def toolTipShow(tt):
        TTkHelper.toolTipClose()
        if not TTkHelper._rootWidget: return
        TTkHelper.toolTipWidget = tt
        rw,rh = TTkHelper._rootWidget.size()
        tw,th = tt.size()
        mx,my =  TTkHelper._mousePos
        x = max(0, min(mx-(tw//2),rw-tw))
        if my <= th: # Draw below the Mouse
            y = my+1
        else: # Draw above the Mouse
            y = max(0,my-th)
        tt.move(x,y)
        TTkHelper._rootWidget.rootLayout().addWidget(tt)
        tt.raiseWidget()

    def toolTipClose():
        TTkHelper.toolTipReset()
        if TTkHelper.toolTipWidget:
            TTkHelper._rootWidget.rootLayout().removeWidget(TTkHelper.toolTipWidget)
            TTkHelper.toolTipWidget = None
