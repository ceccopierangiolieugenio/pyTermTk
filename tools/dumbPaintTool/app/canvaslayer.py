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

__all__ = ['CanvasLayer']

import TermTk as ttk

from .const import ToolType

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
    __slot__ = ('_pos','_name','_visible','_size','_data','_colors','_preview','_offset',
                '_snapVersion', '_snapshots',
                #signals
                'nameChanged','changed')
    def __init__(self,name:ttk.TTkString=ttk.TTkString('New')) -> None:
        self.changed = ttk.pyTTkSignal()
        self._name:ttk.TTkString = ttk.TTkString(name) if isinstance(name,str) else name
        self.nameChanged = ttk.pyTTkSignal(ttk.TTkString)
        self._snapVersion = 0
        self._snapshots = {}
        self._pos  = (0,0)
        self._size = (0,0)
        self._offset = (0,0)
        self._visible = True
        self._preview = None
        self._data:  list[list[str         ]] = []
        self._colors:list[list[ttk.TTkColor]] = []

    def clone(self) -> object:
        cl = CanvasLayer()
        cl._snapVersion = self._snapVersion
        cl._pos     = self._pos
        cl._size    = self._size
        cl._offset  = self._offset
        cl._visible = self._visible
        cl._data    = [row.copy() for row in self._data]
        cl._colors  = [row.copy() for row in self._colors]
        return cl

    def restore(self, cl: object) -> None:
        self._preview = None
        self._snapVersion = cl._snapVersion
        self._pos     = cl._pos
        self._size    = cl._size
        self._offset  = cl._offset
        self._visible = cl._visible
        self._data    = [row.copy() for row in cl._data]
        self._colors  = [row.copy() for row in cl._colors]
        self.changed.emit()

    def restoreSnapshot(self, id:int) -> None:
        if id == self._snapVersion:
            return
        ttk.TTkLog.debug(f"restore {id=}")
        if id in self._snapshots:
            self.restore(self._snapshots[id])

    def saveSnapshot(self) -> int:
        self._snapshots = {key:self._snapshots[key] for key in self._snapshots if key <= self._snapVersion}
        if self._snapVersion not in self._snapshots:
            ttk.TTkLog.debug(f"{self._snapVersion=}")
            self._snapshots[self._snapVersion] = self.clone()
        return self._snapVersion

    def clearSnapshot(self) -> None:
        self._snapshots = {}
        self.saveSnapshot()

    def __eq__(self, value: object) -> bool:
        return (
            issubclass(type(value),CanvasLayer) and
            self._pos     == value._pos     and
            self._size    == value._size    and
            self._offset  == value._offset  and
            self._visible == value._visible and
            all(a==b for a,b in zip(self._data,  value._data)) and
            all(a==b for a,b in zip(self._colors,value._colors)) )

    def update(self):
        self.changed.emit()

    def pos(self):
        return self._pos
    def size(self):
        return self._size

    def visible(self):
        return self._visible
    @ttk.pyTTkSlot(bool)
    def setVisible(self, visible):
        if visible == self._visible: return
        self._snapVersion += 1
        self._visible = visible
        self.changed.emit()

    def name(self):
        return self._name
    @ttk.pyTTkSlot(str)
    def setName(self, name):
        self._snapVersion += 1
        self._name = name

    def glyphColorAt(self, x, y):
        ox,oy = self._offset
        w,h = self._size
        data = self._data
        colors = self._colors
        return data[oy+y][ox+x], colors[oy+y][ox+x]

    def isOpaque(self,x,y):
        if not self._visible: return False
        ox,oy = self._offset
        w,h = self._size
        data = self._data
        colors = self._colors
        if 0<=x<w and 0<=y<h:
            return data[oy+y][ox+x] != ' ' or colors[oy+y][ox+x].hasBackground()
        return False

    def move(self,x,y):
        self._pos=(x,y)
        self._snapVersion += 1
        self.changed.emit()

    def resize(self,w,h):
        self._size = (w,h)
        self._data   = (self._data   + [[] for _ in range(h)])[:h]
        self._colors = (self._colors + [[] for _ in range(h)])[:h]
        for i in range(h):
            self._data[i]   = (self._data[i]   + [' '              for _ in range(w)])[:w]
            self._colors[i] = (self._colors[i] + [ttk.TTkColor.RST for _ in range(w)])[:w]
        self._snapVersion += 1
        self.changed.emit()

    def superResize(self,dx,dy,dw,dh):
        ox,oy = self._offset
        x,y = self.pos()
        w,h = self.size()
        daw = len(self._data[0])
        dah = len(self._data)
        diffx = dx-x
        diffy = dy-y
        self._preview = None
        if ox < x-dx: # we need to resize and move ox
            _nw = x-dx-ox
            ox  = x-dx
            self._data   = [([' ']*_nw             ) + _r for _r in self._data]
            self._colors = [([ttk.TTkColor.RST]*_nw) + _r for _r in self._colors]
        if dw+ox > daw:
            _nw = dw+ox-daw
            self._data   = [_r + ([' ']*_nw             )  for _r in self._data]
            self._colors = [_r + ([ttk.TTkColor.RST]*_nw)  for _r in self._colors]
        daw = len(self._data[0])
        if oy < y-dy: # we need to resize and move ox
            _nh = y-dy-oy
            oy  = y-dy
            self._data   = [[' ']*daw              for _ in range(_nh)] + self._data
            self._colors = [[ttk.TTkColor.RST]*daw for _ in range(_nh)] + self._colors
        if dh+oy > dah:
            _nh = dh+oy-dah
            self._data   = self._data   + [[' ']*daw              for _ in range(_nh)]
            self._colors = self._colors + [[ttk.TTkColor.RST]*daw for _ in range(_nh)]
        self._offset = (ox+diffx,oy+diffy)
        self._pos  = (dx,dy)
        self._size = (dw,dh)
        self._snapVersion += 1
        self.changed.emit()

    def clean(self):
        w,h = self._size
        self._offset = (0,0)
        self._preview = None
        for i in range(h):
            self._data[i]   = [' ']*w
            self._colors[i] = [ttk.TTkColor.RST]*w
        self._snapVersion += 1
        self.changed.emit()

    def cleanPreview(self):
        self._preview = None
        self.changed.emit()

    def toTTkString(self):
        ret = []
        pw,ph = self._size
        ox,oy = self._offset
        if not (pw and ph) : return ttk.TTkString()
        for d,c in zip(self._data[oy:oy+ph],self._colors[oy:oy+ph]):
            ret.append(ttk.TTkString._importString1(''.join(d[ox:ox+pw]),c[ox:ox+pw]))
        return ttk.TTkString('\n').join(ret)

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
            xa,xb,ya,yb = 0x10000,0,0x10000,0
            for y,(drow,crow) in enumerate(zip(data,colors)):
                for x,(d,c) in enumerate(zip(drow,crow)):
                    if d != ' ' or c.hasBackground():
                        xa,xb = min(x,xa),max(x,xb)
                        ya,yb = min(y,ya),max(y,yb)
            if (xa,xb,ya,yb) == (0x10000,0,0x10000,0):
                xa=xb=ya=yb=0
            else:
                xb+=1
                yb+=1
        else:
            xa,xb,ya,yb = 0,daw,0,dah

        # Visble Area intersecting the bounding box
        vxa,vya = max(px,px+xa-ox),   max(py,py+ya-oy)
        vxb,vyb = min(px+pw,vxa+xb-xa),min(py+ph,vya+yb-ya)
        vw,vh   = vxb-vxa, vyb-vya

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
                    fg = f"{c.getHex(ttk.TTkK.ColorType.Foreground)}" if c.hasForeground() else None
                    bg = f"{c.getHex(ttk.TTkK.ColorType.Background)}" if c.hasBackground() else None
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
                fg = f"{c.getHex(ttk.TTkK.ColorType.Foreground)}" if c.hasForeground() else None
                bg = f"{c.getHex(ttk.TTkK.ColorType.Background)}" if c.hasBackground() else None
                if palette:
                    outData['colors'][-1].append(palette.index((fg,bg)))
                else:
                    outData['colors'][-1].append((fg,bg))

        return outData

    def _import_v1_1_0(self, dd):
        self._import_v1_0_0(dd)
        # Fix the correct size if the data has been trimmed in the wrong save
        ox,oy = self._offset = dd.get('offset',(0,0))
        ttk.TTkLog.debug(f"{self._offset=} {self._size=} {self._pos=}")
        ttk.TTkLog.debug(f"{len(self._data[0])=}")
        w,h = self._size
        dw = len(self._data[0])
        dh = len(self._data)
        w = min(w,dw-ox)
        h = min(h,dh-oy)
        self._size = w,h
        # px,py = self._pos
        # self.superResize(x,y,w,h)

    def _import_v1_0_0(self, dd):
        self._pos  = dd['pos']
        self._size = dd['size']
        self._name = ttk.TTkString(dd['name'])
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
        self._snapVersion += 1
        self.changed.emit()

    def trim(self):
        pw,ph = self._size
        ox,oy = self._offset
        cl = CanvasLayer()
        if not (pw and ph) : return cl

        tmpd = [r[ox:ox+pw] for r in self._data[  oy:oy+ph]]
        tmpc = [r[ox:ox+pw] for r in self._colors[oy:oy+ph]]
        # Trim
        xa,xb,ya,yb = 0x10000,0,0x10000,0
        for y,(drow,crow) in enumerate(zip(tmpd,tmpc)):
            for x,(d,c) in enumerate(zip(drow,crow)):
                if d != ' ' or c.hasBackground():
                    xa,xb = min(x,xa),max(x,xb)
                    ya,yb = min(y,ya),max(y,yb)
        if (xa,xb,ya,yb) == (0x10000,0,0x10000,0):
            xa=xb=ya=yb=0

        cl._data   = [r[xa:xb+1] for r in tmpd[ya:yb+1]]
        cl._colors = [r[xa:xb+1] for r in tmpc[ya:yb+1]]

        w = xb-xa+1
        h = yb-ya+1

        cl._size = (w,h)
        cl._name = self._name
        return cl

    def importTTkString(self, txt:ttk.TTkString):
        tmpd = []
        tmpc = []
        for line in txt.split('\n'):
            d,c = line.getData()
            tmpd.append(list(d))
            tmpc.append(list(c))
        # Trim
        xa,xb,ya,yb = 0x10000,0,0x10000,0
        for y,(drow,crow) in enumerate(zip(tmpd,tmpc)):
            for x,(d,c) in enumerate(zip(drow,crow)):
                if d != ' ' or c.hasBackground():
                    xa,xb = min(x,xa),max(x,xb)
                    ya,yb = min(y,ya),max(y,yb)
        if (xa,xb,ya,yb) == (0x10000,0,0x10000,0):
            xa=xb=ya=yb=0

        self._data   = data   = [r[xa:xb+1] for r in tmpd[ya:yb+1]]
        self._colors = colors = [r[xa:xb+1] for r in tmpc[ya:yb+1]]

        w = xb-xa+1
        h = yb-ya+1

        for i,(d,c) in enumerate(zip(data,colors)):
            data[i]   = (d + [' ']*w)[:w]
            colors[i] = (c + [ttk.TTkColor.RST]*w)[:w]

        self._size = (w,h)
        self._name = ttk.TTkString("Pasted")
        self._snapVersion += 1

    def placeFill(self,geometry,tool,glyph:str,color:ttk.TTkColor,glyphEnabled=True,preview=False):
        ox,oy = self._offset
        w,h = self._size
        ax,ay,bx,by = geometry
        ax = max(0,min(w-1,ax))
        ay = max(0,min(h-1,ay))
        bx = max(0,min(w-1,bx))
        by = max(0,min(h-1,by))
        fax,fay = ox+min(ax,bx), oy+min(ay,by)
        fbx,fby = ox+max(ax,bx), oy+max(ay,by)

        if preview:
            data   = [_r.copy() for _r in self._data]
            colors = [_r.copy() for _r in self._colors]
            self._preview = {'data':data,'colors':colors}
        else:
            self._snapVersion += 1
            self._preview = None
            data   = self._data
            colors = self._colors

        if tool == ToolType.RECTFILL:
            for y in range(fay,fby+1):
                for x in range(fax,fbx+1):
                    self._placeGlyph(data,colors,x,y,glyph,color,glyphEnabled,preview)
        if tool == ToolType.RECTEMPTY:
            for x in range(fax,fbx+1):
                self._placeGlyph(data,colors,x,fay,glyph,color,glyphEnabled,preview)
                self._placeGlyph(data,colors,x,fby,glyph,color,glyphEnabled,preview)
            for y in range(fay,fby+1):
                self._placeGlyph(data,colors,fax,y,glyph,color,glyphEnabled,preview)
                self._placeGlyph(data,colors,fbx,y,glyph,color,glyphEnabled,preview)
        self.changed.emit()
        return True

    def placeGlyph(self,x,y,glyph:str,color:ttk.TTkColor,glyphEnabled=True,preview=False):
        if preview:
            data   = [_r.copy() for _r in self._data]
            colors = [_r.copy() for _r in self._colors]
            self._preview = {'data':data,'colors':colors}
        else:
            self._snapVersion += 1
            self._preview = None
            data   = self._data
            colors = self._colors

        self.changed.emit()
        return self._placeGlyph(data,colors,x,y,glyph,color,glyphEnabled,preview)

    def _placeGlyph(self,data,colors,x,y,glyph:str,color:ttk.TTkColor,glyphEnabled=True,preview=False):
        ox,oy = self._offset
        w,h = self._size

        if 0<=x<w and 0<=y<h:
            if glyphEnabled:
                color = color if glyph != ' ' else color.background()
                color = color if color else ttk.TTkColor.RST
                data[  oy+y][ox+x] = glyph
                colors[oy+y][ox+x] = color
            else:
                glyph = data[  oy+y][ox+x]
                oc = colors[oy+y][ox+x]
                nc = color
                if glyph==' ':
                    if oc.hasBackground():
                        colors[oy+y][ox+x] = oc.background()
                else:
                    fg = nc.foreground() if nc.hasForeground()                        else oc.foreground()
                    bg = nc.background() if nc.hasBackground() and oc.hasBackground() else oc.background() if oc.hasBackground() else fg
                    color = fg+bg
                    colors[oy+y][ox+x] = color
            return True
        return False

    def placeArea(self,x,y,area,transparent=False,preview=False):
        ox,oy = self._offset
        w,h = self._size

        dw,dh = area.size()
        darea = area._data
        carea = area._colors
        x-=dw//2
        y-=dh//2

        if preview:
            data   = [_r.copy() for _r in self._data]
            colors = [_r.copy() for _r in self._colors]
            self._preview = {'data':data,'colors':colors}
        else:
            self._snapVersion += 1
            self._preview = None
            data   = self._data
            colors = self._colors

        for _y,(darow,carow) in enumerate(zip(darea,carea),oy+y):
            for _x,(da,ca)   in enumerate(zip(darow,carow),ox+x):
                if 0<=_x<w and 0<=_y<h and ( da!=' ' or ca.hasBackground()):
                    if not transparent or (da==' ' and ca._bg):
                        data[_y][_x]   = da
                        colors[_y][_x] = ca
                    elif da!=' ':
                        data[_y][_x]   = da
                        cc = colors[_y][_x]
                        newC = ca.copy()
                        newC._bg = ca._bg if ca._bg else cc._bg
                        colors[_y][_x] = newC

        self.changed.emit()

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
