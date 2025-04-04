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

__all__ = ['LoggWidget']

import TermTk as ttk

from .cfg  import TloggCfg
from .glbl import TloggGlbl
from .fileviewer  import FileViewer, FileViewerArea, FileViewerSearch
from .predefinedfilters import PredefinedFilters

class LoggWidget(ttk.TTkSplitter):
    __slots__ = ('_btn_filters', '_bls_label_1', '_bls_cb_icase', '_bls_search', '_bls_searchbox',
                 '_topViewport', '_bottomViewport',
                 '_fileBuffer')
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs|{'orientation':ttk.TTkK.VERTICAL})

        topFrame    = ttk.TTkFrame(parent=self, border=False, layout=ttk.TTkVBoxLayout())
        bottomFrame = ttk.TTkFrame(parent=self, border=False, layout=ttk.TTkVBoxLayout())


        # Define the bottom layout widgets
        bottomLayoutSearch = ttk.TTkHBoxLayout()
        self._btn_filters   = ttk.TTkButton(text="Filters ^", maxWidth=11)
        self._bls_label_1   = ttk.TTkLabel(text=" Txt:", maxWidth=5)
        self._bls_cb_icase  = ttk.TTkCheckbox(text="Aa", maxWidth=5, checked=True)
        self._bls_search    = ttk.TTkButton(text="Search", maxWidth=10)
        self._bls_searchbox = ttk.TTkComboBox(editable=True)
        self._bls_searchbox.addItems(TloggCfg.searches)
        self._bls_searchbox.setCurrentIndex(0)

        bottomLayoutSearch.addWidget(self._btn_filters)
        bottomLayoutSearch.addWidget(self._bls_label_1)
        bottomLayoutSearch.addWidget(self._bls_searchbox)
        bottomLayoutSearch.addWidget(self._bls_cb_icase)
        bottomLayoutSearch.addWidget(self._bls_search)

        bottomFrame.layout().addItem(bottomLayoutSearch)

        # Define the main file Viewer
        self._fileBuffer = ttk.TTkFileBuffer(filename, 0x100, 0x1000)
        self._topViewport = FileViewer(filebuffer=self._fileBuffer)
        topViewer = FileViewerArea(parent=topFrame, fileView=self._topViewport)
        self._fileBuffer.indexUpdated.connect(self._topViewport.fileIndexing)
        self._fileBuffer.indexed.connect(self._topViewport.fileIndexed)
        # Define the Search Viewer
        self._bottomViewport = FileViewerSearch(filebuffer=self._fileBuffer)
        bottomViewer = FileViewerArea(parent=bottomFrame, fileView=self._bottomViewport)
        self._bottomViewport.selected.connect(self._topViewport.selectAndMove)
        self._bottomViewport.marked.connect(self._topViewport.markIndexes)
        self._topViewport.marked.connect(self._bottomViewport.markIndexes)

        # Add those viewpoers to the global list to allow dynamic refresh
        # TODO: Try to get rid of this
        TloggGlbl.addRefView(self._topViewport)
        TloggGlbl.addRefView(self._bottomViewport)

        self._bls_search.clicked.connect(self._search)
        self._bls_searchbox.editTextChanged.connect(self._search)

        def _openPredefinedFilters():
            ttk.TTkHelper.overlay(self._btn_filters, PredefinedFilters(self._bls_searchbox), -2, 1)
        self._btn_filters.clicked.connect(_openPredefinedFilters)

    @ttk.pyTTkSlot()
    def _search(self):
        searchtext = str(self._bls_searchbox.currentText())
        ttk.TTkLog.debug(f"{searchtext=}")
        indexes = self._fileBuffer.searchRe(searchtext, ignoreCase=self._bls_cb_icase.checkState() == ttk.TTkK.Checked)
        self._bottomViewport.searchedIndexes(indexes)
        self._bottomViewport.searchRe(searchtext)
        self._topViewport.searchedIndexes(indexes)
        self._topViewport.searchRe(searchtext)
        if TloggCfg.searches:
            x = set(TloggCfg.searches)
            ttk.TTkLog.debug(f"{x}")
            TloggCfg.searches = list(x)
            if searchtext in TloggCfg.searches:
                TloggCfg.searches.remove(searchtext)
        TloggCfg.searches.insert(0, searchtext)
        TloggCfg.searches = TloggCfg.searches[:TloggCfg.maxsearches]
        TloggCfg.save(searches=True,filters=False)
        self._bls_searchbox.clear()
        self._bls_searchbox.addItems(TloggCfg.searches)
        self._bls_searchbox.setCurrentIndex(0)
