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

from pathlib import Path
from threading import Thread,Event,Lock
from typing import Generator,List,Tuple,Dict,Optional

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

def _glob_match_patterns(path, patterns) -> bool:
    if path == '.':
        check_path = ''
    elif path.startswith('./'):
        check_path = path[2:]
    else:
        check_path = path
    return any(f"/{_p}/" in path for _p in patterns if _p) or any(fnmatch.fnmatch(check_path, _p) for _p in patterns if _p)

def _custom_walk(directory:str, include_patterns:List[str]=[], exclude_patterns:List[str]=[]) -> Generator[Tuple[str, str], None, None]:
    gitignore_path = os.path.join(directory, '.gitignore')
    exclude_patterns = exclude_patterns + _load_gitignore_patterns(gitignore_path)
    for entry in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, entry)
        if _glob_match_patterns(full_path, exclude_patterns):
            continue
        if not os.path.exists(full_path):
            continue
        if os.path.isdir(full_path):
            if entry == '.git':
                continue
            yield from _custom_walk(full_path, include_patterns, exclude_patterns)
        else:
            if include_patterns and not _glob_match_patterns(full_path, include_patterns):
                # ttk.TTkLog.debug(f"{include_patterns=} {full_path=}")
                continue
            yield directory, entry

def _walk_with_gitignore(root):
    for dirpath, filenames in os.walk(root):
        gitignore_path = os.path.join(dirpath, '.gitignore')
        patterns = _load_gitignore_patterns(gitignore_path)

        filenames[:] = [f for f in filenames if not _glob_match_patterns(os.path.join(dirpath, f), patterns)]

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
        '_runId',
        '_replace_data',
        '_results_tree',
        '_search_thread', '_search_stop_event', '_search_lock',
        '_search_le','_replace_le','_files_inc_le','_files_exc_le')
    _runId:int
    _search_lock:Lock
    _search_thread:Optional[Thread]
    _search_stop_event:Event
    _replace_data:Dict
    _results_tree:ttk.TTkTreeWidget
    _search_le:ttk.TTkLineEdit
    _replace_le:ttk.TTkLineEdit
    _files_inc_le:ttk.TTkLineEdit
    _files_exc_le:ttk.TTkLineEdit
    def __init__(self, **kwargs):
        self._runId = 0
        self._replace_data = {}
        self._search_thread = None
        self._search_lock = Lock()
        self._search_stop_event = Event()
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
        btn_replace.clicked.connect(self._ask_replace)
        btn_expand.clicked.connect(self._results_tree.expandAll)
        btn_collapse.clicked.connect(self._results_tree.collapseAll)

        search.returnPressed.connect(self._search)
        replace.returnPressed.connect(self._search)
        ft_incl.returnPressed.connect(self._search)
        ft_excl.returnPressed.connect(self._search)

        search.textEdited.connect(self._search)
        replace.textEdited.connect(self._search)
        ft_incl.textEdited.connect(self._search)
        ft_excl.textEdited.connect(self._search)

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
    def _ask_replace(self) -> None:
        if not self._replace_le.text():
            return
        _numFiles = len(self._replace_data.get('files',[]))
        _numMatches = sum(len(_r.get('matches',[])) for _r in self._replace_data.get('files',[]))
        _search_pattern = str(self._search_le.text())
        _replace_pattern = str(self._replace_le.text())

        messageBox = ttk.TTkMessageBox(
            title="🚨 Apply? 🚨",
            text=ttk.TTkString(f"Do you want to repace {_numMatches} occurrences of\n'{_search_pattern}'\nin {_numFiles} files with\n'{_replace_pattern}'?"),
            icon=ttk.TTkMessageBox.Icon.Warning,
            standardButtons=
                ttk.TTkMessageBox.StandardButton.Ok|
                ttk.TTkMessageBox.StandardButton.Cancel)

        @ttk.pyTTkSlot(ttk.TTkMessageBox.StandardButton)
        def _cb(btn):
            if btn == ttk.TTkMessageBox.StandardButton.Ok:
                ttk.TTkLog.debug(f"Replace '{_search_pattern}' with '{_replace_pattern}'")
                for _file_def in self._replace_data.get('files',[]):
                    _file = Path(_file_def['root']) / _file_def['file']
                    if not self._replace_data.get('files',[]):
                        ttk.TTkLog.error(f"{_file} does not exists!!!")
                    else:
                        _content = _file.read_text()
                        _new_content = _content.replace(_search_pattern,_replace_pattern)
                        _file.write_text(_new_content)
            else:
                ttk.TTkLog.debug(f"Discard")
            self._search()
        messageBox.buttonSelected.connect(_cb)
        ttk.TTkHelper.overlay(None, messageBox, 5, 5, True)

    def _search_threading(self, search_pattern:str, include_patterns:str, exclude_patterns:str, replace_pattern:str) -> None:
        self._results_tree.clear()
        group = []
        groupSize = 1
        self._replace_data = {'files':[]}
        for (file,root,matches) in self._search_files('.',search_pattern,self._runId,include_patterns,exclude_patterns):
            if self._search_stop_event.is_set():
                return

            self._replace_data['files'].append({'file':file,'root':root,'matches':matches})
            # ttk.TTkLog.debug((file,matches))
            item = ttk.TTkTreeWidgetItem([
                    ttk.TTkString(
                        ttk.TTkCfg.theme.fileIcon.getIcon(file),
                        ttk.TTkCfg.theme.fileIconColor) + " " +
                    ttk.TTkString(f" {file} ", ttk.TTkColor.YELLOW+ttk.TTkColor.BOLD+ttk.TTkColor.bg('#000088')) +
                    ttk.TTkString(f" {root} ", ttk.TTkColor.fg("#888888"))
                ],expanded=True)
            children = []
            for num,line in matches:
                line = line.lstrip(' ')
                # index = line.find(search_pattern)
                # outLine =
                if replace_pattern:
                    _s = line.replace('\n','').split(search_pattern)
                    _j = (
                        ttk.TTkString(search_pattern,ttk.TTkColor.RED + ttk.TTkColor.STRIKETROUGH) +
                        ttk.TTkString(replace_pattern,ttk.TTkColor.GREEN) + ttk.TTkColor.RST)
                    ttkLine = _j.join(_s)
                else:
                    ttkLine = ttk.TTkString(line.replace('\n','')).completeColor(
                            match=search_pattern,
                            color=ttk.TTkColor.GREEN)
                children.append(_MatchTreeWidgetItem([ttk.TTkString(str(num)+" ",ttk.TTkColor.CYAN) + ttkLine] ,
                        match=line,
                        lineNumber=num,
                        path=os.path.join(root,file)))
            item.addChildren(children)
            group.append(item)
            if len(group) > groupSize:
                self._results_tree.addTopLevelItems(group)
                group = []
                if groupSize < 0x400:
                    groupSize <<= 1
            # self._results_tree.addTopLevelItem(item)
        if group:
            self._results_tree.addTopLevelItems(group)

    @ttk.pyTTkSlot()
    def _search(self) -> None:
        with self._search_lock:
            if self._search_thread:
                self._search_stop_event.set()
                self._search_thread.join()
                self._search_stop_event.clear()
                self._search_thread = None
            self._runId += 1
            search_pattern = str(self._search_le.text())
            replace_pattern = str(self._replace_le.text())
            include_patterns = _s.split(',') if (_s:=str(self._files_inc_le.text())) else []
            exclude_patterns = _s.split(',') if (_s:=str(self._files_exc_le.text())) else []
            if not search_pattern:
                self._results_tree.clear()
                return
            if self._search_thread:
                self._search_thread.join()
            self._search_thread = Thread(
                target=self._search_threading,
                args=(search_pattern, include_patterns, exclude_patterns, replace_pattern))
            self._search_thread.start()

    def _search_files(self, root_folder, match, runId, include_patterns, exclude_patterns):
        for root, file in _custom_walk(root_folder,include_patterns,exclude_patterns):
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

