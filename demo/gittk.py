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

import sys, os, time, argparse

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

import git

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Full Screen', action='store_true')
args = parser.parse_args()

fullscreen = args.f

repo = git.Repo('.')
assert not repo.bare

allCommits = list(repo.iter_commits('main'))

commitResults = []
for commit in allCommits:
    t = time.strftime("%d-%m-%Y %H:%M", time.gmtime(commit.committed_date))
    message = commit.message.split('\n')[0]
    author = commit.author
    commitResults.append((message,str(author),str(t)))

ttk.TTkLog.use_default_file_logging()


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

tableCommit.setColumnSize((-1,20,20))

tableCommit.setHeader(("commit","Name","Date"))
tableCommit.setColumnColors((
        ttk.TTkColor.fg('#cccccc', modifier=ttk.TTkColorGradient(increment=-2)),
        ttk.TTkColor.fg('#888800', modifier=ttk.TTkColorGradient(increment=6)),
        ttk.TTkColor.fg('#00dddd', modifier=ttk.TTkColorGradient(increment=-4)),
    ))

for commit in commitResults:
    tableCommit.appendItem(commit)

@ttk.pyTTkSlot(int)
def _tableCallback(val):
    commit = allCommits[val]
    diff = repo.git.diff(f"{commit.hexsha}~",f"{commit.hexsha}")
    # ttk.TTkLog.debug(diff)
    lines = ttk.TTkString()
    for line in diff.split('\n'):
        color = ttk.TTkColor.RST
        if   line.startswith('---') or line.startswith('+++'):
            color = ttk.TTkColor.fg('#000000')+ttk.TTkColor.bg('#888888')
        elif line.startswith('+'):
            color = ttk.TTkColor.fg('#00ff00')
        elif line.startswith('-'):
            color = ttk.TTkColor.fg('#ff0000')
        elif line.startswith('@@'):
            color = ttk.TTkColor.fg('#0088ff')
        lines += ttk.TTkString(line+"\n",color).tab2spaces()
    diffText.setText(lines)

tableCommit.activated.connect(_tableCallback)

root.mainloop()
