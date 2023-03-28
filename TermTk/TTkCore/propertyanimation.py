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

import time, math

from TermTk.TTkCore.signal import pyTTkSignal, pyTTkSlot
from TermTk.TTkCore.helper import TTkHelper

class TTkEasingCurve():
    Linear       = 0
    InQuad       = 1
    OutQuad      = 2
    InOutQuad    = 3
    OutInQuad    = 4
    InCubic      = 5
    OutCubic     = 6
    InOutCubic   = 7
    OutInCubic   = 8
    InQuart      = 9
    OutQuart     = 10
    InOutQuart   = 11
    OutInQuart   = 12
    InQuint      = 13
    OutQuint     = 14
    InOutQuint   = 15
    OutInQuint   = 16
    InSine       = 17
    OutSine      = 18
    InOutSine    = 19
    OutInSine    = 20
    InExpo       = 21
    OutExpo      = 22
    InOutExpo    = 23
    OutInExpo    = 24
    InCirc       = 25
    OutCirc      = 26
    InOutCirc    = 27
    OutInCirc    = 28
    InElastic    = 29
    OutElastic   = 30
    InOutElastic = 31
    OutInElastic = 32
    InBack       = 33
    OutBack      = 34
    InOutBack    = 35
    OutInBack    = 36
    InBounce     = 37
    OutBounce    = 38
    InOutBounce  = 39
    OutInBounce  = 40
    # BezierSpline = 45
    # TCBSpline    = 46
    # Custom       = 47

class TTkPropertyAnimation():
    __slots__ = ('_target', '_propertyName', '_parent',
                 '_duration', '_startValue', '_endValue',
                 '_easingCurve', '_baseTime')
    def __init__(self, target, propertyName, parent=None):
        self._target = target
        self._propertyName = propertyName
        self._parent = parent
        self._duration = 0
        self._baseTime = 0
        self._startValue = None
        self._endValue = None

    def setDuration(self, duration):
        self._duration = duration

    def setStartValue(self, startValue):
        self._startValue = startValue

    def setEndValue(self, endValue):
        self._endValue = endValue

    def setEasingCurve(self, easingCurve):
        self._easingCurve = easingCurve

    @pyTTkSlot()
    def _refreshAnimation(self):
        diff = time.time() - self._baseTime
        if diff >= self._duration:
            TTkHelper._rootWidget.paintExecuted.disconnect(self._refreshAnimation)
            if type(self._endValue) in (list,tuple):
                getattr(self._target,self._propertyName)(*self._endValue)
            else:
                getattr(self._target,self._propertyName)(self._endValue)
        else:
            def _processLinear(_s,_e,_v):
                return int(_e*_v+_s*(1-_v))
            def _processQuad(_s,_e,_v):
                return _processLinear(_s,_e,_v*_v)
            def _processInQuad(_s,_e,_v):
                return _processLinear(_s,_e,math.sqrt(math.sqrt(_v)))
            _process = _processInQuad
            v = diff/self._duration
            if type(self._startValue) in (list,tuple):
                newVal = [_process(s,e,v) for (s,e) in zip(self._startValue,self._endValue)]
                getattr(self._target,self._propertyName)(*newVal)
            else:
                newVal = _process(self._startValue,self._endValue,v)
                getattr(self._target,self._propertyName)(newVal)

    @pyTTkSlot()
    def start(self):
        self._baseTime = time.time()
        if TTkHelper._rootWidget:
            TTkHelper._rootWidget.paintExecuted.connect(self._refreshAnimation)
            self._refreshAnimation()
