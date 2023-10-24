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

__all__ = ['TTkKeyPressView']

from TermTk.TTkCore.TTkTerm.input import TTkInput
from TermTk.TTkCore.TTkTerm.inputkey import TTkKeyEvent, mod2str, key2str
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.signal import pyTTkSlot
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.propertyanimation import TTkPropertyAnimation, TTkEasingCurve
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget

from TermTk.TTkTestWidgets.keypressviewfont import TTkKeyPressViewFont

class TTkKeyPressView(TTkWidget):
    __slots__ = ('_fadeDuration','_keys','_anim')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        TTkInput.inputEvent.connect(self._processInput)
        self._keys = []
        self._fadeDuration = 2.5
        self._anim = TTkPropertyAnimation(self, '_pushFade')

    @pyTTkSlot(TTkKeyEvent, TTkMouseEvent)
    def _processInput(self, kevt, mevt):
        if kevt is not None: self._addKey(kevt)
        if mevt is not None: self._addMouse(mevt)

    @pyTTkSlot(TTkKeyEvent)
    def _addKey(self, evt):
        if evt.type == TTkK.Character:
            text = evt.key
        else:
            text = key2str(evt.key).replace("Key_",'')
            if evt.mod:
                m = mod2str(evt.mod).replace("Modifier",'')
                text = f"{m} {text}"
        if self._keys and evt.type == self._keys[-1][2] == TTkK.Character:
             self._keys[-1][1]+=evt.key
             self._keys[-1][0]=1
        else:
            self._keys.append([1,text,evt.type])
        self._startFade()

    @pyTTkSlot(TTkMouseEvent)
    def _addMouse(self, evt):
              # return f"MouseEvent ({self.x},{self.y}) {self.key2str()} {self.evt2str()} {self.mod2str()} tap:{self.tap} - {self.raw}"
        # text = f"M:{(evt.x,evt.y)} {evt.key2str().replace('Button','')} {evt.evt2str().replace('Release','').replace('Press','')} {evt.mod2str().replace('NoModifier','')}"
        tap = " "
        if evt.tap==2: tap=" DoubleClick "
        if evt.tap==3: tap=" TripleClick "
        if evt.tap>3:  tap=f" {evt.tap} Clicks "

        text = f"M:{(evt.x,evt.y)} {evt.key2str().replace('Button','')}{tap}{evt.mod2str().replace('NoModifier','')}"
        self._keys.append([1,text,0x100])
        self._startFade()

    def _startFade(self):
        self._anim.setDuration(self._fadeDuration)
        self._anim.setStartValue(0)
        self._anim.setEndValue(1)
        self._anim.setEasingCurve(TTkEasingCurve.OutExpo)
        self._anim.start()

    def _pushFade(self, fade: float):
        for k in self._keys:
            k[0] -= fade
        # Apply the main fade to the current key
        if self._keys:
            self._keys[-1][0] = 1-fade
        for i,k in enumerate(self._keys):
            if k[0] <= 0:
                self._keys.pop(i)
        self.update()

    def txt2map(self, txt):
        ret = ["","",""]
        for c in txt:
            m = self.fontMap.get(c,["...",". .","..."])
            ret[0] += m[0]
            ret[1] += m[1]
            ret[2] += m[2]
        return ret

    def paintEvent(self, canvas):
        for alpha,text,_ in self._keys:
            r = int(0xbb*alpha)
            g = int(0xff*alpha)
            b = int(0xff*alpha)
            color = TTkColor.fg(f"#{r<<16|g<<8|b:06x}")
            #canvas.drawText(pos=((self.width()-len(text))//2,0),text=text,color=color)
            m = self.txt2map(text)
            canvas.drawText(pos=((self.width()-len(text)*3)//2,0),text=m[0],color=color)
            canvas.drawText(pos=((self.width()-len(text)*3)//2,1),text=m[1],color=color)
            canvas.drawText(pos=((self.width()-len(text)*3)//2,2),text=m[2],color=color)

    fontMap = TTkKeyPressViewFont.bitmap
    # fontMap = TTkKeyPressViewFont.calvin_s
