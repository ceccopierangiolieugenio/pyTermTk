# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

from random import randint

import TermTk as ttk

import ttkDesigner.app.superobj as so
from .superobj import SuperObject

class SuperWidget(ttk.TTkContainer):
    __slots__ = ('_wid', '_superRootWidget', '_designer',
                 'superMoved', 'superResized')
    def __init__(self, designer, wid, *args, **kwargs):
        self.superMoved   = ttk.pyTTkSignal(int,int)
        self.superResized = ttk.pyTTkSignal(int,int)
        self._designer = designer
        self._wid = wid
        self._wid.move(*kwargs['pos'])
        self._wid._canvas.show()
        self._superRootWidget = kwargs.get('superRootWidget',False)
        kwargs['maxSize'] = wid.maximumSize()
        kwargs['minSize'] = wid.minimumSize()
        kwargs['size']    = wid.size()
        super().__init__(*args, **kwargs)
        #self.resize(*self._wid.size())
        h,s,l = randint(0,359),100,randint(60,80)
        r,g,b = ttk.TTkColor.hsl2rgb(((h+5)%360,s,l))
        self._layoutColor    = ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}", modifier=ttk.TTkColorGradient(increment=+2))
        r,g,b = ttk.TTkColor.hsl2rgb(((h+5)%360,s,l))
        self._layoutPadColor = ttk.TTkColor.bg(f"#{r:02X}{g:02X}{b:02X}", modifier=ttk.TTkColorGradient(increment=-2))
        self.setFocusPolicy(ttk.TTkK.ClickFocus)
        SuperWidget.toggleHighlightLayout.connect(self._toggleHighlightLayout)

    _showLayout = False
    toggleHighlightLayout = ttk.pyTTkSignal(bool)

    # TODO: Find a better way to handle this exception
    # It may require some major rewrite
    def hasControlWidget(self):
        return True

    @ttk.pyTTkSlot(str)
    def setSuperName(self, name):
        if name and name not in [w.name() for w in self._designer.getWidgets()]:
            oldName = self._wid._name
            self._wid.setName(name)
            self._designer.widgetNameChanged.emit(oldName, name)
            self._designer.weModified.emit()

    def getSuperProperties(self):
        additions = {}
        exceptions = {
            'Name': {
                'get':  { 'cb':ttk.TTkWidget.name,               'type':str} ,
                'set':  { 'cb':lambda _,n: self.setSuperName(n), 'type':str} },
        }
        exclude = []
        return additions, exceptions, exclude

    @ttk.pyTTkSlot(bool)
    def _toggleHighlightLayout(self, state):
        SuperWidget._showLayout = state
        self.update()

    def dumpDict(self):
        wid = self._wid
        ret = {
            'class'  : wid.__class__.__name__,
            'params' : SuperObject.dumpParams(wid),
        }
        return ret

    @staticmethod
    def _swFromWidget(wid, swClass, *args, **kwargs):
        sw = swClass(wid=wid, *args, **kwargs)
        return sw

    @staticmethod
    def swFromWidget(wid:object, *args, **kwargs):
        swClass = so.SuperWidget
        for c, sc in {
            # ttk.TTkTextEdit:       so.SuperWidgetTextEdit,
            ttk.TTkRadioButton:    so.SuperWidgetRadioButton,
            # ttk.TTkResizableFrame: so.SuperWidgetFrame,
            # ttk.TTkWindow:         so.SuperWidgetFrame,
            ttk.TTkSplitter:       so.SuperWidgetSplitter,
            # ttk.TTkList:           so.SuperWidgetList,
            ttk.TTkMenuButton:     so.SuperWidgetMenuButton,
            ttk.TTkFrame:          so.SuperWidgetFrame,
            ttk.TTkAbstractScrollArea: so.SuperWidgetAbstractScrollArea,
            ttk.TTkContainer:      so.SuperWidgetContainer,
            ttk.TTkWidget:         so.SuperWidget,
                }.items():
            if c in type(wid).mro():
                swClass = sc
                break
        return swClass._swFromWidget(wid=wid, swClass=swClass, *args, **kwargs)

    @staticmethod
    def loadDict(designer, parent, widProp):
        ttkClass = getattr(ttk,widProp['class'])
        if issubclass(ttkClass,ttk.TTkLayout):
            demiProp = {
                'version':'2.0.0',
                'tui':{
                    'class'  : widProp['class'],
                    'params' : widProp['params'],
                    'children' : []
                },
                'connections':[]
            }
            layout = ttk.TTkUiLoader.loadDict(demiProp)
            x,y,w,h = layout.geometry()
            sl = sup = so.SuperLayout.slFromLayout(designer=designer, layout=layout, lay=ttk.TTkLayout(), pos=(x,y), size=(w,h), selectable=True)
            children = widProp['children']
        elif issubclass(ttkClass,ttk.TTkContainer):
            setLayout  = 'layout'  in widProp
            setMenuBar = 'menuBar' in widProp
            tui = {
                'class'  : widProp['class'],
                'params' : widProp['params'] }
            tui |= {
                'layout': {
                    'class'  : widProp['layout']['class'],
                    'params' : widProp['layout']['params'],
                    'children' : []
                    } } if setLayout else {}
            tui |= {
                'menuBar': widProp['menuBar']
                    } if setMenuBar else {}
            demiProp = {
                'version':'2.0.0',
                'tui': tui,
                'connections':[]
            }
            wid = ttk.TTkUiLoader.loadDict(demiProp)
            sup = so.SuperWidgetContainer.swFromWidget(designer=designer, wid=wid, pos=wid.pos())
            sl = sup._superLayout
            children = widProp['layout']['children'] if setLayout else []
        else:
            setMenuBar = 'menuBar' in widProp
            tui = {
                'class'  : widProp['class'],
                'params' : widProp['params'] }
            demiProp = {
                'version':'2.0.0',
                'tui': tui,
                'connections':[]
            }
            wid = ttk.TTkUiLoader.loadDict(demiProp)
            sup = so.SuperWidget.swFromWidget(designer=designer, wid=wid, pos=wid.pos())
            children = []

        for ch in children:
            sch = SuperWidget.loadDict(designer, parent, ch)
            if issubclass(type(sch),so.SuperLayout):
                schl = sch
            elif issubclass(type(sch),so.SuperWidgetContainer):
                schl = sch._superLayout
            else:
                schl = None

            if issubclass(type(sl),so.SuperLayoutGrid):
                sl.layout().addWidget(sch,ch['row'],ch['col'],ch['rowspan'],ch['colspan'])
                if schl:
                    schl.setDropBorder(1)
            else:
                sl.layout().addWidget(sch)
                if schl:
                    schl.setDropBorder(0)
        return sup

    def updateAll(self):
        self.resize(*(self._wid.size()))
        self.move(*(self._wid.pos()))
        self.setMaximumSize(*(self._wid.maximumSize()))
        self.setMinimumSize(*(self._wid.minimumSize()))
        self.update()

    def mousePressEvent(self, evt) -> bool:
        return True

    def isRootWidget(self):
        return self._superRootWidget

    def makeRootWidget(self):
        self._superRootWidget = True

    def pushSuperControlWidget(self):
        # if self._superRootWidget: return False
        scw = so.SuperControlWidget(self)
        ttk.TTkHelper.removeOverlay()
        ttk.TTkHelper.overlay(self, scw, -1,-1, forceBoundaries=False)

    def mouseReleaseEvent(self, evt) -> bool:
        w,h = self.size()
        if 0<=evt.x<w and 0<=evt.y<h:
            self.pushSuperControlWidget()
            self._designer.thingSelected.emit(self._wid,self)
        return True

    def mouseDragEvent(self, evt) -> bool:
        if self._superRootWidget: return False
        drag = ttk.TTkDrag()
        data = self
        data.paintChildCanvas()
        drag.setHotSpot(evt.x, evt.y)
        drag.setPixmap(data.getCanvas())
        drag.setData(data)
        drag.exec()
        self.parentWidget().removeSuperWidget(self)
        return True

    def superChild(self):
        return self._wid

    def move(self, x: int, y: int):
        self._wid.move(x,y)
        self.update()
        self.superMoved.emit(x,y)
        return super().move(x, y)

    def resizeEvent(self, w, h):
        self._wid.resize(w,h)
        self._wid._canvas.updateSize()
        self.superResized.emit(w,h)
        return super().resizeEvent(w, h)

    def paintEvent(self, canvas):
        w,h = self.size()
        if SuperWidget._showLayout:
            for y in range(h):
                canvas.drawText(pos=(0,y),text='',width=w,color=self._layoutColor)
            for y in range(0,h):
                canvas.drawText(pos=(0,y),text='',width=w,color=self._layoutPadColor)
            # canvas.fill(color=self._layoutColor)
            # canvas.fill(pos=(l,t), size=(w-r-l,h-b-t), color=self._layoutPadColor)
        else:
            self._wid.getCanvas().updateSize()
            self._wid.paintEvent(self._wid.getCanvas())
            canvas.paintCanvas(
                    self._wid.getCanvas(),
                    (    0,     0, w, h), # geometry
                    (    0,     0, w, h), # slice
                    (    0,     0, w, h)) # bound