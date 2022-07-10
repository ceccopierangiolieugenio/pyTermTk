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

from cgitb import text
import sys, os, argparse
import re
import random

sys.path.append(os.path.join(sys.path[0],'../tmp'))
sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

from  showcase.layout_basic  import demoLayout
from  showcase.layout_nested import demoLayoutNested
from  showcase.layout_span   import demoLayoutSpan
from  showcase.tab           import demoTab
from  showcase.graph         import demoGraph
from  showcase.splitter      import demoSplitter
from  showcase.windows       import demoWindows
from  showcase.formwidgets   import demoFormWidgets
from  showcase.scrollarea    import demoScrollArea
from  showcase.list          import demoList
from  showcase.menubar       import demoMenuBar
from  showcase.filepicker    import demoFilePicker
from  showcase.colorpicker   import demoColorPicker
from  showcase.tree          import demoTree
from  showcase.fancytable    import demoFancyTable
from  showcase.fancytree     import demoFancyTree
from  showcase.textedit      import demoTextEdit
from  showcase.dragndrop     import demoDnD
from  showcase.dndtabs       import demoDnDTabs

words = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
def getWord():
    return random.choice(words)
def getSentence(a,b):
    return " ".join([getWord() for i in range(0,random.randint(a,b))])

def stupidPythonHighlighter(txt):
    def _colorize(regex, txt, color):
        ret = txt
        if m := txt.findall(regexp=regex):
            for match in m:
                ret = ret.setColor(color, match=match)
        return ret

    # Operators
    txt = _colorize(re.compile('[\+\*\/\=\-\<\>\!]'), txt, ttk.TTkColor.fg('#00AAAA'))
    # Bool
    txt = _colorize(re.compile('True|False'), txt, ttk.TTkColor.fg('#0000FF'))

    # Numbers
    txt = _colorize(re.compile('[0-9]'), txt, ttk.TTkColor.fg('#00FFFF'))

    # Functions
    txt = _colorize(re.compile('[ \t]*def[ \t]*'), txt, ttk.TTkColor.fg('#00FFFF'))
    txt = _colorize(re.compile('[^= \t\.\()]*[\t ]*\('), txt, ttk.TTkColor.fg('#AAAA00'))
    # Objects
    txt = _colorize(re.compile('[^= \t\.\()]*\.'), txt, ttk.TTkColor.fg('#44AA00'))

    # Fix Extra colors
    txt = _colorize(re.compile('[\(\)]'), txt, ttk.TTkColor.RST)
    txt = _colorize(re.compile("'[^']*'"), txt, ttk.TTkColor.fg('#FF8800'))

    # Strings
    txt = _colorize(re.compile('"[^"]*"'), txt, ttk.TTkColor.fg('#FF8800'))
    txt = _colorize(re.compile("'[^']*'"), txt, ttk.TTkColor.fg('#FF8800'))

    # Comments
    txt = _colorize(re.compile('#.*\n'), txt, ttk.TTkColor.fg('#00FF00'))
    return txt

def showSource(file):
    ttk.TTkLog.debug(f"Placeholder for the Sources - {file}")
    content = "Nothing"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),file)) as f:
        content = stupidPythonHighlighter( ttk.TTkString() + f.read() )
    sourceWin = ttk.TTkWindow(size=(100,40), title=file, layout=ttk.TTkGridLayout())
    texEdit = ttk.TTkTextEdit(parent=sourceWin)
    texEdit.setText(content)
    ttk.TTkHelper.overlay(None, sourceWin, 2, 2)

def demoShowcase(root=None, border=True, quit=None):
    splitter = ttk.TTkSplitter()
    root.layout().addWidget(splitter, 0, 0)

    logInput = ttk.TTkKeyPressView(visible=False, maxHeight=3, minHeight=3)
    root.layout().addWidget(logInput, 1, 0)

    leftFrame   = ttk.TTkFrame(parent=splitter, layout=ttk.TTkGridLayout(), border=False)

    themesFrame = ttk.TTkFrame(title="Theme", border=True, layout=ttk.TTkVBoxLayout(), maxHeight=5, minHeight=5)
    listMenu = ttk.TTkList(maxWidth=15, minWidth=10)
    logInputToggler = ttk.TTkCheckbox(text='ShowInput')
    logInputToggler.stateChanged.connect(lambda x: logInput.setVisible(x==ttk.TTkK.Checked))
    quitButton = ttk.TTkButton(text="Quit", border=True, maxHeight=3)
    quitButton.clicked.connect(quit)

    leftFrame.layout().addWidget(themesFrame, 0, 0)
    leftFrame.layout().addWidget(listMenu,    1, 0)
    leftFrame.layout().addWidget(logInputToggler,  2, 0)
    leftFrame.layout().addWidget(quitButton,  3, 0)

    mainFrame = ttk.TTkFrame(parent=splitter, layout=ttk.TTkGridLayout(), border=False)

    # Themes
    themesFrame.layout().addWidget(r1 := ttk.TTkRadioButton(text="ASCII", name="theme"))
    themesFrame.layout().addWidget(r2 := ttk.TTkRadioButton(text="UTF-8",name="theme", checked=True))
    themesFrame.layout().addWidget(r3 := ttk.TTkRadioButton(text="Nerd",name="theme"))

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
    tabLayouts.addTab(demoLayout(),      " Layout Test ")
    tabLayouts.addTab(demoLayoutNested()," Nested Layout Test ")
    tabLayouts.addTab(demoLayoutSpan(),  " Layout Span Test ")
    tabLayouts.addTab(demoSplitter(),    " Splitter Test ")
    tabLayoutsSources = [
        'showcase/layout_basic.py',
        'showcase/layout_nested.py',
        'showcase/layout_span.py',
        'showcase/splitter.py' ]
    tabLayouts.addMenu("sources", ttk.TTkK.RIGHT).menuButtonClicked.connect(lambda x : showSource(tabLayoutsSources[tabLayouts.currentIndex()]))

    listMenu.addItem(f"MenuBar")
    tabMenuBar = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabMenuBar.addTab(demoMenuBar(),     " MenuBar Test ")
    tabMenuBarSources = [ 'showcase/menubar.py' ]
    tabMenuBar.addMenu("sources", ttk.TTkK.RIGHT).menuButtonClicked.connect(lambda x : showSource(tabMenuBarSources[tabMenuBar.currentIndex()]))

    listMenu.addItem(f"Widgets")
    tabWidgets = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabWidgets.addTab(demoFormWidgets(), " Form Test ")
    tabWidgets.addTab(demoTextEdit(),    " Text Edit ")
    tabWidgets.addTab(demoList(),        " List Test ")
    tabWidgets.addTab(demoTree(),        " Tree Test")
    tabWidgets.addTab(demoTab(),         " Tab Test ")
    tabWidgets.addTab(demoFancyTable(),  " Old Table ")
    tabWidgets.addTab(demoFancyTree(),   " Old Tree ")
    tabWidgetsSources = [
        'showcase/formwidgets.py',
        'showcase/textedit.py',
        'showcase/list.py',
        'showcase/tree.py',
        'showcase/tab.py',
        'showcase/fancytable.py',
        'showcase/fancytree.py' ]
    tabWidgets.addMenu("sources", ttk.TTkK.RIGHT).menuButtonClicked.connect(lambda x : showSource(tabWidgetsSources[tabWidgets.currentIndex()]))

    listMenu.addItem(f"Pickers")
    tabPickers = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabPickers.addTab(demoFilePicker(),  " File Picker ")
    tabPickers.addTab(demoColorPicker(), " Color Picker ")
    tabPickersSources = [
        'showcase/filepicker.py',
        'showcase/colorpicker.py' ]
    tabPickers.addMenu("sources", ttk.TTkK.RIGHT).menuButtonClicked.connect(lambda x : showSource(tabPickersSources[tabPickers.currentIndex()]))

    listMenu.addItem(f"Graphs")
    tabGraphs = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabGraphs.addTab(demoGraph(),       " Graph Test ")
    tabGraphsSources = [ 'showcase/graph.py' ]
    tabGraphs.addMenu("sources", ttk.TTkK.RIGHT).menuButtonClicked.connect(lambda x : showSource(tabGraphsSources[tabGraphs.currentIndex()]))

    listMenu.addItem(f"Windows")
    tabWindows = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabWindows.addTab(demoWindows(),     " Windows Test ")
    tabWindowsSources = [ 'showcase/windows.py' ]
    tabWindows.addMenu("sources", ttk.TTkK.RIGHT).menuButtonClicked.connect(lambda x : showSource(tabWindowsSources[tabWindows.currentIndex()]))

    listMenu.addItem(f"Extra")
    tabArea = ttk.TTkTabWidget(parent=mainFrame, border=False, visible=False)
    tabArea.addTab(demoScrollArea(),  " Scroll Area ")
    tabArea.addTab(demoDnD(),         " Drag'n Drop ")
    tabArea.addTab(demoDnDTabs(),     " D'n D Tabs ")
    tabAreaSources = [
        'showcase/scrollarea.py',
        'showcase/dragndrop.py',
        'showcase/dndtabs.py' ]
    tabArea.addMenu("sources", ttk.TTkK.RIGHT).menuButtonClicked.connect(lambda x : showSource(tabAreaSources[tabArea.currentIndex()]))


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
    parser.add_argument('-f', help='Full Screen', action='store_true')
    args = parser.parse_args()

    ttk.TTkLog.use_default_file_logging()

    root = ttk.TTk(title="pyTermTk Demo")
    if args.f:
        root.setLayout(ttk.TTkGridLayout())
        winTabbed1 = root
        border = False
    else:
        winTabbed1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(120,40), title="pyTermTk Showcase", border=True, layout=ttk.TTkGridLayout())
        border = True

    demoShowcase(winTabbed1, border, root.quit)

    root.mainloop()

if __name__ == "__main__":
    main()

def test_demo():
    root = ttk.TTk()
    assert demoShowcase(root) != None
    root.quit()