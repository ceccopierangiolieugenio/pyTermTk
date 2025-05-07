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

__all__ = ['TTk']

import os
import signal
import time
import queue
import threading
import platform

from TermTk.TTkCore.drivers import TTkSignalDriver
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
from TermTk.TTkCore.shortcut import TTkShortcut
from TermTk.TTkWidgets.about import TTkAbout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.container import TTkContainer

class _MouseCursor():
    __slots__ = ('_cursor','_color', '_pos', 'updated')
    def __init__(self):
        self.updated = pyTTkSignal()
        self._pos = (0,0)
        self._cursor = '✠'
        self._color = TTkColor.RST
        TTkInput.inputEvent.connect(self._mouseInput)

    @pyTTkSlot(TTkKeyEvent, TTkMouseEvent)
    def _mouseInput(self, _, mevt):
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
            self._pos = (mevt.x, mevt.y)
            self.updated.emit()

class TTk(TTkContainer):


    __slots__ = (
        '_termMouse', '_termDirectMouse',
        '_title',
        '_showMouseCursor', '_mouseCursor',
        '_sigmask', '_timer',
        '_drawMutex',
        '_paintEvent',
        '_lastMultiTap',
        'paintExecuted')

    def __init__(self, *,
                 title:str='TermTk',
                 sigmask:TTkTerm.Sigmask=TTkK.NONE,
                 mouseTrack:bool=False,
                 mouseCursor:bool=False,
                 **kwargs) -> None:
        # If the "TERMTK_FILE_LOG" env variable is defined
        # logs are saved in the file identified by this variable
        # i.e.
        #      TERMTK_FILE_LOG=session.log   python3   demo/demo.py
        if ('TERMTK_FILE_LOG' in os.environ and (_logFile := os.environ['TERMTK_FILE_LOG'])):
            TTkLog.use_default_file_logging(_logFile)

        self._timer = None
        self._title = title
        self._sigmask = sigmask
        self.paintExecuted = pyTTkSignal()
        self._termMouse = True
        self._termDirectMouse = mouseTrack
        self._mouseCursor = None
        self._showMouseCursor = os.environ.get("TERMTK_MOUSE",mouseCursor)
        super().__init__(**kwargs)
        TTkInput.inputEvent.connect(self._processInput)
        TTkInput.pasteEvent.connect(self._processPaste)
        TTkSignalDriver.sigStop.connect(self._SIGSTOP)
        TTkSignalDriver.sigCont.connect(self._SIGCONT)
        TTkSignalDriver.sigInt.connect( self._SIGINT)
        self._drawMutex = threading.Lock()
        self._paintEvent = threading.Event()
        self._paintEvent.set()
        self.setFocusPolicy(TTkK.ClickFocus)
        self.hide()
        w,h = TTkTerm.getTerminalSize()
        self.setGeometry(0,0,w,h)

        if 'TERMTK_NEWRENDERER' in os.environ:
            TTkCfg.doubleBuffer = False
            TTkCfg.doubleBufferNew = True

        if os.environ.get("TERMTK_GPM",False):
            self._showMouseCursor = True

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
            TTkLog.debug(f"screen = ({TTkTerm.getTerminalSize()})")

            # Register events
            TTkSignalDriver.init()

            TTkLog.debug("Signal Event Registered")

            TTkTerm.registerResizeCb(self._win_resize_cb)

            self._timer = TTkTimer()
            self._timer.timeout.connect(self._time_event)
            self._timer.start(0.1)
            self.show()

            # Keep track of the multiTap to avoid the extra key release
            self._lastMultiTap = False
            TTkInput.init(
                mouse=self._termMouse,
                directMouse=self._termDirectMouse)
            TTkTerm.init(
                title=self._title,
                sigmask=self._sigmask)

            if self._showMouseCursor:
                self._mouseCursor = _MouseCursor()
                self._mouseCursor.updated.connect(self.update)
                self.paintChildCanvas = self._mouseCursorPaintChildCanvas

            self._mainLoop()
        finally:
            if platform.system() != 'Emscripten':
                TTkHelper.quitEvent.emit()
                if self._timer:
                    self._timer.timeout.disconnect(self._time_event)
                    self._timer.quit()
                    self._paintEvent.set()
                    # self._timer.join()
                TTkSignalDriver.exit()
                self.quit()
                TTkTerm.exit()

    def _mouseCursorPaintChildCanvas(self) -> None:
        super().paintChildCanvas()
        ch = self._mouseCursor._cursor
        pos = self._mouseCursor._pos
        color = self._mouseCursor._color
        self.getCanvas().drawChar(char=ch, pos=pos, color=color)

    def _mainLoop(self):
        if platform.system() == 'Emscripten':
            return
        TTkInput.start()

    @pyTTkSlot(str)
    def _processPaste(self, txt:str):
        if focusWidget := TTkHelper.getFocus():
            while focusWidget and not focusWidget.pasteEvent(txt):
                focusWidget = focusWidget.parentWidget()

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
        TTkWidget._mouseOverProcessed = False

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
        #  - Release
        focusWidget = TTkHelper.getFocus()
        if ( focusWidget is not None and
             ( mevt.evt == TTkK.Drag or
               mevt.evt == TTkK.Release ) and
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
                    TTkHelper.focusLastModal()

        # Clean the Drag and Drop in case of mouse release
        if mevt.evt == TTkK.Release:
            TTkHelper.dndEnd()

    def _key_event(self, kevt):
        keyHandled = False
        # TTkLog.debug(f"Key: {kevt}")
        focusWidget = TTkHelper.getFocus()
        # TTkLog.debug(f"{focusWidget}")
        if focusWidget is not None:
            keyHandled = focusWidget.keyEvent(kevt)
        if not keyHandled:
            TTkShortcut.processKey(kevt, focusWidget)
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
        # Event.{wait and clear} should be atomic,
        # BUTt: ( y )
        #   if an update event (set) happen in between the wait and clear
        #      the widget is still processed in the current paint routine
        #   if an update event (set) happen after the wait and clear
        #      the widget is processed in the current paint routine
        #      an extra paint routine is triggered which return immediately due to
        #      the empty list of widgets to be processed - Not a big deal
        #   if an update event (set) happen after the wait and clear and the paintAll Routine
        #      well, it works as it is supposed to be
        self._paintEvent.wait()
        self._paintEvent.clear()

        w,h = TTkTerm.getTerminalSize()
        self._drawMutex.acquire()
        self.setGeometry(0,0,w,h)
        self._fps()
        TTkHelper.paintAll()
        self.paintExecuted.emit()
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

    @pyTTkSlot()
    def quit(self):
        '''quit TermTk

        .. warning::
            Method Deprecated,

            use :py:class:`TTkHelper` -> :py:meth:`TTkHelper.quit` instead

            i.e.

            .. code:: python

                buttonQuit = TTkButton(text="QUIT",border=True)
                buttonQuit.clicked.connect(TTkHelper.quit)
        '''
        TTkHelper.quit()

    @pyTTkSlot()
    def _quit(self):
        '''Tells the application to exit with a return code.'''
        if self._timer:
            self._timer.timeout.disconnect(self._time_event)
        TTkInput.inputEvent.clear()
        TTkInput.close()

    @pyTTkSlot()
    def _SIGSTOP(self):
        """Reset terminal settings and stop background input read before putting to sleep"""
        TTkLog.debug("Captured SIGSTOP <CTRL-z>")
        TTkTerm.stop()
        TTkInput.stop()
        # TODO: stop the threads
        os.kill(os.getpid(), signal.SIGSTOP)

    @pyTTkSlot()
    def _SIGCONT(self):
        """Set terminal settings and restart background input read"""
        TTkLog.debug("Captured SIGCONT 'fg/bg'")
        TTkTerm.cont()
        TTkInput.cont()
        TTkHelper.rePaintAll()
        # TODO: Restart threads
        # TODO: Redraw the screen

    @pyTTkSlot()
    def _SIGINT(self):
        # If the "TERMTK_STACKTRACE" env variable is defined
        # a stacktrace file is generated once CTRL+C is pressed
        # i.e.
        #      TERMTK_STACKTRACE=stacktracetxt   python3   demo/demo.py
        if ('TERMTK_STACKTRACE' in os.environ and (_stacktraceFile := os.environ['TERMTK_STACKTRACE'])):
            with open(_stacktraceFile,'w') as f:
                import faulthandler
                faulthandler.dump_traceback(f)

        TTkLog.debug("Captured SIGINT <CTRL-C>")
        # Deregister the handler
        # so CTRL-C can be redirected to the default handler if the app does not exit
        signal.signal(signal.SIGINT,  signal.SIG_DFL)
        TTkHelper.quit()

    def isVisibleAndParent(self):
        return self.isVisible()

    @pyTTkSlot()
    def aboutTermTk(self):
        '''
        Displays a simple message box about `pyTermTk <https://github.com/ceccopierangiolieugenio/pyTermTk>`__.
        The message includes the version number of TermTk being used by the application.

        This is useful for inclusion in the Help menu of an application, as shown in the Menus example.
        '''
        TTkHelper.overlay(None, TTkAbout(), 30,10)