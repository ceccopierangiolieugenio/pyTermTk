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
import fnmatch
import mimetypes

from threading import Thread
from typing import Generator,List,Tuple

import TermTk as ttk

import os
import fnmatch

from ttkode import ttkodeProxy
from ttkode.app.ttkode import TTKodeFileWidgetItem

import mimetypes

def is_text_file(file_path, block_size=512):
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    text_based_mime_types = [
        'text/', 'application/json', 'application/xml',
        'application/javascript', 'application/x-httpd-php',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    if mime_type is not None and any(mime_type.startswith(mime) for mime in text_based_mime_types):
        return True

    # Check for non-printable characters
    try:
        with open(file_path, 'rb') as file:
            block = file.read(block_size)
        if b'\0' in block:
            return False
        text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
        return not bool(block.translate(None, text_characters))
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

def _load_gitignore_patterns(gitignore_path):
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            patterns = f.read().splitlines()
        return patterns
    return []

def _should_ignore(path, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

def _custom_walk(directory:str, patterns:List[str]=[]) -> Generator[Tuple[str, str], None, None]:
    gitignore_path = os.path.join(directory, '.gitignore')
    patterns = patterns + _load_gitignore_patterns(gitignore_path)
    for entry in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, entry)
        if _should_ignore(full_path, patterns):
            continue
        if os.path.isdir(full_path):
            if entry == '.git':
                continue
            yield from _custom_walk(full_path, patterns)
        else:
            yield directory, entry

def _walk_with_gitignore(root):
    for dirpath, filenames in os.walk(root):
        gitignore_path = os.path.join(dirpath, '.gitignore')
        patterns = _load_gitignore_patterns(gitignore_path)

        filenames[:] = [f for f in filenames if not _should_ignore(os.path.join(dirpath, f), patterns)]

        yield dirpath, filenames


class _ToggleButton(ttk.TTkButton):
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

class _MatchTreeWidgetItem(TTKodeFileWidgetItem):
    __slots__ = ('_match','_line','_file')
    _match:str
    def __init__(self, *args, match:str, **kwargs):
        self._match = match
        super().__init__(*args, **kwargs)

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
        searchLayout.addWidget(expandReplace:=_ToggleButton(), 0, 0)
        searchLayout.addWidget(search  :=ttk.TTkLineEdit(hint='Search'), 0, 1)
        searchLayout.addWidget(repl__l:=ttk.TTkLabel(visible=False, text='sub:'), 1, 0)
        searchLayout.addWidget(ft_in_l:=ttk.TTkLabel(visible=False, text='inc:'), 2, 0)
        searchLayout.addWidget(ft_ex_l:=ttk.TTkLabel(visible=False, text='exc:'), 3, 0)
        searchLayout.addWidget(replace:=ttk.TTkLineEdit(visible=False, hint='Replace'),          1, 1)
        searchLayout.addWidget(ft_incl:=ttk.TTkLineEdit(visible=False, hint='Files to include'), 2, 1)
        searchLayout.addWidget(ft_excl:=ttk.TTkLineEdit(visible=False, hint='Files to exclude'), 3, 1)
        layout.addItem(searchLayout, 0, 0)

        controlsLayout = ttk.TTkGridLayout()
        controlsLayout.addWidget(btn_search:=ttk.TTkButton(text="Search", border=False), 0,0)
        controlsLayout.addWidget(btn_replace:=ttk.TTkButton(text='Replace', border=False, enabled=False), 0, 1)
        controlsLayout.addWidget(btn_expand  :=ttk.TTkButton(text='+', maxWidth=3, border=False), 0, 2)
        controlsLayout.addWidget(btn_collapse:=ttk.TTkButton(text='-', maxWidth=3, border=False), 0, 3)
        layout.addItem(controlsLayout,1,0)

        layout.addWidget(res_tree:=ttk.TTkTree(dragDropMode=ttk.TTkK.DragDropMode.AllowDrag), 2,0)
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
        btn_expand.clicked.connect(self._results_tree.expandAll)
        btn_collapse.clicked.connect(self._results_tree.collapseAll)
        search.returnPressed.connect(self._search)
        res_tree.itemActivated.connect(self._activated)

        @ttk.pyTTkSlot(str)
        def _replace_txt(value):
            btn_replace.setEnabled(bool(value))

        self._replace_le.textChanged.connect(_replace_txt)


    @ttk.pyTTkSlot(ttk.TTkTreeWidgetItem, int)
    def _activated(self, item:ttk.TTkTreeWidgetItem, _):
        if isinstance(item, _MatchTreeWidgetItem):
            file = item.path()
            line = item.lineNumber()
            ttkodeProxy.openFile(file, line)


    @ttk.pyTTkSlot()
    def _search(self):
        self._runId += 1
        search_pattern = str(self._search_le.text())
        if not search_pattern:
            return
        def _search_threading():
            self._results_tree.clear()
            group = []
            groupSize = 1
            for (file,root,matches) in self._search_files('.',str(search_pattern),self._runId):
                ttk.TTkLog.debug((file,matches))
                item = ttk.TTkTreeWidgetItem([
                        ttk.TTkString(
                            ttk.TTkCfg.theme.fileIcon.getIcon(file),
                            ttk.TTkCfg.theme.fileIconColor) + " " +
                        ttk.TTkString(f" {file} ", ttk.TTkColor.YELLOW+ttk.TTkColor.BOLD+ttk.TTkColor.bg('#000088')) +
                        ttk.TTkString(f" {root} ", ttk.TTkColor.fg("#888888"))
                    ],expanded=True)
                for num,line in matches:
                    line = line.lstrip(' ')
                    # index = line.find(search_pattern)
                    # outLine =
                    item.addChild(
                        _MatchTreeWidgetItem([
                            ttk.TTkString(str(num)+" ",ttk.TTkColor.CYAN) +
                            ttk.TTkString(line.replace('\n','')).completeColor(
                                match=search_pattern,
                                color=ttk.TTkColor.GREEN)
                            ],
                            match=line,
                            lineNumber=num,
                            path=os.path.join(root,file)))
                group.append(item)
                if len(group) > groupSize:
                    self._results_tree.addTopLevelItems(group)
                    group = []
                    groupSize <<= 1
                # self._results_tree.addTopLevelItem(item)
            if group:
                self._results_tree.addTopLevelItems(group)
        Thread(target=_search_threading).start()

    def _search_files(self, root_folder, match, runId):
        matches = []
        for root, file in _custom_walk(root_folder):
            if runId != self._runId:
                return
            if True: # file.endswith('.py'): # file.endswith(file_extension):
                file_path = os.path.join(root, file)
                if not is_text_file(file_path):
                    continue
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    line_matches = [(i, line.split('\n')[0]) for i, line in enumerate(lines) if match in line]
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

