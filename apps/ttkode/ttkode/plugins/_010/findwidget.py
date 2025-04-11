# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['FindWidget']

import os
import re
from threading import Thread
import TermTk as ttk

import ttkode

class _ExpandButton(ttk.TTkButton):
    def __init__(self, **kwargs):
        params = {
            'border':False,
            'checked':False,
            'checkable':True,
            'minSize':(4,1),
            'maxSize':(4,1),
        }
        super().__init__(**kwargs|params)

    def paintEvent(self, canvas):
        if self.isChecked():
            canvas.drawChar(pos=(1,0),char='▼')
        else:
            canvas.drawChar(pos=(1,0),char='▶')

class FindWidget(ttk.TTkContainer):
    __slots__ = (
        '_runId'
        '_results_tree',
        '_search_le','_replace_le','_files_inc_le','_files_exc_le')
    _runId:int
    _results_tree:ttk.TTkTreeWidget
    _search_le:ttk.TTkLineEdit
    _replace_le:ttk.TTkLineEdit
    _files_inc_le:ttk.TTkLineEdit
    _files_exc_le:ttk.TTkLineEdit
    def __init__(self, **kwargs):
        self._runId = 0
        super().__init__(**kwargs)
        self.setLayout(layout:=ttk.TTkGridLayout())

        searchLayout = ttk.TTkGridLayout()
        searchLayout.addWidget(expandReplace:=_ExpandButton(), 0, 0)
        searchLayout.addWidget(search :=ttk.TTkLineEdit(hint='Search'), 0, 1)
        searchLayout.addWidget(repl__l:=ttk.TTkLabel(visible=False, text='sub:'), 1, 0)
        searchLayout.addWidget(ft_in_l:=ttk.TTkLabel(visible=False, text='inc:'), 2, 0)
        searchLayout.addWidget(ft_ex_l:=ttk.TTkLabel(visible=False, text='exc:'), 3, 0)
        searchLayout.addWidget(replace:=ttk.TTkLineEdit(visible=False, hint='Replace'),          1, 1)
        searchLayout.addWidget(ft_incl:=ttk.TTkLineEdit(visible=False, hint='Files to include'), 2, 1)
        searchLayout.addWidget(ft_excl:=ttk.TTkLineEdit(visible=False, hint='Files to exclude'), 3, 1)

        layout.addItem(searchLayout, 0, 0)
        layout.addWidget(btn_search:=ttk.TTkButton(text="Search", border=False), 4,0)
        layout.addWidget(res_tree:=ttk.TTkTree(), 5,0)
        res_tree.setHeaderLabels(["Results"])
        res_tree.setColumnWidth(0,100)

        expandReplace.toggled.connect(replace.setVisible)
        expandReplace.toggled.connect(repl__l.setVisible)
        expandReplace.toggled.connect(ft_incl.setVisible)
        expandReplace.toggled.connect(ft_excl.setVisible)
        expandReplace.toggled.connect(ft_in_l.setVisible)
        expandReplace.toggled.connect(ft_ex_l.setVisible)

        self._results_tree = res_tree
        self._search_le = search
        self._replace_le = replace
        self._files_inc_le = ft_incl
        self._files_exc_le = ft_excl

        btn_search.clicked.connect(self._search)

    @ttk.pyTTkSlot()
    def _search(self):
        self._runId += 1
        search_pattern = str(self._search_le.text())
        if not search_pattern:
            return
        def _search_threading():
            self._results_tree.clear()
            for (file,root,matches) in self._search_files('.',str(search_pattern),self._runId):
                ttk.TTkLog.debug((file,matches))
                item = ttk.TTkTreeWidgetItem([
                        ttk.TTkString(
                            ttk.TTkCfg.theme.fileIcon.getIcon(file),
                            ttk.TTkCfg.theme.fileIconColor) + " " +
                        ttk.TTkString(f" {file} ", ttk.TTkColor.YELLOW+ttk.TTkColor.BOLD) +
                        ttk.TTkString(f" {root} ", ttk.TTkColor.fg("#888888"))
                    ],expanded=True)
                for num,line in matches:
                    item.addChild(
                        ttk.TTkTreeWidgetItem([
                            ttk.TTkString(str(num)+" ",ttk.TTkColor.YELLOW) +
                            ttk.TTkString(line.replace('\n','')).completeColor(
                                match=search_pattern,
                                color=ttk.TTkColor.GREEN)
                        ]))
                self._results_tree.addTopLevelItem(item)
        Thread(target=_search_threading).start()

    def _search_files(self, root_folder, match, runId):
        matches = []
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                if runId != self._runId:
                    return
                if file.endswith('.py'): # file.endswith(file_extension):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        line_matches = [(i+1, line) for i, line in enumerate(lines) if match in line]
                        if line_matches:
                            yield (file, root, line_matches)

    def _search_files_re(self, root_folder, file_extension, search_pattern):
        matches = []
        regex = re.compile(search_pattern)
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                if True: # file.endswith(file_extension):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        line_matches = [i + 1 for i, line in enumerate(lines) if regex.search(line)]
                        if line_matches:
                            yield (file_path, line_matches)

