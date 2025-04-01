# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['BrightnessContrast']

import TermTk as ttk

from ..glbls import glbls
from ..canvaslayer import CanvasLayer


class BrightnessContrast(ttk.TTkWindow):
    __slots__ = ('_sl_brightness','_sl_contrast',
                 '_sb_brightness','_sb_contrast',
                 '_canvasLayer','_colorCopy','_colorCopy2')
    def __init__(self, canvasLayer:CanvasLayer, **kwargs):
        layout = ttk.TTkGridLayout()
        super().__init__(**kwargs|{"layout":layout,'size':(50,11)})
        self.setTitle("Brightness Contrast")
        self._sl_brightness = sl_brightness = ttk.TTkSlider( minimum=-256, maximum=256, orientation=ttk.TTkK.HORIZONTAL)
        self._sl_contrast   = sl_contrast   = ttk.TTkSlider( minimum=-256, maximum=512, orientation=ttk.TTkK.HORIZONTAL)
        self._sb_brightness = sb_brightness = ttk.TTkSpinBox(minimum=-256, maximum=256)
        self._sb_contrast   = sb_contrast   = ttk.TTkSpinBox(minimum=-256, maximum=512)

        self._canvasLayer = canvasLayer
        self._colorCopy  = [r.copy() for r in canvasLayer._colors]
        self._colorCopy2 = [r.copy() for r in canvasLayer._colors]

        btn_ok     = ttk.TTkButton(border=True, text="OK")
        # btn_apply  = ttk.TTkButton(border=True, text="APPLY")
        btn_reset  = ttk.TTkButton(border=True, text="RESET")
        btn_cancel = ttk.TTkButton(border=True, text="CANCEL")

        layout.addWidget(sl_brightness ,1,0,1,3)
        layout.addWidget(sl_contrast   ,3,0,1,3)
        layout.addWidget(sb_brightness ,0,1)
        layout.addWidget(sb_contrast   ,2,1)
        layout.addWidget(ttk.TTkLabel(text="Brightness") ,0,0)
        layout.addWidget(ttk.TTkLabel(text="Contrast")   ,2,0)

        # layout.addWidget(btn_apply,6,0)
        layout.addWidget(btn_reset, 4,0)
        layout.addWidget(btn_cancel,4,1)
        layout.addWidget(btn_ok,    4,2)

        sl_brightness.valueChanged.connect( self._processChange)
        sl_brightness.valueChanged.connect( sb_brightness.setValue)
        sb_brightness.valueChanged.connect( sl_brightness.setValue)
        sl_contrast.valueChanged.connect(   self._processChange)
        sl_contrast.valueChanged.connect(   sb_contrast.setValue)
        sb_contrast.valueChanged.connect(   sl_contrast.setValue)

        btn_ok.clicked.connect(self.close)
        btn_reset.clicked.connect(self._reset)
        btn_cancel.clicked.connect(self._cancel)

    @ttk.pyTTkSlot()
    def _reset(self):
        self._sl_brightness.setValue(0)
        self._sl_contrast.setValue(0)
        self._resetCopy()
        self._pushChanges()

    @ttk.pyTTkSlot()
    def _cancel(self):
        self._reset()
        self.close()

    def _resetCopy(self):
        self._colorCopy2 = [r.copy() for r in self._colorCopy]
    def _pushChanges(self):
        self._canvasLayer._preview = None
        self._canvasLayer._colors = self._colorCopy2
        self._canvasLayer.update()

    @ttk.pyTTkSlot(int)
    def _changeCB(self, value, cb):
        for y,row in enumerate(self._colorCopy2):
            for x,c in enumerate(row):
                fg = c.fgToRGB() if c._fg else None
                bg = c.bgToRGB() if c._bg else None
                fg = cb(fg,value) if fg else None
                bg = cb(bg,value) if bg else None
                newColor = ttk.TTkColor()
                newColor._fg = fg
                newColor._bg = bg
                self._colorCopy2[y][x] = newColor

    def _processChange(self):
        br = self._sl_brightness.value()
        co = self._sl_contrast.value()
        self._resetCopy()
        for row in self._colorCopy2:
            for x,c in enumerate(row):
                fg = c.fgToRGB() if c._fg else None
                bg = c.bgToRGB() if c._bg else None
                fg = adjust_BC(fg,br,1+co/256) if fg else None
                bg = adjust_BC(bg,br,1+co/256) if bg else None
                newColor = ttk.TTkColor()
                newColor._fg = fg
                newColor._bg = bg
                row[x] = newColor
        self._pushChanges()

def adjust_BC(rgb, br, co):
    # Extract RGB components
    red, green, blue = rgb

    # Apply brightness adjustment to each channel
    new_red   = min(max(br+128+(red  -128)*co, 0), 255)
    new_green = min(max(br+128+(green-128)*co, 0), 255)
    new_blue  = min(max(br+128+(blue -128)*co, 0), 255)

    return int(new_red), int(new_green), int(new_blue)