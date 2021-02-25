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

class TTkConstant:
    MOUSE_EVENT  = 0x01
    KEY_EVENT    = 0x02
    SCREEN_EVENT = 0x04
    QUIT_EVENT   = 0x08
    TIME_EVENT   = 0x10

    HORIZONTAL = 0x01
    VERTICAL   = 0x02

    # Keys
    NoButton      = 0x00000000    # The button state does not refer to any button (see QMouseEvent::button()).
    AllButtons    = 0x07ffffff    # This value corresponds to a mask of all possible mouse buttons. Use to set the 'acceptedButtons' property of a MouseArea to accept ALL mouse buttons.
    LeftButton    = 0x00000001    # The left button is pressed, or an event refers to the left button. (The left button may be the right button on left-handed mice.)
    RightButton   = 0x00000002    # The right button.
    MidButton     = 0x00000004    # The middle button.
    MiddleButton  = MidButton     # The middle button.
    Wheel         = 0x00000008

    # Events
    NoEvent = 0x00000000
    Press   = 0x00010000
    Release = 0x00020000
    Drag    = 0x00040000
    Move    = 0x00080000
    WHEEL_Up   = 0x00100000 # Wheel Up
    WHEEL_Down = 0x00200000 # Wheel Down

    # Alignment
    NONE   = 0x0000
    LEFT_ALIGN   = 0x0001
    RIGHT_ALIGN  = 0x0002
    CENTER_ALIGN = 0x0003
    JUSTIFY      = 0x0004


# Alias to TTkConstant
class TTkK(TTkConstant): pass