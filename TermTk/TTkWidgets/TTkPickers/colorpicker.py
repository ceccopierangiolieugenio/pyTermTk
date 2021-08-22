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

import re

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.window import TTkWindow
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkWidgets.lineedit import TTkLineEdit
from TermTk.TTkWidgets.spinbox import TTkSpinBox
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkTemplates.color import TColor

class _TTkHueCanvas(TTkWidget):
    __slots__ = ('_hueList', '_selected', 'colorPicked')
    def __init__(self, *args, **kwargs):
        # signals
        self.colorPicked=pyTTkSignal(int)

        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkHueCanvas' )

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

    def mouseDragEvent(self, evt):
        return self.mousePressEvent(evt)

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

class _TTkColorCanvas(TTkWidget):
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
        self.update()
        return True

    def mouseDragEvent(self, evt):
        return self.mousePressEvent(evt)

    def _colorAt(self,x,y,w,h):
        w-=1
        h-=1
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

class _TTkShowColor(TTkWidget,TColor):
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        TColor.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkShowColor' )

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

class _TTkColorButton(TTkButton):
    lastClicked = None
    __slots__ = ('colorClicked','_custom')
    def __init__(self, *args, **kwargs):
        self.colorClicked = pyTTkSignal(TTkColor)
        TTkButton.__init__(self, *args, **kwargs)
        TColor.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkColorButton' )
        self._custom = kwargs.get('custom', False)
        self.clicked.connect(self._clicked)
        self._textColorFocus = self._textColor

    @pyTTkSlot(TTkColor)
    def setColor(self, color):
        self._textColor = color
        self._textColorFocus = color
        self.update()

    def isCustom(self):
        return self._custom

    @pyTTkSlot()
    def _clicked(self):
        if self._custom:
            _TTkColorButton.lastClicked = self
        self.colorClicked.emit(self._textColor)

class TTkColorDialogPicker(TTkWindow,TColor):
    ''' Color Picker Layout sizes:

    ::
        Terminal window (More or less, It is too annoying to redraw this)
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
    customButtons = None
    __slots__ = (
        '_color',
        '_colorCanvas', '_hueCanvas',
        '_redLE', '_greenLE', '_blueRE', '_htmlLE',
        # Signals
        'colorSelected'
        )
    def __init__(self, *args, **kwargs):
        # Signals
        self.colorSelected = pyTTkSignal(TTkColor)
        TTkWindow.__init__(self, *args, **kwargs)
        TColor.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkColorPicker' )
        self.setLayout(TTkGridLayout())

        colorLayout = TTkGridLayout() # Right
        leftLayout   = TTkLayout(minSize=(25,20), maxWidth=25) # Left

        paletteLayout = TTkGridLayout(pos=(0,0),  size=(24,9))
        customLayout  = TTkGridLayout(pos=(0,10), size=(24,4))
        controlLayout = TTkLayout(    pos=(0,15), size=(24,30))

        # Color Layout Widgets
        self._colorCanvas = _TTkColorCanvas()
        self._hueCanvas = _TTkHueCanvas()
        colorLayout.addWidget(self._colorCanvas,0,0)
        colorLayout.addWidget(self._hueCanvas,1,0)
        self._hueCanvas.colorPicked.connect(self._colorCanvas.setHue)

        # Control
        controlLayout.addWidget( sc := _TTkShowColor(pos=(1,1), size=(4,4),  color=TTkColor.bg('#ffffff')) )
        controlLayout.addWidget( TTkLabel(pos=(1,0), text="rgb:") )
        controlLayout.addWidget( TTkLabel(pos=(6,1), text="HTML:") )
        controlLayout.addWidget( leR := TTkSpinBox(pos=(7,0), size=(5,1),  value=255, minimum=0, maximum=255) )
        controlLayout.addWidget( leG := TTkSpinBox(pos=(12,0), size=(5,1),  value=255, minimum=0, maximum=255) )
        controlLayout.addWidget( leB := TTkSpinBox(pos=(18,0), size=(5,1),  value=255, minimum=0, maximum=255) )

        controlLayout.addWidget( leHTML := TTkLineEdit(pos=(12,1), size=(8,1),  text="#FFFFFF") )

        controlLayout.addWidget( okButton :=     TTkButton(pos=(6,2),  size=(6,3), text="OK",      border=True) )
        controlLayout.addWidget( cancelButton := TTkButton(pos=(13,2), size=(10,3), text="CANCEL",  border=True) )

        controlLayout.addWidget( TTkLabel(pos=(3,20), text="Seriously?") )

        @pyTTkSlot()
        def _okPressed():
            self.color = sc.color
            self.colorSelected.emit(self.color)
            self.close()

        okButton.clicked.connect(_okPressed)

        @pyTTkSlot()
        def _cancelPressed():
            self.colorSelected.emit(self.color)
            self.close()

        cancelButton.clicked.connect(_cancelPressed)

        @pyTTkSlot(int)
        def _controlSetRGBColor(color):
            sc.setRGBColor(color)
            leR.setValue((color&0xff0000)>>16)
            leG.setValue((color&0x00ff00)>> 8)
            leB.setValue((color&0x0000ff)>> 0)
            leHTML.setText("#{:06X}".format(color))

        @pyTTkSlot(TTkColor)
        def _controlSetColor(color):
            r,g,b = color.bgToRGB()
            numColor = r<<16|g<<8|b
            _controlSetRGBColor(numColor)

        @pyTTkSlot()
        def _leHTMLChanged():
            text = leHTML.text()
            if re.match('#[a-f0-9]{6}', text.lower()):
                _controlSetRGBColor(int(text[1:], 16))

        leHTML.returnPressed.connect(_leHTMLChanged)

        @pyTTkSlot(int)
        def _leRGBChanged(value):
            r = leR.value()
            g = leG.value()
            b = leB.value()
            if r&(~0xff) or r&(~0xff) or r&(~0xff): return
            _controlSetRGBColor(r<<16|g<<8|b)

        leR.valueChanged.connect(_leRGBChanged)
        leG.valueChanged.connect(_leRGBChanged)
        leB.valueChanged.connect(_leRGBChanged)

        _controlSetColor(self.color)

        # Palette Layout Widgets
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#ff0000'), border=True, maxSize=(8,3)),0,0,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#ffff00'), border=True, maxSize=(8,3)),0,2,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#00ff00'), border=True, maxSize=(8,3)),0,4,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#00ffff'), border=True, maxSize=(8,3)),1,0,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#0000ff'), border=True, maxSize=(8,3)),1,2,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#ff00ff'), border=True, maxSize=(8,3)),1,4,1,2)
        b.colorClicked.connect(_controlSetColor)

        # Shades of Grey
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#ffffff'), border=True, maxSize=(4,3)),2,0)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#dddddd'), border=True, maxSize=(4,3)),2,1)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#aaaaaa'), border=True, maxSize=(4,3)),2,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#666666'), border=True, maxSize=(4,3)),2,3)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#333333'), border=True, maxSize=(4,3)),2,4)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.bg('#000000'), border=True, maxSize=(4,3)),2,5)
        b.colorClicked.connect(_controlSetColor)

        # Custom frame
        if TTkColorDialogPicker.customButtons is None:
            TTkColorDialogPicker.customButtons = (
                    _TTkColorButton(color=TTkColor.bg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.bg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.bg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.bg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.bg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.bg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.bg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.bg('#ffffff'), custom=True, border=True, maxSize=(3,3)) )


        customLayout.addWidget(b:=TTkColorDialogPicker.customButtons[0],0,0)
        b.colorClicked.connect(_controlSetColor)
        customLayout.addWidget(b:=TTkColorDialogPicker.customButtons[1],0,1)
        b.colorClicked.connect(_controlSetColor)
        customLayout.addWidget(b:=TTkColorDialogPicker.customButtons[2],0,2)
        b.colorClicked.connect(_controlSetColor)
        customLayout.addWidget(b:=TTkColorDialogPicker.customButtons[3],0,3)
        b.colorClicked.connect(_controlSetColor)
        customLayout.addWidget(b:=TTkColorDialogPicker.customButtons[4],0,4)
        b.colorClicked.connect(_controlSetColor)
        customLayout.addWidget(b:=TTkColorDialogPicker.customButtons[5],0,5)
        b.colorClicked.connect(_controlSetColor)
        customLayout.addWidget(b:=TTkColorDialogPicker.customButtons[6],0,6)
        b.colorClicked.connect(_controlSetColor)
        customLayout.addWidget(b:=TTkColorDialogPicker.customButtons[7],0,7)
        b.colorClicked.connect(_controlSetColor)

        customLayout.addWidget(b:=TTkButton(border=False, text='Add to Custom Colors'),1,0,1,8)

        @pyTTkSlot()
        def _addCustomPressed():
            btn = _TTkColorButton.lastClicked
            TTkLog.debug(f"{btn}")
            if btn is not None and \
               btn.isCustom():
                TTkLog.debug(f"2 {btn}")
                btn.setColor(sc.color)
        b.clicked.connect(_addCustomPressed)

        # Events
        self._colorCanvas.colorPicked.connect(_controlSetRGBColor)

        self.layout().addItem(leftLayout ,0,0)
        self.layout().addItem(colorLayout ,0,1)

        leftLayout.addItem(paletteLayout)
        leftLayout.addItem(customLayout)
        leftLayout.addItem(controlLayout)

    def paintEvent(self):
        TTkWindow.paintEvent(self)
        if self.hasFocus():
            color = TTkCfg.theme.windowBorderColorFocus
        else:
            color = TTkCfg.theme.windowBorderColor
        self._canvas.drawGrid(
            pos=(0,2),size=(26,self._height-2),
            hlines=(10,15), vlines=(),
            color=color, grid=6)
        gg = TTkCfg.theme.grid[6]
        self._canvas.drawChar(pos=(0,2),  char=gg[0x08], color=color)
        self._canvas.drawChar(pos=(25,2), char=gg[0x02], color=color)
        self._canvas.drawChar(pos=(25,self._height-1), char=gg[0x0E], color=color)
        self._canvas.drawBoxTitle(pos=(0,2) , size=(26,0), text=" Basic colors ", align=TTkK.CENTER_ALIGN, color=color, colorText=TTkCfg.theme.frameTitleColor)
        self._canvas.drawBoxTitle(pos=(0,12), size=(26,0), text=" Custom colors ", align=TTkK.CENTER_ALIGN, color=color, colorText=TTkCfg.theme.frameTitleColor)
        self._canvas.drawBoxTitle(pos=(0,17), size=(26,0), text=" Conrols ", align=TTkK.CENTER_ALIGN, color=color, colorText=TTkCfg.theme.frameTitleColor)

class TTkColorButtonPicker(_TTkColorButton):
    __slots__ = ('_type', 'colorSelected')
    def __init__(self, *args, **kwargs):
        # Signals
        self.colorSelected = pyTTkSignal(TTkColor)
        _TTkColorButton.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkColorButtonPicker' )
        self._custom = False
        self.clicked.connect(self._colorClicked)
        self._type = self._textColor.colorType()
        hexColor =  self._textColor.getHex(self._type)
        self.setColor(TTkColor.bg(hexColor))

    #@pyTTkSlot(TTkColor)
    #def colorSelected(self, color):
    #    self.setColor(color)
    #    #self.setFocus()
    #    #self.update()

    @pyTTkSlot()
    def _colorClicked(self):
        colorPicker = TTkColorDialogPicker(pos = (3,3), size=(75,24), color=self._textColor, title="Test Color Picker", border=True)
        colorPicker.colorSelected.connect(self.setColor)
        colorPicker.colorSelected.connect(self.colorSelected.emit)
        TTkHelper.overlay(self, colorPicker, -1,-1)

