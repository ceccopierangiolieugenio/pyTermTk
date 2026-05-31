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
**Box Layout** [:ref:`Tutorial <Layout-Tutorial_Intro>`]
'''

__all__ = ['TTkHBoxLayout', 'TTkVBoxLayout']

from TermTk.TTkCore.constant import TTkK

from .gridlayout import TTkGridLayout

class TTkHBoxLayout(TTkGridLayout):
    '''The :py:class:`TTkHBoxLayout` class lines up widgets horizontally.

    ::

        TTkHBoxLayout
         ╔═════════╤═════════╤═════════╗
         ║ Widget1 │ Widget2 │ Widget3 ║
         ║         │         │         ║
         ║         │         │         ║
         ║         │         │         ║
         ║         │         │         ║
         ║         │         │         ║
         ╚═════════╧═════════╧═════════╝
    '''
    pass

class TTkVBoxLayout(TTkGridLayout):
    '''The :py:class:`TTkVBoxLayout` class lines up widgets vertically.

    ::

        TTkVBoxLayout
         ╔═════════════════════════════╗
         ║         Widget 1            ║
         ╟─────────────────────────────╢
         ║         Widget 2            ║
         ╟─────────────────────────────╢
         ║         Widget 3            ║
         ╟─────────────────────────────╢
         ║         Widget 4            ║
         ╚═════════════════════════════╝
    '''
    def addItem(self, item):
        '''Add a layout item on the next available vertical slot.

        :param item: the item to be added
        :type item: :py:class:`TTkLayoutItem`
        '''
        TTkGridLayout.addItems(self, [item], direction=TTkK.VERTICAL)

    def addItems(self, items):
        '''Add layout items stacked vertically.

        :param items: the items to be added
        :type items: list[:py:class:`TTkLayoutItem`]
        '''
        TTkGridLayout.addItems(self,  items, direction=TTkK.VERTICAL)

    def addWidget(self, widget):
        '''Add a widget on the next available vertical slot.

        :param widget: the widget to be added
        :type widget: :py:class:`TTkWidget`
        '''
        TTkGridLayout.addWidgets(self, [widget], direction=TTkK.VERTICAL)

    def addWidgets(self, widgets):
        '''Add widgets stacked vertically.

        :param widgets: the widgets to be added
        :type widgets: list[:py:class:`TTkWidget`]
        '''
        TTkGridLayout.addWidgets(self,  widgets, direction=TTkK.VERTICAL)
