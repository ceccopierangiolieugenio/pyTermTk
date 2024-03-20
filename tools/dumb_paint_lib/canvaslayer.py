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
    class Tool(int):
        MOVE      = 0x01
        RESIZE    = 0x02
        BRUSH     = 0x04
        RECTFILL  = 0x08
        RECTEMPTY = 0x10

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

        if tool == CanvasLayer.Tool.RECTFILL:
            for row in data[fay:fby+1]:
                row[fax:fbx+1] = [glyph]*(fbx-fax+1)
            for row in colors[fay:fby+1]:
                row[fax:fbx+1] = [color]*(fbx-fax+1)
        if tool == CanvasLayer.Tool.RECTEMPTY:
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
