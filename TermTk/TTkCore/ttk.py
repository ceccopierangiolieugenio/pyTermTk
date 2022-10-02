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

import os
import signal
import time
import queue
import threading
import platform

from TermTk.TTkCore.TTkTerm.input import TTkInput
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkCore.TTkTerm.term import TTkTerm
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg, TTkGlbl
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.timer import TTkTimer
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkTheme.theme import TTkTheme
from TermTk.TTkWidgets.widget import TTkWidget

class TTk(TTkWidget):
    class _mouseCursor(TTkWidget):
        __slots__ = ('_cursor','_color')
        def __init__(self, input):
            super().__init__()
            self._name = 'mouseCursor'
            self._cursor = '✠'
            self._color = TTkColor.RST
            self.resize(1,1)
            input.inputEvent.connect(self._mouseInput)
        @pyTTkSlot(TTkKeyEvent, TTkMouseEvent)
        def _mouseInput(self, kevt, mevt):
            if mevt is not None:
                self._cursor = '✠'
                self._color = TTkColor.RST
                if mevt.key == TTkK.Wheel:
                    if mevt.evt == TTkK.WHEEL_Up:
                        self._cursor = '⇑'
                    else:
                        self._cursor = '⇓'
                elif mevt.evt == TTkK.Press:
                    self._color = TTkColor.bg('#FFFF00') + TTkColor.fg('#000000')
                elif mevt.evt == TTkK.Drag:
                    self._color = TTkColor.bg('#666600') + TTkColor.fg('#FFFF00')
                # elif mevt.evt == TTkK.Release:
                #     self._color = TTkColor.bg('#006600') + TTkColor.fg('#00FFFF')
                self.move(mevt.x, mevt.y)
                self.update()
                self.raiseWidget()
        def paintEvent(self):
            self._canvas.drawChar((0,0), self._cursor, self._color)
            #self._canvas.drawChar((0,0),'✜')

    __slots__ = (
        '_input',
        '_title',
        '_showMouseCursor',
        '_sigmask',
        '_drawMutex',
        '_lastMultiTap')

    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTk' )
        self._input = TTkInput()
        self._input.inputEvent.connect(self._processInput)
        self._title = kwargs.get('title','TermTk')
        self._sigmask = kwargs.get('sigmask', TTkK.NONE)
        self._showMouseCursor = os.environ.get("TTK_MOUSE",kwargs.get('mouseCursor', False))
        self._drawMutex = threading.Lock()
        self.setFocusPolicy(TTkK.ClickFocus)
        self.hide()
        w,h = TTkTerm.getTerminalSize()
        self.setGeometry(0,0,w,h)

        TTkCfg.theme = TTkTheme()
        TTkHelper.registerRootWidget(self)

    frame = 0
    time = time.time()
    def _fps(self):
        curtime = time.time()
        self.frame+=1
        delta = curtime - self.time
        if delta > 5:
            TTkLog.debug(f"fps: {int(self.frame/delta)}")
            self.frame = 0
            self.time  = curtime

    def mainloop(self):
        try:
            '''Enters the main event loop and waits until :meth:`~quit` is called or the main widget is destroyed.'''
            TTkLog.debug( "" )
            TTkLog.debug( "         ████████╗            ████████╗    " )
            TTkLog.debug( "         ╚══██╔══╝            ╚══██╔══╝    " )
            TTkLog.debug( "            ██║  ▄▄  ▄ ▄▄ ▄▄▖▄▖  ██║ █ ▗▖  " )
            TTkLog.debug( "    ▞▀▚ ▖▗  ██║ █▄▄█ █▀▘  █ █ █  ██║ █▟▘   " )
            TTkLog.debug( "    ▙▄▞▐▄▟  ██║ ▀▄▄▖ █    █ ▝ █  ██║ █ ▀▄  " )
            TTkLog.debug( "    ▌    ▐  ╚═╝                  ╚═╝       " )
            TTkLog.debug( "      ▚▄▄▘                                 " )
            TTkLog.debug( "" )
            TTkLog.debug(f"  Version: {TTkCfg.version}" )
            TTkLog.debug( "" )
            TTkLog.debug( "Starting Main Loop..." )

            # Register events
            signal.signal(signal.SIGTSTP, self._SIGSTOP) # Ctrl-Z
            signal.signal(signal.SIGCONT, self._SIGCONT) # Resume
            signal.signal(signal.SIGINT,  self._SIGINT)  # Ctrl-C

            TTkLog.debug("Signal Event Registered")

            TTkTerm.registerResizeCb(self._win_resize_cb)

            self._timer = TTkTimer()
            self._timer.timeout.connect(self._time_event)
            self._timer.start(0.1)
            self.show()

            # Keep track of the multiTap to avoid the extra key release
            self._lastMultiTap = False
            TTkTerm.init(title=self._title, sigmask=self._sigmask)

            if self._showMouseCursor:
                TTkTerm.push(TTkTerm.Mouse.DIRECT_ON)
                m = TTk._mouseCursor(self._input)
                self.rootLayout().addWidget(m)

            self._mainLoop()
        finally:
            if platform.system() != 'Emscripten':
                self.quit()
                TTkTerm.exit()

    def _mainLoop(self):
        if platform.system() == 'Emscripten':
            return
        self._input.start()

    @pyTTkSlot(TTkKeyEvent, TTkMouseEvent)
    def _processInput(self, kevt, mevt):
        self._drawMutex.acquire()
        if kevt is not None:
            self._key_event(kevt)
        if mevt is not None:
            self._mouse_event(mevt)
        self._drawMutex.release()

    def _mouse_event(self, mevt):
        # Upload the global mouse position
        # Mainly used by the drag pixmap display
        TTkHelper.setMousePos((mevt.x,mevt.y))

        # Avoid to broadcast a key release after a multitap event
        if mevt.evt == TTkK.Release and self._lastMultiTap: return
        self._lastMultiTap = mevt.tap > 1

        if ( TTkHelper.isDnD() and
             mevt.evt != TTkK.Drag   and
             mevt.evt != TTkK.Release ):
            # Clean Drag Drop status for any event that is not
            # Mouse Drag, Key Release
            TTkHelper.dndEnd()

        # Mouse Events forwarded straight to the Focus widget:
        #  - Drag
        #  - Move
        #  - Release
        focusWidget = TTkHelper.getFocus()
        if ( focusWidget is not None and
             mevt.evt != TTkK.Press  and
             mevt.key != TTkK.Wheel  and
             not TTkHelper.isDnD()   ) :
            x,y = TTkHelper.absPos(focusWidget)
            nmevt = mevt.clone(pos=(mevt.x-x, mevt.y-y))
            focusWidget.mouseEvent(nmevt)
        else:
            # Sometimes the release event is not retrieved
            if ( focusWidget and
                 focusWidget._pendingMouseRelease and
                 not TTkHelper.isDnD() ):
                focusWidget.mouseEvent(mevt.clone(evt=TTkK.Release))
                focusWidget._pendingMouseRelease = False
            # Adding this Crappy logic to handle a corner case in the drop routine
            # where the mouse is leaving any widget able to handle the drop event
            if not self.mouseEvent(mevt):
                if dndw := TTkHelper.dndWidget():
                    dndw.dragLeaveEvent(TTkHelper.dndGetDrag().getDragLeaveEvent(mevt))
                    TTkHelper.dndEnter(None)
                if mevt.evt == TTkK.Press and focusWidget:
                    focusWidget.clearFocus()

        # Clean the Drag and Drop in case of mouse release
        if mevt.evt == TTkK.Release:
            TTkHelper.dndEnd()

    def _key_event(self, kevt):
        keyHandled = False
        # TTkLog.debug(f"Key: {kevt}")
        focusWidget = TTkHelper.getFocus()
        # TTkLog.debug(f"{focusWidget}")
        if focusWidget is not None:
            TTkHelper.execShortcut(kevt.key,focusWidget)
            keyHandled = focusWidget.keyEvent(kevt)
        else:
            TTkHelper.execShortcut(kevt.key)
        # Handle Next Focus Key Binding
        if not keyHandled and \
           ((kevt.key == TTkK.Key_Tab and kevt.mod == TTkK.NoModifier) or
           ( kevt.key == TTkK.Key_Right or kevt.key == TTkK.Key_Down)):
                TTkHelper.nextFocus(focusWidget if focusWidget else self)
        # Handle Prev Focus Key Binding
        if not keyHandled and \
           ((kevt.key == TTkK.Key_Tab and kevt.mod == TTkK.ShiftModifier) or
           ( kevt.key == TTkK.Key_Left or kevt.key == TTkK.Key_Up)):
                TTkHelper.prevFocus(focusWidget if focusWidget else self)

    def _time_event(self):
        w,h = TTkTerm.getTerminalSize()
        self._drawMutex.acquire()
        self.setGeometry(0,0,w,h)
        self._fps()
        TTkHelper.paintAll()
        self._drawMutex.release()
        self._timer.start(1/TTkCfg.maxFps)

    def _win_resize_cb(self, width, height):
        TTkGlbl.term_w = int(width)
        TTkGlbl.term_h = int(height)
        self._drawMutex.acquire()
        self.setGeometry(0,0,TTkGlbl.term_w,TTkGlbl.term_h)
        TTkHelper.rePaintAll()
        self._drawMutex.release()
        TTkLog.info(f"Resize: w:{TTkGlbl.term_w}, h:{TTkGlbl.term_h}")


    def quit(self):
        '''Tells the application to exit with a return code.'''
        self._input.inputEvent.clear()
        TTkTimer.quitAll()
        self._input.close()

    def _SIGSTOP(self, signum, frame):
        """Reset terminal settings and stop background input read before putting to sleep"""
        TTkLog.debug("Captured SIGSTOP <CTRL-z>")
        TTkTerm.stop()
        self._input.stop()
        # TODO: stop the threads
        os.kill(os.getpid(), signal.SIGSTOP)

    def _SIGCONT(self, signum, frame):
        """Set terminal settings and restart background input read"""
        TTkLog.debug("Captured SIGCONT 'fg/bg'")
        TTkTerm.cont()
        self._input.cont()
        TTkHelper.rePaintAll()
        # TODO: Restart threads
        # TODO: Redraw the screen

    def _SIGINT(self, signum, frame):
        TTkLog.debug("Captured SIGINT <CTRL-C>")
        # Deregister the handler
        # so CTRL-C can be redirected to the default handler if the app does not exit
        signal.signal(signal.SIGINT,  signal.SIG_DFL)
        self.quit()
