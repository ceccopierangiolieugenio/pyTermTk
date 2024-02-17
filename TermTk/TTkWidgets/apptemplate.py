
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
        mh=mf=0
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

        mcm = (p:=pns[TTkAppTemplate.MAIN]).minimumWidth()

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