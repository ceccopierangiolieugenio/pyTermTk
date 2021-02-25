#!/usr/bin/env python3

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

'''
    Layout System
'''

from TermTk.TTkCore.log import TTkLog
from TermTk.TTkLayouts.layout import TTkLayout, TTkWidgetItem
from TermTk.TTkLayouts.gridlayout import TTkGridLayout

class TTkHBoxLayout(TTkGridLayout): pass

# class TTkHBoxLayout(TTkLayout):
#     def __init__(self):
#         TTkLayout.__init__(self)
#
#     def minimumWidth(self) -> int:
#         ''' process the widgets and get the min size '''
#         minw = 0
#         for item in self.children():
#             w1  = item.minimumWidth()
#             minw += w1
#         return minw
#
#     def minimumHeight(self) -> int:
#         ''' process the widgets and get the min size '''
#         minh = TTkLayout.minimumHeight(self)
#         for item in self.children():
#             h1  = item.minimumHeight()
#             if h1 > minh : minh = h1
#         return minh
#
#     def maximumWidth(self) -> int:
#         ''' process the widgets and get the min size '''
#         maxw = 0
#         for item in self.children():
#             w1 = item.maximumWidth()
#             maxw += w1
#         return maxw
#
#     def maximumHeight(self) -> int:
#         ''' process the widgets and get the min size '''
#         maxh = TTkLayout.maximumHeight(self)
#         for item in self.children():
#             h1  = item.maximumHeight()
#             if h1 < maxh : maxh = h1
#         return maxh
#
#     def update(self):
#         x, y, w, h = self.geometry()
#         numWidgets = self.count()
#         leftWidgets = numWidgets
#         freeWidth = w
#         newx, newy = x, y
#         # Loop to check the resizable space
#         for item in self.children():
#             item._sMax = False
#             item._sMin = False
#         iterate = True
#
#         # Copy and Sort list of items based on the minsize
#         sortedItems = sorted(self.children(), key=lambda item: item.minimumWidth())
#
#         while iterate and leftWidgets > 0:
#             iterate = False
#             for item in sortedItems:
#                 if item._sMax or item._sMin: continue
#                 sliceSize = freeWidth//leftWidgets
#                 maxs = item.maximumWidth()
#                 mins = item.minimumWidth()
#                 if sliceSize >= maxs:
#                     freeWidth -= maxs
#                     iterate = True
#                     item._sMax = True
#                     item._sMaxVal = maxs
#                     leftWidgets -= 1
#                 elif sliceSize < mins:
#                     freeWidth -= mins
#                     leftWidgets -= 1
#                     iterate = True
#                     item._sMin = True
#                     item._sMinVal = mins
#
#         # loop and set the geometry of any item
#         for item in self.children():
#             if item._sMax:
#                 item.setGeometry(newx, newy, item._sMaxVal, h)
#                 newx += item._sMaxVal
#             elif item._sMin:
#                 item.setGeometry(newx, newy, item._sMinVal, h)
#                 newx += item._sMinVal
#             else:
#                 sliceSize = freeWidth//leftWidgets
#                 item.setGeometry(newx, newy, sliceSize, h)
#                 newx += sliceSize
#                 freeWidth -= sliceSize
#                 leftWidgets -= 1
#             if isinstance(item, TTkWidgetItem) and not item.isEmpty():
#                 item.widget().update()
#             elif isinstance(item, TTkLayout):
#                 item.update()


class TTkVBoxLayout(TTkLayout):
    def __init__(self):
        TTkLayout.__init__(self)

    def minimumWidth(self) -> int:
        ''' process the widgets and get the min size '''
        minw = TTkLayout.minimumWidth(self)
        for item in self.children():
            w1  = item.minimumWidth()
            if w1 > minw : minw = w1
        return minw

    def minimumHeight(self) -> int:
        ''' process the widgets and get the min size '''
        minh = 0
        for item in self.children():
            h1  = item.minimumHeight()
            minh += h1
        return minh

    def maximumWidth(self) -> int:
        ''' process the widgets and get the min size '''
        maxw = TTkLayout.maximumWidth(self)
        for item in self.children():
            w1  = item.maximumWidth()
            if w1 < maxw : maxw = w1
        return maxw

    def maximumHeight(self) -> int:
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

        # Copy and Sort list of items based on the minsize
        sortedItems = sorted(self.children(), key=lambda item: item.minimumHeight())

        while iterate and leftWidgets > 0:
            iterate = False
            for item in sortedItems:
                if item._sMax or item._sMin: continue
                sliceSize = freeHeight//leftWidgets
                maxs = item.maximumHeight()
                mins = item.minimumHeight()
                if sliceSize >= maxs:
                    freeHeight -= maxs
                    iterate = True
                    item._sMax = True
                    item._sMaxVal = maxs
                    leftWidgets -= 1
                elif sliceSize < mins:
                    freeHeight -= mins
                    leftWidgets -= 1
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
            elif isinstance(item, TTkLayout):
                item.update()
