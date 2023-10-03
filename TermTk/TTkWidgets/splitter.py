# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkSplitter']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkLayouts.layout import TTkLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.container import TTkContainer

class TTkSplitter(TTkContainer):
    '''TTkSplitter'''

    classStyle = {
                'default':     {'color': TTkColor.fg("#dddddd")+TTkColor.bg("#222222"),
                                'borderColor': TTkColor.RST},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'borderColor':TTkColor.fg('#888888')},
                'focus':       {'color': TTkColor.fg("#ffddff")+TTkColor.bg("#222222"),
                                'borderColor': TTkColor.fg("#ffffaa")}
            }

    __slots__ = (
        '_orientation', '_separators', '_refSizes',
        '_items', '_titles', '_separatorSelected',
        '_border')
    def __init__(self, *args, **kwargs):
        self._items = []
        self._titles = []
        self._separators = []
        self._refSizes = []
        self._border = False
        self._separatorSelected = None
        self._orientation = TTkK.HORIZONTAL
        super().__init__(*args, **kwargs)
        self._orientation = kwargs.get('orientation', TTkK.HORIZONTAL)
        self.setBorder(kwargs.get('border' , False))
        self.setFocusPolicy(TTkK.ClickFocus)

        class _SplitterLayout(TTkLayout):
            def insertWidget(_, index, widget):
                self.insertWidget(index, widget)
            def addWidget(_, widget):
                self.addWidget(widget)
            def inserItem(_, item):
                self.inserItem(item)
            def addItem(_, item):
                self.addItem(item)
        self.setLayout(_SplitterLayout())

    def setBorder(self, border):
        '''setBorder'''
        self._border = border
        if border: self.setPadding(1,1,1,1)
        else:      self.setPadding(0,0,0,0)
        self.update()

    def border(self):
        '''border'''
        return self._border

    def orientation(self):
        '''orientation'''
        return self._orientation

    def setOrientation(self, orientation):
        if orientation == self._orientation: return
        if orientation not in (TTkK.HORIZONTAL, TTkK.VERTICAL): return
        self._orientation = orientation
        self._updateGeometries()

    def clean(self):
        for i in reversed(self._items):
            if issubclass(type(i),TTkWidget):
                self.removeWidget(i)
            else:
                self.removeItem(i)

    def count(self):
        '''count'''
        return len(self._items)

    def indexOf(self, widget):
        '''indexOf'''
        return self._items.index(widget)

    def widget(self, index):
        '''widget'''
        return self._items[index]

    def replaceItem(self, index, item, title=None):
        '''replaceItem'''
        if index >= len(self._items):
            return self.addItem(item, title=title)
        TTkLayout.removeItem(self.layout(), self._items[index])
        TTkLayout.insertItem(self.layout(), index, item)
        self._items[index] = item
        self._titles[index] = TTkString(title) if title else None
        w,h = self.size()
        b = 2 if self._border else 0
        self._processRefSizes(w-b,h-b)
        self._updateGeometries()

    def replaceWidget(self, index, widget, title=None):
        '''replaceWidget'''
        if index >= len(self._items):
            return self.addWidget(widget, title=title)
        TTkLayout.removeWidget(self.layout(), self._items[index])
        TTkLayout.insertWidget(self.layout(), index, widget)
        self._items[index] = widget
        self._titles[index] = TTkString(title) if title else None
        w,h = self.size()
        b = 2 if self._border else 0
        self._processRefSizes(w-b,h-b)
        self._updateGeometries()

    def removeItem(self, item):
        '''removeItem'''
        index = self.indexOf(item)
        self._items.pop(index)
        self._refSizes.pop(index)
        self._separators.pop(index)
        TTkLayout.removeItem(self.layout(), item)
        w,h = self.size()
        b = 2 if self._border else 0
        self._processRefSizes(w-b,h-b)
        self._updateGeometries()

    def removeWidget(self, widget):
        '''removeWidget'''
        index = self.indexOf(widget)
        self._items.pop(index)
        self._refSizes.pop(index)
        self._separators.pop(index)
        TTkLayout.removeWidget(self.layout(), widget)
        w,h = self.size()
        b = 2 if self._border else 0
        self._processRefSizes(w-b,h-b)
        self._updateGeometries()

    def addItem(self, item, size=None, title=None):
        '''addItem'''
        self.insertItem(len(self._items), item, size=size, title=title)

    def insertItem(self, index, item, size=None, title=None):
        '''insertItem'''
        TTkLayout.insertItem(self.layout(), index, item)
        self._insertWidgetItem(index, item, size=size, title=title)

    def addWidget(self, widget, size=None, title=None):
        '''addWidget'''
        self.insertWidget(len(self._items), widget, size=size, title=title)

    def insertWidget(self, index, widget, size=None, title=None):
        '''insertWidget'''
        TTkLayout.insertWidget(self.layout(), index, widget)
        self._insertWidgetItem(index, widget, size=size, title=title)

    def _insertWidgetItem(self, index, widgetItem, size=None, title=None):
        self._items.insert(index, widgetItem)
        self._titles.insert(index, TTkString(title) if title else None)

        # assign the same slice to all the widgets
        self._refSizes.insert(index, size)
        w,h = self.size()
        b = 2 if self._border else 0
        self._processRefSizes(w-b,h-b)
        self._updateGeometries()
        if self.parentWidget():
            self.parentWidget().update(repaint=True, updateLayout=True)

    def setSizes(self, sizes):
        '''setSizes'''
        ls = len(self._separators)
        sizes=sizes[:ls]+[None]*max(0,ls-len(sizes))
        self._refSizes = sizes.copy()
        w,h = self.size()
        b = 2 if self._border else 0
        self._processRefSizes(w-b,h-b)
        self._updateGeometries()


    def _minMaxSizeBefore(self, index):
        if self._separatorSelected is None:
            return 0, 0x1000
        # this is because there is a hidden splitter at position -1
        minsize = -1
        maxsize = -1
        for i in range(self._separatorSelected+1):
            item = self._items[i]
            minsize += item.minDimension(self._orientation)+1
            maxsize += item.maxDimension(self._orientation)+1
        return minsize, maxsize

    def _minMaxSizeAfter(self, index):
        if self._separatorSelected is None:
            return 0, 0x1000
        minsize = 0x0
        maxsize = 0x0
        for i in range(self._separatorSelected+1, len(self._separators)):
            item = self._items[i]
            minsize += item.minDimension(self._orientation)+1
            maxsize += item.maxDimension(self._orientation)+1
        return minsize, maxsize

    def _updateGeometries(self, resized=False):
        if not self.isVisible() or not self._items: return
        w,h = self.size()
        if w==h==0: return
        sep = self._separators = self._separators[0:len(self._items)]
        if self._border:
            w-=2
            h-=2

        def _processGeometry(index, forward):
            item = self._items[index]
            pa = -1 if index==0 else sep[index-1]
            pb = sep[index]

            if self._orientation == TTkK.HORIZONTAL:
                newPos = pa+1
                size = w-newPos
            else:
                newPos = pa+1
                size = h-newPos

            if i<=len(sep)-2: # this is not the last widget
                size = pb-newPos
                maxsize = item.maxDimension(self._orientation)
                minsize = item.minDimension(self._orientation)
                if   size > maxsize: size = maxsize
                elif size < minsize: size = minsize
                if forward:
                    sep[index]=pa+size+1
                elif i>0 :
                    sep[index-1]=pa=pb-size-1

            if self._orientation == TTkK.HORIZONTAL:
                item.setGeometry(pa+1,0,size,h)
            else:
                item.setGeometry(0,pa+1,w,size)
            pass


        selected = 0
        if self._orientation == TTkK.HORIZONTAL:
            size = w
        else:
            size = h
        if self._separatorSelected is not None:
            selected = self._separatorSelected
            sepPos = sep[selected]
            minsize,maxsize = self._minMaxSizeBefore(selected)
            # TTkLog.debug(f"before:{minsize,maxsize}")
            if sepPos > maxsize: sep[selected] = maxsize
            if sepPos < minsize: sep[selected] = minsize
            minsize,maxsize = self._minMaxSizeAfter(selected)
            # TTkLog.debug(f"after:{minsize,maxsize}")
            if sepPos < size-maxsize: sep[selected] = size-maxsize
            if sepPos > size-minsize: sep[selected] = size-minsize

        if resized:
            l = len(sep)
            for i in reversed(range(l)):
                _processGeometry(i, False)
            for i in range(l):
                _processGeometry(i, True)
        else:
            for i in reversed(range(selected+1)):
                _processGeometry(i, False)
            for i in range(selected+1, len(sep)):
                _processGeometry(i, True)

        if self._separatorSelected is not None:
            s = [ b-a for a,b in zip([0]+self._separators,self._separators)]
            self._refSizes = s
        self.update()

    def _processRefSizes(self, w, h):
        self._separatorSelected = None
        if self._orientation == TTkK.HORIZONTAL:
            sizeRef = w
        else:
            sizeRef = h
        if sizeRef==0:
            self._separators = [0]*len(self._items)
            return

        # get the sum of the fixed sizes
        if None in self._refSizes:
            fixSize = sum(filter(None, self._refSizes))
            numVarSizes = len([x for x in self._refSizes if x is None])
            avalSize = sizeRef-fixSize
            varSize = avalSize//numVarSizes
            sizes = []
            for s in self._refSizes:
                if not s:
                    avalSize -= varSize
                    s = varSize + avalSize if avalSize<varSize else 0
                sizes.append(s)
            sizes = [varSize if s is None else s for s in self._refSizes]
        else:
            sizes = self._refSizes
            sizeRef = sum(sizes)
        self._separators = [sum(sizes[:i+1]) for i in range(len(sizes))]

        # Adjust separators to the new size;
        if sizeRef > 0:
            if self._orientation == TTkK.HORIZONTAL:
                diff = w/sizeRef
            else:
                diff = h/sizeRef
            self._separators = [int(i*diff) for i in self._separators]

    def resizeEvent(self, w, h):
        b = 2 if self._border else 0
        self._processRefSizes(w-b,h-b)
        self._updateGeometries(resized=True)

    def mousePressEvent(self, evt):
        self._separatorSelected = None
        x,y = evt.x, evt.y
        if self._border:
            x-=1 ; y-=1
        # TTkLog.debug(f"{self._separators} {evt}")
        for i, val in enumerate(self._separators):
            if self._orientation == TTkK.HORIZONTAL:
                if x == val:
                    self._separatorSelected = i
                    self._updateGeometries()
            else:
                if y == val:
                    self._separatorSelected = i
                    self._updateGeometries()
        return self._separatorSelected is not None

    def mouseDragEvent(self, evt):
        if self._separatorSelected is not None:
            x,y = evt.x, evt.y
            if self._border:
                x-=1 ; y-=1
            if self._orientation == TTkK.HORIZONTAL:
                self._separators[self._separatorSelected] = x
            else:
                self._separators[self._separatorSelected] = y
            self._updateGeometries()
            return True
        return False

    def focusOutEvent(self):
        self._separatorSelected = None

    def minimumHeight(self) -> int:
        ret = b = 2 if self._border else 0
        if not self._items: return ret
        if self._orientation == TTkK.VERTICAL:
            for item in self._items:
                ret+=item.minimumHeight()+1
            ret = max(0,ret-1)
        else:
            for item in self._items:
                ret = max(ret,item.minimumHeight()+b)
        return ret

    def minimumWidth(self)  -> int:
        ret = b = 2 if self._border else 0
        if not self._items: return ret
        if self._orientation == TTkK.HORIZONTAL:
            for item in self._items:
                ret+=item.minimumWidth()+1
            ret = max(0,ret-1)
        else:
            for item in self._items:
                ret = max(ret,item.minimumWidth()+b)
        return ret

    def maximumHeight(self) -> int:
        b = 2 if self._border else 0
        if not self._items: return 0x10000
        if self._orientation == TTkK.VERTICAL:
            ret = b
            for item in self._items:
                ret+=item.maximumHeight()+1
            ret = max(b,ret-1)
        else:
            ret = 0x10000
            for item in self._items:
                ret = min(ret,item.maximumHeight()+b)
        return ret

    def maximumWidth(self)  -> int:
        b = 2 if self._border else 0
        if not self._items: return 0x10000
        if self._orientation == TTkK.HORIZONTAL:
            ret = b
            for item in self._items:
                ret+=item.maximumWidth()+1
            ret = max(b,ret-1)
        else:
            ret = 0x10000
            for item in self._items:
                ret = min(ret,item.maximumWidth()+b)
        return ret

    def paintEvent(self, canvas):
        style = self.currentStyle()
        color = style['color']
        borderColor = style['borderColor']

        off = 0
        w,h = self.size()

        if self._border:
            off= 1
            canvas.drawBox(pos=(0,0),size=(w,h),color=borderColor)

        if self._orientation == TTkK.HORIZONTAL:
            for i in self._separators[:-1]:
                canvas.drawVLine(pos=(i+off,0), size=h,color=borderColor)
        else:
            for i in self._separators[:-1]:
                canvas.drawHLine(pos=(0,i+off), size=w,color=borderColor)

        if self._orientation == TTkK.HORIZONTAL and self._border:
            for i,t in enumerate(self._titles):
                if not t: continue
                a = (off + self._separators[i-1]) if i>0 else 0
                b =  off + self._separators[i]
                canvas.drawBoxTitle(
                                pos=(a,0),
                                size=(b-a+1,1),
                                text=t,
                                color=borderColor,
                                colorText=color)
        elif self._orientation == TTkK.VERTICAL:
            for i,t in enumerate(self._titles):
                if i == 0 and not self._border: continue
                if not t: continue
                a = (off + self._separators[i-1]) if i>0 else 0
                grid = 0 if i == 0 else 5
                canvas.drawBoxTitle(
                                pos=(0,a),
                                size=(w,1),
                                grid=grid,
                                text=t,
                                color=borderColor,
                                colorText=color)

