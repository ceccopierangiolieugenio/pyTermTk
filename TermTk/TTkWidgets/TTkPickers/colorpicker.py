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

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.window import TTkWindow
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkWidgets.lineedit import TTkLineEdit
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkTemplates.color import TColor

class TTkHueCanvas(TTkWidget):
    __slots__ = ('_hueList', '_selected', 'colorPicked')
    def __init__(self, *args, **kwargs):
        # signals
        self.colorPicked=pyTTkSignal(int)

        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkHueCanvas' )

        self.setMaximumHeight(1)
        self.setMinimumSize(6,1)
        self._hueList = []
        self._selected = -1
        self.setFocusPolicy(TTkK.ClickFocus)


    def resizeEvent(self, w, h):
        self._selected = -1

    def mousePressEvent(self, evt):
        x,y = evt.x, evt.y
        self._selected = x
        if x < len(self._hueList):
            self.colorPicked.emit(self._hueList[x])
        self.update()
        return True

    def paintEvent(self):
        w,_ = self.size()
        self._hueList = [0x00]*(w+1)
        def _linInt(a,b,x):
            return int(a*(1-x)+b*x)

        def _printSlice(num, a, b, inc):
            for x in range(0,w//6+1):
                if inc:
                    rgb =a|(b&_linInt(0,b,6*x/w))
                else:
                    rgb =a|(b&_linInt(b,0,6*x/w))
                color = TTkColor.bg( "#{:06x}".format(rgb) )
                if (num*w//6)+x == self._selected:
                    self._canvas.drawChar(pos=((num*w//6)+x,0), char="◼", color=color+TTkColor.fg("#000000"))
                else:
                    self._canvas.drawChar(pos=((num*w//6)+x,0), char=" ", color=color)
                self._hueList[(num*w//6)+x]=rgb

        _printSlice(0, 0xff0000, 0x00ff00, True)
        _printSlice(1, 0x00ff00, 0xff0000, False)
        _printSlice(2, 0x00ff00, 0x0000ff, True)
        _printSlice(3, 0x0000ff, 0x00ff00, False)
        _printSlice(4, 0x0000ff, 0xff0000, True)
        _printSlice(5, 0xff0000, 0x0000ff, False)

class TTkColorCanvas(TTkWidget):
    __slots__ = ('_hue', 'colorPicked', '_selected')
    def __init__(self, *args, **kwargs):
        # signals
        self.colorPicked=pyTTkSignal(int)
        self._selected=(-1,-1)
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkColorPicker' )
        self._hue = 0xff0000
        self.setFocusPolicy(TTkK.ClickFocus)

    @pyTTkSlot(int)
    def setHue(self, hue):
        self._hue = hue
        self.update()

    def mousePressEvent(self, evt):
        w,h = self.size()
        x,y = evt.x, evt.y
        self._selected = (x,y)
        self.colorPicked.emit(self._colorAt(x,y,w,h))
        return True

    def _colorAt(self,x,y,w,h):
        def _linInt(a,b,x):
            return int(a*(1-x)+b*x)
        r = self._hue&0xff0000
        g = self._hue&0x00ff00
        b = self._hue&0x0000ff
        r = _linInt(0xff0000,r,x/w)&0xff0000
        g = _linInt(0x00ff00,g,x/w)&0x00ff00
        b = _linInt(0x0000ff,b,x/w)&0x0000ff
        r = _linInt(r,0,y/h)&0xff0000
        g = _linInt(g,0,y/h)&0x00ff00
        b = _linInt(b,0,y/h)&0x0000ff
        return r|g|b

    def paintEvent(self):
        w,h = self.size()
        for x in range(w):
            for y in range(h):
                color = TTkColor.bg( "#{:06x}".format(self._colorAt(x,y,w,h)) )
                if (x,y)==self._selected:
                    self._canvas.drawText(pos=(x,y), text="◼", color=color+TTkColor.fg("#000000"))
                else:
                    self._canvas.drawText(pos=(x,y), text=" ", color=color)

class TTkShowColor(TTkWidget,TColor):
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        TColor.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkShowColor' )

    @pyTTkSlot(int)
    def setRGBColor(self, color):
        self.color = TTkColor.bg( "#{:06x}".format(color) )
        self.update()

    @pyTTkSlot(TTkColor)
    def setColor(self, color):
        self.color = color
        self.update()

    def paintEvent(self):
        w,h = self.size()
        for y in range(h):
            self._canvas.drawText(pos=(0,y),text=" "*w, color=self.color)

class TTkColorButton(TTkButton,TColor):
    __slots__ = ('colorClicked')
    def __init__(self, *args, **kwargs):
        self.colorClicked = pyTTkSignal(TTkColor)
        TTkButton.__init__(self, *args, **kwargs)
        TColor.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkColorButton' )
        self.clicked.connect(self._clicked)

    @pyTTkSlot()
    def _clicked(self):
        self.colorClicked.emit(self._textColor)

class TTkColorPicker(TTkWindow):
    '''
    ### Color Picker Layout sizes:
        Terminal window
        ┌────────────────────────────────────────────────┐
        │┌──────[Palette]───────┐┌────[Color]───────────┐│
        ││┌──────┐┌─────┐┌─────┐││┌────────────────────┐││
        │││RED   ││Green││Blue ││││                    │││
        ││└──────┘└─────┘└─────┘│││                    │││
        ││┌──────┐┌─────┐┌─────┐│││                    │││
        │││Purple││White││Black││││                    │││
        ││└──────┘└─────┘└─────┘│││   Color Canvas     │││
        ││┌──────┐┌─────┐┌─────┐│││                    │││
        │││...   ││     ││     ││││                    │││
        ││└──────┘└─────┘└─────┘││└────────────────────┘││
        ││┌──────┐┌─────┐┌─────┐││┌────────────────────┐││
        │││      ││     ││     ││││     HUE Canvas     │││
        ││└──────┘└─────┘└─────┘││└────────────────────┘││
        │└──────────────────────┘└──────────────────────┘│
        │┌───────[Custom]───────┐┌───────[Control]──────┐│
        ││┌──────┐┌─────┐┌─────┐││┌────┐        ┌──────┐││
        │││      ││     ││     ││││    │  Red:  └──────┘││
        ││└──────┘└─────┘└─────┘│││    │        ┌──────┐││
        ││┌──────┐┌─────┐┌─────┐│││    │  Green:└──────┘││
        │││      ││     ││     ││││    │        ┌──────┐││
        ││└──────┘└─────┘└─────┘││└────┘  Blue: └──────┘││
        ││ <Custom Color>       ││      ┌──────────────┐││
        ││ <OK>  <CANCEL>       ││HTML: └──────────────┘││
        │└──────────────────────┘└──────────────────────┘│
        └────────────────────────────────────────────────┘
    '''
    __slots__ = (
        '_colorCanvas', '_hueCanvas',
        '_redLE', '_greenLE', '_blueRE', '_htmlLE',
        )
    def __init__(self, *args, **kwargs):
        TTkWindow.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkColorPicker' )
        self.setLayout(TTkGridLayout())

        colorLayout = TTkGridLayout() # Right
        leftLayout =  TTkGridLayout() # Left

        paletteFrame = TTkFrame(border=True, layout=TTkGridLayout(), title="Basic colors")
        customFrame  = TTkFrame(border=True, layout=TTkGridLayout(), title="Custom colors")
        controlFrame = TTkFrame(border=True, title="Conrols")

        # Color Layout Widgets
        self._colorCanvas = TTkColorCanvas()
        self._hueCanvas = TTkHueCanvas()
        colorLayout.addWidget(self._colorCanvas,0,0)
        colorLayout.addWidget(self._hueCanvas,1,0)
        self._hueCanvas.colorPicked.connect(self._colorCanvas.setHue)

        # Control
        sc = TTkShowColor(pos=(1,1), size=(5,8), parent=controlFrame, color=TTkColor.bg('#ffffff'))
        TTkLabel(pos=(7,2), parent=controlFrame,text="rgb:")
        TTkLabel(pos=(7,4), parent=controlFrame,text="HTML:")
        TTkLineEdit(pos=(13,2), size=(3,1), parent=controlFrame, text="FF")
        TTkLineEdit(pos=(17,2), size=(3,1), parent=controlFrame, text="FF")
        TTkLineEdit(pos=(21,2), size=(3,1), parent=controlFrame, text="FF")

        TTkLineEdit(pos=(13,4), size=(8,1), parent=controlFrame, text="#FFFFFF")

        TTkButton(pos=(7,6),  size=(6,3), text="OK",     parent=controlFrame, border=True)
        TTkButton(pos=(14,6), size=(10,3), text="CANCEL", parent=controlFrame, border=True)

        # Palette Layout Widgets
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#ff0000'), border=True, maxSize=(8,3)),0,0)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffff00'), border=True, maxSize=(8,3)),0,1)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#00ff00'), border=True, maxSize=(8,3)),0,2)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#00ffff'), border=True, maxSize=(8,3)),1,0)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#0000ff'), border=True, maxSize=(8,3)),1,1)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#ff00ff'), border=True, maxSize=(8,3)),1,2)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),2,0)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#dddddd'), border=True, maxSize=(8,3)),2,1)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#aaaaaa'), border=True, maxSize=(8,3)),2,2)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#666666'), border=True, maxSize=(8,3)),3,0)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#333333'), border=True, maxSize=(8,3)),3,1)
        b.colorClicked.connect(sc.setColor)
        paletteFrame.layout().addWidget(b:=TTkColorButton(color=TTkColor.bg('#000000'), border=True, maxSize=(8,3)),3,2)
        b.colorClicked.connect(sc.setColor)

        # Custom frame
        customButtonsLayout = TTkGridLayout()
        customButtonsLayout.addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),0,0)
        b.colorClicked.connect(sc.setColor)
        customButtonsLayout.addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),0,1)
        b.colorClicked.connect(sc.setColor)
        customButtonsLayout.addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),0,2)
        b.colorClicked.connect(sc.setColor)
        customButtonsLayout.addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),1,0)
        b.colorClicked.connect(sc.setColor)
        customButtonsLayout.addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),1,1)
        b.colorClicked.connect(sc.setColor)
        customButtonsLayout.addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),1,2)
        b.colorClicked.connect(sc.setColor)
        customButtonsLayout.addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),2,0)
        b.colorClicked.connect(sc.setColor)
        customButtonsLayout.addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),2,1)
        b.colorClicked.connect(sc.setColor)
        customButtonsLayout.addWidget(b:=TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(8,3)),2,2)
        b.colorClicked.connect(sc.setColor)

        customFrame.layout().addItem(customButtonsLayout,0,0)
        customFrame.layout().addWidget(TTkButton(border=False, text='Add to Custom Colors'),1,0)


        # Events
        self._colorCanvas.colorPicked.connect(sc.setRGBColor)

        self.layout().addItem(leftLayout ,0,0)
        self.layout().addItem(colorLayout,0,1)

        leftLayout.addWidget(paletteFrame,0,0)
        leftLayout.addWidget(customFrame ,1,0)
        leftLayout.addWidget(controlFrame,2,0)
