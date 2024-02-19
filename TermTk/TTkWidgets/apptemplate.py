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

__all__ = ['TTkAppTemplate']

from dataclasses import dataclass
from TermTk.TTkCore.canvas import TTkCanvas

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkLayouts import TTkLayout, TTkGridLayout
from TermTk.TTkWidgets.container import TTkWidget, TTkContainer

class TTkAppTemplate(TTkContainer):
    ''' TTkAppTemplate Layout sizes:

    ::

        App Template Layout
        ┌─────────────────────────────────┐
        │         Header                  │
        ├─────────┬──────────────┬────────┤ H (1,2,3)
        │         │   Top        │        │
        │         ├──────────────┤        │ T
        │         │              │        │
        │  Right  │   Main       │  Left  │
        │         │   Center     │        │
        │         │              │        │
        │         ├──────────────┤        │ B
        │         │   Bottom     │        │
        ├─────────┴──────────────┴────────┤ F (1,2,3)
        │         Footer                  │
        └─────────────────────────────────┘
                  R              L
    '''

    MAIN   = TTkK.CENTER
    TOP    = TTkK.TOP
    BOTTOM = TTkK.BOTTOM
    LEFT   = TTkK.LEFT
    RIGHT  = TTkK.RIGHT
    CENTER = TTkK.CENTER
    HEADER = TTkK.HEADER
    FOOTER = TTkK.FOOTER

    @dataclass(frozen=False)
    class _Panel:
        # It's either item or widget
        item:   TTkLayout = None
        widget: TTkWidget = None
        size   = 0
        border = True
        fixed  = False

        def setGeometry(self,x,y,w,h):
            if it := self.item:
                it.setGeometry(x,y,w,h)
            elif wid := self.widget:
                wid.setGeometry(x,y,w,h)

        def isVisible(self):
            if self.widget:
                return self.widget.isVisible()
            return True

        def geometry(self):
            if it := self.item:
                return it.geometry()
            if wid := self.widget:
                return wid.geometry()
            return (0,0,0,0)

        def getSize(self):
            if it := self.item:
                return it.size()
            if wid := self.widget:
                return wid.size()
            return (0,0)

        def minimumWidth(self):
            if it := self.item:
                return it.minimumWidth()
            if wid := self.widget:
                return wid.minimumWidth()
            return 0

        def minimumHeight(self):
            if it := self.item:
                return it.minimumHeight()
            if wid := self.widget:
                return wid.minimumHeight()
            return 0

        def maximumWidth(self):
            if it := self.item:
                return it.maximumWidth()
            if wid := self.widget:
                return wid.maximumWidth()
            return 0x10000

        def maximumHeight(self):
            if it := self.item:
                return it.maximumHeight()
            if wid := self.widget:
                return wid.maximumHeight()
            return 0x10000

    __slots__ = ('_panels', '_splitters', '_selected'
                 #Signals
                 )
    def __init__(self, **kwargs):
        self._panels = {
            TTkAppTemplate.MAIN   : TTkAppTemplate._Panel(item=TTkLayout()) ,
            TTkAppTemplate.TOP    : None ,
            TTkAppTemplate.BOTTOM : None ,
            TTkAppTemplate.LEFT   : None ,
            TTkAppTemplate.RIGHT  : None ,
            TTkAppTemplate.HEADER : None ,
            TTkAppTemplate.FOOTER : None }
        self._splitters = {
            TTkAppTemplate.TOP    : None ,
            TTkAppTemplate.BOTTOM : None ,
            TTkAppTemplate.LEFT   : None ,
            TTkAppTemplate.RIGHT  : None ,
            TTkAppTemplate.HEADER : None ,
            TTkAppTemplate.FOOTER : None }
        self._selected = None

        super().__init__( **kwargs)
        self.layout().addItem(self._panels[TTkAppTemplate.MAIN].item)
        self._updateGeometries()
        self.setFocusPolicy(TTkK.ClickFocus)

    def setWidget(self, widget, location):
        if not self._panels[location]:
            self._panels[location] = TTkAppTemplate._Panel()
        self._panels[location].widget = widget
        if it:=self._panels[location].item:
            self.layout().removeItem(it)
            self._panels[location].item = None
        if widget:
            self.layout().addWidget(widget)
            self._panels[location].size = widget.minimumWidth() if location in (TTkAppTemplate.LEFT,TTkAppTemplate.RIGHT) else widget.maximumWidth()
        self._updateGeometries()

    def setItem(self, item, location):
        if not self._panels[location]:
            self._panels[location] = TTkAppTemplate._Panel()
        self._panels[location].item = item
        if wid:=self._panels[location].widget:
            self.layout().removeWdget(wid)
            self._panels[location].widget = None
        if item:
            self.layout().addItem(item)
        self._updateGeometries()

    def setBorder(self, border=True, location=MAIN):
        if not self._panels[location]:
            self._panels[location] = TTkAppTemplate._Panel()
        self._panels[location].border = border
        self._updateGeometries()

    def setFixed(self, fixed=False, location=MAIN):
        if not self._panels[location]:
            self._panels[location] = TTkAppTemplate._Panel()
        self._panels[location].fixed = fixed
        self._updateGeometries()

    def resizeEvent(self, w, h):
        self._updateGeometries()

    def focusOutEvent(self):
        self._selected = None
        self.update()

    def mouseReleaseEvent(self, evt):
        self._selected = None
        self.update()
        return True

    def mousePressEvent(self, evt):
        self._selected = []
        self._updateGeometries()
        spl = self._splitters
        pns = self._panels
        for loc in (TTkAppTemplate.TOP, TTkAppTemplate.BOTTOM, TTkAppTemplate.HEADER, TTkAppTemplate.FOOTER):
            if (s:=spl[loc]) and not pns[loc].fixed and (p:=s['pos'])[1]==evt.y and p[0] <= evt.x <=p[0]+s['size']:
                self._selected.append(loc)
        for loc in (TTkAppTemplate.LEFT, TTkAppTemplate.RIGHT):
            if (s:=spl[loc]) and not pns[loc].fixed and (p:=s['pos'])[0]==evt.x and p[1] <= evt.y <=p[1]+s['size']:
                self._selected.append(loc)
        return True

    def mouseDragEvent(self, evt):
        if not self._selected: return False
        pns = self._panels
        for loc in self._selected:
            x,y,w,h = (p:=pns[loc]).geometry()
            if   loc == TTkAppTemplate.LEFT:
                p.size = evt.x-x
            elif loc == TTkAppTemplate.RIGHT:
                p.size = w+x-evt.x
            elif loc in (TTkAppTemplate.HEADER, TTkAppTemplate.TOP):
                p.size = evt.y-y
            else:
                p.size = h+y-evt.y
        self._updateGeometries()
        return True

    def minimumWidth(self):
        pns = self._panels

        # Header and Footer sizes
        mh=mf=0
        if (p:=pns[TTkAppTemplate.HEADER]) and p.isVisible(): mh = p.minimumWidth()
        if (p:=pns[TTkAppTemplate.FOOTER]) and p.isVisible(): mf = p.minimumWidth()

        # Center Right,Left sizes
        mcr=mcl=0
        if (p:=pns[TTkAppTemplate.RIGHT]) and p.isVisible():  mcr = p.minimumWidth() + ( 1 if p.border else 0 )
        if (p:=pns[TTkAppTemplate.LEFT ]) and p.isVisible():  mcl = p.minimumWidth() + ( 1 if p.border else 0 )

        # Center Top,Bottom sizes
        mct=mcb=0
        if (p:=pns[TTkAppTemplate.TOP   ]) and p.isVisible(): mct = p.minimumWidth()
        if (p:=pns[TTkAppTemplate.BOTTOM]) and p.isVisible(): mcb = p.minimumWidth()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).minimumWidth()

        return max(mh, mf, mcr+mcl+max(mct, mcb, mcm)) + (2 if p.border else 0)

    def maximumWidth(self):
        pns = self._panels

        # Header and Footer sizes
        mh=mf=0x10000
        if (p:=pns[TTkAppTemplate.HEADER]) and p.isVisible(): mh = p.maximumWidth()
        if (p:=pns[TTkAppTemplate.FOOTER]) and p.isVisible(): mf = p.maximumWidth()

        # Center Right,Left sizes
        mcr=mcl=0
        if (p:=pns[TTkAppTemplate.RIGHT]) and p.isVisible():  mcr = p.maximumWidth() + ( 1 if p.border else 0 )
        if (p:=pns[TTkAppTemplate.LEFT ]) and p.isVisible():  mcl = p.maximumWidth() + ( 1 if p.border else 0 )

        # Center Top,Bottom sizes
        mct=mcb=0x10000
        if (p:=pns[TTkAppTemplate.TOP   ]) and p.isVisible(): mct = p.maximumWidth()
        if (p:=pns[TTkAppTemplate.BOTTOM]) and p.isVisible(): mcb = p.maximumWidth()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).maximumWidth()

        return min(mh, mf, mcr+mcl+min(mct, mcb, mcm)) + (2 if p.border else 0)

    def minimumHeight(self):
        pns = self._panels

        # Header and Footer border and minHeight
        mh=mf=0
        # Header Footer
        if (p:=pns[TTkAppTemplate.HEADER]) and p.isVisible(): mh = p.minimumHeight() + ( 1 if p.border else 0 )
        if (p:=pns[TTkAppTemplate.FOOTER]) and p.isVisible(): mf = p.minimumHeight() + ( 1 if p.border else 0 )

        # Center Left,Right:
        mcr=mcl=0
        if (p:=pns[TTkAppTemplate.LEFT ]) and p.isVisible():  mcl = p.minimumHeight()
        if (p:=pns[TTkAppTemplate.RIGHT]) and p.isVisible():  mcr = p.minimumHeight()

        # Center Top,Bottom
        mct=mcb=0
        if (p:=pns[TTkAppTemplate.TOP   ]) and p.isVisible(): mct = p.minimumHeight() + ( 1 if p.border else 0 )
        if (p:=pns[TTkAppTemplate.BOTTOM]) and p.isVisible(): mcb = p.minimumHeight() + ( 1 if p.border else 0 )

        mcm = (p:=pns[TTkAppTemplate.MAIN]).minimumHeight()

        return mh+mf+max(mcr ,mcl, mcm+mct+mcb ) + ( 2 if p.border else 0 )

    def maximumHeight(self):
        pns = self._panels

        # Header and Footer border and minHeight
        mh=mf=0
        # Header Footer
        if (p:=pns[TTkAppTemplate.HEADER]) and p.isVisible(): mh = p.maximumHeight() + ( 1 if p.border else 0 )
        if (p:=pns[TTkAppTemplate.FOOTER]) and p.isVisible(): mf = p.maximumHeight() + ( 1 if p.border else 0 )

        # Center Left,Right:
        mcr=mcl=0x10000
        if (p:=pns[TTkAppTemplate.LEFT ]) and p.isVisible():  mcl = p.maximumHeight()
        if (p:=pns[TTkAppTemplate.RIGHT]) and p.isVisible():  mcr = p.maximumHeight()

        # Center Top,Bottom
        mct=mcb=0
        if (p:=pns[TTkAppTemplate.TOP   ]) and p.isVisible(): mct = p.maximumHeight() + ( 1 if p.border else 0 )
        if (p:=pns[TTkAppTemplate.BOTTOM]) and p.isVisible(): mcb = p.maximumHeight() + ( 1 if p.border else 0 )

        mcm = (p:=pns[TTkAppTemplate.MAIN]).maximumHeight()

        return mh+mf+min(mcr ,mcl, mcm+mct+mcb ) + ( 2 if p.border else 0 )

    def _updateGeometries(self):
        w,h = self.size()
        pns = self._panels
        spl = self._splitters

        sl=sr=st=sb=sh=sf=0
        bm=bl=br=bt=bb=bh=bf=0
        # A,B,C,D HSplitters
        pt=pb=ph=pf=None
        if ( (p:=pns[TTkAppTemplate.TOP   ]) and p.isVisible() ): pt=p ; ptmin=p.minimumHeight() ; ptmax=p.maximumHeight() ; st=min(max(p.size,ptmin),ptmax) ; ft=p.fixed ; bt=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.BOTTOM]) and p.isVisible() ): pb=p ; pbmin=p.minimumHeight() ; pbmax=p.maximumHeight() ; sb=min(max(p.size,pbmin),pbmax) ; fb=p.fixed ; bb=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.HEADER]) and p.isVisible() ): ph=p ; phmin=p.minimumHeight() ; phmax=p.maximumHeight() ; sh=min(max(p.size,phmin),phmax) ; fh=p.fixed ; bh=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.FOOTER]) and p.isVisible() ): pf=p ; pfmin=p.minimumHeight() ; pfmax=p.maximumHeight() ; sf=min(max(p.size,pfmin),pfmax) ; ff=p.fixed ; bf=1 if p.border else 0
        # E,F     VSplitters
        pl=pr=None
        if ( (p:=pns[TTkAppTemplate.LEFT  ]) and p.isVisible() ): pl=p ; plmin=p.minimumWidth()  ; plmax=p.maximumWidth()  ; sl=min(max(p.size,plmin),plmax) ; fl=p.fixed ; bl=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.RIGHT ]) and p.isVisible() ): pr=p ; prmin=p.minimumWidth()  ; prmax=p.maximumWidth()  ; sr=min(max(p.size,prmin),prmax) ; fr=p.fixed ; br=1 if p.border else 0

        # Main Boundaries
        pm=pns[TTkAppTemplate.MAIN]
        mmaxw = pm.maximumWidth()
        mminw = pm.minimumWidth()
        mmaxh = pm.maximumHeight()
        mminh = pm.minimumHeight()
        bm = 1 if pns[TTkAppTemplate.MAIN].border else 0
        w-=(bm<<1)+bl+br
        h-=(bm<<1)+bt+bb+bh+bf

        # check horizontal sizes
        if not (mminw <= (newszw:=(w-sl-sr)) <= mmaxw):
            # the main width does not fit
            # we need to move the (E,F) splitters
            # * to avoid extra complexity,
            #   Let's resize the right panel first
            #   and adjust the left one to allows the
            #   main panel to fit again
            if newszw < mminw:
                if pr:                    pr.size = sr = max(prmin, w-mminw-sl) ; newszw=w-sl-sr
                if newszw < mminw and pl: pl.size = sl = max(plmin, w-mminw-sr) ; newszw=w-sl-sr
            else:
                if pr:                    pr.size = sr = min(prmax, w-mmaxw-sl) ; newszw=w-sl-sr
                if newszw > mmaxw and pl: pl.size = sl = min(plmax, w-mmaxw-sr) ; newszw=w-sl-sr

        # check vertical sizes
        if not (mminh <= (newszh:=(h-st-sb-sh-sf)) <= mmaxh):
            # almost same as before except that there are 4 panels to be considered instead of 2
            if newszh < mminh:
                if pf:                    pf.size = sf = max(pfmin, h-mminh-sb-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh < mminh and pb: pb.size = sb = max(pbmin, h-mminh-sf-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh < mminh and pt: pt.size = st = max(ptmin, h-mminh-sf-sb-sh) ; newszh=h-st-sb-sh-sf
                if newszh < mminh and ph: ph.size = sh = max(phmin, h-mminh-sf-sb-st) ; newszh=h-st-sb-sh-sf
            else:
                if pf:                    pf.size = sf = min(pfmax, h-mmaxh-sb-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh > mmaxh and pb: pb.size = sb = min(pbmax, h-mmaxh-sf-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh > mmaxh and pt: pt.size = st = min(ptmax, h-mmaxh-sf-sb-sh) ; newszh=h-st-sb-sh-sf
                if newszh > mmaxh and ph: ph.size = sh = min(phmax, h-mmaxh-sf-sb-st) ; newszh=h-st-sb-sh-sf

        # check vertical sizes
        w+=bl+br
        h+=bt+bb+bh+bf
        pm.setGeometry(        bm+sl+bl           , bm+sh+bh+st+bt                 , newszw , newszh )

        if pl: pl.setGeometry( bm                 , bm+sh+bh                       , sl     , h-sh-bh-sf-bf )
        if pr: pr.setGeometry( bm+sl+bl+newszw+br , bm+sh+bh                       , sr     , h-sh-bh-sf-bf )

        if ph: ph.setGeometry( bm                 , bm                             , w      , sh )
        if pt: pt.setGeometry( bm+sl+bl           , bm+sh+bh                       , newszw , st )
        if pb: pb.setGeometry( bm+sl+bl           , bm+sh+bh+st+bt+newszh+bb       , newszw , sb )
        if pf: pf.setGeometry( bm                 , bm+sh+bh+st+bt+newszh+bb+sb+bf , w      , sf )

        # Define Splitter geometries
        w,h = self.size()
        spl[loc:=TTkAppTemplate.HEADER] = None if not bh else {'pos':(0   , bm+sh                      ) ,'size':w     , 'fixed':fh  }
        spl[loc:=TTkAppTemplate.FOOTER] = None if not bf else {'pos':(0   , bm+sh+bh+st+bt+newszh+bb+sb) ,'size':w     , 'fixed':ff  }

        ca = sh                          + (bm if ph else 0 )
        cb = bm+sh+bh+st+bt+newszh+bb+sb + (bf if pf else bm)
        spl[loc:=TTkAppTemplate.LEFT]   = None if not bl else {'pos':(bm+sl           , ca             ) ,'size':cb-ca , 'fixed':fl  }
        spl[loc:=TTkAppTemplate.RIGHT]  = None if not br else {'pos':(bm+sl+bl+newszw , ca             ) ,'size':cb-ca , 'fixed':fr  }

        ca = sl              + (bm if pl else 0 )
        cb = bm+sl+bl+newszw + (br if pr else bm)
        spl[loc:=TTkAppTemplate.TOP]    = None if not bt else {'pos':(ca        , bm+sh+bh+st          ) ,'size':cb-ca , 'fixed':ft }
        spl[loc:=TTkAppTemplate.BOTTOM] = None if not bb else {'pos':(ca        , bm+sh+bh+st+bt+newszh) ,'size':cb-ca , 'fixed':fb }

        self.update()

    def update(self, repaint: bool =True, updateLayout: bool =False, updateParent: bool =False):
        if updateLayout:
            self._updateGeometries()
        super().update(repaint=repaint,updateLayout=updateLayout,updateParent=updateParent)

    #def layout(self):
    #    return self._panels[TTkAppTemplate.MAIN].item

    #def setLayout(self, layout):
    #    self._panels[TTkAppTemplate.MAIN].item = layout

    def paintEvent(self, canvas: TTkCanvas):
        w,h = self.size()
        pns = self._panels
        spl = self._splitters

        if b:=pns[TTkAppTemplate.MAIN].border:
            canvas.drawBox(pos=(0,0), size=(w,h))

        selectColor = TTkColor.fg('#88FF00')

        # hline = ('╞','═','╡')
        # vline = ('╥','║','╨')

        def drawVLine(sp, color=TTkColor.RST):
            _x,_y = sp['pos']
            _w,_h = 1,sp['size']
            chs = ('│','┬','┴','╿','╽') if sp['fixed'] else ('║','╥','╨','┇','┇')
            canvas.fill(pos=(_x,_y), size=(_w,_h), color=color, char=chs[0] )
            canvas.drawChar(pos=(_x,_y),           color=color, char=chs[1]if b and _y==0    else chs[3])
            canvas.drawChar(pos=(_x,_y+_h-1),      color=color, char=chs[2]if b and _y+_h==h else chs[4])
        def drawHLine(sp, color=TTkColor.RST):
            _x,_y = sp['pos']
            _w,_h = sp['size'],1
            chs = ('─','├','┤','╾','╼') if sp['fixed'] else ('═','╞','╡','╍','╍')
            canvas.fill(pos=(_x,_y), size=(_w,_h), color=color, char=chs[0] )
            canvas.drawChar(pos=(_x,_y),           color=color, char=chs[1]if b and _x==0    else chs[3])
            canvas.drawChar(pos=(_x+_w-1,_y),      color=color, char=chs[2]if b and _x+_w==w else chs[4])

        # Draw the 4 splittters
        if (sp:=spl[loc:=TTkAppTemplate.HEADER]) : drawHLine(sp, color=selectColor if self._selected and loc in self._selected else TTkColor.RST)
        if (sp:=spl[loc:=TTkAppTemplate.FOOTER]) : drawHLine(sp, color=selectColor if self._selected and loc in self._selected else TTkColor.RST)
        if (sp:=spl[loc:=TTkAppTemplate.LEFT])   : drawVLine(sp, color=selectColor if self._selected and loc in self._selected else TTkColor.RST)
        if (sp:=spl[loc:=TTkAppTemplate.RIGHT])  : drawVLine(sp, color=selectColor if self._selected and loc in self._selected else TTkColor.RST)
        if (sp:=spl[loc:=TTkAppTemplate.TOP])    : drawHLine(sp, color=selectColor if self._selected and loc in self._selected else TTkColor.RST)
        if (sp:=spl[loc:=TTkAppTemplate.BOTTOM]) : drawHLine(sp, color=selectColor if self._selected and loc in self._selected else TTkColor.RST)

        # Draw the 12 intersect
        def drawIntersect(sph,spv,chs):
            if sph and spv:
                x = spv['pos'][0]
                y = sph['pos'][1]
                ch = chs[( 0 if sph['fixed'] else 0x01 ) | ( 0 if spv['fixed'] else 0x02 )]
                canvas.drawChar(pos=(x,y), char=ch)

        drawIntersect(spl[TTkAppTemplate.HEADER], spl[TTkAppTemplate.LEFT] , ('┬','╤','╥','╦'))
        drawIntersect(spl[TTkAppTemplate.HEADER], spl[TTkAppTemplate.RIGHT], ('┬','╤','╥','╦'))
        drawIntersect(spl[TTkAppTemplate.FOOTER], spl[TTkAppTemplate.LEFT] , ('┴','╧','╨','╩'))
        drawIntersect(spl[TTkAppTemplate.FOOTER], spl[TTkAppTemplate.RIGHT], ('┴','╧','╨','╩'))
        drawIntersect(spl[TTkAppTemplate.TOP   ], spl[TTkAppTemplate.LEFT] , ('├','╞','╟','╠'))
        drawIntersect(spl[TTkAppTemplate.TOP   ], spl[TTkAppTemplate.RIGHT], ('┤','╡','╢','╣'))
        drawIntersect(spl[TTkAppTemplate.BOTTOM], spl[TTkAppTemplate.LEFT] , ('├','╞','╟','╠'))
        drawIntersect(spl[TTkAppTemplate.BOTTOM], spl[TTkAppTemplate.RIGHT], ('┤','╡','╢','╣'))


        return super().paintEvent(canvas)