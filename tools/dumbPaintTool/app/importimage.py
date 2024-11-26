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

__all__ = ['ImportImage']

from PIL import Image

import TermTk as ttk

class TTkImageNew(ttk.TTkWidget):
    FULLBLOCK = 0x00
    HALFBLOCK = 0x01
    QUADBLOCK = 0x02
    SEXBLOCK   = 0x03

    _quadMap =[
        # 0x00 0x01 0x02 0x03
          ' ', '▘', '▝', '▀',
        # 0x04 0x05 0x06 0x07
          '▖', '▌', '▞', '▛',
        # 0x08 0x09 0x0A 0x0B
          '▗', '▚', '▐', '▜',
        # 0x0C 0x0D 0x0E 0x0F
          '▄', '▙', '▟', '█']

    _sexMap  = [
        # 0x00 0x01 0x02 0x03 0x04 0x05 0x06 0x07
          ' ', '🬀', '🬁', '🬂', '🬃', '🬄', '🬅', '🬆',
        # 0x08 0x09 0x0A 0x0B 0x0C 0x0D 0x0E 0x0F
          '🬇', '🬈', '🬉', '🬊', '🬋', '🬌', '🬍', '🬎',

        # 0x10 0x11 0x12 0x13 0x14 0x15 0x16 0x17
          '🬏', '🬐', '🬑', '🬒', '🬓', '▌', '🬔', '🬕',
        # 0x18 0x19 0x1A 0x1B 0x1C 0x1D 0x1E 0x1F
          '🬖', '🬗', '🬘', '🬙', '🬚', '🬛', '🬜', '🬝',

        # 0x20 0x21 0x22 0x23 0x24 0x25 0x26 0x27
          '🬞', '🬟', '🬠', '🬡', '🬢', '🬣', '🬤', '🬥',
        # 0x28 0x29 0x2A 0x2B 0x2C 0x2D 0x2E 0x2F
          '🬦', '🬧', '▐', '🬨', '🬩', '🬪', '🬫', '🬬',

        # 0x30 0x31 0x32 0x33 0x34 0x35 0x36 0x37
          '🬭', '🬮', '🬯', '🬰', '🬱', '🬲', '🬳', '🬴',
        # 0x38 0x39 0x3A 0x3B 0x3C 0x3D 0x3E 0x3F
          '🬵', '🬶', '🬷', '🬸', '🬹', '🬺', '🬻', '█']

    __slots__ = ('_data', '_rasterType', '_canvasImage', '_alphaThreshold')
    def __init__(self, **kwargs):
        self._alphaThreshold = 127
        self._rasterType = kwargs.get('rasteriser' , ttk.TTkImage.QUADBLOCK )
        self._data = kwargs.get('data' , [] )
        self._canvasImage = ttk.TTkCanvas()
        self._canvasImage.setTransparent(True)
        super().__init__(**kwargs)
        if self._data:
            self.setData(self._data)

    def toTTkString(self):
        return ttk.TTkString(self._canvasImage.toAnsi())

    def alphaThrteshold(self):
        return self._alphaThreshold

    @ttk.pyTTkSlot(int)
    def setAlphaThreshold(self, value):
        value = max(0,min(255,value))
        if value == self._alphaThreshold:return
        self._alphaThreshold = value
        self._drawImage(self._canvasImage)
        self.update()

    def setData(self, data):
        self._data = data
        w = min(len(i) for i in self._data)
        h = len(self._data)
        if w>0<h and len(data[0][0])==3: # Add alpha channel if missing
            self._data = [[(r,g,b,255) for r,g,b in row] for row in data]
        if self._rasterType == ttk.TTkImage.FULLBLOCK:
            w,h = w,h
        elif self._rasterType == ttk.TTkImage.HALFBLOCK:
            w,h = w,h//2
        elif self._rasterType == ttk.TTkImage.QUADBLOCK:
            w,h = w//2,h//2
        elif self._rasterType == ttk.TTkImage.SEXBLOCK:
            w,h = w//2,h//3
        self._canvasImage.resize(*(self.size()))
        self.resize(w,h)
        self._canvasImage.resize(w,h)
        self._canvasImage.updateSize()
        self._drawImage(self._canvasImage)
        self.update()

    def setRasteriser(self, rasteriser):
        if self._rasterType == rasteriser: return
        self._rasterType = rasteriser
        if self._data:
            self.setData(self._data)

    def _reduceQuad(self, a,b,c,d):
        # quadblitter notcurses like
        th = self._alphaThreshold
        l = [a,b,c,d]
        lth = [(px,1<<i) for i,px in enumerate(l) if px[3]>=th]
        if not lth:
            # Transparent block
            return ttk.TTkString(' ')

        if (ll:=len(lth))<4:
            # Semi-Transparent Block
            cr = sum(px[0] for px,_ in lth)//ll
            cg = sum(px[1] for px,_ in lth)//ll
            cb = sum(px[2] for px,_ in lth)//ll
            ch = sum(g     for  _,g in lth)
            color = ttk.TTkColor.fg(f'#{cr:02X}{cg:02X}{cb:02X}')
            return ttk.TTkString(ttk.TTkImage._quadMap[ch],color)

        if a[:3]==b[:3]==c[:3]==d[:3]:
            color = ttk.TTkColor.bg(f'#{a[0]:02X}{a[1]:02X}{a[2]:02X}')
            return ttk.TTkString(' ',color)

        def delta(i):
            return max(v[i] for v in l) - min(v[i] for v in l)
        deltaR = delta(0)
        deltaG = delta(1)
        deltaB = delta(2)

        def midColor(c1,c2):
            return ((c1[0]+c2[0])//2,(c1[1]+c2[1])//2,(c1[2]+c2[2])//2)

        def closer(a,b,c):
            return \
                ( (a[0]-c[0])**2 + (a[1]-c[1])**2 + (a[2]-c[2])**2 ) > \
                ( (b[0]-c[0])**2 + (b[1]-c[1])**2 + (b[2]-c[2])**2 )

        def splitReduce(i):
            s = sorted(l,key=lambda x:x[i])
            mid = (s[3][i]+s[0][i])//2
            if s[1][i] < mid:
                if s[2][i] > mid:
                    c1 = midColor(s[0],s[1])
                    c2 = midColor(s[2],s[3])
                else:
                    c1 = midColor(s[0],s[1])
                    c1 = midColor(c1,s[2])
                    c2 = s[3]
            else:
                c1 = s[0]
                c2 = midColor(s[1],s[2])
                c2 = midColor(c1,s[3])


            ch  = 0x01 if closer(c1,c2,l[0]) else 0
            ch |= 0x02 if closer(c1,c2,l[1]) else 0
            ch |= 0x04 if closer(c1,c2,l[2]) else 0
            ch |= 0x08 if closer(c1,c2,l[3]) else 0

            return  ttk.TTkString() + \
                    (ttk.TTkColor.bg(f'#{c1[0]:02X}{c1[1]:02X}{c1[2]:02X}') +
                     ttk.TTkColor.fg(f'#{c2[0]:02X}{c2[1]:02X}{c2[2]:02X}')) + \
                    ttk.TTkImage._quadMap[ch]

        if deltaR >= deltaG and deltaR >= deltaB:
            # Use Red as splitter
            return splitReduce(0)
        elif deltaG >= deltaB and deltaG >= deltaR:
            # Use Green as splitter
            return splitReduce(1)
        else:
            # Use Blue as splitter
            return splitReduce(2)

    def _reduceSex(self, a,b,c,d,e,f):
        # quadblitter notcurses like
        th = self._alphaThreshold
        l = [a,b,c,d,e,f]
        lth = [(px,1<<i) for i,px in enumerate(l) if px[3]>=th]
        if not lth:
            # Transparent block
            return ttk.TTkString(' ')

        if (ll:=len(lth))<4:
            # Semi-Transparent Block
            cr = sum(px[0] for px,_ in lth)//ll
            cg = sum(px[1] for px,_ in lth)//ll
            cb = sum(px[2] for px,_ in lth)//ll
            ch = sum(g     for  _,g in lth)
            color = ttk.TTkColor.fg(f'#{cr:02X}{cg:02X}{cb:02X}')
            return ttk.TTkString(ttk.TTkImage._sexMap[ch],color)

        if a[:3]==b[:3]==c[:3]==d[:3]==e[:3]==f[:3]:
            color = ttk.TTkColor.bg(f'#{a[0]:02X}{a[1]:02X}{a[2]:02X}')
            return ttk.TTkString(' ',color)

        def delta(i):
            return max(v[i] for v in l) - min(v[i] for v in l)
        deltaR = delta(0)
        deltaG = delta(1)
        deltaB = delta(2)

        def midColor(c1,c2):
            return ((c1[0]+c2[0])//2,(c1[1]+c2[1])//2,(c1[2]+c2[2])//2)

        def closer(a,b,c):
            return \
                ( (a[0]-c[0])**2 + (a[1]-c[1])**2 + (a[2]-c[2])**2 ) > \
                ( (b[0]-c[0])**2 + (b[1]-c[1])**2 + (b[2]-c[2])**2 )

        def splitReduce(i):
            s = sorted(l,key=lambda x:x[i])
            mid = (s[5][i]+s[0][i])//2
            if s[1][i] < mid:
                if s[2][i] > mid:
                    c1 = midColor(s[0],s[1])
                    c2 = midColor(s[2],s[3])
                else:
                    c1 = midColor(s[0],s[1])
                    c1 = midColor(c1,s[2])
                    c2 = s[3]
            else:
                c1 = s[0]
                c2 = midColor(s[1],s[2])
                c2 = midColor(c1,s[3])


            ch  = 0x01 if closer(c1,c2,l[0]) else 0
            ch |= 0x02 if closer(c1,c2,l[1]) else 0
            ch |= 0x04 if closer(c1,c2,l[2]) else 0
            ch |= 0x08 if closer(c1,c2,l[3]) else 0
            ch |= 0x10 if closer(c1,c2,l[4]) else 0
            ch |= 0x20 if closer(c1,c2,l[5]) else 0

            return  ttk.TTkString() + \
                    (ttk.TTkColor.bg(f'#{c1[0]:02X}{c1[1]:02X}{c1[2]:02X}') +
                     ttk.TTkColor.fg(f'#{c2[0]:02X}{c2[1]:02X}{c2[2]:02X}')) + \
                    ttk.TTkImage._sexMap[ch]

        if deltaR >= deltaG and deltaR >= deltaB:
            # Use Red as splitter
            return splitReduce(0)
        elif deltaG >= deltaB and deltaG >= deltaR:
            # Use Green as splitter
            return splitReduce(1)
        else:
            # Use Blue as splitter
            return splitReduce(2)

    def rotHue(self, deg):
        old = self._data
        self._data = [[p for p in l ] for l in old]
        for row in self._data:
            for i,pixel in enumerate(row):
                h,s,l = ttk.TTkColor.rgb2hsl(pixel)
                row[i] = ttk.TTkColor.hsl2rgb(((h+deg)%360,s,l))
        self.setData(self._data)

    def _drawImage(self, canvas):
        img = self._data
        threshold = self._alphaThreshold
        if self._rasterType == ttk.TTkImage.FULLBLOCK:
            for y in range(0, len(img)):
                for x in range(0, len(img[y])):
                    r,g,b,a = img[y][x]
                    color = ttk.TTkColor.bg(f'#{r:02X}{g:02X}{b:02X}') if a>threshold else ttk.TTkColor.RST
                    canvas.drawChar(pos=(x,y), char=' ', color=color)
        elif self._rasterType == ttk.TTkImage.HALFBLOCK:
            for y in range(0, len(img)&(~1), 2):
                for x in range(0, len(img[y])):
                    c1, c2 = img[y][x] ,img[y+1][x]
                    if c1[3]<threshold and c2[3]<threshold:
                        canvas.drawChar(pos=(x,y//2), char=' ', color=ttk.TTkColor.RST)
                    elif c2[3]<threshold:
                        color = ttk.TTkColor.fg(f'#{c1[0]:02X}{c1[1]:02X}{c1[2]:02X}')
                        canvas.drawChar(pos=(x,y//2), char='▀', color=color)
                    elif c1[3]<threshold:
                        color = ttk.TTkColor.fg(f'#{c2[0]:02X}{c2[1]:02X}{c2[2]:02X}')
                        canvas.drawChar(pos=(x,y//2), char='▄', color=color)
                    elif c1[:3]==c2[:3]:
                        color = ttk.TTkColor.bg(f'#{c1[0]:02X}{c1[1]:02X}{c1[2]:02X}')
                        canvas.drawChar(pos=(x,y//2), char=' ', color=color)
                    else:
                        color = ( ttk.TTkColor.fg(f'#{c1[0]:02X}{c1[1]:02X}{c1[2]:02X}') +
                                  ttk.TTkColor.bg(f'#{c2[0]:02X}{c2[1]:02X}{c2[2]:02X}') )
                        canvas.drawChar(pos=(x,y//2), char='▀', color=color)
        elif self._rasterType == ttk.TTkImage.QUADBLOCK:
            for y in range(0, len(img)&(~1), 2):
                for x in range(0, min(len(img[y])&(~1),len(img[y+1])&(~1)), 2):
                    canvas.drawText(
                            pos=(x//2,y//2),
                            text=self._reduceQuad(
                                        img[y][x]   , img[y][x+1]   ,
                                        img[y+1][x] , img[y+1][x+1] ))
        elif self._rasterType == ttk.TTkImage.SEXBLOCK:
            for y in range(0, len(img)-2, 3):
                for x in range(0, min(len(img[y])-1,len(img[y+1])-1,len(img[y+2])-1), 2):
                    canvas.drawText(
                            pos=(x//2,y//3),
                            text=self._reduceSex(
                                        img[y][x]   , img[y][x+1]   ,
                                        img[y+1][x] , img[y+1][x+1] ,
                                        img[y+2][x] , img[y+2][x+1] ))

    def paintEvent(self, canvas: ttk.TTkCanvas):
        w,h=self.size()
        s = (0,0,w,h)
        for y,(rowd,rowc) in enumerate(zip(self._canvasImage._data[:h],self._canvasImage._colors[:h])):
            for x,(gl,c) in enumerate(zip(rowd[:w],rowc[:w])):
                if gl == ' ' and not c.hasBackground():
                    continue
                elif gl == ' ':
                    canvas._data[  y][x] = ' '
                    canvas._colors[y][x] = c.background()
                elif not c.hasBackground():
                    nbg = canvas._colors[y][x].background()
                    canvas._data[  y][x] = gl
                    canvas._colors[y][x] = c.foreground() + nbg
                else:
                    canvas._data[  y][x] = gl
                    canvas._colors[y][x] = c

class ImagePreview(TTkImageNew):
    __slots__ = ('_trColor1','_trColor2')
    def __init__(self, **kwargs):
        self._trColor1 = ttk.TTkColor.bg("#777777")
        self._trColor2 = ttk.TTkColor.bg("#bbbbbb")
        super().__init__(**kwargs)

    def setTransparentColor(self, c:ttk.TTkColor):
        r,g,b = c.bgToRGB()
        if r+g+b < 127*3:
            r1,g1,b1 = 200,200,200
            r2,g2,b2 = 220,220,220
        else:
            r1,g1,b1 =  80, 80, 80
            r2,g2,b2 = 100,100,100
        self._trColor1 = ttk.TTkColor.bg(f'#{r1:02X}{g1:02X}{b1:02X}')
        self._trColor2 = ttk.TTkColor.bg(f'#{r2:02X}{g2:02X}{b2:02X}')
        self.update()

    def paintEvent(self, canvas: ttk.TTkCanvas):
        w,h = self.size()
        ws,hs=8,4
        c = [self._trColor1,self._trColor2]
        for y in range(1+h//hs):
            for x in range(1+w//ws):
                canvas.fill(pos=(x*ws,y*hs),size=(ws,hs),color=c[(x+y)%2])
        super().paintEvent(canvas)

class ImportImage(ttk.TTkWindow):
    __slots__ = ('_pilImage_bk','_pilImage','_image','_b_width','_b_height','_cb_resample','_b_color',
                 'exportedImage')
    def __init__(self, pilImage:Image, **kwargs):
        self.exportedImage = ttk.pyTTkSignal(ttk.TTkString)
        self._pilImage =  self._pilImage_bk = pilImage.convert('RGBA')
        layout = ttk.TTkGridLayout()
        super().__init__(**kwargs|{"layout":layout,'size':(100,30)})

        saImage = ttk.TTkScrollArea()
        self._image = image = ImagePreview(parent=saImage.viewport())
        image.setRasteriser(ttk.TTkImage.HALFBLOCK)

        resizeFrame     = ttk.TTkFrame(title='Resize',layout=ttk.TTkGridLayout())
        propertiesFrame = ttk.TTkFrame(title='Image Properties',layout=ttk.TTkGridLayout())

        resizeFrame.layout().addWidget(ttk.TTkLabel(text='Width:'   ),0,0)
        resizeFrame.layout().addWidget(b_width  := ttk.TTkSpinBox(maximum=0x1000),0,1)
        resizeFrame.layout().addWidget(ttk.TTkLabel(text='Height:'  ),1,0)
        resizeFrame.layout().addWidget(b_height := ttk.TTkSpinBox(maximum=0x1000),1,1)
        resizeFrame.layout().addWidget(ttk.TTkLabel(text='Resample:'),2,0)
        resizeFrame.layout().addWidget(cb_resample := ttk.TTkComboBox(),2,1)

        resizeFrame.layout().addWidget(b_quadAR := ttk.TTkButton(text='Quad A/R', border=True),0,2,3,1)
        resizeFrame.layout().addWidget(b_sexAR  := ttk.TTkButton(text='Sex A/R', border=True), 0,3,3,1)
        resizeFrame.layout().addWidget(b_resize := ttk.TTkButton(text='Resize', border=True),  0,4,3,1)

        resizeFrame.layout().addWidget(ttk.TTkLabel(text='Adjust:'),3,0)
        sl_res = ttk.TTkSlider(value=100, minimum=1, maximum=200, orientation=ttk.TTkK.HORIZONTAL)
        resizeFrame.layout().addWidget(sl_res, 3,1,1,4)

        cb_resample.addItems(['NEAREST','BOX','BILINEAR','HAMMING','BICUBIC','LANCZOS'])
        cb_resample.setCurrentIndex(0)

        propertiesFrame.layout().addWidget(ttk.TTkLabel(text='Resolution:',maxWidth=11), 0,0)
        propertiesFrame.layout().addWidget(cb_resolution := ttk.TTkComboBox(),           0,1,1,2)
        propertiesFrame.layout().addWidget(ttk.TTkLabel(text='AlphaColor:'),             1,0)
        propertiesFrame.layout().addWidget(b_color  := ttk.TTkColorButtonPicker(color=ttk.TTkColor.bg("#000000")),  1,1,1,2)
        propertiesFrame.layout().addWidget(b_export := ttk.TTkButton(text="Export"),     3,0,1,3)
        # propertiesFrame.layout().addItem(ttk.TTkLayout(),3,0,1,2)

        propertiesFrame.layout().addWidget(ttk.TTkLabel(text='AlphaTres.:'),             2,0)
        sl_alpha_tre = ttk.TTkSlider(value=127, minimum=0, maximum=255, orientation=ttk.TTkK.HORIZONTAL)
        propertiesFrame.layout().addWidget(sl_alpha_tre, 2,1,1,2)

        cb_resolution.addItems(['FULLBLOCK','HALFBLOCK','QUADBLOCK','SEXBLOCK'])
        cb_resolution.setCurrentIndex(1)

        layout.addWidget(saImage        ,0,0,1,2)
        layout.addWidget(resizeFrame    ,1,0)
        layout.addWidget(propertiesFrame,1,1)

        self._b_width     = b_width
        self._b_height    = b_height
        self._b_color     = b_color
        self._cb_resample = cb_resample

        width, height = pilImage.size
        b_width.setValue(width)
        b_height.setValue(height)

        @ttk.pyTTkSlot()
        def _quadAR():
            if not self._pilImage: return
            width, height = self._pilImage.size
            b_width.setValue(width)
            b_height.setValue(height//2)

        @ttk.pyTTkSlot()
        def _sexAR():
            if not self._pilImage: return
            width, height = self._pilImage.size
            # w/h = 4/3
            b_width.setValue(width)
            b_height.setValue(height*3//4)

        @ttk.pyTTkSlot(int)
        def _adjustResolution(val):
            if not self._pilImage: return
            width, height = self._pilImage.size
            b_width.setValue(val*width//100)
            b_height.setValue(val*height//100)

        @ttk.pyTTkSlot(str)
        def _resolutionChanged(res):
            newRes = {
                'FULLBLOCK' : ttk.TTkImage.FULLBLOCK,
                'HALFBLOCK' : ttk.TTkImage.HALFBLOCK,
                'QUADBLOCK' : ttk.TTkImage.QUADBLOCK,
                'SEXBLOCK'  : ttk.TTkImage.SEXBLOCK
                    }.get(res, ttk.TTkImage.QUADBLOCK)
            image.setRasteriser(newRes)

        b_export.clicked.connect(self.export)
        b_quadAR.clicked.connect(_quadAR)
        b_sexAR.clicked.connect(_sexAR)
        b_resize.clicked.connect(self._resize)
        b_color.colorSelected.connect(self._updateImage)
        cb_resolution.currentTextChanged.connect(_resolutionChanged)
        sl_alpha_tre.valueChanged.connect(image.setAlphaThreshold)
        sl_res.valueChanged.connect(_adjustResolution)

        self._updateImage()

    @ttk.pyTTkSlot()
    def _resize(self):
        if not (pilImage := self._pilImage): return
        w = self._b_width.value()
        h = self._b_height.value()
        resample = {'NEAREST' : Image.NEAREST,
                    'BOX' :     Image.BOX,
                    'BILINEAR': Image.BILINEAR,
                    'HAMMING' : Image.HAMMING,
                    'BICUBIC' : Image.BICUBIC,
                    'LANCZOS' : Image.LANCZOS}.get(
                        self._cb_resample.currentText(),Image.NEAREST)
        self._pilImage = self._pilImage_bk.resize((w,h),resample)
        self._updateImage()

    @ttk.pyTTkSlot()
    def _updateImage(self):
        data = list(self._pilImage.getdata())
        w,h = self._pilImage.size
        br,bg,bb = self._b_color.color().bgToRGB()
        rgbList = [
            ((r*a+(255-a)*br)//255,
            (g*a+(255-a)*bg)//255,
            (b*a+(255-a)*bb)//255, a)
            for r,g,b,a in data]

        self._image.setTransparentColor(self._b_color.color())
        imageList = [rgbList[i:i+w] for i in range(0, len(rgbList), w)]
        self._image.setData(imageList)

    @ttk.pyTTkSlot()
    def export(self):
        self.exportedImage.emit(self._image.toTTkString())
