
__all__ = ['TTkAppTemplate']

from dataclasses import dataclass

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkLayouts import TTkLayout, TTkGridLayout
from TermTk.TTkWidgets.container import TTkContainer

class TTkAppTemplate(TTkContainer):
    ''' TTkAppTemplate Layout sizes:

    ::

        App Template Layout
        ┌─────────────────────────────────┐
        │         Header                  │
        ├─────────┬──────────────┬────────┤ A (1,2,3)
        │         │   Top        │        │
        │         ├──────────────┤        │ B
        │         │              │        │
        │  Right  │   Main       │  Left  │
        │         │   Center     │        │
        │         │              │        │
        │         ├──────────────┤        │ C
        │         │   Bottom     │        │
        ├─────────┴──────────────┴────────┤ D (1,2,3)
        │         Footer                  │
        └─────────────────────────────────┘
                  E              F
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
    class _Border:
        pos = 0
        visible = False
        fixed = False

    @dataclass(frozen=False)
    class _Panel:
        # It's either item or widget
        item   = None
        widget = None
        size   = 0
        border = True
        fixed  = False

        def isVisible(self):
            if self.widget:
                return self.widget.isVisible()
            return True

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
                return it.maximumWidth()
            if wid := self.widget:
                return wid.maximumWidth()
            return 0x10000

    __slots__ = ('_panels',
                 '_ba','_bb','_bc','_bd','_be','_bf'
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
        self._ba=TTkAppTemplate._Border()
        self._bb=TTkAppTemplate._Border()
        self._bc=TTkAppTemplate._Border()
        self._bd=TTkAppTemplate._Border()
        self._be=TTkAppTemplate._Border()
        self._bf=TTkAppTemplate._Border()
        super().__init__( **kwargs)
        self.layout().addItem(self._panels[TTkAppTemplate.MAIN].item)
        self._updateGeometries()

    def setWidget(self, widget, location):
        self._panels[location].widget = widget
        if it:=self._panels[location].item:
            self.layout().removeItem(it)
            self._panels[location].item = None
        if widget:
            self.layout().addWidget(widget)
        self._updateGeometries()

    def setItem(self, item, location):
        self._panels[location].item = item
        if wid:=self._panels[location].widget:
            self.layout().removeWdget(wid)
            self._panels[location].widget = None
        if item:
            self.layout().addItem(item)
        self._updateGeometries()

    def minimumWidth(self):
        # ┌─────────────────────────────────┐
        # │         Header                  │
        # ├─────────┬──────────────┬────────┤
        # │         A   Top        B        │
        # │         ├──────────────┤        │
        # │         │              │        │
        # │  Right  C   Main       D  Left  │
        # │         │   Center     │        │
        # │         │              │        │
        # │         ├──────────────┤        │
        # │         E   Bottom     F        │
        # ├─────────┴──────────────┴────────┤
        # │         Footer                  │
        # └─────────────────────────────────┘
        pns = self._panels
        A=B=C=D=E=F=0

        # Header and Footer sizes
        mh=mf=0
        if p:=pns[TTkAppTemplate.HEADER]:
            mh = p.minimumWidth()
        if p:=pns[TTkAppTemplate.FOOTER]:
            mf = p.minimumWidth()

        # Center Right,Left sizes
        mcr=mcl=0
        pr,pl=0
        if p:=pns[TTkAppTemplate.RIGHT]:
            pr=1
            if p.border: A=C=E=1
            mcr = p.minimumWidth()
        if p:=pns[TTkAppTemplate.LEFT]:
            pl=1
            if p.border: B=D=F=1
            mcl = p.minimumWidth()

        # Center Top,Bottom sizes
        mct=mcb=0x10000
        if p:=pns[TTkAppTemplate.TOP]:
            if p.border:
                A=pr
                B=pl
            mct = p.minimumWidth()
        if p:=pns[TTkAppTemplate.BOTTOM]:
            if p.border:
                E=pr
                F=pl
            mcb = p.minimumWidth()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).minimumWidth()
        if p.border:
            C=pr
            D=pl

        return max(mh, mf, mcr+mcl+max(mct+A+B, mcb+E+F, mcm+C+D) )

    def maximumWidth(self):
        # ┌─────────────────────────────────┐
        # │         Header                  │
        # ├─────────┬──────────────┬────────┤
        # │         A   Top        B        │
        # │         ├──────────────┤        │
        # │         │              │        │
        # │  Right  C   Main       D  Left  │
        # │         │   Center     │        │
        # │         │              │        │
        # │         ├──────────────┤        │
        # │         E   Bottom     F        │
        # ├─────────┴──────────────┴────────┤
        # │         Footer                  │
        # └─────────────────────────────────┘
        pns = self._panels
        A=B=C=D=E=F=0

        # Header and Footer sizes
        mh=mf=0
        if p:=pns[TTkAppTemplate.HEADER]:
            mh = p.maximumWidth()
        if p:=pns[TTkAppTemplate.FOOTER]:
            mf = p.maximumWidth()

        # Center Right,Left sizes
        mcr=mcl=0
        pr,pl=0
        if p:=pns[TTkAppTemplate.RIGHT]:
            pr=1
            if p.border: A=C=E=1
            mcr = p.maximumWidth()
        if p:=pns[TTkAppTemplate.LEFT]:
            pl=1
            if p.border: B=D=F=1
            mcl = p.maximumWidth()

        # Center Top,Bottom sizes
        mct=mcb=0x10000
        if p:=pns[TTkAppTemplate.TOP]:
            if p.border:
                A=pr
                B=pl
            mct = p.maximumWidth()
        if p:=pns[TTkAppTemplate.BOTTOM]:
            if p.border:
                E=pr
                F=pl
            mcb = p.maximumWidth()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).maximumWidth()
        if p.border:
            C=pr
            D=pl

        return min(mh, mf, mcr+mcl+min(mct+A+B, mcb+E+F, mcm+C+D) )

    def minimumHeight(self):
        # ┌─────────────────────────────────┐
        # │         Header                  │
        # ├── A ────┬──── B ───────┬── C ───┤
        # │         │   Top        │        │
        # │         ├──── D ───────┤        │
        # │         │              │        │
        # │  Right  │   Main       │  Left  │
        # │         │   Center     │        │
        # │         │              │        │
        # │         ├──── E ───────┤        │
        # │         │   Bottom     │        │
        # ├── F ────┴──── G ───────┴── H ───┤
        # │         Footer                  │
        # └─────────────────────────────────┘
        pns = self._panels
        A=B=C=D=E=F=G=0 # 0 or 1 if the border is defined

        # Header and Footer border and minHeight
        mh=mf=0
        ph=pf=0

        # Header Footer
        if p:=pns[TTkAppTemplate.HEADER]:
            ph=1
            if p.border: A=B=C=1
            mh = p.minimumHeight()
        if p:=pns[TTkAppTemplate.FOOTER]:
            pf=1
            if p.border: F=G=H=1
            mf = p.minimumHeight()

        # Center Left,Right:
        mcr=mcl=0x10000
        if p:=pns[TTkAppTemplate.LEFT]:
            if p.border:
                C = ph
                H = pf
            mcl = p.minimumHeight()
        if p:=pns[TTkAppTemplate.RIGHT]:
            if p.border:
                A = ph
                F = pf
            mcr = p.minimumHeight()

        # Center Top,Bottom
        mct=mcb=0
        pct=pcb=0
        if p:=pns[TTkAppTemplate.TOP]:
            pct=1
            if p.border:
                B=ph
                D=1
            mct = p.minimumHeight()
        if p:=pns[TTkAppTemplate.BOTTOM]:
            pcb=1
            if p.border:
                G=pf
                E=1
            mcb = p.minimumHeight()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).minimumHeight()
        if p.border:
            D=pct
            E=pcb

        return mh+mf+max( mcr+A+F ,mcl+C+H, mcm+mct+mcb+B+D+E+G )

    def maximumHeight(self):
        # ┌─────────────────────────────────┐
        # │         Header                  │
        # ├── A ────┬──── B ───────┬── C ───┤
        # │         │   Top        │        │
        # │         ├──── D ───────┤        │
        # │         │              │        │
        # │  Right  │   Main       │  Left  │
        # │         │   Center     │        │
        # │         │              │        │
        # │         ├──── E ───────┤        │
        # │         │   Bottom     │        │
        # ├── F ────┴──── G ───────┴── H ───┤
        # │         Footer                  │
        # └─────────────────────────────────┘
        pns = self._panels
        A=B=C=D=E=F=G=0 # 0 or 1 if the border is defined

        # Header and Footer border and minHeight
        mh=mf=0
        ph=pf=0

        # Header Footer
        if p:=pns[TTkAppTemplate.HEADER]:
            ph=1
            if p.border: A=B=C=1
            mh = p.maximumHeight()
        if p:=pns[TTkAppTemplate.FOOTER]:
            pf=1
            if p.border: F=G=H=1
            mf = p.maximumHeight()

        # Center Left,Right:
        mcr=mcl=0x10000
        if p:=pns[TTkAppTemplate.LEFT]:
            if p.border:
                C = ph
                H = pf
            mcl = p.maximumHeight()
        if p:=pns[TTkAppTemplate.RIGHT]:
            if p.border:
                A = ph
                F = pf
            mcr = p.maximumHeight()

        # Center Top,Bottom
        mct=mcb=0
        pct=pcb=0
        if p:=pns[TTkAppTemplate.TOP]:
            pct=1
            if p.border:
                B=ph
                D=1
            mct = p.maximumHeight()
        if p:=pns[TTkAppTemplate.BOTTOM]:
            pcb=1
            if p.border:
                G=pf
                E=1
            mcb = p.maximumHeight()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).maximumHeight()
        if p.border:
            D=pct
            E=pcb

        return mh+mf+min( mcr+A+F ,mcl+C+H, mcm+mct+mcb+B+D+E+G )




    def _updateGeometries(self):
        w,h = self.size()
        pns = self._panels

        # E,F Splitters
        p = pns[TTkAppTemplate.RIGHT]
        if ( not p or not p.isVisible() ):
            pass
        p = pns[TTkAppTemplate.LEFT]
        if ( not p or not p.isVisible() ):
            pass





        self.update()


    #def layout(self):
    #    return self._panels[TTkAppTemplate.MAIN].item

    #def setLayout(self, layout):
    #    self._panels[TTkAppTemplate.MAIN].item = layout