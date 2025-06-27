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

import sys, os, argparse
import re
import random

sys.path.append(os.path.join(sys.path[0],'../libs/pyTermTk'))
import TermTk as ttk

from  showcase.layout_basic  import demoLayout
from  showcase.layout_nested import demoLayoutNested
from  showcase.layout_span   import demoLayoutSpan
from  showcase.tab           import demoTab
from  showcase.graph         import demoGraph
from  showcase.splitter      import demoSplitter
from  showcase.windows       import demoWindows
from  showcase.windowsflags  import demoWindowsFlags
from  showcase.formwidgets02 import demoFormWidgets
from  showcase.scrollarea01  import demoScrollArea01
from  showcase.scrollarea02  import demoScrollArea02
from  showcase.list          import demoList
from  showcase.menubar       import demoMenuBar
from  showcase.filepicker    import demoFilePicker
from  showcase.colorpicker   import demoColorPicker
from  showcase.textpicker    import demoTextPicker
from  showcase.tree          import demoTree
from  showcase.table         import demoTTkTable
from  showcase.fancytable    import demoFancyTable
from  showcase.fancytree     import demoFancyTree
from  showcase.textedit      import demoTextEdit
from  showcase.dragndrop     import demoDnD
from  showcase.dndtabs       import demoDnDTabs
from  showcase.sigmask       import demoSigmask
from  showcase.apptemplate   import demoAppTemplate

def stupidPythonHighlighter(txt):
    def _colorize(regex, txt, color):
        ret = txt
        if m := txt.findall(regexp=regex):
            for match in m:
                ret = ret.setColor(color, match=match)
        return ret

    # Operators
    txt = _colorize(re.compile(r'[\+\*\/\=\-\<\>\!]'), txt, ttk.TTkColor.fg('#00AAAA'))
    # Bool
    txt = _colorize(re.compile(r'True|False'), txt, ttk.TTkColor.fg('#0000FF'))

    # Numbers
    txt = _colorize(re.compile(r'[0-9]'), txt, ttk.TTkColor.fg('#00FFFF'))

    # Functions
    txt = _colorize(re.compile(r'[ \t]*def[ \t]*'), txt, ttk.TTkColor.fg('#00FFFF'))
    txt = _colorize(re.compile(r'[^= \t\.\()]*[\t ]*\('), txt, ttk.TTkColor.fg('#AAAA00'))
    # Objects
    txt = _colorize(re.compile(r'[^= \t\.\()]*\.'), txt, ttk.TTkColor.fg('#44AA00'))

    # Fix Extra colors
    txt = _colorize(re.compile(r'[\(\)]'), txt, ttk.TTkColor.RST)
    txt = _colorize(re.compile(r"'[^']*'"), txt, ttk.TTkColor.fg('#FF8800'))

    # Strings
    txt = _colorize(re.compile(r'"[^"]*"'), txt, ttk.TTkColor.fg('#FF8800'))
    txt = _colorize(re.compile(r"'[^']*'"), txt, ttk.TTkColor.fg('#FF8800'))

    # Comments
    txt = _colorize(re.compile(r'#.*\n'), txt, ttk.TTkColor.fg('#00FF00'))
    return txt

def showSource(file):
    if not file: return
    ttk.TTkLog.debug(f"Placeholder for the Sources - {file}")
    content = "Nothing"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),file)) as f:
        content = stupidPythonHighlighter( ttk.TTkString() + f.read() )
    sourceWin = ttk.TTkWindow(size=(100,40), title=file, layout=ttk.TTkGridLayout(), flags=ttk.TTkK.WindowFlag.WindowMaximizeButtonHint|ttk.TTkK.WindowFlag.WindowCloseButtonHint)
    texEdit = ttk.TTkTextEdit(parent=sourceWin, lineNumber=True)
    texEdit.setText(content)
    ttk.TTkHelper.overlay(None, sourceWin, 2, 2)

def demoShowcase(root=None, border=True):
    splitter = ttk.TTkSplitter()
    root.layout().addWidget(splitter, 0, 0)

    logInput = ttk.TTkKeyPressView(visible=False, maxHeight=3, minHeight=3)
    root.layout().addWidget(logInput, 1, 0)

    # domTree = ttk.TTkFrame(title="Tom Inspector", border=True, visible=False, layout=ttk.TTkGridLayout())
    # ttk.TTkTomInspector(parent=domTree)
    # root.layout().addWidget(domTree, 0, 1)

    leftFrame   = ttk.TTkFrame(parent=splitter, layout=ttk.TTkGridLayout(), border=False)

    themesFrame = ttk.TTkFrame(title="Theme", border=True, layout=ttk.TTkVBoxLayout(), maxHeight=5, minHeight=5)
    listMenu = ttk.TTkList(maxWidth=30, minWidth=10)
    logInputToggler = ttk.TTkCheckbox(text='ShowInput')
    logInputToggler.stateChanged.connect(lambda x: logInput.setVisible(x==ttk.TTkK.Checked))
    tomTreeToggler = ttk.TTkCheckbox(text='Tom View', enabled=False)
    # tomTreeToggler.stateChanged.connect(lambda x: domTree.setVisible(x==ttk.TTkK.Checked))
    mouseToggler = ttk.TTkCheckbox(text='Mouse 🐀', checked=True)
    mouseToggler.stateChanged.connect(lambda x: ttk.TTkTerm.push(ttk.TTkTerm.Mouse.ON if x==ttk.TTkK.Checked else ttk.TTkTerm.Mouse.OFF))
    quitButton = ttk.TTkButton(text="Quit", border=True, maxHeight=3)
    quitButton.clicked.connect(ttk.TTkHelper.quit)

    leftFrame.layout().addWidget(themesFrame,     0, 0)
    leftFrame.layout().addWidget(listMenu,        1, 0)
    leftFrame.layout().addWidget(mouseToggler,    2, 0)
    leftFrame.layout().addWidget(tomTreeToggler,  3, 0)
    leftFrame.layout().addWidget(logInputToggler, 4, 0)
    leftFrame.layout().addWidget(quitButton,      5, 0)

    mainFrame = ttk.TTkFrame(parent=splitter, layout=ttk.TTkGridLayout(), border=False)

    # Set the size of the left column (quite useless but required by my OCD)
    splitter.setSizes([15,root.width()-11])

    # Themes
    themesFrame.layout().addWidget(r1 := ttk.TTkRadioButton(text="ASCII", radiogroup="theme"))
    themesFrame.layout().addWidget(r2 := ttk.TTkRadioButton(text="UTF-8", radiogroup="theme", checked=True))
    themesFrame.layout().addWidget(r3 := ttk.TTkRadioButton(text="Nerd",  radiogroup="theme"))

    r1.clicked.connect( lambda : ttk.TTkTheme.loadTheme(ttk.TTkTheme.ASCII))
    r2.clicked.connect( lambda : ttk.TTkTheme.loadTheme(ttk.TTkTheme.UTF8 ))
    r3.clicked.connect( lambda : ttk.TTkTheme.loadTheme(ttk.TTkTheme.NERD ))

    # Menu

    listMenu.addItem(f"Test")
    tabTest = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabTest.addTab(ttk.TTkLogViewer(), " LogViewer ")
    tabTest.addTab(ttk.TTkTestWidgetSizes(border=True, title="Frame1.1"), " Label 1.1 ")
    tabTest.addTab(ttk.TTkTestWidget(border=True, title="Frame1.2"), " Label Test 1.2 ")

    listMenu.addItem(f"Layouts")
    tabLayouts = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabLayouts.addTab(demoLayout(),      " Layout Test ",        'showcase/layout_basic.py')
    tabLayouts.addTab(demoLayoutNested()," Nested Layout Test ", 'showcase/layout_nested.py')
    tabLayouts.addTab(demoLayoutSpan(),  " Layout Span Test ",   'showcase/layout_span.py')
    tabLayouts.addTab(demoSplitter(),    " Splitter Test ",      'showcase/splitter.py')
    tabLayouts.addTab(demoAppTemplate(), " App Template ",       'showcase/apptemplate.py')
    tabLayouts.addMenu("sources", ttk.TTkK.RIGHT, tabLayouts).menuButtonClicked.connect(lambda _menuButton : showSource(_menuButton.data().currentData()))

    listMenu.addItem(f"MenuBar")
    tabMenuBar = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabMenuBar.addTab(demoMenuBar(),     " MenuBar Test ", 'showcase/menubar.py')
    tabMenuBar.addMenu("sources", ttk.TTkK.RIGHT, tabMenuBar).menuButtonClicked.connect(lambda _menuButton : showSource(_menuButton.data().currentData()))

    listMenu.addItem(f"Widgets")
    tabWidgets = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabWidgets.addTab(demoFormWidgets(), " Form Test ", 'showcase/formwidgets02.py')
    tabWidgets.addTab(demoTextEdit(),    " Text Edit ", 'showcase/textedit.py')
    tabWidgets.addTab(demoList(),        " List Test ", 'showcase/list.py')
    tabWidgets.addTab(demoTree(),        " Tree Test",  'showcase/tree.py')
    tabWidgets.addTab(demoTTkTable(),    " Table Test", 'showcase/table.py')
    tabWidgets.addTab(demoTab(),         " Tab Test ",  'showcase/tab.py')
    tabWidgets.addTab(demoFancyTable(),  " Old Table ", 'showcase/fancytable.py')
    tabWidgets.addTab(demoFancyTree(),   " Old Tree ",  'showcase/fancytree.py')
    tabWidgets.addMenu("sources", ttk.TTkK.RIGHT, tabWidgets).menuButtonClicked.connect(lambda _menuButton : showSource(_menuButton.data().currentData()))

    listMenu.addItem(f"Pickers")
    tabPickers = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabPickers.addTab(demoFilePicker(),  " File Picker ",  'showcase/filepicker.py')
    tabPickers.addTab(demoColorPicker(), " Color Picker ", 'showcase/colorpicker.py')
    tabPickers.addTab(demoTextPicker(), " Text Picker ",  'showcase/textpicker.py')
    tabPickers.addMenu("sources", ttk.TTkK.RIGHT, tabPickers).menuButtonClicked.connect(lambda _menuButton : showSource(_menuButton.data().currentData()))

    listMenu.addItem(f"Graphs")
    tabGraphs = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabGraphs.addTab(demoGraph(),       " Graph Test ", 'showcase/graph.py')
    tabGraphs.addMenu("sources", ttk.TTkK.RIGHT, tabGraphs).menuButtonClicked.connect(lambda _menuButton : showSource(_menuButton.data().currentData()))

    listMenu.addItem(f"Windows")
    tabWindows = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabWindows.addTab(demoWindows(),     " Windows Test ",  'showcase/windows.py')
    tabWindows.addTab(demoWindowsFlags()," Windows Flags ", 'showcase/windowsflags.py')
    tabWindows.addMenu("sources", ttk.TTkK.RIGHT, tabWindows).menuButtonClicked.connect(lambda _menuButton : showSource(_menuButton.data().currentData()))

    listMenu.addItem(f"Extra")
    tabArea = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabArea.addTab(demoScrollArea01()," Scroll Area 1 ", 'showcase/scrollarea01.py')
    tabArea.addTab(demoScrollArea02()," Scroll Area 2 ", 'showcase/scrollarea02.py')
    tabArea.addTab(demoDnD(),         " Drag'n Drop ",   'showcase/dragndrop.py')
    tabArea.addTab(demoDnDTabs(),     " D'n D Tabs ",    'showcase/dndtabs.py')
    tabArea.addTab(demoSigmask(),     " Sigmask ",       'showcase/sigmask.py')
    tabArea.addMenu("sources", ttk.TTkK.RIGHT, tabArea).menuButtonClicked.connect(lambda _menuButton : showSource(_menuButton.data().currentData()))

    @ttk.pyTTkSlot(str)
    def _listCallback(label):
        widget = None
        if   label == "Test":    widget = tabTest
        elif label == "Layouts": widget = tabLayouts
        elif label == "MenuBar": widget = tabMenuBar
        elif label == "Widgets": widget = tabWidgets
        elif label == "Pickers": widget = tabPickers
        elif label == "Graphs":  widget = tabGraphs
        elif label == "Windows": widget = tabWindows
        elif label == "Extra":   widget = tabArea
        if widget:
            if _listCallback.active:
                _listCallback.active.hide()
            widget.show()
            _listCallback.active = widget
    _listCallback.active = None

    listMenu.textClicked.connect(_listCallback)

    listMenu.setCurrentRow(6)

    return splitter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    parser.add_argument('-t', help='Track Mouse', action='store_true')
    args = parser.parse_args()
    windowed = args.w
    mouseTrack = args.t

    root = ttk.TTk(title="pyTermTk Demo", mouseTrack=mouseTrack)
    if windowed:
        winTabbed1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(120,40), title="pyTermTk Showcase", border=True, layout=ttk.TTkGridLayout(), flags=ttk.TTkK.NONE)
        border = True
    else:
        root.setLayout(ttk.TTkGridLayout())
        winTabbed1 = root
        border = False

    demoShowcase(winTabbed1, border)

    root.mainloop()

if __name__ == "__main__":
    main()
