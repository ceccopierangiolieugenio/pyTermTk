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

import sys, os, time, argparse, re
import subprocess

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

class GitHelper():
    def graph():
        return subprocess.run(['git',"log", "--all", "--pretty=format:---CC%hCC--- ---DD%adDD--- ---MM%s%dMM--- ---AA%anAA---", "--graph", "--date=short", "--color=always"],capture_output=True).stdout.decode('utf-8').split('\n')

    def show(commit) -> str:
        return subprocess.run(['git',"show", commit, "--color=always"],capture_output=True).stdout.decode('utf-8')

    def fileList(commit) -> str:
        return subprocess.run(['git',"show", "--name-only", "--pretty=", commit],capture_output=True).stdout.decode('utf-8')

class GitTTK(ttk.TTkAppTemplate):

    def __init__(self, border=False, **kwargs):
        self._allCommits = []
        self._commitResults = []
        self._diffLines = []

        super().__init__(border, **kwargs)

        self._tableCommit = ttk.TTkFancyTable(selectColor=ttk.TTkColor.bg('#882200'))
        self._diffText:ttk.TTkTextEditView = ttk.TTkTextEdit(readOnly=False)
        self._fileList:ttk.TTkListWidget = ttk.TTkList()
        self._logView = ttk.TTkLogViewer()

        w,h = self.size()

        self.setWidget(widget=self._tableCommit, title="Diff",  size=h//2, position=ttk.TTkAppTemplate.HEADER)
        self.setWidget(widget=self._diffText,    title="Diff",             position=ttk.TTkAppTemplate.MAIN)
        self.setWidget(widget=self._fileList,    title="Files", size=50,   position=ttk.TTkAppTemplate.RIGHT)
        self.setWidget(widget=self._logView,     title="Logs",  size=0,    position=ttk.TTkAppTemplate.FOOTER)

        self._refreshCommits()

        @ttk.pyTTkSlot(int)
        def _tableCallback(val):
            commit = self._allCommits[val]
            if not commit: return
            diff = GitHelper.show(commit).replace(chr(65039),' ')
            self._diffText.setText(diff)
            self._diffLines = diff.split('\n')
            files = GitHelper.fileList(commit).split('\n')
            files = [l for l in files if l] # remove empty lines
            self._fileList.removeItems(self._fileList.items())
            self._fileList.addItem('Comment')
            self._fileList.addItems(files)

        self._tableCommit.activated.connect(_tableCallback)
        self._fileList.textClicked.connect(self._selectFileCallback)

    def _refreshCommits(self):
        minGraph = 0
        minAuthor = 0
        minDate = 0
        reGraph   = re.compile(r'^(.*)---CC.*$')
        reTime    = re.compile(r'^.*---DD(.*)DD---.*$')
        reMessage = re.compile(r'^.*---MM(.*)MM---.*$')
        reAuthor  = re.compile(r'^.*---AA(.*)AA---.*$')
        reCommit  = re.compile(r'^.*---CC(.*)CC---.*$')

        for line in GitHelper.graph():
            g = _m.group(1) if (_m:=reGraph.match(line))   else line
            g = ttk.TTkString(g)
            minGraph = max(minGraph, g.termWidth())
            d = _m.group(1) if (_m:=reTime.match(line))    else ""
            minDate = max(minDate, len(d))
            a = _m.group(1) if (_m:=reAuthor.match(line))  else ""
            minAuthor = max(minAuthor, len(a))
            m = _m.group(1) if (_m:=reMessage.match(line)) else ""
            c = _m.group(1) if (_m:=reCommit.match(line))  else ""
            cc = f"{c} - {m}" if c and m else ""
            self._allCommits.append(c)
            self._commitResults.append((g, cc, a, d))

        self._tableCommit.setHeader(("","commit","Name","Date"))
        self._tableCommit.setColumnSize((minGraph,-1,minAuthor+1,15))
        self._tableCommit.setColumnColors((
                ttk.TTkColor.RST,
                ttk.TTkColor.fg('#cccccc', modifier=ttk.TTkColorGradient(increment=-2)),
                ttk.TTkColor.fg('#888800', modifier=ttk.TTkColorGradient(increment=6)),
                ttk.TTkColor.fg('#00dddd', modifier=ttk.TTkColorGradient(increment=-4)),
            ))
        for commit in self._commitResults:
            self._tableCommit.appendItem(commit)

    ttk.pyTTkSlot(str)
    def _selectFileCallback(self, file):
        # cursor = diffText.textCursor()
        # cursor.
        self._diffText.textCursor().movePosition(operation=ttk.TTkTextCursor.MoveOperation.End)
        self._diffText.ensureCursorVisible()
        if file == 'Comment':
            self._diffText.textCursor().setPosition(line=0,pos=0)
            self._diffText.setExtraSelections([])
        elif self._diffText.find(file):
            cursor = self._diffText.textCursor().copy()
            cursor.clearSelection()
            selection = ttk.TTkTextEdit.ExtraSelection(
                                            cursor=cursor,
                                            color=ttk.TTkColor.BG_RED,
                                            format=ttk.TTkK.SelectionFormat.FullWidthSelection)
            self._diffText.setExtraSelections([selection])
        self._diffText.ensureCursorVisible()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', help='Windowed', action='store_true')
    args = parser.parse_args()

    fullscreen = not args.w

    root = ttk.TTk()
    if fullscreen:
        gittk = root
        root.setLayout(ttk.TTkGridLayout())
    else:
        root = ttk.TTk()
        gittk = ttk.TTkWindow(parent=root,pos = (1,1), size=(100,40), title="gittk", border=True, layout=ttk.TTkGridLayout())
    GitTTK(parent=gittk)

    root.mainloop()

if __name__ == "__main__":
    main()
