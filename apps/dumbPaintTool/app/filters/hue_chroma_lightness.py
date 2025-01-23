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

__all__ = ['HueChromaLightness']

import TermTk as ttk

from ..glbls import glbls
from ..canvaslayer import CanvasLayer


class HueChromaLightness(ttk.TTkWindow):
    __slots__ = ('_sl_hue','_sl_chroma','_sl_lightness',
                 '_sb_hue','_sb_chroma','_sb_lightness',
                 '_canvasLayer','_colorCopy','_colorCopy2')
    def __init__(self, canvasLayer:CanvasLayer, **kwargs):
        layout = ttk.TTkGridLayout()
        super().__init__(**kwargs|{"layout":layout,'size':(50,13)})
        self.setTitle("Hue Chroma Lightness")
        self._sl_hue       = sl_hue       = ttk.TTkSlider( minimum=-180, maximum=180, orientation=ttk.TTkK.HORIZONTAL)
        self._sl_chroma    = sl_chroma    = ttk.TTkSlider( minimum=-100, maximum=100, orientation=ttk.TTkK.HORIZONTAL)
        self._sl_lightness = sl_lightness = ttk.TTkSlider( minimum=-100, maximum=100, orientation=ttk.TTkK.HORIZONTAL)
        self._sb_hue       = sb_hue       = ttk.TTkSpinBox(minimum=-180, maximum=180)
        self._sb_chroma    = sb_chroma    = ttk.TTkSpinBox(minimum=-100, maximum=100)
        self._sb_lightness = sb_lightness = ttk.TTkSpinBox(minimum=-100, maximum=100)

        self._canvasLayer = canvasLayer
        self._colorCopy  = [r.copy() for r in canvasLayer._colors]
        self._colorCopy2 = [r.copy() for r in canvasLayer._colors]

        btn_ok     = ttk.TTkButton(border=True, text="OK")
        # btn_apply  = ttk.TTkButton(border=True, text="APPLY")
        btn_reset  = ttk.TTkButton(border=True, text="RESET")
        btn_cancel = ttk.TTkButton(border=True, text="CANCEL")

        layout.addWidget(sl_hue      ,1,0,1,3)
        layout.addWidget(sl_chroma   ,3,0,1,3)
        layout.addWidget(sl_lightness,5,0,1,3)
        layout.addWidget(sb_hue      ,0,1)
        layout.addWidget(sb_chroma   ,2,1)
        layout.addWidget(sb_lightness,4,1)
        layout.addWidget(ttk.TTkLabel(text="Hue")      ,0,0)
        layout.addWidget(ttk.TTkLabel(text="Chroma")   ,2,0)
        layout.addWidget(ttk.TTkLabel(text="Lightness"),4,0)

        # layout.addWidget(btn_apply,6,0)
        layout.addWidget(btn_reset, 6,0)
        layout.addWidget(btn_cancel,6,1)
        layout.addWidget(btn_ok,    6,2)

        sl_hue.valueChanged.connect(      self._processChange)
        sl_hue.valueChanged.connect(      sb_hue.setValue)
        sb_hue.valueChanged.connect(      sl_hue.setValue)
        sl_chroma.valueChanged.connect(   self._processChange)
        sl_chroma.valueChanged.connect(   sb_chroma.setValue)
        sb_chroma.valueChanged.connect(   sl_chroma.setValue)
        sl_lightness.valueChanged.connect(self._processChange)
        sl_lightness.valueChanged.connect(sb_lightness.setValue)
        sb_lightness.valueChanged.connect(sl_lightness.setValue)

        btn_ok.clicked.connect(self.close)
        btn_reset.clicked.connect(self._reset)
        btn_cancel.clicked.connect(self._cancel)

    @ttk.pyTTkSlot()
    def _reset(self):
        self._sl_hue.setValue(0)
        self._sl_chroma.setValue(0)
        self._sl_lightness.setValue(0)
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
        hue       = self._sl_hue.value()
        chroma    = self._sl_chroma.value()
        lightness = self._sl_lightness.value()
        self._resetCopy()
        self._changeCB(hue          ,change_hue)
        self._changeCB(chroma   /100,change_chroma)
        self._changeCB(lightness/100,change_lightness)
        self._pushChanges()

def rgb_to_hsl(red, green, blue):
    # Convert RGB to HSL
    r = red / 255.0
    g = green / 255.0
    b = blue / 255.0

    max_color = max(r, g, b)
    min_color = min(r, g, b)
    delta = max_color - min_color

    # Calculate Lightness
    lightness = (max_color + min_color) / 2.0

    # Calculate Saturation
    if delta == 0:
        saturation = 0
    else:
        if lightness < 0.5:
            saturation = delta / (max_color + min_color)
        else:
            saturation = delta / (2.0 - max_color - min_color)

    # Calculate Hue
    if delta == 0:
        hue = 0
    else:
        if max_color == r:
            hue = 60 * (((g - b) / delta) % 6)
        elif max_color == g:
            hue = 60 * (((b - r) / delta) + 2)
        else:  # max_color == b
            hue = 60 * (((r - g) / delta) + 4)

    return hue, saturation, lightness

def hsl_to_rgb(hue, saturation, lightness):
    # Convert HSL to RGB
    if saturation == 0:
        r = g = b = lightness
    else:
        if lightness < 0.5:
            temp2 = lightness * (1 + saturation)
        else:
            temp2 = lightness + saturation - (lightness * saturation)

        temp1 = 2 * lightness - temp2

        hue /= 360

        def hue_to_rgb(temp1, temp2, hue):
            if hue < 0:
                hue += 1
            elif hue > 1:
                hue -= 1

            if 6 * hue < 1:
                return temp1 + (temp2 - temp1) * 6 * hue
            elif 2 * hue < 1:
                return temp2
            elif 3 * hue < 2:
                return temp1 + (temp2 - temp1) * ((2 / 3 - hue) * 6)
            else:
                return temp1

        r = hue_to_rgb(temp1, temp2, hue + 1/3)
        g = hue_to_rgb(temp1, temp2, hue)
        b = hue_to_rgb(temp1, temp2, hue - 1/3)

    return int(r * 255), int(g * 255), int(b * 255)

def change_hue(rgb, target_hue):
    # Extract RGB components
    red, green, blue = rgb

    # Convert RGB to HSL
    hue, saturation, lightness = rgb_to_hsl(red, green, blue)

    # Set the new hue
    hue += target_hue

    # Convert HSL back to RGB
    new_red, new_green, new_blue = hsl_to_rgb(hue, saturation, lightness)

    return new_red, new_green, new_blue

def change_chroma(rgb, target_chroma):
    # Extract RGB components
    red, green, blue = rgb

    # Convert RGB to HSL
    hue, saturation, lightness = rgb_to_hsl(red, green, blue)

    # Set the new saturation
    # ttk.TTkLog.debug(f"{saturation=} {target_chroma+saturation=}")
    saturation = min(max(target_chroma+saturation, 0), 1)  # Ensure saturation is within [0, 1]
    # Convert HSL back to RGB
    new_red, new_green, new_blue = hsl_to_rgb(hue, saturation, lightness)

    return new_red, new_green, new_blue

def change_lightness(rgb, target_lightness):
    # Extract RGB components
    red, green, blue = rgb

    # Convert RGB to HSL
    hue, saturation, lightness = rgb_to_hsl(red, green, blue)

    # Set the new lightness
    lightness = min(max(target_lightness+lightness, 0), 1)  # Ensure lightness is within [0, 1]

    # Convert HSL back to RGB
    new_red, new_green, new_blue = hsl_to_rgb(hue, saturation, lightness)

    return new_red, new_green, new_blue

