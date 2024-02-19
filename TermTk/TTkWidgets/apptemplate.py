
__all__ = ['TTkAppTemplate']

from dataclasses import dataclass
from TermTk.TTkCore.canvas import TTkCanvas

from TermTk.TTkCore.constant import TTkK
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

    __slots__ = ('_panels', '_splitters',
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

        super().__init__( **kwargs)
        self.layout().addItem(self._panels[TTkAppTemplate.MAIN].item)
        self._updateGeometries()

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

    def resizeEvent(self, w, h):
        self._updateGeometries()

    def minimumWidth(self):
        pns = self._panels

        # Header and Footer sizes
        mh=mf=0
        if p:=pns[TTkAppTemplate.HEADER]:
            mh = p.minimumWidth()
        if p:=pns[TTkAppTemplate.FOOTER]:
            mf = p.minimumWidth()

        # Center Right,Left sizes
        mcr=mcl=0
        if p:=pns[TTkAppTemplate.RIGHT]:
            mcr = p.minimumWidth() + ( 1 if p.border else 0 )
        if p:=pns[TTkAppTemplate.LEFT]:
            mcl = p.minimumWidth() + ( 1 if p.border else 0 )

        # Center Top,Bottom sizes
        mct=mcb=0
        if p:=pns[TTkAppTemplate.TOP]:
            mct = p.minimumWidth()
        if p:=pns[TTkAppTemplate.BOTTOM]:
            mcb = p.minimumWidth()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).minimumWidth()

        return max(mh, mf, mcr+mcl+max(mct, mcb, mcm)) + (2 if p.border else 0)

    def maximumWidth(self):
        pns = self._panels

        # Header and Footer sizes
        mh=mf=0x10000
        if p:=pns[TTkAppTemplate.HEADER]:
            mh = p.maximumWidth()
        if p:=pns[TTkAppTemplate.FOOTER]:
            mf = p.maximumWidth()

        # Center Right,Left sizes
        mcr=mcl=0
        if p:=pns[TTkAppTemplate.RIGHT]:
            mcr = p.maximumWidth() + ( 1 if p.border else 0 )
        if p:=pns[TTkAppTemplate.LEFT]:
            mcl = p.maximumWidth() + ( 1 if p.border else 0 )

        # Center Top,Bottom sizes
        mct=mcb=0x10000
        if p:=pns[TTkAppTemplate.TOP]:
            mct = p.maximumWidth()
        if p:=pns[TTkAppTemplate.BOTTOM]:
            mcb = p.maximumWidth()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).maximumWidth()

        return min(mh, mf, mcr+mcl+min(mct, mcb, mcm)) + (2 if p.border else 0)

    def minimumHeight(self):
        pns = self._panels

        # Header and Footer border and minHeight
        mh=mf=0
        # Header Footer
        if p:=pns[TTkAppTemplate.HEADER]:
            mh = p.minimumHeight() + ( 1 if p.border else 0 )
        if p:=pns[TTkAppTemplate.FOOTER]:
            mf = p.minimumHeight() + ( 1 if p.border else 0 )

        # Center Left,Right:
        mcr=mcl=0
        if p:=pns[TTkAppTemplate.LEFT]:
            mcl = p.minimumHeight()
        if p:=pns[TTkAppTemplate.RIGHT]:
            mcr = p.minimumHeight()

        # Center Top,Bottom
        mct=mcb=0
        if p:=pns[TTkAppTemplate.TOP]:
            mct = p.minimumHeight() + ( 1 if p.border else 0 )
        if p:=pns[TTkAppTemplate.BOTTOM]:
            mcb = p.minimumHeight() + ( 1 if p.border else 0 )

        mcm = (p:=pns[TTkAppTemplate.MAIN]).minimumHeight()

        return mh+mf+max(mcr ,mcl, mcm+mct+mcb ) + ( 2 if p.border else 0 )

    def maximumHeight(self):
        pns = self._panels

        # Header and Footer border and minHeight
        mh=mf=0
        # Header Footer
        if p:=pns[TTkAppTemplate.HEADER]:
            mh = p.maximumHeight() + ( 1 if p.border else 0 )
        if p:=pns[TTkAppTemplate.FOOTER]:
            mf = p.maximumHeight() + ( 1 if p.border else 0 )

        # Center Left,Right:
        mcr=mcl=0x10000
        if p:=pns[TTkAppTemplate.LEFT]:
            mcl = p.maximumHeight()
        if p:=pns[TTkAppTemplate.RIGHT]:
            mcr = p.maximumHeight()

        # Center Top,Bottom
        mct=mcb=0
        if p:=pns[TTkAppTemplate.TOP]:
            mct = p.maximumHeight() + ( 1 if p.border else 0 )
        if p:=pns[TTkAppTemplate.BOTTOM]:
            mcb = p.maximumHeight() + ( 1 if p.border else 0 )

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
        if ( (p:=pns[TTkAppTemplate.TOP])    and p.isVisible() ): pt=p ; st=p.size ; bt=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.BOTTOM]) and p.isVisible() ): pb=p ; sb=p.size ; bb=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.HEADER]) and p.isVisible() ): ph=p ; sh=p.size ; bh=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.FOOTER]) and p.isVisible() ): pf=p ; sf=p.size ; bf=1 if p.border else 0
        # E,F     VSplitters
        pl=pr=None
        if ( (p:=pns[TTkAppTemplate.LEFT])  and p.isVisible() ):  pl=p ; sl=p.size ; bl=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.RIGHT]) and p.isVisible() ):  pr=p ; sr=p.size ; br=1 if p.border else 0

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
                if pr:                    pr.size = sr = max(pr.minimumWidth(), w-mminw-sl) ; newszw=w-sl-sr
                if newszw < mminw and pl: pl.size = sl = max(pl.minimumWidth(), w-mminw-sr) ; newszw=w-sl-sr
            else:
                if pr:                    pr.size = sr = min(pr.maximumWidth(), w-mmaxw-sl) ; newszw=w-sl-sr
                if newszw > mmaxw and pl: pl.size = sl = min(pl.maximumWidth(), w-mmaxw-sr) ; newszw=w-sl-sr

        # check vertical sizes
        if not (mminh <= (newszh:=(h-st-sb-sh-sf)) <= mmaxh):
            # almost same as before except that there are 4 panels to be considered instead of 2
            if newszh < mminh:
                if pf:                    pf.size = sf = max(pf.minimumHeight(), h-mminh-sb-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh < mminh and pb: pb.size = sb = max(pb.minimumHeight(), h-mminh-sf-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh < mminh and pt: pt.size = st = max(pt.minimumHeight(), h-mminh-sf-sb-sh) ; newszh=h-st-sb-sh-sf
                if newszh < mminh and ph: ph.size = sh = max(ph.minimumHeight(), h-mminh-sf-sb-st) ; newszh=h-st-sb-sh-sf
            else:
                if pf:                    pf.size = sf = min(pf.maximumHeight(), h-mmaxh-sb-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh > mmaxh and pb: pb.size = sb = min(pb.maximumHeight(), h-mmaxh-sf-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh > mmaxh and pt: pt.size = st = min(pt.maximumHeight(), h-mmaxh-sf-sb-sh) ; newszh=h-st-sb-sh-sf
                if newszh > mmaxh and ph: ph.size = sh = min(ph.maximumHeight(), h-mmaxh-sf-sb-st) ; newszh=h-st-sb-sh-sf

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
        spl[TTkAppTemplate.HEADER] = None if not bh else {'pos':(0   , bm+sh                      ) ,'size':w }
        spl[TTkAppTemplate.FOOTER] = None if not bf else {'pos':(0   , bm+sh+bh+st+bt+newszh+bb+sb) ,'size':w }

        ca = sh                          + (bm if ph else 0 )
        cb = bm+sh+bh+st+bt+newszh+bb+sb + (bf if pf else bm)
        spl[TTkAppTemplate.LEFT]   = None if not bl else {'pos':(bm+sl           , ca             ) ,'size':cb-ca }
        spl[TTkAppTemplate.RIGHT]  = None if not br else {'pos':(bm+sl+bl+newszw , ca             ) ,'size':cb-ca }

        ca = sl              + (bm if pl else 0 )
        cb = bm+sl+bl+newszw + (br if pr else bm)
        spl[TTkAppTemplate.TOP]    = None if not bt else {'pos':(ca        , bm+sh+bh+st          ) ,'size':cb-ca }
        spl[TTkAppTemplate.BOTTOM] = None if not bb else {'pos':(ca        , bm+sh+bh+st+bt+newszh) ,'size':cb-ca }

        self.update()

    def update(self, repaint: bool =True, updateLayout: bool =False, updateParent: bool =False):
        if updateLayout:
            self._updateGeometries()
        super().update(repaint=repaint,updateLayout=updateLayout,updateParent=updateParent)

    #def layout(self):
    #    return self._panels[TTkAppTemplate.MAIN].item

    #def setLayout(self, layout):
    #    self._panels[TTkAppTemplate.MAIN].item = layout

    def paintEventOld(self, canvas: TTkCanvas):
        w,h = self.size()
        pns = self._panels

        sl=sr=st=sb=sh=sf=0
        bl=br=bt=bb=bh=bf=0

        bm = 1 if pns[TTkAppTemplate.MAIN].border else 0
        smw,smh = pns[TTkAppTemplate.MAIN].getSize()
        # A,B,C,D HSplitters
        pt=pb=ph=pf=None
        if ( (p:=pns[TTkAppTemplate.TOP])    and p.isVisible() ): pt=p ; st=p.size ; bt=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.BOTTOM]) and p.isVisible() ): pb=p ; sb=p.size ; bb=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.HEADER]) and p.isVisible() ): ph=p ; sh=p.size ; bh=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.FOOTER]) and p.isVisible() ): pf=p ; sf=p.size ; bf=1 if p.border else 0
        # E,F     VSplitters
        pl=pr=None
        if ( (p:=pns[TTkAppTemplate.LEFT])  and p.isVisible() ):  pl=p ; sl=p.size ; bl=1 if p.border else 0
        if ( (p:=pns[TTkAppTemplate.RIGHT]) and p.isVisible() ):  pr=p ; sr=p.size ; br=1 if p.border else 0

        if bm: canvas.drawBox(  pos= (0            , 0)                        , size= (w,h) )
        if bh: canvas.drawHLine(pos= (0            , bm+sh)                    , size= w )
        if bf: canvas.drawHLine(pos= (0            , bm+sh+bh+st+bt+smh+bb+sb) , size= w )

        ca = sh                       + (bm if ph else 0 )
        cb = bm+sh+bh+st+bt+smh+bb+sb + (bf if pf else bm)
        if bl: canvas.drawVLine(pos= (bm+sl        , ca)                    , size= cb-ca )
        if br: canvas.drawVLine(pos= (bm+sl+bl+smw , ca)                    , size= cb-ca )
        ca = sl           + (bm if pl else 0 )
        cb = bm+sl+bl+smw + (br if pr else bm)
        if bt: canvas.drawHLine(pos= (ca    , bm+sh+bh+st)              , size= cb-ca )
        if bb: canvas.drawHLine(pos= (ca    , bm+sh+bh+st+bt+smh)       , size= cb-ca )

        return super().paintEvent(canvas)

    def paintEvent(self, canvas: TTkCanvas):
        w,h = self.size()
        pns = self._panels
        spl = self._splitters

        if pns[TTkAppTemplate.MAIN].border:
            canvas.drawBox(pos=(0,0), size=(w,h))

        if (sp:=spl[TTkAppTemplate.HEADER]) : canvas.drawHLine(pos=sp['pos'],size=sp['size'])
        if (sp:=spl[TTkAppTemplate.FOOTER]) : canvas.drawHLine(pos=sp['pos'],size=sp['size'])
        if (sp:=spl[TTkAppTemplate.LEFT])   : canvas.drawVLine(pos=sp['pos'],size=sp['size'])
        if (sp:=spl[TTkAppTemplate.RIGHT])  : canvas.drawVLine(pos=sp['pos'],size=sp['size'])
        if (sp:=spl[TTkAppTemplate.TOP])    : canvas.drawHLine(pos=sp['pos'],size=sp['size'])
        if (sp:=spl[TTkAppTemplate.BOTTOM]) : canvas.drawHLine(pos=sp['pos'],size=sp['size'])

        return super().paintEvent(canvas)