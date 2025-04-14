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

__all__ = ['TTkMouseEvent']

from TermTk.TTkCore.constant import TTkK

class TTkMouseEvent:
    ''' Mouse Events

    :Demo: `test.input.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tests/test.input.py>`_

    .. py:attribute:: x
        :type: int

        The horizontal (x) position relative to the widget

    .. py:attribute:: y
        :type: int

        The vertical (y) position relative to the widget

    .. py:attribute:: key
        :type: MouseKey

        The :py:class:`TTkConstant.MouseKey` reported in this event (i.e. :py:class:`~TermTk.TTkCore.constant.TTkConstant.MouseKey.LeftButton`)

    .. py:attribute:: mod
        :type: KeyModifier

        The :py:class:`TTkConstant.KeyModifier` used, default :py:class:`~TermTk.TTkCore.constant.TTkConstant.KeyModifier.NoModifier`

    .. py:attribute:: evt
        :type: MouseEvent

        The :py:class:`TTkConstant.MouseEvent` reported in this event (i.e. :py:class:`~TermTk.TTkCore.constant.TTkConstant.MouseKey.Press`)

    .. py:attribute:: tap
        :type: int

        The number of tap (keypressed) reported in this event, (i.e. a **doubleclick** is reported as tap=2)

    .. py:attribute:: raw
        :type: str

        The terminal "raw" information reporting this event (Do not use it unless you know what you are looking for)

    '''
    # Keys
    NoButton      = TTkK.NoButton     # The button state does not refer to any button (see QMouseEvent::button()).
    AllButtons    = TTkK.AllButtons   # This value corresponds to a mask of all possible mouse buttons. Use to set the 'acceptedButtons' property of a MouseArea to accept ALL mouse buttons.
    LeftButton    = TTkK.LeftButton   # The left button is pressed, or an event refers to the left button. (The left button may be the right button on left-handed mice.)
    RightButton   = TTkK.RightButton  # The right button.
    MidButton     = TTkK.MidButton    # The middle button.
    MiddleButton  = TTkK.MiddleButton # The middle button.
    Wheel         = TTkK.Wheel

    # Events
    NoEvent = TTkK.NoEvent
    Press   = TTkK.Press
    Release = TTkK.Release
    Drag    = TTkK.Drag
    Move    = TTkK.Move
    Up      = TTkK.WHEEL_Up
    Down    = TTkK.WHEEL_Down
    Left    = TTkK.WHEEL_Left
    Right   = TTkK.WHEEL_Right

    __slots__ = ('x', 'y', 'key', 'evt', 'mod', 'tap', 'raw')
    x: int
    y: int
    key: int
    evt: int
    mod: int
    tap: int
    raw: str
    def __init__(self, x: int, y: int, key: int, evt: int, mod: int, tap: int, raw: str):
        self.x = x
        self.y = y
        self.key = key
        self.evt = evt
        self.mod = mod
        self.raw = raw
        self.tap = tap

    def pos(self) -> tuple[int,int]:
        '''
        Returns the position of the mouse cursor relative to the current widget.

        :return: the position.
        :rtype:  tuple[int,int]
        '''
        return (self.x, self.y)

    def clone(self, pos=None, evt=None):
        x,y = pos or (self.x, self.y)
        evt = evt or self.evt
        return TTkMouseEvent(x, y, self.key, evt, self.mod, self.tap, self.raw)

    def key2str(self):
        return {
            TTkMouseEvent.NoButton     : "NoButton",
            TTkMouseEvent.AllButtons   : "AllButtons",
            TTkMouseEvent.LeftButton   : "LeftButton",
            TTkMouseEvent.RightButton  : "RightButton",
            TTkMouseEvent.MidButton    : "MidButton",
            TTkMouseEvent.MiddleButton : "MiddleButton",
            TTkMouseEvent.Wheel        : "Wheel",
        }.get(self.key, "Undefined")

    def evt2str(self):
        return {
            TTkMouseEvent.NoEvent : "NoEvent",
            TTkMouseEvent.Press   : "Press",
            TTkMouseEvent.Release : "Release",
            TTkMouseEvent.Drag    : "Drag",
            TTkMouseEvent.Move    : "Move",
            TTkMouseEvent.Up      : "Up",
            TTkMouseEvent.Down    : "Down",
            TTkMouseEvent.Left    : "Left",
            TTkMouseEvent.Right   : "Right",
        }.get(self.evt, "Undefined")

    def mod2str(self):
        if self.mod == TTkK.NoModifier         : return "NoModifier"
        ret = []
        if self.mod & TTkK.ShiftModifier       : ret.append("Shift")
        if self.mod & TTkK.ControlModifier     : ret.append("Control")
        if self.mod & TTkK.AltModifier         : ret.append("Alt")
        if self.mod & TTkK.MetaModifier        : ret.append("Meta")
        if self.mod & TTkK.KeypadModifier      : ret.append("Keypad")
        if self.mod & TTkK.GroupSwitchModifier : ret.append("GroupSwitch")
        if ret: return ",".join(ret)
        return "NONE!!!"

    def __str__(self):
        return f"MouseEvent ({self.x},{self.y}) {self.key2str()} {self.evt2str()} {self.mod2str()} tap:{self.tap} - {self.raw}"
