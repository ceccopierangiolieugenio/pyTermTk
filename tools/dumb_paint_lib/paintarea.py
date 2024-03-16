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

__all__ = ['PaintArea','PaintScrollArea','PaintToolKit','CanvasLayer']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


class PaintToolKit(ttk.TTkContainer):
    __slots__ = ('_rSelect', '_rPaint', '_lgliph',
                 '_cbFg', '_cbBg',
                 '_bpFg', '_bpBg', '_bpDef',
                 '_glyph',
                 #Signals
                 'updatedColor', 'updatedTrans')
    def __init__(self, *args, **kwargs):
        ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"paintToolKit.tui.json"),self)
        self._glyph = 'X'
        self.updatedColor = ttk.pyTTkSignal(ttk.TTkColor)
        self.updatedTrans = ttk.pyTTkSignal(ttk.TTkColor)
        self._lgliph  = self.getWidgetByName("lglyph")
        self._cbFg    = self.getWidgetByName("cbFg")
        self._cbBg    = self.getWidgetByName("cbBg")
        self._bpFg    = self.getWidgetByName("bpFg")
        self._bpBg    = self.getWidgetByName("bpBg")
        self._bpDef   = self.getWidgetByName("bpDef")

        self._bpDef.setColor(ttk.TTkColor.bg('#FF00FF'))
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
                ttk.TTkString("Glyph: '") +
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
    __slot__ = ('_pos','_name','_visible','_size','_data','_colors')
    def __init__(self) -> None:
        self._pos  = (0,0)
        self._size = (0,0)
        self._name = ""
        self._visible = True
        self._data:  list[list[str         ]] = []
        self._colors:list[list[ttk.TTkColor]] = []

    def pos(self):
        return self._pos
    def size(self):
        return self._size

    def visible(self):
        return self._visible
    @ttk.pyTTkSlot(bool)
    def setVisible(self, visible):
        self._visible = visible

    def name(self):
        return self._name
    @ttk.pyTTkSlot(str)
    def setName(self, name):
        self._name = name

    def isOpaque(self,x,y):
        if not self._visible: return False
        w,h = self._size
        data = self._data
        colors = self._colors
        if 0<=x<w and 0<=y<h:
            return data[y][x] != ' ' or colors[y][x].background()
        return False

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

        color = color if glyph != ' ' else color.background()
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
        color = color if glyph != ' ' else color.background()
        data = self._data
        colors = self._colors
        if 0<=x<w and 0<=y<h:
            data[y][x]   = glyph
            colors[y][x] = color
            return True
        return False

    def drawInCanvas(self, pos, canvas:ttk.TTkCanvas):
        if not self._visible: return
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


class PaintArea(ttk.TTkAbstractScrollView):
    class Tool(int):
        MOVE      = 0x01
        BRUSH     = 0x02
        RECTFILL  = 0x03
        RECTEMPTY = 0x04

    __slots__ = ('_canvasLayers', '_currentLayer',
                 '_transparentColor',
                 '_documentPos','_documentOffset','_documentSize',
                 '_mouseMove', '_mouseDrag', '_mousePress', '_mouseRelease',
                 '_moveData',
                 '_tool',
                 '_glyph', '_glyphColor')

    def __init__(self, *args, **kwargs):
        self._transparentColor = {'base':ttk.TTkColor.RST,'dim':ttk.TTkColor.RST}
        self._currentLayer:CanvasLayer = None
        self._canvasLayers:list[CanvasLayer] = []
        self._glyph = 'X'
        self._glyphColor = ttk.TTkColor.RST
        self._moveData = None
        self._mouseMove = None
        self._mouseDrag = None
        self._mousePress   = None
        self._mouseRelease = None
        self._tool = self.Tool.BRUSH
        self._documentOffset = ( 0, 0)
        self._documentPos    = (6,3)
        self._documentSize   = ( 0, 0)
        super().__init__(*args, **kwargs)
        self.setTrans(ttk.TTkColor.bg('#FF00FF'))
        self.resizeCanvas(80,25)
        self.setFocusPolicy(ttk.TTkK.ClickFocus + ttk.TTkK.TabFocus)

    def _getGeometry(self):
        dx,dy = self._documentPos
        # doffx,doffy = self._documentOffset
        # dx+=doffx
        # dy+=doffy
        dw,dh = self._documentSize
        ww,wh = self.size()
        # dw,dh = max(dw,dx+ww),max(dh,dx+wh)
        x1,y1 = min(0,dx),min(0,dy)
        x2,y2 = max(dx+dw,ww),max(dy+dh,wh)
        for l in self._canvasLayers:
            lx,ly = l.pos()
            lw,lh = l.size()
            x1 = min(x1,dx+lx)
            y1 = min(y1,dy+ly)
            x2 = max(x2,dx+lx+lw)
            y2 = max(y2,dy+ly+lh)
        ttk.TTkLog.debug(f"{x1=},{y1=},{x2-x1=},{y2-y1=}")
        return x1,y1,x2-x1,y2-y1

    def _retuneGeometry(self):
            x1,y1,_,_ = self._getGeometry()
            self._documentOffset = (max(0,-x1),max(0,-y1))
            self.viewMoveTo(max(0,-x1),max(0,-y1))
            self.viewChanged.emit()
            # dx,dy = self._documentPos
            # self.chan

    def viewFullAreaSize(self) -> tuple[int,int]:
        _,_,w,h = self._getGeometry()
        return w,h

    def viewDisplayedSize(self) -> tuple:
        return self.size()

    def maximumWidth(self):   return 0x10000
    def maximumHeight(self):  return 0x10000
    def minimumWidth(self):   return 0
    def minimumHeight(self):  return 0

    def canvasLayers(self):
        return self._canvasLayers

    def resizeCanvas(self, w, h):
        if self._currentLayer:
            self._currentLayer.resize(w,h)
        self._documentSize  = (w,h)
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
        self._retuneGeometry()

    def importDocument(self, dd):
        self._canvasLayers = []
        if 'version' in dd and dd['version']=='1.0.0':
            self.resizeCanvas(*dd['size'])
            for l in dd['layers']:
                nl = self.newLayer()
                nl.importLayer(l)
        self._retuneGeometry()

    def exportImage(self):
        return {}

    def exportLayer(self) -> dict:
        if self._currentLayer:
            return self._currentLayer.exportLayer()
        return {}

    def exportDocument(self):
        pw,ph = self._documentSize
        outData  = {
            'version':'1.0.0',
            'size':(pw,ph),
            'layers':[l.exportLayer() for l in self._canvasLayers]}
        return outData

    def leaveEvent(self, evt):
        self._mouseMove = None
        self._moveData  = None
        self.update()
        return super().leaveEvent(evt)

    @ttk.pyTTkSlot(Tool)
    def setTool(self, tool):
        self._tool = tool
        self.update()

    def _handleAction(self):
        dx,dy = self._documentPos
        doffx,doffy = self._documentOffset
        dx+=doffx
        dy+=doffy
        ox, oy = self.getViewOffsets()
        mp = self._mousePress
        # mm = self._mouseMove
        md = self._mouseDrag
        mr = self._mouseRelease
        l = self._currentLayer
        lx,ly = l.pos()
        if self._tool == self.Tool.MOVE and mp and not md:
            # Get The Layer to Move
            self._moveData = None
            for lm in reversed(self._canvasLayers):
                mpx,mpy = mp
                lmx,lmy = lm.pos()
                if lm.isOpaque(mpx-lmx,mpy-lmy):
                    tml = lm
                    self._moveData = {'pos':tml.pos(),'layer':tml}
                    break
        elif self._tool == self.Tool.MOVE and mp and md:
            mpx,mpy = mp
            mdx,mdy = md
            pdx,pdy = mdx-mpx,mdy-mpy
            if self._moveData:
                px,py = self._moveData['pos']
                self._moveData['layer'].move(px+pdx,py+pdy)
            else:
                self._documentPos = (dx+pdx,dy+pdy)
            self._retuneGeometry()
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
        dx,dy = self._documentPos
        doffx,doffy = self._documentOffset
        dx+=doffx
        dy+=doffy
        ox, oy = self.getViewOffsets()
        self._mouseMove=(evt.x+ox-dx,evt.y+oy-dy)
        self._mouseDrag    = None
        self.update()
        return True

    def mouseDragEvent(self, evt) -> bool:
        dx,dy = self._documentPos
        doffx,doffy = self._documentOffset
        dx+=doffx
        dy+=doffy
        ox, oy = self.getViewOffsets()
        self._mouseDrag=(evt.x+ox-dx,evt.y+oy-dy)
        self._mouseMove= None
        self._handleAction()
        return True

    def mousePressEvent(self, evt) -> bool:
        dx,dy = self._documentPos
        doffx,doffy = self._documentOffset
        dx+=doffx
        dy+=doffy
        ox, oy = self.getViewOffsets()
        self._mousePress=(evt.x+ox-dx,evt.y+oy-dy)
        self._moveData     = None
        self._mouseMove    = None
        self._mouseDrag    = None
        self._mouseRelease = None
        self._handleAction()
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        dx,dy = self._documentPos
        doffx,doffy = self._documentOffset
        dx+=doffx
        dy+=doffy
        ox, oy = self.getViewOffsets()
        self._mouseRelease=(evt.x+ox-dx,evt.y+oy-dy)
        self._mouseMove   = None
        self._handleAction()
        self._moveData     = None
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
    def setTrans(self, color:ttk.TTkColor):
        r,g,b = color.bgToRGB()
        self._transparentColor = {
            'base':color,
            'dim':     ttk.TTkColor.bg(f'#{int(r*0.3):02x}{int(g*0.3):02x}{int(b*0.3):02x}'),
            'layer':   ttk.TTkColor.bg(f'#{int(r*0.6):02x}{int(g*0.6):02x}{int(b*0.6):02x}'),
            'layerDim':ttk.TTkColor.bg(f'#{int(r*0.2):02x}{int(g*0.2):02x}{int(b*0.2):02x}')}
        self.update()

    def _placeFill(self):
        if not self._mouseDrag: return False
        mfill = self._mouseDrag
        self._mouseDrag = None
        self._mouseMove = None
        self._moveData  = None
        ret = self._currentLayer.placeFill(mfill,self._tool,self._glyph,self._glyphColor)
        self.update()
        return ret

    def _placeGlyph(self,x,y):
        self._mouseMove = None
        self._moveData  = None
        ret = self._currentLayer.placeGlyph(x,y,self._glyph,self._glyphColor)
        self.update()
        return ret

    def paintEvent(self, canvas:ttk.TTkCanvas):
        dx,dy = self._documentPos
        doffx,doffy = self._documentOffset
        dx+=doffx
        dy+=doffy
        ox, oy = self.getViewOffsets()
        dw,dh = self._documentSize
        dox,doy = dx-ox,dy-oy
        cw,ch = canvas.size()
        w=min(cw,dw)
        h=min(ch,dh)
        tcb = self._transparentColor['base']
        tcd = self._transparentColor['dim']
        # canvas.fill(pos=(0    ,dy-oy),size=(cw,dh),color=tcd)
        # canvas.fill(pos=(dx-ox,0    ),size=(dw,ch),color=tcd)

        if l:=self._currentLayer:
            tclb = self._transparentColor['layer']
            tcld = self._transparentColor['layerDim']
            lx,ly = l.pos()
            lw,lh = l.size()
            canvas.fill(pos=(0     ,ly+doy),size=(cw,lh),color=tcld)
            canvas.fill(pos=(lx+dox,0     ),size=(lw,ch),color=tcld)
            canvas.fill(pos=(lx+dox,ly+doy),size=(lw,lh),color=tclb)
        canvas.fill(pos=(dx-ox,dy-oy),size=(dw,dh),color=tcb)
        canvas.fill(pos=(0    ,dy-oy-1), size=(cw,1),color=tcd)
        canvas.fill(pos=(0    ,dy-oy+dh),size=(cw,1),color=tcd)
        canvas.fill(pos=(dx-ox-2 ,0    ),size=(2,ch),color=tcd)
        canvas.fill(pos=(dx-ox+dw,0    ),size=(2,ch),color=tcd)

        # Draw canvas/currentLayout ruler

        ruleColor = ttk.TTkColor.fg("#444444")
        # # canvas.drawText(pos=((0,dy-oy-1 )),text="═"*cw,color=ruleColor)
        # # canvas.drawText(pos=((0,dy-oy+dh)),text="═"*cw,color=ruleColor)
        # # canvas.drawText(pos=((0,dy-oy-1 )),text="▁"*cw,color=ruleColor)
        # # canvas.drawText(pos=((0,dy-oy+dh)),text="▔"*cw,color=ruleColor)
        # canvas.drawText(pos=((0,dy-oy-1 )),text="▄"*cw,color=ruleColor)
        # canvas.drawText(pos=((0,dy-oy+dh)),text="▀"*cw,color=ruleColor)
        # for y in range(ch):
        #     canvas.drawText(pos=((dx-ox-1 ,y)),text="▐",color=ruleColor)
        #     canvas.drawText(pos=((dx-ox+dw,y)),text="▌",color=ruleColor)
        # canvas.drawText(pos=((dx-ox-1 ,dy-oy-1 )),text="▟",color=ruleColor)
        # canvas.drawText(pos=((dx-ox+dw,dy-oy-1 )),text="▙",color=ruleColor)
        # canvas.drawText(pos=((dx-ox-1 ,dy-oy+dh)),text="▜",color=ruleColor)
        # canvas.drawText(pos=((dx-ox+dw,dy-oy+dh)),text="▛",color=ruleColor)

        for l in self._canvasLayers:
            lx,ly = l.pos()
            l.drawInCanvas(pos=(lx+dox,ly+doy),canvas=canvas)
        return
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

class PaintScrollArea(ttk.TTkAbstractScrollArea):
    def __init__(self, pwidget:PaintArea, **kwargs):
        super().__init__(**kwargs)
        self.setViewport(pwidget)