# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import os
import fnmatch
from threading import Thread,Event,Lock

from pathlib import Path
from typing import List, Generator, Tuple, Optional

import TermTk as ttk

from ttkode.app.helpers.search_file import TTKode_SearchFile

class TTKode_CP_SearchFileThreading():
    __slots__ = (
        '_runId',
        '_search_thread', '_search_stop_event', '_search_lock',
        'search_results'
    )

    _runId:int
    _search_lock:Lock
    _search_thread:Optional[Thread]
    _search_stop_event:Event

    search_results:ttk.pyTTkSignal

    def __init__(self, **kwargs):
        self._runId = 0
        self._search_thread = None
        self._search_lock = Lock()
        self._search_stop_event = Event()
        self.search_results = ttk.pyTTkSignal(List[Path])

    @ttk.pyTTkSlot(str)
    def search(self, pattern:str) -> None:
        ttk.TTkLog.debug(pattern)
        with self._search_lock:
            if self._search_thread:
                self._search_stop_event.set()
                self._search_thread.join()
                self._search_stop_event.clear()
                self._search_thread = None
            if not pattern:
                return
            self._runId += 1
            self._search_thread = Thread(
                target=self._search_threading,
                args=(pattern,))
            self._search_thread.start()

    def _search_threading(self, search_pattern:str) -> None:
        items = 1
        ret:List[Path] = []
        for file in TTKode_SearchFile.getFilesFromPattern('.', pattern=search_pattern):
            if self._search_stop_event.is_set():
                return
            ret.append(file)
            if len(ret) >= items:
                self.search_results.emit(ret)
                items *= 2
                ret = []
        if ret:
            self.search_results.emit(ret)