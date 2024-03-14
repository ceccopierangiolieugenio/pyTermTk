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

__all__ = ['PaintArea','PaintToolKit','CanvasLayer']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


class PaintToolKit(ttk.TTkGridLayout):


    __slots__ = ('_rSelect', '_rPaint', '_lgliph',
                 '_cbFg', '_cbBg',
                 '_bpFg', '_bpBg', '_bpDef',
                 '_glyph',
                 #Signals
                 'updatedColor', 'updatedTrans')
    def __init__(self, *args, **kwargs):
        self._glyph = 'X'
        self.updatedColor = ttk.pyTTkSignal(ttk.TTkColor)
        self.updatedTrans = ttk.pyTTkSignal(ttk.TTkColor)
        super().__init__(*args, **kwargs)
        self._rSelect = ttk.TTkRadioButton(text='Select '     , maxWidth=10, enabled=False)
        self._rPaint  = ttk.TTkRadioButton(text='Paint  '     ,              enabled=False)
        self._lgliph   = ttk.TTkLabel(text=""                 , maxWidth=8)
        self._cbFg    = ttk.TTkCheckbox(text="Fg"             , maxWidth= 6)
        self._cbBg    = ttk.TTkCheckbox(text="Bg"                    )
        self._bpFg    = ttk.TTkColorButtonPicker(enabled=False, maxWidth= 6)
        self._bpBg    = ttk.TTkColorButtonPicker(enabled=False,            )
        self._bpDef   = ttk.TTkColorButtonPicker(color=ttk.TTkColor.bg('#FF00FF'), maxWidth=6)
        self.addWidget(self._rSelect ,0,0)
        self.addWidget(self._rPaint  ,1,0)
        self.addWidget(self._lgliph  ,0,1,2,1)
        self.addWidget(self._cbFg    ,0,2)
        self.addWidget(self._cbBg    ,1,2)
        self.addWidget(self._bpFg    ,0,3)
        self.addWidget(self._bpBg    ,1,3)

        self.addWidget(ttk.TTkLabel(text=" Trans:", maxWidth=7) ,1,4)
        self.addWidget(self._bpDef          ,1,5)
        self.addItem(ttk.TTkLayout() ,0,6,2,1)

        self._cbFg.toggled.connect(self._bpFg.setEnabled)
        self._cbBg.toggled.connect(self._bpBg.setEnabled)
        self._cbFg.toggled.connect(self._refreshColor)
        self._cbBg.toggled.connect(self._refreshColor)

        self._bpFg.colorSelected.connect(self._refreshColor)
        self._bpBg.colorSelected.connect(self._refreshColor)
        self._bpDef.colorSelected.connect(self.updatedTrans.emit)

        self._refreshColor(emit=False)

    @ttk.pyTTkSlot()
    def _refreshColor(self, emit=True):
        color =self.color()
        self._lgliph.setText(
                ttk.TTkString("Glyph\n '") +
                ttk.TTkString(self._glyph,color) +
                ttk.TTkString("'"))
        if emit:
            self.updatedColor.emit(color)


    @ttk.pyTTkSlot(ttk.TTkString)
    def glyphFromString(self, ch:ttk.TTkString):
        if len(ch)<=0: return
        self._glyph = ch.charAt(0)
        self._refreshColor()
        # self.setColor(ch.colorAt(0))

    def color(self):
        color = ttk.TTkColor()
        if self._cbFg.checkState() == ttk.TTkK.Checked:
            color += self._bpFg.color().invertFgBg()
        if self._cbBg.checkState() == ttk.TTkK.Checked:
           color += self._bpBg.color()
        return color

    @ttk.pyTTkSlot(ttk.TTkColor)
    def setColor(self, color:ttk.TTkColor):
        if fg := color.foreground():
            self._cbFg.setCheckState(ttk.TTkK.Checked)
            self._bpFg.setEnabled()
            self._bpFg.setColor(fg.invertFgBg())
        else:
            self._cbFg.setCheckState(ttk.TTkK.Unchecked)
            self._bpFg.setDisabled()

        if bg := color.background():
            self._cbBg.setCheckState(ttk.TTkK.Checked)
            self._bpBg.setEnabled()
            self._bpBg.setColor(bg)
        else:
            self._cbBg.setCheckState(ttk.TTkK.Unchecked)
            self._bpBg.setDisabled()
        self._refreshColor(emit=False)

class CanvasLayer():
    __slot__ = ('_pos','_name','_size','_data','_colors')
    def __init__(self) -> None:
        self._pos  = (0,0)
        self._size = (0,0)
        self._name = ""
        self._data:  list[list[str         ]] = []
        self._colors:list[list[ttk.TTkColor]] = []

    def pos(self):
        return self._pos
    def size(self):
        return self._size

    def name(self):
        return self._name
    @ttk.pyTTkSlot(str)
    def setName(self, name):
        self._name = name

    def move(self,x,y):
        self._pos=(x,y)

    def resize(self,w,h):
        self._size = (w,h)
        self._data   = (self._data   + [[] for _ in range(h)])[:h]
        self._colors = (self._colors + [[] for _ in range(h)])[:h]
        for i in range(h):
            self._data[i]   = (self._data[i]   + [' '              for _ in range(w)])[:w]
            self._colors[i] = (self._colors[i] + [ttk.TTkColor.RST for _ in range(w)])[:w]

    def copy(self):
        w,h = self._size
        ret = CanvasLayer()
        ret._size   = (w,h)
        ret._data   = [d.copy() for d in self._data]
        ret._colors = [c.copy() for c in self._colors]
        return ret

    def clean(self):
        w,h = self._size
        for i in range(h):
            self._data[i]   = [' ']*w
            self._colors[i] = [ttk.TTkColor.RST]*w

    def exportLayer(self):
        # Don't try this at home
        px,py  = self.pos()
        pw,ph  = self.size()
        data   = self._data
        colors = self._colors
        # get the bounding box
        xa,xb,ya,yb = pw,0,ph,0
        for y,row in enumerate(data):
            for x,d in enumerate(row):
                c = colors[y][x]
                if d != ' ' or c.background():
                    xa = min(x,xa)
                    xb = max(x,xb)
                    ya = min(y,ya)
                    yb = max(y,yb)

        if (xa,xb,ya,yb) == (pw,0,ph,0):
            xa=xb=ya=yb=0


        #if xa>xb or ya>yb:
        #    return {}

        outData  = {
            'version':'1.0.0',
            'size':[xb-xa+1,yb-ya+1],
            'pos': (px+xa,py+ya),
            'name':str(self.name()),
            'data':[], 'colors':[], 'palette':[]}

        palette=outData['palette']
        for row in colors:
            for c in row:
                fg = f"{c.getHex(ttk.TTkK.Foreground)}" if c.foreground() else None
                bg = f"{c.getHex(ttk.TTkK.Background)}" if c.background() else None
                if (pc:=(fg,bg)) not in palette:
                    palette.append(pc)

        for row in data[ya:yb+1]:
            outData['data'].append(row[xa:xb+1])
        for row in colors[ya:yb+1]:
            outData['colors'].append([])
            for c in row[xa:xb+1]:
                fg = f"{c.getHex(ttk.TTkK.Foreground)}" if c.foreground() else None
                bg = f"{c.getHex(ttk.TTkK.Background)}" if c.background() else None
                outData['colors'][-1].append(palette.index((fg,bg)))
        return outData

    def importLayer(self, dd):
        self.clean()

        if 'version' in dd and dd['version']=='1.0.0':
            self._pos  = dd['pos']
            self._size = dd['size']
            self._name = dd['name']
            self._data = dd['data']
            def _getColor(cd):
                fg,bg = cd
                if fg and bg: return ttk.TTkColor.fg(fg)+ttk.TTkColor.bg(bg)
                elif fg:      return ttk.TTkColor.fg(fg)
                elif bg:      return ttk.TTkColor.bg(bg)
                else:         return ttk.TTkColor.RST
            if 'palette' in dd:
                palette = [_getColor(c) for c in  dd['palette']]
                self._colors = [[palette[c] for c in row] for row in dd['colors']]
            else:
                self._colors = [[_getColor(c) for c in row] for row in dd['colors']]
        else: # Legacy old import
            w = len(dd['data'][0]) + 10
            h = len(dd['data']) + 4
            x,y=5,2
            self.resize(w,h)
            self._pos = (0,0)
            for i,rd in enumerate(dd['data']):
                for ii,cd in enumerate(rd):
                    self._data[i+y][ii+x] = cd
            for i,rd in enumerate(dd['colors']):
                for ii,cd in enumerate(rd):
                    fg,bg = cd
                    if fg and bg:
                        self._colors[i+y][ii+x] = ttk.TTkColor.fg(fg)+ttk.TTkColor.bg(bg)
                    elif fg:
                        self._colors[i+y][ii+x] = ttk.TTkColor.fg(fg)
                    elif bg:
                        self._colors[i+y][ii+x] = ttk.TTkColor.bg(bg)
                    else:
                        self._colors[i+y][ii+x] = ttk.TTkColor.RST

    def placeFill(self,geometry,tool,glyph,color):
        w,h = self._size
        ax,ay,bx,by = geometry
        ax = max(0,min(w-1,ax))
        ay = max(0,min(h-1,ay))
        bx = max(0,min(w-1,bx))
        by = max(0,min(h-1,by))
        fax,fay = min(ax,bx), min(ay,by)
        fbx,fby = max(ax,bx), max(ay,by)

        data   = self._data
        colors = self._colors

        if tool == PaintArea.Tool.RECTFILL:
            for row in data[fay:fby+1]:
                row[fax:fbx+1] = [glyph]*(fbx-fax+1)
            for row in colors[fay:fby+1]:
                row[fax:fbx+1] = [color]*(fbx-fax+1)
        if tool == PaintArea.Tool.RECTEMPTY:
            data[fay][fax:fbx+1]   = [glyph]*(fbx-fax+1)
            data[fby][fax:fbx+1]   = [glyph]*(fbx-fax+1)
            colors[fay][fax:fbx+1] = [color]*(fbx-fax+1)
            colors[fby][fax:fbx+1] = [color]*(fbx-fax+1)
            for row in data[fay:fby]:
                row[fax]=row[fbx]=glyph
            for row in colors[fay:fby]:
                row[fax]=row[fbx]=color
        return True

    def placeGlyph(self,x,y,glyph,color):
        w,h = self._size
        data = self._data
        colors = self._colors
        if 0<=x<w and 0<=y<h:
            data[y][x]   = glyph
            colors[y][x] = color
            return True
        return False

    def drawInCanvas(self, pos, canvas:ttk.TTkCanvas):
        px,py = pos
        pw,ph = self._size
        cw,ch = canvas.size()
        if px+pw<0 or py+ph<0:return
        if px>=cw or py>=ch:return
        # x,y position in the Canvas
        cx = max(0,px)
        cy = max(0,py)
        # x,y position in the Layer
        lx,ly = (cx-px),(cy-py)
        # Area to be copyed
        dw = min(cw-cx,pw-lx)
        dh = min(ch-cy,ph-ly)

        data   = self._data
        colors = self._colors
        for y in range(cy,cy+dh):
            for x in range(cx,cx+dw):
                gl = data[y+ly-cy][x+lx-cx]
                c  = colors[y+ly-cy][x+lx-cx]
                if gl==' ' and c._bg:
                    canvas._data[y][x]   = gl
                    canvas._colors[y][x] = c
                elif gl!=' ':
                    canvas._data[y][x]   = gl
                    cc = canvas._colors[y][x]
                    newC = c.copy()
                    newC._bg = c._bg if c._bg else cc._bg
                    canvas._colors[y][x] = newC


class PaintArea(ttk.TTkWidget):
    class Tool(int):
        MOVE      = 0x01
        BRUSH     = 0x02
        RECTFILL  = 0x03
        RECTEMPTY = 0x04

    __slots__ = ('_canvasLayers', '_currentLayer',
                 '_transparentColor',
                 '_mouseMove', '_mouseDrag', '_mousePress', '_mouseRelease',
                 '_posBk',
                 '_tool',
                 '_glyph', '_glyphColor')

    def __init__(self, *args, **kwargs):
        self._transparentColor = ttk.TTkColor.bg('#FF00FF')
        self._currentLayer:CanvasLayer = None
        self._canvasLayers:list[CanvasLayer] = []
        self._glyph = 'X'
        self._glyphColor = ttk.TTkColor.RST
        self._posBk = (0,0)
        self._mouseMove = None
        self._mouseDrag = None
        self._mousePress   = None
        self._mouseRelease = None
        self._tool = self.Tool.BRUSH
        super().__init__(*args, **kwargs)
        self.resizeCanvas(80,25)
        self.setFocusPolicy(ttk.TTkK.ClickFocus + ttk.TTkK.TabFocus)

    def canvasLayers(self):
        return self._canvasLayers

    def resizeCanvas(self, w, h):
        if self._currentLayer:
            self._currentLayer.resize(w,h)
        self._canvasSize = (w,h)
        self.update()

    def setCurrentLayer(self, layer:CanvasLayer):
        self._currentLayer = layer

    def newLayer(self) -> CanvasLayer:
        newLayer = CanvasLayer()
        w,h = self.size()
        w,h = (w,h) if (w,h)!=(0,0) else (80,24)
        newLayer.resize(w,h)
        self._currentLayer = newLayer
        self._canvasLayers.append(newLayer)
        return newLayer

    def importLayer(self, dd):
        self._currentLayer.importLayer(dd)
        self.update()

    def importDocument(self, dd):
        self._canvasLayers = []
        if 'version' in dd and dd['version']=='1.0.0':
            self.resizeCanvas(*dd['size'])
            for l in dd['layers']:
                nl = self.newLayer()
                nl.importLayer(l)

    def exportImage(self):
        return {}

    def exportLayer(self) -> dict:
        if self._currentLayer:
            return self._currentLayer.exportLayer()
        return {}

    def exportDocument(self):
        pw,ph = self._canvasSize
        outData  = {
            'version':'1.0.0',
            'size':(pw,ph),
            'layers':[l.exportLayer() for l in self._canvasLayers]}
        return outData

    def leaveEvent(self, evt):
        self._mouseMove = None
        self.update()
        return super().leaveEvent(evt)

    @ttk.pyTTkSlot(Tool)
    def setTool(self, tool):
        self._tool = tool
        self.update()

    def _handleAction(self):
        mp = self._mousePress
        # mm = self._mouseMove
        md = self._mouseDrag
        mr = self._mouseRelease
        l = self._currentLayer
        lx,ly = l.pos()
        if self._tool == self.Tool.MOVE and mp and not md:
            self._posBk = (lx,ly)
        elif self._tool == self.Tool.MOVE and mp and md:
            mpx,mpy = mp
            mdx,mdy = md
            px,py = self._posBk
            dx,dy = mdx-mpx,mdy-mpy
            l.move(px+dx,py+dy)
        elif self._tool == self.Tool.BRUSH and (mp or md):
            if md: mx,my = md
            else:  mx,my = mp
            self._currentLayer.placeGlyph(mx-lx,my-ly,self._glyph,self._glyphColor)
        elif self._tool in (self.Tool.RECTEMPTY, self.Tool.RECTFILL) and mr and mp:
            mpx,mpy = mp
            mrx,mry = mr
            self._currentLayer.placeFill((mpx-lx,mpy-ly,mrx-lx,mry-ly),self._tool,self._glyph,self._glyphColor)
        self.update()

    def mouseMoveEvent(self, evt) -> bool:
        self._mouseMove = (evt.x,evt.y)
        self._mouseDrag    = None
        self.update()
        return True

    def mouseDragEvent(self, evt) -> bool:
        self._mouseDrag=(evt.x,evt.y)
        self._mouseMove= None
        self._handleAction()
        return True

    def mousePressEvent(self, evt) -> bool:
        self._mousePress=(evt.x,evt.y)
        self._mouseMove    = None
        self._mouseDrag    = None
        self._mouseRelease = None
        self._handleAction()
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        self._mouseRelease=(evt.x,evt.y)
        self._mouseMove   = None
        self._handleAction()
        self._mousePress   = None
        self._mouseDrag    = None
        self._mouseRelease = None
        return super().mousePressEvent(evt)

    @ttk.pyTTkSlot(ttk.TTkString)
    def glyphFromString(self, ch:ttk.TTkString):
        if len(ch)<=0: return
        self._glyph = ch.charAt(0)

    def glyph(self):
        return self._glyph
    def setGlyph(self, glyph):
        if len(glyph) <= 0: return
        if type(glyph)==str:
            self._glyph = glyph[0]
        if type(glyph)==ttk.TTkString:
            self._glyph = glyph.charAt(0)
            self._glyphColor = glyph.colorAt(0)

    def glyphColor(self):
        return self._glyphColor
    def setGlyphColor(self, color):
        self._glyphColor = color

    @ttk.pyTTkSlot(ttk.TTkColor)
    def setTrans(self, color):
        self._transparentColor = color
        self.update()

    def _placeFill(self):
        if not self._mouseDrag: return False
        mfill = self._mouseDrag
        self._mouseDrag = None
        self._mouseMove = None
        ret = self._currentLayer.placeFill(mfill,self._tool,self._glyph,self._glyphColor)
        self.update()
        return ret

    def _placeGlyph(self,x,y):
        self._mouseMove = None
        ret = self._currentLayer.placeGlyph(x,y,self._glyph,self._glyphColor)
        self.update()
        return ret

    def paintEvent(self, canvas:ttk.TTkCanvas):
        pw,ph = self._canvasSize
        cw,ch = canvas.size()
        w=min(cw,pw)
        h=min(ch,ph)
        tc = self._transparentColor
        canvas.fill(pos=(0,0),size=(pw,ph),color=tc)
        for l in self._canvasLayers:
            l.drawInCanvas(pos=l.pos(),canvas=canvas)
        if self._mouseMove:
            x,y = self._mouseMove
            gc = self._glyphColor
            canvas._data[y][x] = self._glyph
            canvas._colors[y][x] = gc if gc._bg else gc+tc
        if self._mouseDrag and self._mousePress:
            ax,ay = self._mousePress
            bx,by = self._mouseDrag
            ax = max(0,min(w-1,ax))
            ay = max(0,min(h-1,ay))
            bx = max(0,min(w-1,bx))
            by = max(0,min(h-1,by))
            x,y = min(ax,bx),     min(ay,by)
            w,h = max(ax-x,bx-x)+1, max(ay-y,by-y)+1
            gl = self._glyph
            gc = self._glyphColor
            if self._tool == PaintArea.Tool.RECTFILL:
                canvas.fill(pos=(x,y), size=(w,h),
                            color=gc if gc._bg else gc+tc,
                            char=gl)
            elif self._tool == PaintArea.Tool.RECTEMPTY:
                canvas.drawText(pos=(x,y    ),text=gl*w,color=gc)
                canvas.drawText(pos=(x,y+h-1),text=gl*w,color=gc)
                for y in range(y+1,y+h-1):
                    canvas.drawChar(pos=(x    ,y),char=gl,color=gc)
                    canvas.drawChar(pos=(x+w-1,y),char=gl,color=gc)