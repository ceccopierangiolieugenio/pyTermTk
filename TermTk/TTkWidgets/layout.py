'''
    Layout System
'''

class TTkLayoutItem:
    __slots__ = ('_x', '_y', '_w', '_h', '_sMax', '_sMaxVal', '_sMin', '_sMinVal')
    def __init__(self):
        self._x, self._y = 0, 0
        self._w, self._h = 0, 0
        self._sMax,    self._sMin    = False, False
        self._sMaxVal, self._sMinVal = 0, 0
        pass
    def minimumSize(self):
        return self.minimumWidth(), self.minimumHeight()
    def minimumHeight(self): return 0
    def minimumWidth(self):  return 0

    def maximumSize(self):
        return self.maximumWidth(), self.maximumHeight()
    def maximumHeight(self): return 0x80000000
    def maximumWidth(self):  return 0x80000000

    def geometry(self):
        return self._x, self._y, self._w, self._h

    def setGeometry(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h


class TTkLayout(TTkLayoutItem):
    def __init__(self):
        TTkLayoutItem.__init__(self)
        self._items = []
        self._parent = None
        pass

    def children(self):
        return self._items

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if index < len(self._items):
            return self._items[index]
        return 0

    def setParent(self, parent):
        self._parent = parent

    def parentWidget(self):
        return self._parent

    def addItem(self, item):
        self._items.append(item)

    def addWidget(self, widget):
        self.addItem(TTkWidgetItem(widget))

    def removeWidget(self, widget):
        for i in self._items:
            if i.widget() == widget:
                self._items.remove(i)
                return

    def update(self):
        for i in self.children():
            if isinstance(i, TTkWidgetItem) and not i.isEmpty():
                i.widget().update()
                # TODO: Have a look at this:
                # i.getCanvas().top()
            elif isinstance(i, TTkLayout):
                i.update()

class TTkWidgetItem(TTkLayoutItem):
    def __init__(self, widget):
        TTkLayoutItem.__init__(self)
        self._widget = widget

    def widget(self):
        return self._widget

    def isEmpty(self): return self._widget is None

    def minimumSize(self):   return self._widget.minimumSize()
    def minimumHeight(self): return self._widget.minimumHeight()
    def minimumWidth(self):  return self._widget.minimumWidth()
    def maximumSize(self):   return self._widget.maximumSize()
    def maximumHeight(self): return self._widget.maximumHeight()
    def maximumWidth(self):  return self._widget.maximumWidth()

    def geometry(self):      return self._widget.geometry()

    def setGeometry(self, x, y, w, h):
        self._widget.setGeometry(x, y, w, h)



class TTkHBoxLayout(TTkLayout):
    def __init__(self):
        TTkLayout.__init__(self)

    def minimumWidth(self):
        ''' process the widgets and get the min size '''
        minw = 0
        for item in self.children():
            w1  = item.minimumWidth()
            minw += w1
        return minw

    def minimumHeight(self):
        ''' process the widgets and get the min size '''
        minh = TTkLayout.minimumHeight(self)
        for item in self.children():
            h1  = item.minimumHeight()
            if h1 > minh : minh = h1
        return minh

    def maximumWidth(self):
        ''' process the widgets and get the min size '''
        maxw = 0
        for item in self.children():
            w1 = item.maximumWidth()
            maxw += w1
        return maxw

    def maximumHeight(self):
        ''' process the widgets and get the min size '''
        maxh = TTkLayout.maximumHeight(self)
        for item in self.children():
            h1  = item.maximumHeight()
            if h1 < maxh : maxh = h1
        return maxh

    def update(self):
        x, y, w, h = self.geometry()
        numWidgets = self.count()
        leftWidgets = numWidgets
        freeWidth = w
        newx, newy = x, y
        # Loop to check the resizable space
        for item in self.children():
            item._sMax = False
            item._sMin = False
        iterate = True
        while iterate and leftWidgets > 0:
            iterate = False
            sliceSize = freeWidth//leftWidgets
            for item in self.children():
                if item._sMax or item._sMin: continue
                maxs = item.maximumWidth()
                mins = item.minimumWidth()
                if sliceSize > maxs:
                    freeWidth -= maxs
                    iterate = True
                    item._sMax = True
                    item._sMaxVal = maxs
                    leftWidgets -= 1
                elif sliceSize < mins:
                    freeWidth -= mins
                    leftWidgets -= 1
                    # slicesize = freeWidth//leftWidgets
                    iterate = True
                    item._sMin = True
                    item._sMinVal = mins

        # loop and set the geometry of any item
        for item in self.children():
            if item._sMax:
                item.setGeometry(newx, newy, item._sMaxVal, h)
                newx += item._sMaxVal
            elif item._sMin:
                item.setGeometry(newx, newy, item._sMinVal, h)
                newx += item._sMinVal
            else:
                sliceSize = freeWidth//leftWidgets
                item.setGeometry(newx, newy, sliceSize, h)
                newx += sliceSize
                freeWidth -= sliceSize
                leftWidgets -= 1
            if isinstance(item, TTkWidgetItem) and not item.isEmpty():
                item.widget().update()
                item.widget().getCanvas().zTop()
            elif isinstance(item, TTkLayout):
                item.update()


class TTkVBoxLayout(TTkLayout):
    def __init__(self):
        TTkLayout.__init__(self)

    def minimumWidth(self):
        ''' process the widgets and get the min size '''
        minw = TTkLayout.minimumWidth(self)
        for item in self.children():
            w1  = item.minimumWidth()
            if w1 > minw : minw = w1
        return minw

    def minimumHeight(self):
        ''' process the widgets and get the min size '''
        minh = 0
        for item in self.children():
            h1  = item.minimumHeight()
            minh += h1
        return minh

    def maximumWidth(self):
        ''' process the widgets and get the min size '''
        maxw = TTkLayout.maximumWidth(self)
        for item in self.children():
            w1  = item.maximumWidth()
            if w1 < maxw : maxw = w1
        return maxw

    def maximumHeight(self):
        ''' process the widgets and get the min size '''
        maxh = 0
        for item in self.children():
            h1 = item.maximumHeight()
            maxh += h1
        return maxh

    def update(self):
        x, y, w, h = self.geometry()
        numWidgets = self.count()
        leftWidgets = numWidgets
        freeHeight = h
        newx, newy = x, y
        # Loop to check the resizable space
        for item in self.children():
            item._sMax = False
            item._sMin = False
        iterate = True
        while iterate and leftWidgets > 0:
            iterate = False
            sliceSize = freeHeight//leftWidgets
            for item in self.children():
                if item._sMax or item._sMin: continue
                maxs = item.maximumHeight()
                mins = item.minimumHeight()
                if sliceSize > maxs:
                    freeHeight -= maxs
                    iterate = True
                    item._sMax = True
                    item._sMaxVal = maxs
                    leftWidgets -= 1
                elif sliceSize < mins:
                    freeHeight -= mins
                    leftWidgets -= 1
                    # slicesize = freeHeight//leftWidgets
                    iterate = True
                    item._sMin = True
                    item._sMinVal = mins

        # loop and set the geometry of any item
        for item in self.children():
            if item._sMax:
                item.setGeometry(newx, newy, w, item._sMaxVal)
                newy += item._sMaxVal
            elif item._sMin:
                item.setGeometry(newx, newy, w, item._sMinVal)
                newy += item._sMinVal
            else:
                sliceSize = freeHeight//leftWidgets
                item.setGeometry(newx, newy, w, sliceSize)
                newy += sliceSize
                freeHeight -= sliceSize
                leftWidgets -= 1
            if isinstance(item, TTkWidgetItem) and not item.isEmpty():
                item.widget().update()
                item.widget().getCanvas().zTop()
            elif isinstance(item, TTkLayout):
                item.update()
