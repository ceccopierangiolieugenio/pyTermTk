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
from inspect import getfullargspec
from types import LambdaType

from TermTk.TTkCore.log import TTkLog
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

    __slots__ = ('_easingFunc')
    def __init__(self, easingCurve=Linear):
        self._easingFunc = {self.Linear    : TTkEasingCurve._ecLinear,
         self.InQuad    : TTkEasingCurve._ecInQuad,
         self.OutQuad   : TTkEasingCurve._ecOutQuad,
         self.InOutQuad : TTkEasingCurve._ecInOutQuad,
         self.OutInQuad : TTkEasingCurve._ecOutInQuad,
         self.InCubic   : TTkEasingCurve._ecInCubic,
         self.OutCubic  : TTkEasingCurve._ecOutCubic,

         self.OutBounce : TTkEasingCurve._ecOutBounce,
         }.get(easingCurve,TTkEasingCurve._ecLinear)

    def process(self,a,b,v):
        v = self._easingFunc(v)
        return float(b)*v+float(a)*(1-v)

    # Formulas from https://easings.net
    @staticmethod
    def _ecLinear(v):
        return v
    @staticmethod
    def _ecInQuad(v):
        return v*v
    @staticmethod
    def _ecOutQuad(v):
        return 1-(1-v)*(1-v)
    @staticmethod
    def _ecInOutQuad(v):
        return v
    @staticmethod
    def _ecOutInQuad(v):
        return v
    @staticmethod
    def _ecInCubic(v):
        return v*v*v
    @staticmethod
    def _ecOutCubic(v):
        return 1-(1-v)*(1-v)*(1-v)
    @staticmethod
    def _ecOutBounce(x):
        n1 = 7.5625
        d1 = 2.75

        if x < 1 / d1: return n1 * x * x
        elif x < 2 / d1:
            x -= 1.5 / d1
            return n1 * x * x + 0.75
        elif x < 2.5 / d1:
            x -= 2.25 / d1
            return n1 * x * x + 0.9375
        else:
            x -= 2.625 / d1
            return n1 * x * x + 0.984375

class TTkPropertyAnimation():
    __slots__ = ('_target', '_propertyName', '_parent', '_cb', '_cast',
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
        self._easingCurve = TTkEasingCurve(TTkEasingCurve.Linear)

        if type(propertyName) == str:
            self._cb = getattr(self._target,self._propertyName)
        else:
            self._cb = propertyName

        def _cast():
            _spec = getfullargspec(self._cb)
            if isinstance(self._cb, LambdaType) and self._cb.__name__ == "<lambda>":
                _args = _spec.args
            else:
                _args = _spec.args[1:] if hasattr(self._cb, '__self__') else _spec.args
            _castList = [
                (lambda x:_spec.annotations[a](x)) if a in _spec.annotations else (lambda x:x) for a in _args]
            def _ret(*args):
                return [c(x) for (c,x) in zip(_castList, args)]
            return _ret

        self._cast = _cast()

    def setDuration(self, duration):
        self._duration = duration

    def setStartValue(self, startValue):
        self._startValue = startValue

    def setEndValue(self, endValue):
        self._endValue = endValue

    def setEasingCurve(self, easingCurve):
        self._easingCurve = TTkEasingCurve(easingCurve)

    @pyTTkSlot()
    def _refreshAnimation(self):
        diff = time.time() - self._baseTime
        # TTkLog.info(f"diff: {diff}")
        if diff >= self._duration:
            TTkHelper._rootWidget.paintExecuted.disconnect(self._refreshAnimation)
            if type(self._endValue) in (list,tuple):
                self._cb(*self._cast(*self._endValue))
            else:
                self._cb(*self._cast(self._endValue))
        else:
            v = diff/self._duration
            if type(self._startValue) in (list,tuple):
                newVal = [self._easingCurve.process(s,e,v) for (s,e) in zip(self._startValue,self._endValue)]
                self._cb(*self._cast(*newVal))
            else:
                newVal = self._easingCurve.process(self._startValue,self._endValue,v)
                self._cb(*self._cast(newVal))
        TTkHelper.unlockPaint()

    @pyTTkSlot()
    def start(self):
        self._baseTime = time.time()
        if TTkHelper._rootWidget:
            TTkHelper._rootWidget.paintExecuted.connect(self._refreshAnimation)
            self._refreshAnimation()
