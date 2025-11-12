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

from __future__ import annotations

__all__ = ['TTkAppTemplate']

from enum import IntEnum
from dataclasses import dataclass

from typing import Optional,List,Dict,Literal,Tuple

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.canvas import TTkCanvas
from TermTk.TTkCore.string import TTkString, TTkStringType
from TermTk.TTkCore.TTkTerm.inputmouse import TTkMouseEvent
from TermTk.TTkLayouts import TTkLayout, TTkGridLayout
from TermTk.TTkWidgets.container import TTkWidget, TTkContainer
from TermTk.TTkWidgets.menubar import TTkMenuBarLayout

class TTkAppTemplate(TTkContainer):
    ''' TTkAppTemplate:

    A flexible application template layout with multiple resizable panels.

    ::

        App Template Layout
        ┌─────────────────────────────────┐
        │         Header                  │
        ├─────────┬──────────────┬────────┤ H
        │         │   Top        │        │
        │         ├──────────────┤        │ T
        │         │              │        │
        │  Right  │   Main       │  Left  │
        │         │   Center     │        │
        │         │              │        │
        │         ├──────────────┤        │ B
        │         │   Bottom     │        │
        ├─────────┴──────────────┴────────┤ F
        │         Footer                  │
        └─────────────────────────────────┘
                  R              L

    Demo: `apptemplate.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/apptemplate.py>`_
    `online <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=showcase/apptemplate.py>`_
    '''

    class Position(IntEnum):
        ''' This Class enumerate the different panels available in the layout of :py:class:`TTkAppTemplate`

        .. autosummary::
          MAIN
          TOP
          BOTTOM
          LEFT
          RIGHT
          CENTER
          HEADER
          FOOTER
        '''
        MAIN   = TTkK.CENTER
        '''Main'''
        TOP    = TTkK.TOP
        '''Top'''
        BOTTOM = TTkK.BOTTOM
        '''Bottom'''
        LEFT   = TTkK.LEFT
        '''Left'''
        RIGHT  = TTkK.RIGHT
        '''Right'''
        CENTER = TTkK.CENTER
        '''Center'''
        HEADER = TTkK.HEADER
        '''Header'''
        FOOTER = TTkK.FOOTER
        '''Footer'''

    MAIN   =  Position.MAIN
    ''':py:class:`Position.MAIN`'''
    TOP    =  Position.TOP
    ''':py:class:`Position.TOP`'''
    BOTTOM =  Position.BOTTOM
    ''':py:class:`Position.BOTTOM`'''
    LEFT   =  Position.LEFT
    ''':py:class:`Position.LEFT`'''
    RIGHT  =  Position.RIGHT
    ''':py:class:`Position.RIGHT`'''
    CENTER =  Position.CENTER
    ''':py:class:`Position.CENTER`'''
    HEADER =  Position.HEADER
    ''':py:class:`Position.HEADER`'''
    FOOTER =  Position.FOOTER
    ''':py:class:`Position.FOOTER`'''

    @dataclass(frozen=False)
    class _Panel:
        # It's either item or widget
        item:    Optional[TTkLayout] = None
        widget:  Optional[TTkWidget] = None
        title:   Optional[TTkString] = None
        menubar: Optional[TTkMenuBarLayout] = None
        size:    int  = 0
        border:  bool = True
        fixed:   bool = False

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

    @dataclass
    class _Splitter():
        pos:Tuple[int,int]
        size:int
        fixed:bool
        panel:TTkAppTemplate._Panel

    @dataclass
    class _MenuBarLine():
        pos:Tuple[int,int]
        text:str

    __slots__ = ('_panels', '_splitters', '_menubarLines', '_selected'
                 #Signals
                 )
    _selected:List[Position]
    _panels:Dict[Position,Optional[_Panel]]
    _splitters:Dict[Position,Optional[_Splitter]]
    _menubarLines:Dict[Position,Optional[_MenuBarLine]]
    def __init__(self,
                 border=False,
                 **kwargs) -> None:
        mp = TTkAppTemplate._Panel(item=TTkLayout(), border=border)
        self._panels = {
            TTkAppTemplate.MAIN   : mp ,
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
        self._menubarLines = {
            TTkAppTemplate.MAIN   : None ,
            TTkAppTemplate.TOP    : None ,
            TTkAppTemplate.BOTTOM : None ,
            TTkAppTemplate.LEFT   : None ,
            TTkAppTemplate.RIGHT  : None ,
            TTkAppTemplate.HEADER : None ,
            TTkAppTemplate.FOOTER : None }
        self._selected = []

        super().__init__( **kwargs)
        self.layout().addItem(mp.item)
        self._updateGeometries(force=True)
        self.setFocusPolicy(TTkK.ClickFocus)

    def setWidget(self,
                  widget:TTkWidget, position:Position=Position.MAIN,
                  size:Optional[int]=None, title:TTkStringType="",
                  border:Optional[bool]=None, fixed:Optional[bool]=None) -> None:
        '''
        Place the :py:class:`TTkWidget` in the :py:class:`TTkAppTemplate`'s panel identified by its :py:class:`Position`

        :param widget: The widget to place in the panel
        :type widget: :py:class:`TTkWidget`
        :param position: The panel position, defaults to :py:class:`Position.MAIN`
        :type position: :py:class:`Position`, optional
        :param size: The panel size in characters (width for LEFT/RIGHT, height for TOP/BOTTOM/HEADER/FOOTER), defaults to widget's minimum size
        :type size: int, optional
        :param title: The panel title displayed in the border, defaults to ""
        :type title: :py:class:`TTkString`, optional
        :param border: Whether to draw a border around the panel, defaults to True
        :type border: bool, optional
        :param fixed: Whether the panel size is fixed (non-resizable), defaults to False
        :type fixed: bool, optional
        '''
        if not (p:=self._panels[position]):
            p = self._panels[position] = TTkAppTemplate._Panel()
        if wid:=p.widget:
            self.layout().removeWidget(wid)
            p.widget = None
        if it:=p.item:
            self.layout().removeItem(it)
            p.item = None
        if widget:
            p.widget = widget
            self.layout().addWidget(widget)
            if border is not None:
                p.border = border
            if fixed is not None:
               p.fixed = fixed
            p.title = title if isinstance(title,TTkString) else TTkString(title)
            p.size = (
                size if size is not None else
                widget.minimumWidth() if position in (TTkAppTemplate.LEFT,TTkAppTemplate.RIGHT) else
                widget.minimumHeight() )
        self._updateGeometries(force=True)

    def setItem(self,
                item:TTkLayout, position:Position=Position.MAIN,
                size:Optional[int]=None, title:TTkStringType="",
                border:Optional[bool]=None, fixed:Optional[bool]=None) -> None:
        ''' Place the :py:class:`TTkLayout` in the :py:class:`TTkAppTemplate`'s panel identified by its :py:class:`Position`

        :param item: The layout to place in the panel
        :type item: :py:class:`TTkLayout`
        :param position: The panel position, defaults to :py:class:`Position.MAIN`
        :type position: :py:class:`Position`, optional
        :param size: The panel size in characters (width for LEFT/RIGHT, height for TOP/BOTTOM/HEADER/FOOTER), defaults to layout's minimum size
        :type size: int, optional
        :param title: The panel title displayed in the border, defaults to ""
        :type title: :py:class:`TTkString`, optional
        :param border: Whether to draw a border around the panel, defaults to True
        :type border: bool, optional
        :param fixed: Whether the panel size is fixed (non-resizable), defaults to False
        :type fixed: bool, optional
        '''
        if not (p:=self._panels[position]):
            p = self._panels[position] = TTkAppTemplate._Panel()
        if wid:=p.widget:
            self.layout().removeWidget(wid)
            p.widget = None
        if it:=p.item:
            self.layout().removeItem(it)
            p.item = None
        if item:
            p.item = item
            self.layout().addItem(item)
            if border!=None:
                p.border = border
            if fixed is not None:
               p.fixed = fixed
            p.title = title if isinstance(title,TTkString) else TTkString(title)
            p.size = (
                size if size is not None else
                item.minimumWidth() if position in (TTkAppTemplate.LEFT,TTkAppTemplate.RIGHT) else
                item.minimumHeight() )
        self._updateGeometries(force=True)

    def setTitle(self, position:Position=Position.MAIN, title:TTkStringType="") -> None:
        ''' Set the title of the panel identified by the position

        :param position: The panel position, defaults to :py:class:`Position.MAIN`
        :type position: :py:class:`Position`, optional
        :param title: The title text to display, defaults to ""
        :type title: :py:class:`TTkString`, optional
        '''
        if not (p:=self._panels[position]):
            return
        p.title =  title if isinstance(title,TTkString) else TTkString(title)
        self._updateGeometries(force=True)

    def menuBar(self, position:Position=MAIN) -> Optional[TTkMenuBarLayout]:
        ''' Retrieve the :py:class:`TTkMenuBarLayout` in the panel identified by the position

        :param position: The panel position, defaults to :py:class:`Position.MAIN`
        :type position: :py:class:`Position`, optional

        :return: The menu bar layout or None if not set
        :rtype: :py:class:`TTkMenuBarLayout` or None
        '''
        return None if not (p:=self._panels[position]) else p.menubar

    def setMenuBar(self, menuBar:TTkMenuBarLayout, position:Position=MAIN) -> None:
        ''' Set the :py:class:`TTkMenuBarLayout` for the panel identified by the position

        :param menuBar: The menu bar layout to set
        :type menuBar: :py:class:`TTkMenuBarLayout`
        :param position: The panel position, defaults to :py:class:`Position.MAIN`
        :type position: :py:class:`Position`, optional
        '''
        if not (p:=self._panels[position]):
            p = self._panels[position] = TTkAppTemplate._Panel()
        if p.menubar:
            self.rootLayout().removeItem(p.menubar)
            # TODO: Dispose the menubar
        p.menubar = menuBar
        if menuBar:
            self.rootLayout().addItem(p.menubar)
        self._updateGeometries(force=True)

    def setBorder(self, border=True, position=MAIN) -> None:
        ''' Set whether to draw a border around the panel

        :param border: True to show border, False to hide, defaults to True
        :type border: bool, optional
        :param position: The panel position, defaults to :py:class:`Position.MAIN`
        :type position: :py:class:`Position`, optional
        '''
        if not (p:=self._panels[position]):
            p = self._panels[position] = TTkAppTemplate._Panel()
        p.border = border
        self._updateGeometries(force=True)

    def setFixed(self, fixed=False, position=MAIN) -> None:
        ''' Set whether the panel size is fixed (non-resizable)

        :param fixed: True for fixed size, False for resizable, defaults to False
        :type fixed: bool, optional
        :param position: The panel position, defaults to :py:class:`Position.MAIN`
        :type position: :py:class:`Position`, optional
        '''
        if not (p:=self._panels[position]):
            p = self._panels[position] = TTkAppTemplate._Panel()
        p.fixed = fixed
        self._updateGeometries(force=True)

    def resizeEvent(self, width: int, height: int) -> None:
        self._updateGeometries()

    def focusOutEvent(self) -> None:
        self._selected = []
        self.update()

    def mouseReleaseEvent(self, evt:TTkMouseEvent) -> bool:
        self._selected = []
        self.update()
        return True

    def mousePressEvent(self, evt:TTkMouseEvent) -> bool:
        self._selected = []
        self._updateGeometries()
        spl = self._splitters
        pns = self._panels
        for loc in (TTkAppTemplate.TOP, TTkAppTemplate.BOTTOM, TTkAppTemplate.HEADER, TTkAppTemplate.FOOTER):
            if (s:=spl[loc]) and (pn:=pns[loc]) and not pn.fixed and (p:=s.pos)[1]==evt.y and p[0] <= evt.x <=p[0]+s.size:
                self._selected.append(loc)
        for loc in (TTkAppTemplate.LEFT, TTkAppTemplate.RIGHT):
            if (s:=spl[loc]) and (pn:=pns[loc]) and not pn.fixed and (p:=s.pos)[0]==evt.x and p[1] <= evt.y <=p[1]+s.size:
                self._selected.append(loc)
        return True

    def mouseDragEvent(self, evt:TTkMouseEvent) -> bool:
        if not self._selected: return False
        pns = self._panels
        for loc in self._selected:
            if not (p:=pns[loc]):
                raise ValueError()
            x,y,w,h = p.geometry()
            if   loc == TTkAppTemplate.LEFT:
                p.size = evt.x-x
            elif loc == TTkAppTemplate.RIGHT:
                p.size = w+x-evt.x
            elif loc in (TTkAppTemplate.HEADER, TTkAppTemplate.TOP):
                p.size = evt.y-y
            else:
                p.size = h+y-evt.y-1
        self._updateGeometries()
        return True

    def minimumWidth(self) -> int:
        ''' Get the minimum width required for the template

        :return: The minimum width in characters
        :rtype: int
        '''
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

        if not (p:=pns[TTkAppTemplate.MAIN]):
            raise ValueError()
        mcm = p.minimumWidth()

        return max(mh, mf, mcr+mcl+max(mct, mcb, mcm)) + (2 if p.border else 0)

    def maximumWidth(self) -> int:
        ''' Get the maximum width allowed for the template

        :return: The maximum width in characters
        :rtype: int
        '''
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

        if not (p:=pns[TTkAppTemplate.MAIN]):
            raise ValueError()
        mcm = p.maximumWidth()
        return min(mh, mf, mcr+mcl+min(mct, mcb, mcm)) + (2 if p.border else 0)

    def minimumHeight(self) -> int:
        ''' Get the minimum height required for the template

        :return: The minimum height in characters
        :rtype: int
        '''
        pns = self._panels

        # Retrieve all the panels parameters and hide the menubar if required
        def _processPanel(_loc):
            _p = pns[_loc]
            if not (_p and _p.isVisible()):
                return None, 0, False, False
            return _p, _p.minimumHeight(), _p.border, _p.menubar

        ph,mh,bh,menh = _processPanel(TTkAppTemplate.HEADER)
        pl,ml,bl,menl = _processPanel(TTkAppTemplate.LEFT)
        pr,mr,br,menr = _processPanel(TTkAppTemplate.RIGHT)
        pt,mt,bt,ment = _processPanel(TTkAppTemplate.TOP)
        pm,mm,bm,menm = _processPanel(TTkAppTemplate.MAIN)
        pb,mb,bb,menb = _processPanel(TTkAppTemplate.BOTTOM)
        pf,mf,bf,menf = _processPanel(TTkAppTemplate.FOOTER)

        # Adjust the sizes based on the menubar and the borders
        if menh and not (bm): mh += 1
        if menl and not (bh or (bm and ph==None)): ml += 1
        if menr and not (bh or (bm and ph==None)): mr += 1
        if ment and not (bh or (bm and ph==None)): mt += 1
        if menm and not (bt or (bh and pt==None) or (bm and pt==ph==None)): mm += 1
        if menb and not (bb): mb += 1
        if menf and not (bf): mf += 1

        return mh+mf+max(mr ,ml, mm+mt+mb ) + ( 2 if bm else 0 )

    def maximumHeight(self) -> int:
        ''' Get the maximum height allowed for the template

        :return: The maximum height in characters
        :rtype: int
        '''
        pns = self._panels

        # Retrieve all the panels parameters and hide the menubar if required
        def _processPanel(_loc):
            _p = pns[_loc]
            if not (_p and _p.isVisible()):
                return None, 0, False, False
            return _p, _p.maximumHeight(), _p.border, _p.menubar

        ph,mh,bh,menh = _processPanel(TTkAppTemplate.HEADER)
        pl,ml,bl,menl = _processPanel(TTkAppTemplate.LEFT)
        pr,mr,br,menr = _processPanel(TTkAppTemplate.RIGHT)
        pt,mt,bt,ment = _processPanel(TTkAppTemplate.TOP)
        pm,mm,bm,menm = _processPanel(TTkAppTemplate.MAIN)
        pb,mb,bb,menb = _processPanel(TTkAppTemplate.BOTTOM)
        pf,mf,bf,menf = _processPanel(TTkAppTemplate.FOOTER)

        # Adjust the sizes based on the menubar and the borders
        if menh and not (bm): mh += 1
        if menl and not (bh or (bm and ph==None)): ml += 1
        if menr and not (bh or (bm and ph==None)): mr += 1
        if ment and not (bh or (bm and ph==None)): mt += 1
        if menm and not (bt or (bh and pt==None) or (bm and pt==ph==None)): mm += 1
        if menb and not (bb): mb += 1
        if menf and not (bf): mf += 1

        # Those panels cannot have null size
        if not mm: mm=0x10000
        if not ml: ml=0x10000
        if not mr: mr=0x10000

        return mh+mf+min(mr ,ml, mm+mt+mb ) + ( 2 if bm else 0 )

    def _updateGeometries(self, force:bool=False) -> None:
        w,h = self.size()
        if w<=0 or h<=0 or (not force and not self.isVisibleAndParent()): return
        pns = self._panels
        spl = self._splitters
        mbl = self._menubarLines

        # Retrieve all the panels parameters and hide the menubar if required
        def _processPanel(_loc):
            _p = pns[_loc]
            if not (_p and _p.isVisible()):
                if _p and (_menu:=_p.menubar):
                    _menu.setGeometry(-1,-1,0,0)
                return None, 0, 0x1000, 0, True, 0, None
            _min    = _p.minimumHeight()
            _max    = _p.maximumHeight()
            _size   = min(max(_p.size,_min),_max)
            _fixed  = _p.fixed
            _border = 1 if _p.border else 0
            return _p, _min, _max, _size, _fixed, _border, _p.menubar

        pt,ptmin,ptmax,st,ft,bt,mt = _processPanel(TTkAppTemplate.TOP)
        pb,pbmin,pbmax,sb,fb,bb,mb = _processPanel(TTkAppTemplate.BOTTOM)
        ph,phmin,phmax,sh,fh,bh,mh = _processPanel(TTkAppTemplate.HEADER)
        pf,pfmin,pfmax,sf,ff,bf,mf = _processPanel(TTkAppTemplate.FOOTER)
        pl,plmin,plmax,sl,fl,bl,ml = _processPanel(TTkAppTemplate.LEFT)
        pr,prmin,prmax,sr,fr,br,mr = _processPanel(TTkAppTemplate.RIGHT)

        # Main Boundaries
        if not (pm:=pns[TTkAppTemplate.MAIN]):
            raise ValueError()
        mm=pm.menubar
        mmaxw = pm.maximumWidth()
        mminw = pm.minimumWidth()
        mmaxh = pm.maximumHeight()
        mminh = pm.minimumHeight()
        bm = 1 if pm.border else 0
        w-=(bm<<1)+bl+br
        h-=(bm<<1)+bt+bb+bh+bf

        adjm =adjt =adjb =adjh =adjf =adjl =adjr =0 # Adjustment if we need extra space for the menubar
        adjtf=adjbf=adjhf=adjff=adjlf=adjrf=adjmf=0 # 1 if the menu is on a single line bar
        # Retune the max/min sizes and adjustment based on the menubar,border and visible widgets
        #                                                           Check if there is a splitter to be used for the menubar
        #                               Fix bar status if the menu is on the closest splitter
        if pt and mt: (adjt,adjtf) = ( 0, fh if _phbh else True ) if (_phbh:=(ph and bh)) or (not ph and bm) else (1,True) ; st+=adjt ; ptmin+=adjt ; ptmax+=adjt
        if pb and mb: (adjb,adjbf) = ( 0, fb                    ) if  bb                                     else (1,True) ; sb+=adjb ; pbmin+=adjb ; pbmax+=adjb
        if ph and mh: (adjh,adjhf) = ( 0,  0                    ) if  bm                                     else (1,True) ; sh+=adjh ; phmin+=adjh ; phmax+=adjh
        if pf and mf: (adjf,adjff) = ( 0, ff                    ) if  bf                                     else (1,True) ; sf+=adjf ; pfmin+=adjf ; pfmax+=adjf
        if pl and ml: (adjl,adjlf) = ( 0, fh if _phbh else True ) if (_phbh:=(ph and bh)) or (not ph and bm) else (1,True)            ; plmin+=adjl ; plmax+=adjl
        if pr and mr: (adjr,adjrf) = ( 0, fh if _phbh else True ) if (_phbh:=(ph and bh)) or (not ph and bm) else (1,True)            ; prmin+=adjr ; prmax+=adjr
        if        mm: (adjm,adjmf) = ( 0, ft if (pt and bt) else fh if _phbh else True) if (_phbh:=(ph and bh)) or (not pt and ph and bh) or (not pt and not ph and bm) else (1,True) ; mminh+=adjm ; mmaxh+=adjm

        # check horizontal sizes
        if not (mminw <= (newszw:=(w-sl-sr)) <= mmaxw):
            # the main width does not fit
            # we need to move the (R,L) splitters
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

        # Resize any panel to the proper dimension
        w+=bl+br
        h+=bt+bb+bh+bf
        def _setGeometries(
                _loc:TTkAppTemplate.Position,
                _p:TTkAppTemplate._Panel,
                _x:int,_y:int,_w:int,_h:int,
                _mb:Optional[TTkMenuBarLayout],
                _adj:int,
                _fix:int) -> None:
            if _mb:
                if _fix: # Fixed
                    styleToMerge = {'default':{'glyphs':('├','─','┤','┄','┄','▶')}}
                else:
                    styleToMerge = {'default':{'glyphs':('╞','═','╡','┄','┄','▶')}}
                if not _adj:
                    mbl[_loc] = None
                else:
                    mbl[_loc] = TTkAppTemplate._MenuBarLine(pos=(_x,_y), text=f"┄{'─'*(_w-2)}┄")
                for m in _mb._menus(TTkK.LEFT_ALIGN):   m.mergeStyle(styleToMerge)
                for m in _mb._menus(TTkK.RIGHT_ALIGN):  m.mergeStyle(styleToMerge)
                for m in _mb._menus(TTkK.CENTER_ALIGN): m.mergeStyle(styleToMerge)
                _moff = 0 if _adj else -1
                _mb.setGeometry(_x+1,_y+_moff,_w-2,1)
            _p.setGeometry(_x,_y+_adj,_w,_h-_adj)

        #                                                 x                    y                                w        h              _mb _adj   _fix
        _setGeometries(       TTkAppTemplate.MAIN   , pm, bm+sl+bl           , bm+sh+bh+st+bt                 , newszw , newszh        , mm, adjm, adjmf)
        if pl: _setGeometries(TTkAppTemplate.LEFT   , pl, bm                 , bm+sh+bh                       , sl     , h-sh-bh-sf-bf , ml, adjl, adjlf)
        if pr: _setGeometries(TTkAppTemplate.RIGHT  , pr, bm+sl+bl+newszw+br , bm+sh+bh                       , sr     , h-sh-bh-sf-bf , mr, adjr, adjrf)
        if ph: _setGeometries(TTkAppTemplate.HEADER , ph, bm                 , bm                             , w      , sh            , mh, adjh, adjhf)
        if pt: _setGeometries(TTkAppTemplate.TOP    , pt, bm+sl+bl           , bm+sh+bh                       , newszw , st            , mt, adjt, adjtf)
        if pb: _setGeometries(TTkAppTemplate.BOTTOM , pb, bm+sl+bl           , bm+sh+bh+st+bt+newszh+bb       , newszw , sb            , mb, adjb, adjbf)
        if pf: _setGeometries(TTkAppTemplate.FOOTER , pf, bm                 , bm+sh+bh+st+bt+newszh+bb+sb+bf , w      , sf            , mf, adjf, adjff)

        # Define Splitter geometries
        w,h = self.size()
        spl[TTkAppTemplate.HEADER] = None if not bh else TTkAppTemplate._Splitter( pos=(0   , bm+sh                      ) ,size=w     , fixed=fh , panel=ph )
        spl[TTkAppTemplate.FOOTER] = None if not bf else TTkAppTemplate._Splitter( pos=(0   , bm+sh+bh+st+bt+newszh+bb+sb) ,size=w     , fixed=ff , panel=pf )

        ca = sh                          + (bm if ph else 0 )
        cb = bm+sh+bh+st+bt+newszh+bb+sb + (bf if pf else bm)
        spl[TTkAppTemplate.LEFT]   = None if not bl else TTkAppTemplate._Splitter( pos=(bm+sl           , ca             ) ,size=cb-ca , fixed=fl , panel=pl )
        spl[TTkAppTemplate.RIGHT]  = None if not br else TTkAppTemplate._Splitter( pos=(bm+sl+bl+newszw , ca             ) ,size=cb-ca , fixed=fr , panel=pr )

        ca = sl              + (bm if pl else 0 )
        cb = bm+sl+bl+newszw + (br if pr else bm)
        spl[TTkAppTemplate.TOP]    = None if not bt else TTkAppTemplate._Splitter( pos=(ca        , bm+sh+bh+st          ) ,size=cb-ca , fixed=ft , panel=pt )
        spl[TTkAppTemplate.BOTTOM] = None if not bb else TTkAppTemplate._Splitter( pos=(ca        , bm+sh+bh+st+bt+newszh) ,size=cb-ca , fixed=fb , panel=pb )

        self.update()

    def update(self, repaint: bool =True, updateLayout: bool =False, updateParent: bool =False) -> None:
        if updateLayout:
            self._updateGeometries()
        super().update(repaint=repaint,updateLayout=updateLayout,updateParent=updateParent)

    #def layout(self):
    #    return self._panels[TTkAppTemplate.MAIN].item

    #def setLayout(self, layout):
    #    self._panels[TTkAppTemplate.MAIN].item = layout

    def paintEvent(self, canvas:TTkCanvas) -> None:
        w,h = self.size()
        pns = self._panels
        spl = self._splitters
        mbl = self._menubarLines

        b = False
        if (_am:=pns[TTkAppTemplate.MAIN]) is not None and (b:=_am.border):
            canvas.drawBox(pos=(0,0), size=(w,h))

        selectColor = TTkColor.fg('#88FF00')

        # hline = ('╞','═','╡')
        # vline = ('╥','║','╨')

        def drawVLine(sp:TTkAppTemplate._Splitter, color:TTkColor=TTkColor.RST) -> None:
            _x,_y = sp.pos
            _w,_h = 1,sp.size
            chs = ('│','┬','┴','╿','╽') if sp.fixed else ('║','╥','╨','┇','┇')
            canvas.fill(pos=(_x,_y), size=(_w,_h), color=color, char=chs[0] )
            canvas.drawChar(pos=(_x,_y),           color=color, char=chs[1]if b and _y==0    else chs[3])
            canvas.drawChar(pos=(_x,_y+_h-1),      color=color, char=chs[2]if b and _y+_h==h else chs[4])
        def drawHLine(sp:TTkAppTemplate._Splitter, color:TTkColor=TTkColor.RST) -> None:
            _x,_y = sp.pos
            _w,_h = sp.size,1
            chs = ('─','├','┤','╾','╼') if sp.fixed else ('═','╞','╡','╍','╍')
            canvas.fill(pos=(_x,_y), size=(_w,_h), color=color, char=chs[0] )
            canvas.drawChar(pos=(_x,_y),           color=color, char=chs[1]if b and _x==0    else chs[3])
            canvas.drawChar(pos=(_x+_w-1,_y),      color=color, char=chs[2]if b and _x+_w==w else chs[4])
            if _title:=sp.panel.title:
                _l = min(w-2,_title.termWidth())
                _tx = (_w-_l)//2
                canvas.drawChar(pos=(_x+_tx,_y),     color=color, char=chs[2])
                canvas.drawChar(pos=(_x+_tx+_l+1,_y),color=color, char=chs[1])
                canvas.drawTTkString(pos=(_x+_tx+1,_y),text=_title,width=_l)

        # Draw the 4 splittters
        if (sp:=spl[TTkAppTemplate.HEADER]) : drawHLine(sp, color=selectColor if TTkAppTemplate.HEADER in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.FOOTER]) : drawHLine(sp, color=selectColor if TTkAppTemplate.FOOTER in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.LEFT])   : drawVLine(sp, color=selectColor if TTkAppTemplate.LEFT   in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.RIGHT])  : drawVLine(sp, color=selectColor if TTkAppTemplate.RIGHT  in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.TOP])    : drawHLine(sp, color=selectColor if TTkAppTemplate.TOP    in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.BOTTOM]) : drawHLine(sp, color=selectColor if TTkAppTemplate.BOTTOM in self._selected else TTkColor.RST)

        # Draw the 12 intersect
        def drawIntersect(sph:Optional[TTkAppTemplate._Splitter],spv:Optional[TTkAppTemplate._Splitter],chs:Tuple[str,str,str,str]) -> None:
            if sph and spv:
                x = spv.pos[0]
                y = sph.pos[1]
                ch = chs[( 0 if sph.fixed else 0x01 ) | ( 0 if spv.fixed else 0x02 )]
                canvas.drawChar(pos=(x,y), char=ch)

        drawIntersect(spl[TTkAppTemplate.HEADER], spl[TTkAppTemplate.LEFT] , ('┬','╤','╥','╦'))
        drawIntersect(spl[TTkAppTemplate.HEADER], spl[TTkAppTemplate.RIGHT], ('┬','╤','╥','╦'))
        drawIntersect(spl[TTkAppTemplate.FOOTER], spl[TTkAppTemplate.LEFT] , ('┴','╧','╨','╩'))
        drawIntersect(spl[TTkAppTemplate.FOOTER], spl[TTkAppTemplate.RIGHT], ('┴','╧','╨','╩'))
        drawIntersect(spl[TTkAppTemplate.TOP   ], spl[TTkAppTemplate.LEFT] , ('├','╞','╟','╠'))
        drawIntersect(spl[TTkAppTemplate.TOP   ], spl[TTkAppTemplate.RIGHT], ('┤','╡','╢','╣'))
        drawIntersect(spl[TTkAppTemplate.BOTTOM], spl[TTkAppTemplate.LEFT] , ('├','╞','╟','╠'))
        drawIntersect(spl[TTkAppTemplate.BOTTOM], spl[TTkAppTemplate.RIGHT], ('┤','╡','╢','╣'))

        # Draw extra MenuBar Lines if there is no border to place them
        for l in mbl:
            if mb:=mbl[l]:
                canvas.drawText(pos=mb.pos,text=mb.text)

        return super().paintEvent(canvas)