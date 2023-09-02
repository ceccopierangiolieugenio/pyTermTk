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

__all__ = ['TTkPropertyAnimation', 'TTkEasingCurve']

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
         self.InQuad       : TTkEasingCurve._ecInQuad,
         self.OutQuad      : TTkEasingCurve._ecOutQuad,
         self.InOutQuad    : TTkEasingCurve._ecInOutQuad,
         self.OutInQuad    : TTkEasingCurve._ecOutInQuad,
         self.InCubic      : TTkEasingCurve._ecInCubic,
         self.OutCubic     : TTkEasingCurve._ecOutCubic,
         self.InOutCubic   : TTkEasingCurve._ecInOutCubic,
         self.OutInCubic   : TTkEasingCurve._ecOutInCubic,
         self.InQuart      : TTkEasingCurve._ecInQuart,
         self.OutQuart     : TTkEasingCurve._ecOutQuart,
         self.InOutQuart   : TTkEasingCurve._ecInOutQuart,
         self.OutInQuart   : TTkEasingCurve._ecOutInQuart,
         self.InQuint      : TTkEasingCurve._ecInQuint,
         self.OutQuint     : TTkEasingCurve._ecOutQuint,
         self.InOutQuint   : TTkEasingCurve._ecInOutQuint,
         self.OutInQuint   : TTkEasingCurve._ecOutInQuint,
         self.InSine       : TTkEasingCurve._ecInSine,
         self.OutSine      : TTkEasingCurve._ecOutSine,
         self.InOutSine    : TTkEasingCurve._ecInOutSine,
         self.OutInSine    : TTkEasingCurve._ecOutInSine,
         self.InExpo       : TTkEasingCurve._ecInExpo,
         self.OutExpo      : TTkEasingCurve._ecOutExpo,
         self.InOutExpo    : TTkEasingCurve._ecInOutExpo,
         self.OutInExpo    : TTkEasingCurve._ecOutInExpo,
         self.InCirc       : TTkEasingCurve._ecInCirc,
         self.OutCirc      : TTkEasingCurve._ecOutCirc,
         self.InOutCirc    : TTkEasingCurve._ecInOutCirc,
         self.OutInCirc    : TTkEasingCurve._ecOutInCirc,
         self.InElastic    : TTkEasingCurve._ecInElastic,
         self.OutElastic   : TTkEasingCurve._ecOutElastic,
         self.InOutElastic : TTkEasingCurve._ecInOutElastic,
         self.OutInElastic : TTkEasingCurve._ecOutInElastic,
         self.InBack       : TTkEasingCurve._ecInBack,
         self.OutBack      : TTkEasingCurve._ecOutBack,
         self.InOutBack    : TTkEasingCurve._ecInOutBack,
         self.OutInBack    : TTkEasingCurve._ecOutInBack,
         self.InBounce     : TTkEasingCurve._ecInBounce,
         self.OutBounce    : TTkEasingCurve._ecOutBounce,
         self.InOutBounce  : TTkEasingCurve._ecInOutBounce,
         self.OutInBounce  : TTkEasingCurve._ecOutInBounce,
         self.OutBounce    : TTkEasingCurve._ecOutBounce,
         }.get(easingCurve,TTkEasingCurve._ecLinear)

    def process(self,a,b,v):
        v = self._easingFunc(v)
        return float(b)*v+float(a)*(1-v)

    @staticmethod
    def _ecMixCbHelper(incb,outcb,v):
        if v < 0.5: return incb(2*v)/2
        return 0.5+outcb(2*v-1)/2
    @staticmethod
    def _ecInOutHelper(incb,outcb,v):
        if v < 0.5: return incb(2*v)/2
        return 0.5+outcb(2*v-1)/2
    @staticmethod
    def _ecOutInHelper(incb,outcb,v):
        if v < 0.5: return outcb(2*v)/2
        return 0.5+incb(2*v-1)/2

    # Equations adapted from
    #  - https://easings.net
    #  - https://github.com/qt/qtbase/blob/dev/src/3rdparty/easing/easing.cpp

    @staticmethod
    def _ecLinear(v): return v
    @staticmethod
    def _ecInQuad(v): return v*v
    @staticmethod
    def _ecOutQuad(v): return -v*(v-2)
    @staticmethod
    def _ecInOutQuad(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInQuad,
                                        TTkEasingCurve._ecOutQuad,
                                        v)
    @staticmethod
    def _ecOutInQuad(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutQuad,
                                        TTkEasingCurve._ecInQuad,
                                        v)
    @staticmethod
    def _ecInCubic(v): return v*v*v
    @staticmethod
    def _ecOutCubic(v): v-=1 ; return 1+v*v*v
    @staticmethod
    def _ecInOutCubic(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInCubic,
                                        TTkEasingCurve._ecOutCubic,
                                        v)
    @staticmethod
    def _ecOutInCubic(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutCubic,
                                        TTkEasingCurve._ecInCubic,
                                        v)
    @staticmethod
    def _ecInQuart(v): return v*v*v*v
    @staticmethod
    def _ecOutQuart(v): v-=1 ; return 1-v*v*v*v
    @staticmethod
    def _ecInOutQuart(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInQuart,
                                        TTkEasingCurve._ecOutQuart,
                                        v)
    @staticmethod
    def _ecOutInQuart(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutQuart,
                                        TTkEasingCurve._ecInQuart,
                                        v)
    @staticmethod
    def _ecInQuint(v): return v*v*v*v*v
    @staticmethod
    def _ecOutQuint(v): v-=1 ; return 1+v*v*v*v*v
    @staticmethod
    def _ecInOutQuint(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInQuint,
                                        TTkEasingCurve._ecOutQuint,
                                        v)
    @staticmethod
    def _ecOutInQuint(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutQuint,
                                        TTkEasingCurve._ecInQuint,
                                        v)
    @staticmethod
    def _ecInSine(v): return 1-math.sin(math.pi*(1-v)/2)
    @staticmethod
    def _ecOutSine(v): return math.sin(math.pi*v/2)
    @staticmethod
    def _ecInOutSine(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInSine,
                                        TTkEasingCurve._ecOutSine,
                                        v)
    @staticmethod
    def _ecOutInSine(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutSine,
                                        TTkEasingCurve._ecInSine,
                                        v)
    @staticmethod
    def _ecInExpo(v): return v if v==1 or v==0 else math.pow(2,10*(v-1))-0.001
    @staticmethod
    def _ecOutExpo(v): return 1 if v==1 else 1.001*(1-math.pow(2,-10*v))
    @staticmethod
    def _ecInOutExpo(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInExpo,
                                        TTkEasingCurve._ecOutExpo,
                                        v)
    @staticmethod
    def _ecOutInExpo(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutExpo,
                                        TTkEasingCurve._ecInExpo,
                                        v)
    @staticmethod
    def _ecInCirc(v): return 1-math.sqrt(1-v*v)
    @staticmethod
    def _ecOutCirc(v): v-=1 ; return math.sqrt(1-v*v)
    @staticmethod
    def _ecInOutCirc(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInCirc,
                                        TTkEasingCurve._ecOutCirc,
                                        v)
    @staticmethod
    def _ecOutInCirc(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutCirc,
                                        TTkEasingCurve._ecInCirc,
                                        v)
    @staticmethod
    def _ecInElastic(v): return v if v in [0,1] else -math.pow(2, 10 *v-10)*math.sin((v*10-10.75)*(2*math.pi)/3)
    @staticmethod
    def _ecOutElastic(v): return 1-TTkEasingCurve._ecInElastic(1-v)
    @staticmethod
    def _ecInOutElastic(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInElastic,
                                        TTkEasingCurve._ecOutElastic,
                                        v)
    @staticmethod
    def _ecOutInElastic(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutElastic,
                                        TTkEasingCurve._ecInElastic,
                                        v)
    @staticmethod
    def _ecInBack(v,s=1.7): return v*v*((s+1)*v-s)
    @staticmethod
    def _ecOutBack(v,s=1.7): v-=1 ; return v*v*((s+1)*v+s)+1
    @staticmethod
    def _ecInOutBack(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInBack,
                                        TTkEasingCurve._ecOutBack,
                                        v)
    @staticmethod
    def _ecOutInBack(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutBack,
                                        TTkEasingCurve._ecInBack,
                                        v)
    @staticmethod
    def _ecInBounce(v): return 1-TTkEasingCurve._ecOutBounce(1-v)
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
    @staticmethod
    def _ecInOutBounce(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecInBounce,
                                        TTkEasingCurve._ecOutBounce,
                                        v)
    @staticmethod
    def _ecOutInBounce(v): return TTkEasingCurve._ecMixCbHelper(
                                        TTkEasingCurve._ecOutBounce,
                                        TTkEasingCurve._ecInBounce,
                                        v)


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
