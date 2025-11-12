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

__all__ = ['TTkToolTip']

from typing import List

# from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.log       import TTkLog
from TermTk.TTkCore.canvas    import TTkCanvas
from TermTk.TTkCore.cfg       import TTkCfg
from TermTk.TTkCore.color     import TTkColor
from TermTk.TTkCore.timer     import TTkTimer
from TermTk.TTkCore.helper    import TTkHelper
from TermTk.TTkCore.string    import TTkString, TTkStringType
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkCore.signal    import pyTTkSlot

class _TTkToolTipDisplayWidget(TTkWidget):
    ''' _TTkToolTipDisplayWidget:

    Internal widget that renders tooltip content in a bordered box.

    ::

        ╭────────────────╮
        │ Tooltip text   │
        │ Multiple lines │
        ╰────────────────╯

    This widget is automatically sized based on tooltip content
    and uses a rounded border style for visual distinction.
    '''
    __slots__ = ('_tooltip_list', '_x', '_y')
    _tooltip_list:List[TTkString]
    def __init__(self, *,
                 toolTip:TTkStringType="",
                 **kwargs) -> None:
        ''' Initialize the tooltip display widget

        :param toolTip: The tooltip text to display (supports multiline with \\n)
        :type toolTip: :py:class:`TTkString`, optional
        '''
        super().__init__(**kwargs)
        if isinstance(toolTip,TTkString):
            self._tooltip_list = toolTip.split('\n')
        else:
            self._tooltip_list = TTkString(toolTip).split('\n')
        w = 2+max([s.termWidth() for s in self._tooltip_list])
        h = 2+len(self._tooltip_list)
        self.resize(w,h)

    def mouseEvent(self, evt: TTkMouseEvent) -> bool:
        ''' Handle mouse events (always returns False to allow click-through)

        :param evt: The mouse event
        :type evt: :py:class:`TTkMouseEvent`

        :return: False to propagate event
        :rtype: bool
        '''
        return False

    def paintEvent(self, canvas: TTkCanvas) -> None:
        ''' Paint the tooltip with rounded border and text content

        :param canvas: The canvas to draw on
        :type canvas: :py:class:`TTkCanvas`
        '''
        w,h = self.size()
        borderColor = TTkColor.fg("#888888")
        canvas.drawBox(pos=(0,0),size=(w,h), color=borderColor)
        canvas.drawChar(pos=(0,  0),  char='╭', color=borderColor)
        canvas.drawChar(pos=(w-1,0),  char='╮', color=borderColor)
        canvas.drawChar(pos=(w-1,h-1),char='╯', color=borderColor)
        canvas.drawChar(pos=(0,  h-1),char='╰', color=borderColor)
        for i,s in enumerate(self._tooltip_list,1):
            canvas.drawTTkString(pos=(1,i), text=s)

class TTkToolTip():
    ''' TTkToolTip:

    Global tooltip manager for delayed display of help text.

    This class manages tooltip behavior across the application, including:

    - Delayed tooltip display after hover timeout (configurable via :py:class:`TTkToolTip._toolTipTime`)
    - Automatic positioning and sizing
    - Support for multiline tooltips

    .. note::
        This is a singleton-like class using class methods. Do not instantiate it directly.

    Usage:

    .. code-block:: python

        # Widgets set tooltips via their toolTip property
        button = TTkButton(text="Click me", toolTip="This button does something")

        # The tooltip system automatically handles display timing and positioning
    '''

    _toolTipTime:int = 1
    '''Timeout in seconds'''

    toolTipTimer:TTkTimer = TTkTimer(name='ToolTip')
    '''Internal timer for delayed tooltip display'''

    toolTip:TTkStringType = ''
    '''Current tooltip text to be displayed'''

    @pyTTkSlot()
    @staticmethod
    def _toolTipShow() -> None:
        ''' Internal slot that creates and displays the tooltip widget

        This method is called by the timer after the configured delay period.
        '''
        # TTkLog.debug(f"TT:{TTkToolTip.toolTip}")
        TTkHelper.toolTipShow(_TTkToolTipDisplayWidget(toolTip=TTkToolTip.toolTip))

    @staticmethod
    def trigger(toolTip:TTkStringType) -> None:
        ''' Trigger a tooltip to be displayed after the configured delay

        :param toolTip: The tooltip text to display (supports \\n for multiline)
        :type toolTip: :py:class:`TTkString`
        '''
        # TTkToolTip.toolTipTimer.stop()
        TTkToolTip.toolTip = toolTip
        TTkToolTip.toolTipTimer.start(TTkToolTip._toolTipTime)

    @staticmethod
    def reset() -> None:
        ''' Cancel any pending tooltip display

        This is typically called when the mouse leaves a widget
        or when the tooltip should be hidden.
        '''
        TTkToolTip.toolTipTimer.stop()

TTkToolTip.toolTipTimer.timeout.connect(TTkToolTip._toolTipShow)
TTkHelper.toolTipTrigger = TTkToolTip.trigger
TTkHelper.toolTipReset = TTkToolTip.reset