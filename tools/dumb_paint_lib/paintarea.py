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

__all__ = ['PaintArea','PaintScrollArea','CanvasLayer']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

# Canvas Layer structure
# The data may include more areas than the visible one
# This is helpful in case of resize to not lose the drawn areas
#
#   |---| OffsetX
#       x
#   ╭────────────────╮    -             -
#   │                │    | OffsetY     |
# y │   ┌───────┐    │ \  -             | Data
#   │   │Visible│    │ | h              |
#   │   └───────┘    │ /                |
#   │                │                  |
#   └────────────────┘                  -
#        \---w--/

class CanvasLayer():
    __slot__ = ('_pos','_name','_visible','_size','_data','_colors','_preview','_offset')
    def __init__(self) -> None:
        self._pos  = (0,0)
        self._size = (0,0)
        self._offset = (0,0)
        self._name = ""
        self._visible = True
        self._preview = None
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
        ox,oy = self._offset
        w,h = self._size
        data = self._data
        colors = self._colors
        if 0<=x<w and 0<=y<h:
            return data[oy+y][ox+x] != ' ' or colors[oy+y][ox+x].background()
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

    def superResize(self,dx,dy,dw,dh):
        ox,oy = self._offset
        x,y = self.pos()
        w,h = self.size()
        daw = len(self._data[0])
        dah = len(self._data)
        diffx = dx-x
        diffy = dy-y
        self._preview = None
        if ox<=x-dx: # we need to resize and move ox
            _nw = x-dx-ox
            ox  = x-dx
            self._data   = [([' ']*_nw             ) + _r for _r in self._data]
            self._colors = [([ttk.TTkColor.RST]*_nw) + _r for _r in self._colors]
        if x+dw+ox > daw:
            _nw = x+dw+ox-daw
            self._data   = [_r + ([' ']*_nw             )  for _r in self._data]
            self._colors = [_r + ([ttk.TTkColor.RST]*_nw)  for _r in self._colors]
        if oy<=y-dy: # we need to resize and move ox
            _nh = y-dy-oy
            oy  = y-dy
            self._data   = [[' ']*daw              for _ in range(_nh)] + self._data
            self._colors = [[ttk.TTkColor.RST]*daw for _ in range(_nh)] + self._colors
        if y+dh+oy > dah:
            _nh = y+dh+oy-dah
            self._data   = self._data   + [[' ']*daw              for _ in range(_nh)]
            self._colors = self._colors + [[ttk.TTkColor.RST]*daw for _ in range(_nh)]
        self._offset = (ox+diffx,oy+diffy)
        self._pos  = (dx,dy)
        self._size = (dw,dh)


    def clean(self):
        w,h = self._size
        self._offset = (0,0)
        self._preview = None
        for i in range(h):
            self._data[i]   = [' ']*w
            self._colors[i] = [ttk.TTkColor.RST]*w


    def exportLayer(self, full=False, palette=True, crop=True):
        #           xa|----------|  xb
        #     px        |-----------| = max(px,px+xa-ox)
        # Offset |------|    pw
        #   Data |----------------------------|
        #             daw

        # Don't try this at home
        ox,oy = self._offset
        px,py  = self.pos()
        pw,ph  = self.size()

        if full:
            data   = self._data
            colors = self._colors
        else:
            data   = [row[ox:ox+pw] for row in self._data[  oy:oy+ph]  ]
            colors = [row[ox:ox+pw] for row in self._colors[oy:oy+ph]  ]
            ox=oy=0

        daw = len(data[0])
        dah = len(data)

        # get the bounding box
        if crop:
            xa,xb,ya,yb = daw,0,dah,0
            for y,(drow,crow) in enumerate(zip(data,colors)):
                for x,(d,c) in enumerate(zip(drow,crow)):
                    if d != ' ' or c.background():
                        xa = min(x,xa)
                        xb = max(x,xb)
                        ya = min(y,ya)
                        yb = max(y,yb)
            if (xa,xb,ya,yb) == (daw,0,dah,0):
                xa=xb=ya=yb=0
        else:
            xa,xb,ya,yb = 0,daw,0,dah

        # Visble Area intersecting the bounding box
        vxa,vya = max(px,px+xa-ox),   max(py,py+ya-oy)
        vxb,vyb = min(px+pw,vxa+xb-xa),min(py+ph,vya+yb-ya)
        vw,vh   = vxb-vxa+1, vyb-vya+1

        outData  = {
            'version':'1.1.0',
            'size':[vw,vh],
            'pos': (vxa,vya),
            'name':str(self.name()),
            'data':[], 'colors':[]}

        if palette:
            palette = outData['palette'] = []
            for row in colors:
                for c in row:
                    fg = f"{c.getHex(ttk.TTkK.Foreground)}" if c.foreground() else None
                    bg = f"{c.getHex(ttk.TTkK.Background)}" if c.background() else None
                    if (pc:=(fg,bg)) not in palette:
                        palette.append(pc)

        if full:
            wslice = slice(xa,xb+1)
            hslice = slice(ya,yb+1)
            outData['offset'] = (max(0,ox-xa),max(0,oy-ya))
        else:
            wslice = slice(ox+vxa-px,ox+vxa-px+vw)
            hslice = slice(oy+vya-py,oy+vya-py+vh)

        for row in data[hslice]:
            outData['data'].append(row[wslice])
        for row in colors[hslice]:
            outData['colors'].append([])
            for c in row[wslice]:
                fg = f"{c.getHex(ttk.TTkK.Foreground)}" if c.foreground() else None
                bg = f"{c.getHex(ttk.TTkK.Background)}" if c.background() else None
                if palette:
                    outData['colors'][-1].append(palette.index((fg,bg)))
                else:
                    outData['colors'][-1].append((fg,bg))

        return outData

    def _import_v1_1_0(self, dd):
        self._import_v1_0_0(dd)
        self._offset = dd.get('offset',(0,0))

    def _import_v1_0_0(self, dd):
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

    def _import_v0_0_0(self, dd):
        # Legacy old import
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

    def importLayer(self, dd):
        self.clean()

        if 'version' in dd:
            ver = dd['version']
            if   ver == ('1.0.0'):
                self._import_v1_0_0(dd)
            elif ver == ('1.1.0'):
                self._import_v1_1_0(dd)
        else:
            self._import_v0_0_0(dd)

    def placeFill(self,geometry,tool,glyph,color,preview=False):
        ox,oy = self._offset
        w,h = self._size
        ax,ay,bx,by = geometry
        ax = max(0,min(w-1,ax))
        ay = max(0,min(h-1,ay))
        bx = max(0,min(w-1,bx))
        by = max(0,min(h-1,by))
        fax,fay = ox+min(ax,bx), oy+min(ay,by)
        fbx,fby = ox+max(ax,bx), oy+max(ay,by)

        color = color if glyph != ' ' else color.background()
        if preview:
            data   = [_r.copy() for _r in self._data]
            colors = [_r.copy() for _r in self._colors]
            self._preview = {'data':data,'colors':colors}
        else:
            self._preview = None
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

    def placeGlyph(self,x,y,glyph,color,preview=False):
        ox,oy = self._offset
        w,h = self._size
        color = color if glyph != ' ' else color.background()
        if preview:
            data   = [_r.copy() for _r in self._data]
            colors = [_r.copy() for _r in self._colors]
            self._preview = {'data':data,'colors':colors}
        else:
            self._preview = None
            data   = self._data
            colors = self._colors
        if 0<=x<w and 0<=y<h:
            data[  oy+y][ox+x]   = glyph
            colors[oy+y][ox+x] = color
            return True
        return False

    def drawInCanvas(self, pos, canvas:ttk.TTkCanvas):
        if not self._visible: return
        px,py = pos
        pw,ph = self._size
        cw,ch = canvas.size()
        if px+pw<0 or py+ph<0:return
        if px>=cw or py>=ch:return
        # Data Offset
        ox,oy = self._offset
        # x,y position in the Canvas
        cx = max(0,px)
        cy = max(0,py)
        # x,y position in the Layer
        lx,ly = (cx-px),(cy-py)
        # Area to be copyed
        dw = min(cw-cx,pw-lx)
        dh = min(ch-cy,ph-ly)

        if _p := self._preview:
            data   = _p['data']
            colors = _p['colors']
        else:
            data   = self._data
            colors = self._colors
        for y in range(cy,cy+dh):
            for x in range(cx,cx+dw):
                gl = data[  oy+y+ly-cy][ox+x+lx-cx]
                c  = colors[oy+y+ly-cy][ox+x+lx-cx]
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
        RESIZE    = 0x02
        BRUSH     = 0x04
        RECTFILL  = 0x08
        RECTEMPTY = 0x10

    __slots__ = ('_canvasLayers', '_currentLayer',
                 '_transparentColor',
                 '_documentPos','_documentSize',
                 '_mouseMove', '_mouseDrag', '_mousePress', '_mouseRelease',
                 '_moveData','_resizeData',
                 '_tool',
                 '_glyph', '_glyphColor',
                 # Signals
                 'selectedLayer')

    def __init__(self, *args, **kwargs):
        self.selectedLayer = ttk.pyTTkSignal(CanvasLayer)
        self._transparentColor = {'base':ttk.TTkColor.RST,'dim':ttk.TTkColor.RST}
        self._currentLayer:CanvasLayer = None
        self._canvasLayers:list[CanvasLayer] = []
        self._glyph = 'X'
        self._glyphColor = ttk.TTkColor.RST
        self._moveData = None
        self._resizeData = None
        self._mouseMove = None
        self._mouseDrag = None
        self._mousePress   = None
        self._mouseRelease = None
        self._tool = self.Tool.BRUSH
        self._documentPos    = (6,3)
        self._documentSize   = ( 0, 0)
        super().__init__(*args, **kwargs)
        self.setTrans(ttk.TTkColor.bg('#FF00FF'))
        self.resizeCanvas(80,25)
        self.setFocusPolicy(ttk.TTkK.ClickFocus + ttk.TTkK.TabFocus)

    def _getGeometry(self):
        dx,dy = self._documentPos
        dw,dh = self._documentSize
        ww,wh = self.size()
        x1,y1 = min(0,dx),min(0,dy)
        x2,y2 = max(dx+dw,ww),max(dy+dh,wh)
        for l in self._canvasLayers:
            lx,ly = l.pos()
            lw,lh = l.size()
            x1 = min(x1,dx+lx)
            y1 = min(y1,dy+ly)
            x2 = max(x2,dx+lx+lw)
            y2 = max(y2,dy+ly+lh)
        # ttk.TTkLog.debug(f"{x1=},{y1=},{x2-x1=},{y2-y1=}")
        return x1,y1,x2-x1,y2-y1

    def _retuneGeometry(self):
            dx,dy = self._documentPos
            x1,y1,_,_ = self._getGeometry()
            self._documentPos = max(dx,-dx,-x1),max(dy,-dy,-y1)
            # self.viewMoveTo(max(0,-x1),max(0,-y1))
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
        self._documentSize  = (w,h)
        self._retuneGeometry()
        self.update()

    def superResize(self,x,y,w,h):
        dx,dy = self._documentPos
        dw,dh = self._documentSize
        if (x,y,w,h) == (dx,dy,dw,dh): return
        if w<0: x=dx;w=dw
        if h<0: y=dy;h=dh
        self._documentPos  = (x,y)
        self._documentSize = (w,h)
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

    def exportLayer(self, full=False, palette=True, crop=True) -> dict:
        if self._currentLayer:
            return self._currentLayer.exportLayer(full=full,palette=palette,crop=crop)
        return {}

    def exportDocument(self, full=True, palette=True, crop=True) -> dict:
        pw,ph = self._documentSize
        outData  = {
            'version':'1.0.0',
            'size':(pw,ph),
            'layers':[l.exportLayer(full=full,palette=palette,crop=crop) for l in self._canvasLayers]}
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
        dw,dh = self._documentSize
        ox, oy = self.getViewOffsets()
        mp = self._mousePress
        mm = self._mouseMove
        md = self._mouseDrag
        mr = self._mouseRelease
        l = self._currentLayer
        lx,ly = l.pos()

        if self._tool & self.Tool.MOVE and mp and not md:
            if self._tool & self.Tool.RESIZE and not md:
                mpx,mpy = mp
                self._resizeData = None
                def _getSelected(_x,_y,_w,_h):
                    _selected = ttk.TTkK.NONE
                    if _x <= mpx < _x+_w and mpy == _y:      _selected |= ttk.TTkK.TOP
                    if _x <= mpx < _x+_w and mpy == _y+_h-1: _selected |= ttk.TTkK.BOTTOM
                    if _y <= mpy < _y+_h and mpx == _x:      _selected |= ttk.TTkK.LEFT
                    if _y <= mpy < _y+_h and mpx == _x+_w-1: _selected |= ttk.TTkK.RIGHT
                    return _selected
                # Main Area Resize Borders
                if selected :=  _getSelected(dx-1,dy-1,dw+2,dh+2):
                    self._resizeData = {'type':PaintArea,'selected':selected,'cb':self.superResize,'geometry':(dx,dy,dw,dh)}
                elif  l:
                    # Selected Layer Resize Borders
                    lx,ly = l.pos()
                    lw,lh = l.size()
                    if selected := _getSelected(dx+lx-1,dy+ly-1,lw+2,lh+2):
                        self._resizeData = {'type':CanvasLayer,'selected':selected,'cb':l.superResize,'geometry':(lx,ly,lw,lh)}
            if not self._resizeData:
                # Get The Layer to Move
                self._moveData = None
                for lm in reversed(self._canvasLayers):
                    mpx,mpy = mp
                    lmx,lmy = lm.pos()
                    self._moveData = {'type':PaintArea,'pos':(dx,dy)}
                    if lm.isOpaque(mpx-lmx-dx,mpy-lmy-dy):
                        self._currentLayer = lm
                        tml = lm
                        self._moveData = {'type':CanvasLayer,'pos':tml.pos(),'layer':tml}
                        self.selectedLayer.emit(lm)
                        break

        elif self._tool & self.Tool.MOVE and mp and md:
            # Move/Resize Tool
            if self._tool & self.Tool.RESIZE and (rData:=self._resizeData):
                _rx,_ry,_rw,_rh = rData['geometry']
                _rdx,_rdy,_rdw,_rdh=(_rx,_ry,_rw,_rh)
                mpx,mpy = mp
                mdx,mdy = md
                diffx = mdx-mpx
                diffy = mdy-mpy
                if rData['selected'] & ttk.TTkK.TOP:    _rdh-=diffy ; _rdy+=diffy
                if rData['selected'] & ttk.TTkK.BOTTOM: _rdh+=diffy
                if rData['selected'] & ttk.TTkK.LEFT:   _rdw-=diffx ; _rdx+=diffx
                if rData['selected'] & ttk.TTkK.RIGHT:  _rdw+=diffx
                rData['cb'](_rdx,_rdy,_rdw,_rdh)
            if not self._resizeData and (mData:=self._moveData):
                mpx,mpy = mp
                mdx,mdy = md
                pdx,pdy = mdx-mpx,mdy-mpy
                if mData['type']==CanvasLayer:
                    px,py = self._moveData['pos']
                    self._moveData['layer'].move(px+pdx,py+pdy)
                    self.selectedLayer.emit(self._moveData['layer'])
                elif mData['type']==PaintArea:
                    px,py = self._moveData['pos']
                    self._documentPos = (px+pdx,py+pdy)
            self._retuneGeometry()

        elif self._tool == self.Tool.BRUSH:
            if mp or md:
                if md: mx,my = md
                else:  mx,my = mp
                preview=False
                self._currentLayer.placeGlyph(mx-lx-dx,my-ly-dy,self._glyph,self._glyphColor,preview)
            elif mm:
                mx,my = mm
                preview=True
                self._currentLayer.placeGlyph(mx-lx-dx,my-ly-dy,self._glyph,self._glyphColor,preview)

        elif self._tool in (self.Tool.RECTEMPTY, self.Tool.RECTFILL):
            if mr and mp:
                mpx,mpy = mp
                mrx,mry = mr
                preview=False
                self._currentLayer.placeFill((mpx-lx-dx,mpy-ly-dy,mrx-lx-dx,mry-ly-dy),self._tool,self._glyph,self._glyphColor,preview)
            elif md:
                mpx,mpy = mp
                mrx,mry = md
                preview=True
                self._currentLayer.placeFill((mpx-lx-dx,mpy-ly-dy,mrx-lx-dx,mry-ly-dy),self._tool,self._glyph,self._glyphColor,preview)
        self.update()

    def mouseMoveEvent(self, evt) -> bool:
        ox, oy = self.getViewOffsets()
        self._mouseMove = (evt.x+ox,evt.y+oy)
        self._mouseDrag = None
        self._handleAction()
        return True

    def mouseDragEvent(self, evt) -> bool:
        ox, oy = self.getViewOffsets()
        self._mouseDrag=(evt.x+ox,evt.y+oy)
        self._mouseMove= None
        self._handleAction()
        return True

    def mousePressEvent(self, evt) -> bool:
        ox, oy = self.getViewOffsets()
        self._mousePress=(evt.x+ox,evt.y+oy)
        self._moveData     = None
        self._mouseMove    = None
        self._mouseDrag    = None
        self._mouseRelease = None
        self._handleAction()
        return True

    def mouseReleaseEvent(self, evt) -> bool:
        ox, oy = self.getViewOffsets()
        self._mouseRelease=(evt.x+ox,evt.y+oy)
        self._mouseMove   = None
        self._handleAction()
        self._moveData     = None
        self._resizeData   = None
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

    def paintEvent(self, canvas:ttk.TTkCanvas):
        dx,dy = self._documentPos
        ox, oy = self.getViewOffsets()
        dw,dh = self._documentSize
        dox,doy = dx-ox,dy-oy
        cw,ch = canvas.size()
        w=min(cw,dw)
        h=min(ch,dh)
        tcb = self._transparentColor['base']
        tcd = self._transparentColor['dim']

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

        for l in self._canvasLayers:
            lx,ly = l.pos()
            l.drawInCanvas(pos=(lx+dox,ly+doy),canvas=canvas)

        if self._tool & self.Tool.RESIZE:
            rd = self._resizeData
            def _drawResizeBorders(_rx,_ry,_rw,_rh,_sel):
                selColor = ttk.TTkColor.YELLOW + ttk.TTkColor.BG_BLUE
                # canvas.drawBox(pos=_pos,size=_size)
                canvas.drawText(pos=(_rx      ,_ry      ),text='─'*_rw, color=selColor if _sel & ttk.TTkK.TOP    else ttk.TTkColor.RST)
                canvas.drawText(pos=(_rx      ,_ry+_rh-1),text='─'*_rw, color=selColor if _sel & ttk.TTkK.BOTTOM else ttk.TTkColor.RST)
                for _y in range(_ry,_ry+_rh):
                    canvas.drawText(pos=(_rx      ,_y),text='│',color=selColor if _sel & ttk.TTkK.LEFT  else ttk.TTkColor.RST)
                    canvas.drawText(pos=(_rx+_rw-1,_y),text='│',color=selColor if _sel & ttk.TTkK.RIGHT else ttk.TTkColor.RST)
                canvas.drawChar(pos=(_rx      ,_ry      ), char='▛')
                canvas.drawChar(pos=(_rx+_rw-1,_ry      ), char='▜')
                canvas.drawChar(pos=(_rx      ,_ry+_rh-1), char='▙')
                canvas.drawChar(pos=(_rx+_rw-1,_ry+_rh-1), char='▟')

            sMain  = rd['selected'] if rd and rd['type'] == PaintArea   else ttk.TTkK.NONE
            sLayer = rd['selected'] if rd and rd['type'] == CanvasLayer else ttk.TTkK.NONE

            _drawResizeBorders(dx-ox-1, dy-oy-1, dw+2, dh+2, sMain)

            if l:=self._currentLayer:
                lx,ly = l.pos()
                lw,lh = l.size()
                _drawResizeBorders(lx+dx-ox-1, ly+dy-oy-1, lw+2, lh+2, sLayer)


class PaintScrollArea(ttk.TTkAbstractScrollArea):
    def __init__(self, pwidget:PaintArea, **kwargs):
        super().__init__(**kwargs)
        self.setViewport(pwidget)