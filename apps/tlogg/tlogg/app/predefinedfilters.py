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

__all__ = ['PredefinedFilters','PredefinedFiltersFormWindow']

import copy
from readline import insert_text

from . import TloggCfg, TloggGlbl

from TermTk import *

class PredefinedFiltersFormWindow(TTkWindow):
    '''
    This form is inspired by klogg "PredefinedFilters..." form
    '''

    def __init__(self, *args, **kwargs):
        TTkWindow.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'PredefinedFiltersFormWindow' )

        self._filters = copy.deepcopy(TloggCfg.filters)
        self._selected = -1

        self._retLayout     = TTkVBoxLayout() # Full Layout
        self._controlLayout = TTkGridLayout() # Layout including the add/remove/move buttons
        self._filtersLayout = TTkGridLayout() # Layout having the filters form
        self._bottomLayout  = TTkGridLayout() # Layout including the OK,Cancel,Apply Buttons

        self.setLayout(self._retLayout)

        self._retLayout.addItem(self._controlLayout)
        self._retLayout.addItem(self._filtersLayout)
        self._retLayout.addItem(self._bottomLayout)

        self._addButton    = TTkButton(text="+",maxWidth=3)
        self._removeButton = TTkButton(text="-",maxWidth=3)
        self._upButton     = TTkButton(text="▲",maxWidth=3)
        self._downButton   = TTkButton(text="▼",maxWidth=3)

        self._controlLayout.addWidget(self._addButton    ,1,0)
        self._controlLayout.addWidget(self._removeButton ,1,1)
        self._controlLayout.addWidget(TTkSpacer(maxHeight=1) ,1,2)
        self._controlLayout.addWidget(self._upButton     ,1,3)
        self._controlLayout.addWidget(self._downButton   ,1,4)

        self._bottomLayout.addWidget(applyBtn  := TTkButton(text="Apply",  border=True, maxHeight=3),0,1)
        self._bottomLayout.addWidget(cancelBtn := TTkButton(text="Cancel", border=True, maxHeight=3),0,2)
        self._bottomLayout.addWidget(okBtn     := TTkButton(text="OK",     border=True, maxHeight=3),0,3)

        self._refreshFilters()

        def _move(offset):
            def _moveUpDown():
                if self._selected < 0: return
                if self._selected + offset < 0: return
                if self._selected + offset >= len(self._filters): return
                item = self._filters.pop(self._selected)
                self._filters = self._filters[:self._selected+offset] + [item] + self._filters[self._selected+offset:]
                self._refreshFilters()
                self._selected += offset
            return _moveUpDown
        self._upButton.clicked.connect(_move(-1))
        self._downButton.clicked.connect(_move(1))

        def _addCallback():
            filter = {'name':f'n:{len(self._filters)+1}', 'pattern':'' }
            self._filters.append(filter)
            self._selected = -1
            self._refreshFilters()
        self._addButton.clicked.connect(_addCallback)

        def _removeCallback():
            if self._selected > -1:
                self._filters.pop(self._selected)
            self.selected = -1
            self._refreshFilters()
        self._removeButton.clicked.connect(_removeCallback)

        def _saveFilters():
            TloggCfg.filters = self._filters
            TloggCfg.save(searches=False, filters=True, colors=False, options=False)

        applyBtn.clicked.connect(_saveFilters)
        okBtn.clicked.connect(_saveFilters)
        okBtn.clicked.connect(self.close)
        cancelBtn.clicked.connect(self.close)

    def _refreshFilters(self):
        for item in self._filtersLayout.children():
            self._filtersLayout.removeItem(item)
        splitter = TTkSplitter(border=True)
        names    = TTkVBoxLayout()
        patterns = TTkVBoxLayout()
        splitter.addWidget(TTkFrame(border=False, layout=names))
        splitter.addWidget(TTkFrame(border=False, layout=patterns))
        splitter.setSizes([20,100])
        for i, filter in enumerate(self._filters):
            names.addWidget(   nl := TTkLineEdit(text=filter['name']))
            patterns.addWidget(pl := TTkLineEdit(text=filter['pattern']))
            # Stupid way to attach the textEdited signal directly to the array modification
            # It could have been made much better but Lazyness is an Issue
            def _setName(pos):
                def _set(txt): self._filters[pos]['name'] = txt
                return _set
            def _setPattern(pos):
                def _set(txt): self._filters[pos]['pattern'] = txt
                return _set
            def _setSelected(pos):
                def _set(focus):
                    if focus:
                        self._selected = pos
                return _set
            nl.textEdited.connect(_setName(i))
            pl.textEdited.connect(_setPattern(i))
            nl.focusChanged.connect(_setSelected(i))
            pl.focusChanged.connect(_setSelected(i))

        names.addWidget(   TTkSpacer())
        patterns.addWidget(TTkSpacer())
        self._filtersLayout.addWidget(splitter)


class PredefinedFilters(TTkResizableFrame):
    __slots__ = ('checked', 'unchecked', '_searchbox')
    def __init__(self, searchbox):
        layout=TTkVBoxLayout()
        TTkResizableFrame.__init__(self, layout=layout)
        self._name = 'PredefinedFilters'

        self._searchbox = searchbox

        filters = copy.deepcopy(TloggCfg.filters)
        for filter in filters:
            def _cb(p, sb):
                def _ret(state):
                    txt = sb.currentText()
                    if state == TTkK.Checked:
                        if not txt:
                            txt = p
                        elif txt.find(p) == -1:
                            txt += '|'+p
                    else:
                        p1 = f"|{p}"
                        p2 = f"{p}|"
                        if txt.find(p1) != -1:
                            txt = txt.replace(p1,'')
                        elif txt.find(p2) != -1:
                            txt = txt.replace(p2,'')
                        else:
                            txt = txt.replace(p,'')
                    sb.setCurrentText(txt)
                return _ret

            layout.addWidget(cb := TTkCheckbox(text=filter['name'],checked=searchbox.currentText().find(filter['pattern'])!=-1))
            cb.stateChanged.connect(_cb(filter['pattern'], searchbox))
        w,h = self.minimumSize()
        self.resize(w,h)

