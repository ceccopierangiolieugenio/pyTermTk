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

import os
import re
import sys
import argparse

import appdirs

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter, Terminal256Formatter, TerminalTrueColorFormatter

from TermTk import TTk, TTkK, TTkLog, TTkCfg, TTkColor, TTkTheme, TTkTerm, TTkHelper
from TermTk import TTkString
from TermTk import TTkColorGradient
from TermTk import pyTTkSlot, pyTTkSignal

from TermTk import TTkFrame, TTkButton
from TermTk import TTkTabWidget, TTkKodeTab
from TermTk import TTkAbstractScrollArea, TTkAbstractScrollView
from TermTk import TTkFileDialogPicker
from TermTk import TTkFileTree, TTkTextEdit

from TermTk import TTkGridLayout
from TermTk import TTkSplitter

from .cfg  import *
from .about import *
# from .options import optionsFormLayout, optionsLoadTheme
from .kodetextedit import KodeTextEditView
from .kodetextdocument import KodeTextDocument

class TTKode(TTkGridLayout):
    __slots__ = ('_kodeTab', '_documents')
    def __init__(self, *, files, **kwargs):
        self._documents = {}

        super().__init__(**kwargs)

        self.addWidget(splitter := TTkSplitter())

        layoutLeft = TTkGridLayout()
        splitter.addItem(layoutLeft, 20)

        hSplitter = TTkSplitter(parent=splitter,  orientation=TTkK.HORIZONTAL)

        menuFrame = TTkFrame(border=False, maxHeight=1)

        self._kodeTab = TTkKodeTab(parent=hSplitter, border=False, closable=True)

        fileMenu = menuFrame.newMenubarTop().addMenu("&File")
        fileMenu.addMenu("Open").menuButtonClicked.connect(self._showFileDialog)
        fileMenu.addMenu("Close") # .menuButtonClicked.connect(self._closeFile)
        fileMenu.addMenu("Exit").menuButtonClicked.connect(lambda _:TTkHelper.quit())

        def _showAbout(btn):
            TTkHelper.overlay(None, About(), 30,10)
        def _showAboutTTk(btn):
            TTkHelper.overlay(None, TTkAbout(), 30,10)

        helpMenu = menuFrame.newMenubarTop().addMenu("&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAbout)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(_showAboutTTk)

        fileTree = TTkFileTree(path='.')

        layoutLeft.addWidget(menuFrame, 0,0)
        layoutLeft.addWidget(fileTree, 1,0)
        layoutLeft.addWidget(quitbtn := TTkButton(border=True, text="Quit", maxHeight=3), 2,0)

        quitbtn.clicked.connect(TTkHelper.quit)

        for file in files:
            self._openFile(file)

        fileTree.fileActivated.connect(lambda x: self._openFile(x.path()))

    pyTTkSlot()
    def _showFileDialog(self):
        filePicker = TTkFileDialogPicker(pos = (3,3), size=(75,24), caption="Pick Something", path=".", fileMode=TTkK.FileMode.AnyFile ,filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        filePicker.pathPicked.connect(self._openFile)
        TTkHelper.overlay(None, filePicker, 20, 5, True)

    def _openFile(self, filePath):
        filePath = os.path.realpath(filePath)
        if filePath in self._documents:
            doc = self._documents[filePath]['doc']
        else:
            with open(filePath, 'r') as f:
                content = f.read()
            doc = KodeTextDocument(text=content, filePath=filePath)
            self._documents[filePath] = {'doc':doc,'tabs':[]}
        tview = KodeTextEditView(document=doc, readOnly=False)
        tedit = TTkTextEdit(textEditView=tview, lineNumber=True)
        doc.kodeHighlightUpdate.connect(tedit.update)
        label = TTkString(TTkCfg.theme.fileIcon.getIcon(filePath),TTkCfg.theme.fileIconColor) + TTkColor.RST + " " + os.path.basename(filePath)

        self._kodeTab.addTab(tedit, label)
        self._kodeTab.setCurrentWidget(tedit)

        # def _closeFile():
        #     if (index := KodeTab.lastUsed.currentIndex()) >= 0:
        #         KodeTab.lastUsed.removeTab(index)

def main():
    TTKodeCfg.pathCfg = appdirs.user_config_dir("ttkode")

    parser = argparse.ArgumentParser()
    # parser.add_argument('-f', help='Full Screen', action='store_true')
    parser.add_argument('-c', help=f'config folder (default: "{TTKodeCfg.pathCfg}")', default=TTKodeCfg.pathCfg)
    parser.add_argument('filename', type=str, nargs='*',
                    help='the filename/s')
    args = parser.parse_args()

    # TTkLog.use_default_file_logging()

    TTKodeCfg.pathCfg = args.c
    TTkLog.debug(f"Config Path: {TTKodeCfg.pathCfg}")

    TTKodeCfg.load()

    # if 'theme' not in TTKodeCfg.options:
    #     TTKodeCfg.options['theme'] = 'NERD'
    # optionsLoadTheme(TTKodeCfg.options['theme'])

    TTkTheme.loadTheme(TTkTheme.NERD)

    root = TTk( layout=TTKode(files=args.filename), title="TTkode",
                sigmask=(
                    # TTkTerm.Sigmask.CTRL_C |
                    TTkTerm.Sigmask.CTRL_Q |
                    TTkTerm.Sigmask.CTRL_S |
                    TTkTerm.Sigmask.CTRL_Z ))

    root.mainloop()
