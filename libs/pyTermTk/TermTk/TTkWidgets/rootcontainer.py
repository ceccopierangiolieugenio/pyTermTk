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

__all__ = ['_TTkRootContainer']

from typing import Optional, List, Tuple

from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.shortcut import TTkShortcut
from TermTk.TTkWidgets.container import TTkContainer
from TermTk.TTkWidgets.widget import TTkWidget

def _absPos(widget: TTkWidget) -> Tuple[int,int]:
    wx, wy = 0,0
    layout = widget.widgetItem()
    while layout:
        px, py = layout.pos()
        ox, oy = layout.offset()
        wx, wy = wx+px+ox, wy+py+oy
        layout = layout.parent()
    return (wx, wy)

class _TTkOverlay():
        __slots__ = ('_widget','_prevFocus','_modal')

        _widget:TTkWidget
        _prevFocus:Optional[TTkWidget]
        _modal:bool

        def __init__(
                self,
                pos:Tuple[int,int],
                widget:TTkWidget,
                prevFocus:Optional[TTkWidget],
                modal:bool):
            self._widget = widget
            self._prevFocus = prevFocus
            self._modal = modal
            widget.move(*pos)

class _TTkRootContainer(TTkContainer):
    ''' _TTkRootContainer:

    Internal root container class that manages the application's root widget hierarchy and focus navigation.

    This class is not meant to be used directly by application code. It is instantiated internally by :py:class:`TTk`
    to provide the top-level container for all widgets and handle keyboard-based focus traversal.

    The root container manages focus cycling when Tab/Shift+Tab or arrow keys are pressed and no widget
    consumes the event, ensuring focus loops back to the first/last focusable widget.
    '''
    __slots__ = (
        '_focusWidget',
        '_overlay')

    _focusWidget:Optional[TTkWidget]
    _overlay:List[_TTkOverlay]

    def __init__(self, **kwargs) -> None:
        self._focusWidget = None
        self._overlay = []
        super().__init__(**kwargs)

    def _getFocusWidget(self) -> Optional[TTkWidget]:
        '''
        Returns the currently focused widget.

        :return: the widget with focus, or None if no widget has focus
        :rtype: :py:class:`TTkWidget` or None
        '''
        return self._focusWidget

    def _setFocusWidget(self, widget:Optional[TTkWidget]) -> None:
        '''
        Sets the currently focused widget and triggers a repaint.

        :param widget: the widget to receive focus, or None to clear focus
        :type widget: :py:class:`TTkWidget` or None
        '''
        if self._focusWidget is widget:
            return
        self._focusWidget = widget
        self.update()

    def _loopFocus(self, container:TTkContainer, evt:TTkKeyEvent) -> bool:
        if ( (evt.key == TTkK.Key_Tab and evt.mod == TTkK.NoModifier) or
             (evt.key in (TTkK.Key_Right, TTkK.Key_Down ) ) ) :
            if _nfw:=container._getFirstFocus(widget=None,focusPolicy=TTkK.FocusPolicy.TabFocus):
                _nfw.setFocus()
                return True
        if ( (evt.key == TTkK.Key_Tab and evt.mod == TTkK.ShiftModifier) or
             (evt.key in ( TTkK.Key_Left, TTkK.Key_Up ) ) ) :
            if _pfw:=container._getLastFocus(widget=None,focusPolicy=TTkK.FocusPolicy.TabFocus):
                _pfw.setFocus()
                return True
        return False

    def _handleOverlay(self, evt:TTkKeyEvent) -> bool:
        if not self._overlay:
            return False
        _overlay = self._overlay[-1]
        _widget = _overlay._widget
        if _widget.keyEvent(evt=evt):
            return True
        if isinstance(_widget, TTkContainer) and self._loopFocus(evt=evt, container=_widget):
            return True

    def overlay(self,
                caller: Optional[TTkWidget],
                widget: TTkWidget,
                pos:Tuple[int,int],
                modal:bool=False,
                forceBoundaries:bool=True,
                toolWindow:bool=False) -> None:
        '''
        Adds a widget as an overlay on top of the current widget hierarchy.

        The overlay widget is positioned relative to the caller widget and automatically
        adjusted to stay within the root container boundaries (if forceBoundaries is True).
        Overlays can be modal (blocking interaction with underlying widgets) or non-modal.

        :param caller: the widget relative to which the overlay is positioned, or None to use root
        :type caller: :py:class:`TTkWidget` or None
        :param widget: the widget to display as an overlay
        :type widget: :py:class:`TTkWidget`
        :param pos: the (x, y) position offset relative to the caller widget
        :type pos: tuple[int, int]
        :param modal: if True, blocks interaction with underlying widgets
        :type modal: bool
        :param forceBoundaries: if True, adjusts position and size to keep overlay within root boundaries
        :type forceBoundaries: bool
        :param toolWindow: if True, treats the overlay as a tool window without focus management
        :type toolWindow: bool
        '''
        if not caller:
            caller = self
        x,y = pos
        wx, wy = _absPos(caller)
        w,h = widget.size()
        rw,rh = self.rootLayout().size()

        # Try to keep the overlay widget inside the rootContainer boundaries
        if forceBoundaries:
            wx = max(0, wx+x if wx+x+w < rw else rw-w )
            wy = max(0, wy+y if wy+y+h < rh else rh-h )
            mw,mh = widget.minimumSize()
            ww = min(w,max(mw, rw))
            wh = min(h,max(mh, rh))
            widget.resize(ww,wh)
        else:
            wx += x
            wy += y

        wi = widget.widgetItem()
        # Forcing the layer to:
        # TTkLayoutItem.LAYER1    =  0x40000000
        wi.setLayer(wi.LAYER1)

        if  toolWindow:
            widget.move(wx,wy)
        else:
            _fw = self._getFocusWidget()
            self._overlay.append(_TTkOverlay(
                    pos=(wx,wy),
                    widget=widget,
                    prevFocus=_fw,
                    modal=modal))

        self.rootLayout().addWidget(widget)
        widget.raiseWidget()
        widget.setFocus()
        if isinstance(widget, TTkContainer):
            for w in widget.rootLayout().iterWidgets(onlyVisible=True):
                w.update()

    def _removeOverlay(self) -> None:
        '''
        Removes the topmost overlay widget and restores focus to the previous widget.

        If the overlay is modal, it must be explicitly removed before any underlying
        overlays can be removed. Focus is restored to the widget that had focus before
        the overlay was added.
        '''
        if not self._overlay:
            return
        bkFocus = None
        # Remove the first element also if it is modal
        self._overlay[-1]._modal = False
        while self._overlay:
            if self._overlay[-1]._modal:
                break
            owidget = self._overlay.pop()
            bkFocus = owidget._prevFocus
            self.rootLayout().removeWidget(owidget._widget)
        if _fw:=self._getFocusWidget():
            _fw.clearFocus()
        if bkFocus:
            bkFocus.setFocus()

    def _removeOverlayAndChild(self, widget: Optional[TTkWidget]) -> None:
        '''
        Removes the specified overlay widget and all overlays added after it.

        This method finds the root overlay containing the given widget and removes it
        along with any child overlays that were added on top of it. Focus is restored
        to the widget that had focus before the overlay stack was created.

        :param widget: the widget whose root overlay (and children) should be removed
        :type widget: :py:class:`TTkWidget` or None
        '''
        if not widget:
            return
        if not self._isOverlay(widget):
            return
        if len(self._overlay) <= 1:
            return self._removeOverlay()
        rootWidget = self._rootOverlay(widget)
        bkFocus = None
        found = False
        newOverlay = []
        for o in self._overlay:
            if o._widget == rootWidget:
                found = True
                bkFocus = o._prevFocus
            if not found:
                newOverlay.append(o)
            else:
                self.rootLayout().removeWidget(o._widget)
        self._overlay = newOverlay
        if bkFocus:
            bkFocus.setFocus()
        if not found:
            self._removeOverlay()

    def _removeOverlayChild(self, widget: TTkWidget) -> None:
        '''
        Removes all overlay widgets that were added after the specified widget.

        This method preserves the overlay containing the given widget but removes
        all overlays that were added on top of it. If the widget is not found in
        the overlay stack, removes the topmost overlay.

        :param widget: the widget whose child overlays should be removed
        :type widget: :py:class:`TTkWidget`
        '''
        rootWidget = self._rootOverlay(widget)
        found = False
        newOverlay = []
        for o in self._overlay:
            if o._widget == rootWidget:
                found = True
                newOverlay.append(o)
                continue
            if not found:
                newOverlay.append(o)
            else:
                self.rootLayout().removeWidget(o._widget)
        self._overlay = newOverlay
        if not found:
            self._removeOverlay()

    def _focusLastModal(self) -> None:
        '''
        Sets focus to the last modal overlay widget in the stack.

        This method is used internally to ensure modal overlays maintain focus
        when interaction is attempted with underlying widgets.
        '''
        if modal := self._getLastModal():
            modal._widget.setFocus()

    def _checkModalOverlay(self, widget: TTkWidget) -> bool:
        '''
        Checks if a widget is allowed to receive input given the current modal overlay state.

        :param widget: the widget to check for input permission
        :type widget: :py:class:`TTkWidget`

        :return: True if the widget can receive input, False if blocked by a modal overlay
        :rtype: bool
        '''
        #if not TTkHelper._overlay:
        #    # There are no Overlays
        #    return True

        if not (lastModal := self._getLastModal()):
            return True

        # if not TTkHelper._overlay[-1]._modal:
        #     # The last window is not modal
        #     return True
        if not (rootWidget := self._rootOverlay(widget)):
            # This widget is not overlay
            return False
        if rootWidget in [ o._widget for o in self._overlay[self._overlay.index(lastModal):]]:
            return True
        # if TTkHelper._overlay[-1]._widget == rootWidget:
        #     return True
        return False

    def _getLastModal(self) -> Optional[_TTkOverlay]:
        '''
        Returns the last modal overlay in the stack.

        :return: the last modal overlay wrapper, or None if no modal overlays exist
        :rtype: :py:class:`_TTkOverlay` or None
        '''
        modal = None
        for o in self._overlay:
            if o._modal:
                modal = o
        return modal

    def _isOverlay(self, widget: Optional[TTkWidget]) -> bool:
        '''
        Checks if a widget is part of the overlay hierarchy.

        :param widget: the widget to check
        :type widget: :py:class:`TTkWidget` or None

        :return: True if the widget is contained in any overlay, False otherwise
        :rtype: bool
        '''
        return self._rootOverlay(widget) is not None

    def _rootOverlay(self, widget: Optional[TTkWidget]) -> Optional[TTkWidget]:
        '''
        Finds the root overlay widget that contains the specified widget.

        Traverses the widget's parent hierarchy to find which overlay (if any)
        contains it as a child.

        :param widget: the widget to search for in the overlay hierarchy
        :type widget: :py:class:`TTkWidget` or None

        :return: the root overlay widget containing the specified widget, or None if not in any overlay
        :rtype: :py:class:`TTkWidget` or None
        '''
        if not widget:
            return None
        if not self._overlay:
            return None
        overlayWidgets = [o._widget for o in self._overlay]
        while widget is not None:
            if widget in overlayWidgets:
                return widget
            widget = widget.parentWidget()
        return None

    def keyEvent(self, evt:TTkKeyEvent) -> bool:
        '''
        Handles keyboard events for focus navigation.

        Implements focus cycling behavior when Tab/Shift+Tab or arrow keys are pressed
        and no child widget consumes the event. When the last focusable widget is reached,
        focus cycles back to the first widget (and vice versa).

        :param evt: the keyboard event
        :type evt: :py:class:`TTkKeyEvent`

        :return: True if the event was handled, False otherwise
        :rtype: bool
        '''
        if self._handleOverlay(evt=evt):
            return True
        if super().keyEvent(evt=evt):
            return True

        # If this is reached after a tab focus event, it means that either
        # no focus widgets are defined
        # or the last/first focus is reached - the focus need to go to start from the opposite side
        return self._loopFocus(evt=evt, container=self)
