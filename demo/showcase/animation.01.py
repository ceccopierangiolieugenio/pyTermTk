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
import sys
import random
import argparse

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

sys.path.append(os.path.join(sys.path[0],'..'))
from showcase._showcasehelper import getUtfColoredSentence

class EasingShow(ttk.TTkWidget):
    __slots__ = ('_easingCb')
    def __init__(self, easingCb, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._easingCb = ttk.TTkEasingCurve(easingCb)
    def paintEvent(self):
        # gen w*2,h*4 pixmap
        w,h = self.size()
        pm = [[0]*h*4 for _ in range(w*2)]
        vs = []
        # populate the pixmap
        for x in range(w*2):
            v = float(x)/(w*2-1) # v goes from 0 -> 1
            vs.append(self._easingCb.process(0,1,v))

        maxv = max(vs)
        minv = min(vs)
        for x,v in enumerate(vs):
            y = int((h*4-1)*(v-minv)/(maxv-minv))
            pm[x][h*4-y-1] = 1

        '''
            Braille bits:
            o2  o1 = 4 bits each

            1   5   Braille dots
            2   6
            3   7
            4   8

            TTkTheme.braille[( o1<<4 | o2 )] = Braille UTF-8 char
        '''
        canvas = self.getCanvas()
        gb=ttk.TTkCfg.theme.braille
        color=ttk.TTkColor.fg("#FFFF00")+ttk.TTkColor.bg("#004400", modifier=ttk.TTkColorGradient(increment=-5))
        for x in range(w):
            for y in range(h):
                o1 = pm[2*x  ][4*y] | pm[2*x  ][4*y+1]<<1 | pm[2*x  ][4*y+2]<<2 | pm[2*x  ][4*y+3]<<3
                o2 = pm[2*x+1][4*y] | pm[2*x+1][4*y+1]<<1 | pm[2*x+1][4*y+2]<<2 | pm[2*x+1][4*y+3]<<3
                ch = gb[( o1<<4 | o2 )]
                canvas.drawChar(pos=(x,y),char=ch, color=color)

def demoTextEditRO(root=None):
    easingList = (
        (ttk.TTkEasingCurve.Linear , 'Linear'),
        (ttk.TTkEasingCurve.InQuad , 'InQuad'),
        (ttk.TTkEasingCurve.OutQuad , 'OutQuad'),
        (ttk.TTkEasingCurve.InOutQuad , 'InOutQuad'),
        (ttk.TTkEasingCurve.OutInQuad , 'OutInQuad'),
        (ttk.TTkEasingCurve.InCubic , 'InCubic'),
        (ttk.TTkEasingCurve.OutCubic , 'OutCubic'),
        (ttk.TTkEasingCurve.InOutCubic , 'InOutCubic'),
        (ttk.TTkEasingCurve.OutInCubic , 'OutInCubic'),
        (ttk.TTkEasingCurve.InQuart , 'InQuart'),
        (ttk.TTkEasingCurve.OutQuart , 'OutQuart'),
        (ttk.TTkEasingCurve.InOutQuart , 'InOutQuart'),
        (ttk.TTkEasingCurve.OutInQuart , 'OutInQuart'),
        (ttk.TTkEasingCurve.InQuint , 'InQuint'),
        (ttk.TTkEasingCurve.OutQuint , 'OutQuint'),
        (ttk.TTkEasingCurve.InOutQuint , 'InOutQuint'),
        (ttk.TTkEasingCurve.OutInQuint , 'OutInQuint'),
        (ttk.TTkEasingCurve.InSine , 'InSine'),
        (ttk.TTkEasingCurve.OutSine , 'OutSine'),
        (ttk.TTkEasingCurve.InOutSine , 'InOutSine'),
        (ttk.TTkEasingCurve.OutInSine , 'OutInSine'),
        (ttk.TTkEasingCurve.InExpo , 'InExpo'),
        (ttk.TTkEasingCurve.OutExpo , 'OutExpo'),
        (ttk.TTkEasingCurve.InOutExpo , 'InOutExpo'),
        (ttk.TTkEasingCurve.OutInExpo , 'OutInExpo'),
        (ttk.TTkEasingCurve.InCirc , 'InCirc'),
        (ttk.TTkEasingCurve.OutCirc , 'OutCirc'),
        (ttk.TTkEasingCurve.InOutCirc , 'InOutCirc'),
        (ttk.TTkEasingCurve.OutInCirc , 'OutInCirc'),
        (ttk.TTkEasingCurve.InElastic , 'InElastic'),
        (ttk.TTkEasingCurve.OutElastic , 'OutElastic'),
        (ttk.TTkEasingCurve.InOutElastic , 'InOutElastic'),
        (ttk.TTkEasingCurve.OutInElastic , 'OutInElastic'),
        (ttk.TTkEasingCurve.InBack , 'InBack'),
        (ttk.TTkEasingCurve.OutBack , 'OutBack'),
        (ttk.TTkEasingCurve.InOutBack , 'InOutBack'),
        (ttk.TTkEasingCurve.OutInBack , 'OutInBack'),
        (ttk.TTkEasingCurve.InBounce , 'InBounce'),
        (ttk.TTkEasingCurve.OutBounce , 'OutBounce'),
        (ttk.TTkEasingCurve.InOutBounce , 'InOutBounce'),
        (ttk.TTkEasingCurve.OutInBounce , 'OutInBounce'))

    frame = ttk.TTkFrame(parent=root, border=False)

    winTe = ttk.TTkWindow(parent=frame, title="Text Edit", pos=(20,3), size=(50,30), layout=ttk.TTkGridLayout())
    te = ttk.TTkTextEdit(parent=winTe, lineNumber=True)

    winAc = ttk.TTkWindow(parent=frame, title="Animation Controls", pos=(0,0), size=(50,30))
    animBtnScroll = ttk.TTkButton(parent=winAc, text="Anim Scroll",border=True,pos=(0,0))
    animBtnWinPos = ttk.TTkButton(parent=winAc, text="Anim Pos",border=True,pos=(15,0))
    animBoth = ttk.TTkButton(parent=winAc, text="Anim Both",border=True,pos=(25,0))
    animHelper = ttk.TTkButton(parent=winAc, text="Anim Easing Charts",border=True,pos=(0,23))

    winHelper = ttk.TTkWindow(parent=frame, title="Easing Charts", pos=(80,0), size=(50,30), layout=ttk.TTkGridLayout())
    scrollArea = ttk.TTkScrollArea(parent=winHelper)
    saWp = scrollArea.viewport()
    for i,(easing,name) in enumerate(easingList):
        ttk.TTkLabel(parent=saWp, pos=(0,i*9),     size=(40,1), text=name)
        EasingShow(  parent=saWp, pos=( 0, 1+i*9), size=(40,8), easingCb=easing)

    class PosControls(ttk.TTkFrame):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs|{'border':True})
            ttk.TTkLabel(          parent=self,pos=(0,0),text='Starting Position (x,y)')
            self.axspb = ttk.TTkSpinBox(parent=self,maximum=500, minimum=-100, pos=(0,1),size=(8,1),value=0)
            self.ayspb = ttk.TTkSpinBox(parent=self,maximum=500, minimum=-100, pos=(8,1),size=(8,1),value=100)
            ttk.TTkLabel(          parent=self,pos=(0,2),text='Ending Position (x,y)')
            self.bxspb = ttk.TTkSpinBox(parent=self,maximum=500, minimum=-100, pos=(0,3),size=(8,1),value=0)
            self.byspb = ttk.TTkSpinBox(parent=self,maximum=500, minimum=-100, pos=(8,3),size=(8,1),value=0)
            ttk.TTkLabel(          parent=self,pos=(0,4),text='Duration (sec.)')
            self.dursb = ttk.TTkSpinBox(parent=self,maximum=500, minimum=0, pos=(0,5),size=(12,1),value=2)
            ttk.TTkLabel(          parent=self,pos=(0,6),text='Easing Curve')
            self.ecb = ttk.TTkComboBox(parent=self,pos=(0,7),size=(20,1),list=[v for (_,v) in easingList],index=0)

    pcScroll = PosControls(parent=winAc, pos=(0,3), size=(25,10), title="Text Scroll")
    pcWinPos = PosControls(parent=winAc, pos=(0,13), size=(25,10), title="Window Position")
    pcHelpSc = PosControls(parent=winAc, pos=(0,26), size=(25,10), title="Helper scroll")

    animScroll = ttk.TTkPropertyAnimation(te.viewport(),'viewMoveTo')
    animWinPos = ttk.TTkPropertyAnimation(None, winTe.move)
    animHelpSc = ttk.TTkPropertyAnimation(saWp, 'viewMoveTo')

    def _startAnimScroll():
        animScroll.setDuration(pcScroll.dursb.value())
        animScroll.setStartValue((pcScroll.axspb.value(), pcScroll.ayspb.value()))
        animScroll.setEndValue(  (pcScroll.bxspb.value(), pcScroll.byspb.value()))
        animScroll.setEasingCurve({t:v for (v,t) in easingList}.get(pcScroll.ecb.currentText(),easingList[0][0]))
        animScroll.start()
    def _startAnimWinPos():
        animWinPos.setDuration(pcWinPos.dursb.value())
        animWinPos.setStartValue((pcWinPos.axspb.value(), pcWinPos.ayspb.value()))
        animWinPos.setEndValue(  (pcWinPos.bxspb.value(), pcWinPos.byspb.value()))
        animWinPos.setEasingCurve({t:v for (v,t) in easingList}.get(pcWinPos.ecb.currentText(),easingList[0][0]))
        animWinPos.start()
    def _startAnimHelpSc():
        animHelpSc.setDuration(pcHelpSc.dursb.value())
        animHelpSc.setStartValue((pcHelpSc.axspb.value(), pcHelpSc.ayspb.value()))
        animHelpSc.setEndValue(  (pcHelpSc.bxspb.value(), pcHelpSc.byspb.value()))
        animHelpSc.setEasingCurve({t:v for (v,t) in easingList}.get(pcHelpSc.ecb.currentText(),easingList[0][0]))
        animHelpSc.start()

    animBtnScroll.clicked.connect(_startAnimScroll)
    animBtnWinPos.clicked.connect(_startAnimWinPos)
    animBoth.clicked.connect(_startAnimScroll)
    animBoth.clicked.connect(_startAnimWinPos)
    animHelper.clicked.connect(_startAnimHelpSc)

    # Initialize the textedit with come text

    te.setText(ttk.TTkString("Text Edit DEMO\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD+ttk.TTkColor.ITALIC))

    # Load ANSI input
    te.append(ttk.TTkString("ANSI Input Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'textedit.ANSI.txt')) as f:
        te.append(f.read())

    # Test Variable sized chars
    te.append(ttk.TTkString("Test Variable sized chars\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    te.append( "Emoticons: -😁😂😍😎----")
    te.append( "           --😐😁😂😍😎-")
    te.append("")

    te.append( "    UTF-8: £ @ £ ¬ ` 漢 _ _ あ _ _")
    te.append( "           |.|.|.|.|.||.|.|.||.|.|.")
    te.append("")


    zc1 = chr(0x07a6)
    zc2 = chr(0x20D7)
    zc3 = chr(0x065f)
    te.append( "           - |  |  |  |  | -")
    te.append(f"Zero Size: - o{zc1}  o{zc2}  o{zc3}  o{zc1}{zc2}  o{zc1}{zc2}{zc3} -")
    te.append( "           - |  |  |  |  | -")
    te.append("")

    te.append(f"Plus Tabs: -\t😁\t😍\to{zc1}{zc2}{zc3}\t😎\to{zc1}{zc2}{zc3}\t😂-")
    te.append("")

    # Test Tabs
    te.append(ttk.TTkString("Tabs Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    te.append("Word\tAnother Word\tYet more words")
    te.append("What a wonderful word\tOut of this word\tBattle of the words\tThe city of thousand words\tThe word is not enough\tJurassic word\n")
    te.append("tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("-tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("--tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("---tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("----tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("-----tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("------tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab")
    te.append("-------tab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\ttab\n")

    te.append(ttk.TTkString("Random TTkString Input Test\n",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))
    te.append(ttk.TTkString('\n').join([ getUtfColoredSentence(10,15) for _ in range(100)]))

    te.append(ttk.TTkString("-- The Very END --",ttk.TTkColor.UNDERLINE+ttk.TTkColor.BOLD))

    # use the widget size to wrap
    # te.setLineWrapMode(ttk.TTkK.WidgetWidth)
    # te.setWordWrapMode(ttk.TTkK.WordWrap)

    # Use a fixed wrap size
    # te.setLineWrapMode(ttk.TTkK.FixedWidth)
    # te.setWrapWidth(100)





    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    args = parser.parse_args()
    windowed = args.w

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk()
    if windowed:
        rootTree = ttk.TTkWindow(parent=root,pos = (0,0), size=(70,40), title="Test Text Edit", layout=ttk.TTkGridLayout(), border=True)
    else:
        rootTree = root
        root.setLayout(ttk.TTkGridLayout())
    demoTextEditRO(rootTree)
    root.mainloop()

if __name__ == "__main__":
    main()