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

__all__ = ['TTkTerminal']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea, _ForwardData
from TermTk.TTkWidgets.TTkTerminal.terminalview import TTkTerminalView

class TTkTerminal(TTkAbstractScrollArea):
    __doc__ = '''
    :py:class:`TTkTerminal` is a container widget which place :py:class:`TTkTerminalView` in a scrolling area with on-demand scroll bars.

    ''' + TTkTerminalView.__doc__

    _ttk_forward = _ForwardData(
        forwardClass=TTkTerminalView ,
        instance="self._terminalView",
        signals=[# Forwarded Signals From TTkTreeWidget
            'bell', 'titleChanged', 'terminalClosed', 'textSelected',
            'termData', 'termResized'],
        methods=[# Forwarded Methods From TTkTreeWidget
            'termWrite', 'termSize']
    )

    __slots__ = ('_terminalView')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        kwargs.pop('parent',None)
        kwargs.pop('visible',None)
        self._terminalView = TTkTerminalView(**kwargs)
        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._terminalView)

    def close(self):
        self._terminalView.close()
        return super().close()

    #--FORWARD-AUTOGEN-START--#
    @property
    def bell(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTerminalView.bell`

        This signal is emitted when the `bell <https://en.wikipedia.org/wiki/Bell_character>`__ is received.
        '''
        return self._terminalView.bell
    @property
    def titleChanged(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTerminalView.titleChanged`

        This signal is emitted when the terminal title change through OSC "ESC ]0;"
        
        :param title: the new title
        :type title: str
        '''
        return self._terminalView.titleChanged
    @property
    def terminalClosed(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTerminalView.terminalClosed`

        This signal is emitted when the terminal is closed.
        '''
        return self._terminalView.terminalClosed
    @property
    def textSelected(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTerminalView.textSelected`

        This signal is emitted when a text is selected.
        
        :param text: the selected text
        :type text: :py:class:`ttkString`
        '''
        return self._terminalView.textSelected
    @property
    def termData(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTerminalView.termData`

        This signal is emitted when data event fires.
        
        This happens for example when the user types or pastes into the terminal.
        The event value is whatever 'str' results, in a typical setup,
        this should be passed on to the backing pty.
        
        This signal is used in :py:class:`TTkTerminalHelper` through :py:meth:`TTkTerminalHelper.attachTTkTerminal`
        to frward all the terminal events to the pty interface.
        
        :param data: the event data
        :type data: str
        '''
        return self._terminalView.termData
    @property
    def termResized(self) -> pyTTkSignal:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTerminalView.termResized`

        This signal is emitted when the terminal is resized.
        
        :param size: the new size [width, height] of the terminal
        :type size: (int,int)
        '''
        return self._terminalView.termResized
    def termWrite(self, data:str) -> None:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTerminalView.termWrite`

        Write data to the terminal.

        :params data: the data to write
        :type data: str
        '''
        return self._terminalView.termWrite(data=data)
    def termSize(self) -> tuple[int,int]:
        '''
        .. seealso:: this method is forwarded to :py:meth:`TTkTerminalView.termSize`

        This property holds the size of the terminal

        :return: a tuple of 2 integers (width, height)
        :rtype: tuple
        '''
        return self._terminalView.termSize()
    #--FORWARD-AUTOGEN-END--#