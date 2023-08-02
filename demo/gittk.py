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
        return subprocess.run(['git',"log", "--pretty=format:---CC%hCC--- ---DD%adDD--- ---MM%s%dMM--- ---AA%anAA---", "--graph", "--date=short", "--color=always"],capture_output=True).stdout.decode('utf-8').split('\n')

    def show(commit):
        return subprocess.run(['git',"show", commit, "--color=always"],capture_output=True).stdout.decode('utf-8')


parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen', action='store_true')
args = parser.parse_args()

fullscreen = args.f
allCommits = []
commitResults = []
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
    allCommits.append(c)
    commitResults.append((g, cc, a, d))


root = ttk.TTk()
if fullscreen:
    gittk = root
    root.setLayout(ttk.TTkGridLayout())
else:
    root = ttk.TTk()
    gittk = ttk.TTkWindow(parent=root,pos = (1,1), size=(100,40), title="gittk", border=True, layout=ttk.TTkGridLayout())

gittkVsplitter = ttk.TTkSplitter(parent=gittk, orientation=ttk.TTkK.VERTICAL)
tableCommit = ttk.TTkFancyTable(parent=gittkVsplitter, selectColor=ttk.TTkColor.bg('#882200'))
gittkHsplitter = ttk.TTkSplitter(parent=gittkVsplitter, orientation=ttk.TTkK.HORIZONTAL)
diffText = ttk.TTkTextEdit(parent=gittkHsplitter)
gittkHsplitter.addWidget(ttk.TTkTestWidgetSizes(border=True, title="Details"),20)
gittkVsplitter.addWidget(ttk.TTkLogViewer(),3)

tableCommit.setColumnSize((minGraph,-1,minAuthor+1,15))

tableCommit.setHeader(("","commit","Name","Date"))
tableCommit.setColumnColors((
        ttk.TTkColor.RST,
        ttk.TTkColor.fg('#cccccc', modifier=ttk.TTkColorGradient(increment=-2)),
        ttk.TTkColor.fg('#888800', modifier=ttk.TTkColorGradient(increment=6)),
        ttk.TTkColor.fg('#00dddd', modifier=ttk.TTkColorGradient(increment=-4)),
    ))

for commit in commitResults:
    tableCommit.appendItem(commit)

@ttk.pyTTkSlot(int)
def _tableCallback(val):
    commit = allCommits[val]
    if not commit: return
    diff = GitHelper.show(commit)
    diffText.setText(diff)

tableCommit.activated.connect(_tableCallback)

root.mainloop()
