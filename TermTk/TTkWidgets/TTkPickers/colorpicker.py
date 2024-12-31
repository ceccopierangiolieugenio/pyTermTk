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

__all__ = ['TTkColorButtonPicker', 'TTkColorDialogPicker']

import re

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.window import TTkWindow
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.label import TTkLabel
from TermTk.TTkWidgets.lineedit import TTkLineEdit
from TermTk.TTkWidgets.spinbox import TTkSpinBox
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout

class _TTkHueCanvas(TTkWidget):
    __slots__ = ('_hueList', '_selected', 'colorPicked')
    def __init__(self, **kwargs) -> None:
        # signals
        self.colorPicked=pyTTkSignal(int)

        TTkWidget.__init__(self, **kwargs)

        self.setMaximumHeight(1)
        self.setMinimumSize(6,1)
        self._hueList = []
        self._selected = -1
        self.setFocusPolicy(TTkK.ClickFocus)


    def resizeEvent(self, width: int, height: int) -> None:
        self._selected = -1

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        self._selected = evt.x
        if evt.x < len(self._hueList):
            self.colorPicked.emit(self._hueList[evt.x])
        self.update()
        return True

    def mouseDragEvent(self, evt:TTkMouseEvent) -> bool:
        return self.mousePressEvent(evt)

    def paintEvent(self, canvas: TTkCanvas) -> None:
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
                color = TTkColor.bg( f"#{rgb:06x}" )
                if (num*w//6)+x == self._selected:
                    canvas.drawChar(pos=((num*w//6)+x,0), char="◼", color=color+TTkColor.fg("#000000"))
                else:
                    canvas.drawChar(pos=((num*w//6)+x,0), char=" ", color=color)
                self._hueList[(num*w//6)+x]=rgb

        _printSlice(0, 0xff0000, 0x00ff00, True)
        _printSlice(1, 0x00ff00, 0xff0000, False)
        _printSlice(2, 0x00ff00, 0x0000ff, True)
        _printSlice(3, 0x0000ff, 0x00ff00, False)
        _printSlice(4, 0x0000ff, 0xff0000, True)
        _printSlice(5, 0xff0000, 0x0000ff, False)

class _TTkColorCanvas(TTkWidget):
    __slots__ = ('_hue', 'colorPicked', '_selected')
    def __init__(self, **kwargs) -> None:
        # signals
        self.colorPicked=pyTTkSignal(int)
        self._selected=(-1,-1)
        TTkWidget.__init__(self, **kwargs)
        self._hue = 0xff0000
        self.setFocusPolicy(TTkK.ClickFocus)

    @pyTTkSlot(int)
    def setHue(self, hue:int):
        self._hue = hue
        self.update()

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        w,h = self.size()
        x,y = evt.x, evt.y
        self._selected = (x,y)
        self.colorPicked.emit(self._colorAt(x,y,w,h))
        self.update()
        return True

    def mouseDragEvent(self, evt:TTkMouseEvent) -> bool:
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

    def paintEvent(self, canvas: TTkCanvas) -> None:
        w,h = self.size()
        for x in range(w):
            for y in range(h):
                color = TTkColor.bg( f"#{self._colorAt(x,y,w,h):06x}" )
                if (x,y)==self._selected:
                    canvas.drawText(pos=(x,y), text="◼", color=color+TTkColor.fg("#000000"))
                else:
                    canvas.drawText(pos=(x,y), text=" ", color=color)

class _TTkShowColor(TTkWidget):
    __slots__ = ('_color')
    def __init__(self, *,
                 color:TTkColor=TTkColor.RST,
                 **kwargs) -> None:
        self._color = color
        TTkWidget.__init__(self, **kwargs)

    def color(self) -> TTkColor:
        return self._color

    @pyTTkSlot(TTkColor)
    def setColor(self, color:TTkColor) -> None:
        if self._color != color:
            self._color = color
            self.update()

    @pyTTkSlot(int)
    def setRGBColor(self, color:int) -> None:
        self.setColor(TTkColor.bg( f"#{color:06x}" ))
        self.update()

    def paintEvent(self, canvas: TTkCanvas) -> None:
        w,h = self.size()
        for y in range(h):
            canvas.drawText(pos=(0,y),text=" "*w, color=self._color)

class _TTkColorButton(TTkButton):
    lastClicked = None

    colorClicked:pyTTkSignal
    '''
    This signal is emitted when a color is selected

    :param color:
    :type  color: :py:class:`TTkColor`
    '''
    __slots__ = ('colorClicked','_custom','_color','_returnType')
    def __init__(self, *,
                 color:TTkColor=TTkColor.RST,
                 returnType:TTkK.ColorPickerReturnType=TTkK.ColorPickerReturnType.Default,
                 custom:bool=False,
                 **kwargs) -> None:
        # Signals
        self.colorClicked = pyTTkSignal(TTkColor)

        self._color:TTkColor=color if color and color!=TTkColor.RST else TTkColor.BLACK
        self._custom=custom
        self._returnType=returnType
        super().__init__(**kwargs)
        self.clicked.connect(self._clicked)
        self.setColor(self._color)

    @pyTTkSlot(TTkColor)
    def setColor(self, color:TTkColor) -> None:
        self._color:TTkColor=color if color and color!=TTkColor.RST else TTkColor.BLACK
        style = self.style()
        for t in style:
            if 'color' in style[t]:
                if   color.hasForeground():
                    style[t]['color'] = color.foreground().invertFgBg()
                elif color.hasBackground():
                    style[t]['color'] = color.background()
                else:
                    style[t]['color'] = TTkColor.BG_BLACK
        self.setStyle(style)
        self.update()

    def returnType(self) -> TTkK.ColorPickerReturnType:
        return self._returnType

    def setReturnType(self, returnType:TTkK.ColorPickerReturnType) -> None:
        self._returnType = returnType

    def color(self) -> TTkColor:
        if self._returnType==TTkK.ColorPickerReturnType.Foreground:
            if self._color.hasForeground():
                return self._color.foreground()
            else:
                return self._color.background().invertFgBg()
        if self._returnType==TTkK.ColorPickerReturnType.Background:
            if self._color.hasBackground():
                return self._color.background()
            else:
                return self._color.foreground().invertFgBg()
        return self._color

    def isCustom(self) -> bool:
        return self._custom

    @pyTTkSlot()
    def _clicked(self) -> None:
        if self._custom:
            _TTkColorButton.lastClicked = self
        self.colorClicked.emit(self.color())

class TTkColorDialogPicker(TTkWindow):
    '''
    :py:class:`TTkColorDialogPicker` is a Color Picker Dialog, normally spawned from :py:class:`TTkColorButtonPicker`

    ::

        ╔═════════════════════════════════════════════════════════════════════════╗
        ║ Color Picker                                                      [^][x]║
        ╟────┤ Basic colors ├────┬────────────────────────────────────────────────╢
        ║┌──────┐┌──────┐┌──────┐│                                                ║
        ║│      ││      ││      ││                                                ║
        ║╘══════╛╘══════╛╘══════╛│                                                ║
        ║┌──────┐┌──────┐┌──────┐│                                                ║
        ║│      ││      ││      ││                                                ║
        ║╘══════╛╘══════╛╘══════╛│                                                ║
        ║┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐│                                                ║
        ║│  ││  ││  ││  ││  ││  ││        [Color Gradient]                        ║
        ║╘══╛╘══╛╘══╛╘══╛╘══╛╘══╛│                                                ║
        ╟───┤ Custom colors ├────┤                                                ║
        ║┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐│                                                ║
        ║│ ││ ││ ││ ││ ││ ││ ││ ││                                                ║
        ║╘═╛╘═╛╘═╛╘═╛╘═╛╘═╛╘═╛╘═╛│                                                ║
        ║[ Add to Custom Colors ]│                                                ║
        ╟──────┤ Conrols ├───────┤                                                ║
        ║ rgb:  136▲▼255▲▼ 255▲▼ │                                                ║
        ║      HTML: #88FFFF     │                                                ║
        ║      ┌────┐ ┌────────┐ │                                                ║
        ║      │ OK │ │ CANCEL │ │                                                ║
        ║      ╘════╛ ╘════════╛ │                                                ║
        ╚════════════════════════╧════════════════════════════════════════════════╝

    Quickstart:

    .. code-block:: python

        from TermTk import TTk,TTkColor,TTkColorDialogPicker,TTkLabel

        root = TTk()

        cdp = TTkColorDialogPicker(
                parent=root,
                pos=(3,3), size=(75,24), border=True,
                color=TTkColor.RED,
                title="Test Color Picker")

        lfg = TTkLabel(parent=root, pos=(0,0), text="Test Color")

        cdp.colorSelected.connect(lfg.setColor)

        root.mainloop()

    '''
    #     Terminal window (More or less, It is too annoying to redraw this)
    #     ┌────────────────────────────────────────────────┐
    #     │┌──────[Palette]───────┐┌────[Color]───────────┐│
    #     ││┌──────┐┌─────┐┌─────┐││┌────────────────────┐││
    #     │││RED   ││Green││Blue ││││                    │││
    #     ││└──────┘└─────┘└─────┘│││                    │││
    #     ││┌──────┐┌─────┐┌─────┐│││                    │││
    #     │││Purple││White││Black││││                    │││
    #     ││└──────┘└─────┘└─────┘│││   Color Canvas     │││
    #     ││┌──────┐┌─────┐┌─────┐│││                    │││
    #     │││...   ││     ││     ││││                    │││
    #     ││└──────┘└─────┘└─────┘││└────────────────────┘││
    #     ││┌──────┐┌─────┐┌─────┐││┌────────────────────┐││
    #     │││      ││     ││     ││││     HUE Canvas     │││
    #     ││└──────┘└─────┘└─────┘││└────────────────────┘││
    #     │└──────────────────────┘└──────────────────────┘│
    #     │┌───────[Custom]───────┐┌───────[Control]──────┐│
    #     ││┌──────┐┌─────┐┌─────┐││┌────┐        ┌──────┐││
    #     │││      ││     ││     ││││    │  Red:  └──────┘││
    #     ││└──────┘└─────┘└─────┘│││    │        ┌──────┐││
    #     ││┌──────┐┌─────┐┌─────┐│││    │  Green:└──────┘││
    #     │││      ││     ││     ││││    │        ┌──────┐││
    #     ││└──────┘└─────┘└─────┘││└────┘  Blue: └──────┘││
    #     ││ <Custom Color>       ││      ┌──────────────┐││
    #     ││ <OK>  <CANCEL>       ││HTML: └──────────────┘││
    #     │└──────────────────────┘└──────────────────────┘│
    #     └────────────────────────────────────────────────┘

    classStyle = {
                'default':     {'color': TTkColor.RST,
                                'fillColor':TTkColor.RST,
                                'borderColor': TTkColor.RST,
                                'titleColor': TTkColor.fg("#dddddd")+TTkColor.bg("#222222")},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'fillColor':TTkColor.RST,
                                'borderColor':TTkColor.fg('#888888'),
                                'titleColor': TTkColor.fg('#888888')},
                'focus':       {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044")+TTkColor.BOLD,
                                'fillColor':TTkColor.RST,
                                'borderColor': TTkColor.fg("#ffff55"),
                                'titleColor': TTkColor.fg("#ffffdd")+TTkColor.bg("#222222")},
            }

    customButtons = None

    colorSelected:pyTTkSignal
    '''
    This signal is emitted when a color is selected or the cancel button is pressed

    :param color: the current color
    :type  color: :py:class:`TTkColor`
    '''
    __slots__ = (
        '_color', '_returnType',
        '_colorCanvas', '_hueCanvas',
        '_isForeground',
        # '_redLE', '_greenLE', '_blueRE', '_htmlLE',
        # Signals
        'colorSelected'
        )
    def __init__(self, *,
                 color:TTkColor=TTkColor.RST,
                 returnType:TTkK.ColorPickerReturnType=TTkK.ColorPickerReturnType.Default,
                 **kwargs) -> None:
        '''
        :param color: the current color
        :type  color: :py:class:`TTkColor`
        :param returnType: the type of the returuning color
        :type  returnType: :py:class:`TTkK.ColorPickerReturnType`
        '''
        # Signals
        self.colorSelected = pyTTkSignal(TTkColor)
        self._returnType=returnType
        self._color:TTkColor=color if color and color!=TTkColor.RST else TTkColor.BLACK
        self._isForeground:bool = color.hasForeground() or not color.hasBackground()
        super().__init__(**kwargs)
        self.setWindowFlag(TTkK.WindowFlag.WindowMaximizeButtonHint | TTkK.WindowFlag.WindowCloseButtonHint)
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
        def _okPressed() -> None:
            color = sc.color().invertFgBg() if self._isForeground else sc.color()
            # self.setColor(color)
            self.colorSelected.emit(color)
            self.close()

        okButton.clicked.connect(_okPressed)

        @pyTTkSlot()
        def _cancelPressed() -> None:
            self.colorSelected.emit(self._color)
            self.close()

        cancelButton.clicked.connect(_cancelPressed)

        @pyTTkSlot(int)
        def _controlSetRGBColor(color:int) -> None:
            sc.setRGBColor(color)
            leR.setValue((color&0xff0000)>>16)
            leG.setValue((color&0x00ff00)>> 8)
            leB.setValue((color&0x0000ff)>> 0)
            leHTML.setText(f"#{color:06X}")

        @pyTTkSlot(TTkColor)
        def _controlSetColor(color:TTkColor) -> None:
            r,g,b = color.fgToRGB()
            numColor = r<<16|g<<8|b
            _controlSetRGBColor(numColor)

        @pyTTkSlot()
        def _leHTMLChanged() -> None:
            text = leHTML.text()
            if re.match('#[a-f0-9]{6}', str(text).lower()):
                _controlSetRGBColor(int(str(text)[1:], 16))

        leHTML.returnPressed.connect(_leHTMLChanged)

        @pyTTkSlot(int)
        def _leRGBChanged(value:int) -> None:
            r = leR.value()
            g = leG.value()
            b = leB.value()
            if r&(~0xff) or r&(~0xff) or r&(~0xff): return
            _controlSetRGBColor(r<<16|g<<8|b)

        leR.valueChanged.connect(_leRGBChanged)
        leG.valueChanged.connect(_leRGBChanged)
        leB.valueChanged.connect(_leRGBChanged)

        _controlSetColor(self._color if self._isForeground else self._color.invertFgBg())

        # Palette Layout Widgets
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#ff0000'), border=True, maxSize=(8,3)),0,0,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#ffff00'), border=True, maxSize=(8,3)),0,2,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#00ff00'), border=True, maxSize=(8,3)),0,4,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#00ffff'), border=True, maxSize=(8,3)),1,0,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#0000ff'), border=True, maxSize=(8,3)),1,2,1,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#ff00ff'), border=True, maxSize=(8,3)),1,4,1,2)
        b.colorClicked.connect(_controlSetColor)

        # Shades of Grey
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#ffffff'), border=True, maxSize=(4,3)),2,0)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#dddddd'), border=True, maxSize=(4,3)),2,1)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#aaaaaa'), border=True, maxSize=(4,3)),2,2)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#666666'), border=True, maxSize=(4,3)),2,3)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#333333'), border=True, maxSize=(4,3)),2,4)
        b.colorClicked.connect(_controlSetColor)
        paletteLayout.addWidget(b:=_TTkColorButton(color=TTkColor.fg('#000000'), border=True, maxSize=(4,3)),2,5)
        b.colorClicked.connect(_controlSetColor)

        # Custom frame
        if TTkColorDialogPicker.customButtons is None:
            TTkColorDialogPicker.customButtons = (
                    _TTkColorButton(color=TTkColor.fg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.fg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.fg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.fg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.fg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.fg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.fg('#ffffff'), custom=True, border=True, maxSize=(3,3)) ,
                    _TTkColorButton(color=TTkColor.fg('#ffffff'), custom=True, border=True, maxSize=(3,3)) )


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

        _TTkColorButton.lastClicked = TTkColorDialogPicker.customButtons[0]

        customLayout.addWidget(b:=TTkButton(border=False, text='Add to Custom Colors'),1,0,1,8)
        customLayout.update()

        @pyTTkSlot()
        def _addCustomPressed() -> None:
            btn = _TTkColorButton.lastClicked
            TTkLog.debug(f"{btn}")
            if btn is not None and \
               btn.isCustom():
                TTkLog.debug(f"2 {btn}")
                btn.setColor(sc.color().invertFgBg().foreground())
        b.clicked.connect(_addCustomPressed)

        # Events
        self._colorCanvas.colorPicked.connect(_controlSetRGBColor)

        self.layout().addItem(leftLayout ,0,0)
        self.layout().addItem(colorLayout ,0,1)

        leftLayout.addItem(paletteLayout)
        leftLayout.addItem(customLayout)
        leftLayout.addItem(controlLayout)

    def _colorToBg(self) -> TTkColor:
        if self._isForeground:
            return self._color.invertFgBg()
        else:
            return self._color

    def _colorToFg(self) -> TTkColor:
        if self._isForeground:
            return self._color
        else:
            return self._color.invertFgBg()

    def color(self) -> TTkColor:
        '''
        :return: the current color
        :rtype: :py:class:`TTkColor`
        '''
        if self._returnType==TTkK.ColorPickerReturnType.Foreground:
            if self._color.hasForeground():
                return self._color.foreground()
            else:
                return self._color.background().invertFgBg()
        if self._returnType==TTkK.ColorPickerReturnType.Background:
            if self._color.hasBackground():
                return self._color.background()
            else:
                return self._color.foreground().invertFgBg()
        return self._color

    def setColor(self, color:TTkColor) -> None:
        '''
        Set the current color

        :param color:
        :type  color: :py:class:`TTkColor`
        '''
        if self._color != color:
            self._color:TTkColor=color if color and color!=TTkColor.RST else TTkColor.BLACK
            self.update()

    def paintEvent(self, canvas):
        TTkWindow.paintEvent(self, canvas)
        style = self.currentStyle()
        color = style['borderColor']
        titleColor = style['titleColor']

        canvas.drawGrid(
            pos=(0,2),size=(26,self._height-2),
            hlines=(10,15), vlines=(),
            color=color, grid=6)
        gg = TTkCfg.theme.grid[6]
        canvas.drawChar(pos=(0,2),  char=gg[0x08], color=color)
        canvas.drawChar(pos=(25,2), char=gg[0x02], color=color)
        canvas.drawChar(pos=(25,self._height-1), char=gg[0x0E], color=color)
        canvas.drawBoxTitle(pos=(0,2) , size=(26,0), text=TTkString(" Basic colors "), align=TTkK.CENTER_ALIGN, color=color, colorText=titleColor)
        canvas.drawBoxTitle(pos=(0,12), size=(26,0), text=TTkString(" Custom colors "), align=TTkK.CENTER_ALIGN, color=color, colorText=titleColor)
        canvas.drawBoxTitle(pos=(0,17), size=(26,0), text=TTkString(" Conrols "), align=TTkK.CENTER_ALIGN, color=color, colorText=titleColor)

class TTkColorButtonPicker(_TTkColorButton):
    '''
    :py:class:`TTkColorButtonPicker` is a button widget that spawn, if pressed, a :py:class:`TTkColorDialogPicker` can be used to choose a :py:class:`TTkColor`.

    Quickstart:

    .. code-block:: python

        import TermTk as ttk

        root = ttk.TTk()

        btn = ttk.TTkColorButtonPicker(
                parent=root,
                size=(8,3),
                border=True,
                color=ttk.TTkColor.RED )

        lfg = ttk.TTkLabel(parent=root, pos=(0,3), text="Test FG")
        lbg = ttk.TTkLabel(parent=root, pos=(0,4), text="Test BG")

        btn.colorSelectedFG.connect(lfg.setColor)
        btn.colorSelectedBG.connect(lbg.setColor)

        root.mainloop()

    '''

    colorSelected:pyTTkSignal
    '''
    This signal is emitted when a color is chosen (with the "OK" button in the :py:class:`TTkColorDialogPicker`)

    :param color: the Color
    :type  color: :py:class:`TTkColor`
    '''
    colorSelectedFG:pyTTkSignal
    '''
    This signal is emitted when a color is chosen (with the "OK" button in the :py:class:`TTkColorDialogPicker`)

    :param fgColor: the Foreground Color
    :type  fgColor: :py:class:`TTkColor`
    '''
    colorSelectedBG:pyTTkSignal
    '''
    This signal is emitted when a color is chosen (with the "OK" button in the :py:class:`TTkColorDialogPicker`)

    This is a convenience signal that mrrors :py:class:`colorSelectedFG` providing a background color instead.

    :param bgColor: the Background Color
    :type  bgColor: :py:class:`TTkColor`
    '''

    __slots__ = ('colorSelected','colorSelectedFG', 'colorSelectedBG')
    def __init__(self, **kwargs) -> None:
        '''
        :param color: the current color
        :type  color: :py:class:`TTkColor`
        :param returnType: the type of the returuning color
        :type  returnType: :py:class:`TTkK.ColorPickerReturnType`
        '''
        # Signals
        self.colorSelected   = pyTTkSignal(TTkColor)
        self.colorSelectedFG = pyTTkSignal(TTkColor)
        self.colorSelectedBG = pyTTkSignal(TTkColor)
        super().__init__(**kwargs)
        self._custom = False
        self.clicked.connect(self._colorClicked)

    @pyTTkSlot()
    def _colorClicked(self):
        colorPicker = TTkColorDialogPicker(pos = (3,3), size=(75,24), color=self.color(), title="Test Color Picker", border=True)
        colorPicker.colorSelected.connect(self.setColor)
        colorPicker.colorSelected.connect(self._processColorSelected)
        TTkHelper.overlay(self, colorPicker, -1,-1, True)

    @pyTTkSlot(TTkColor)
    def _processColorSelected(self, color:TTkColor):
        if   color.hasForeground():
            fg = color.foreground()
            bg = color.foreground().invertFgBg()
        elif color.hasBackground():
            fg = color.background().invertFgBg()
            bg = color.background()
        else:
            fg = TTkColor.BLACK
            bg = TTkColor.BG_BLACK

        self.colorSelected.emit(color)
        self.colorSelectedFG.emit(fg)
        self.colorSelectedBG.emit(bg)
