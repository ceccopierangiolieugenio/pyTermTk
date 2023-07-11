# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import TermTk as ttk
from TermTk.TTkCore.canvas import TTkCanvas

from .superobj.superwidgetmenubutton import SuperWidgetMenuButton


class _MenuItem(ttk.TTkWidget):
    ''' Generic Control Button for the MenuEditor

        [Menu[+][x]

    '''
    __slots__ = ('_text', '_lineEdit', '_autoResize', '_menuButton', '_superMenuButton', '_designer',
                 # Signals
                 'closeClicked')
    def __init__(self, menuButton, designer, autoResize=True, *args, **kwargs):
        self._text = ttk.TTkString(menuButton.text())
        self._menuButton = menuButton
        self._autoResize = autoResize
        self._designer = designer
        self._superMenuButton = SuperWidgetMenuButton.factoryGetSuperWidgetMenuButton(wid=menuButton, designer=self._designer)
        self.closeClicked  = ttk.pyTTkSignal(_MenuItem)
        super().__init__(*args, **(kwargs|{'size':(self._text.termWidth()+7,1)}))
        self.processWidgetName(self._menuButton.name())
        self._lineEdit = ttk.TTkLineEdit(parent=self, visible=False, text=self._text)
        self._lineEdit.returnPressed.connect(self._lineEdit.hide)
        self._lineEdit.textEdited.connect(self._textEdited)
        self._lineEdit.focusChanged.connect(self._lineEdit.setVisible)

    def processWidgetName(self, name):
        names = {w.name() for w in self._designer.getWidgets() if w is not self._menuButton}
        index = 1
        className = name
        while className in names:
            className = f"{name}-{index}"
            index += 1
        self._menuButton.setName(className)

    @ttk.pyTTkSlot(str)
    def _textEdited(self, text):
        self._text = text
        self._menuButton.setText(text)
        width = text.termWidth()
        if self._autoResize:
            self.resize(width+7,1)
            self._lineEdit.setGeometry(1,0,width,1)
        self.processWidgetName(f"menu_{text}")
        self._designer.weModified.emit()
        self.update()

    def mouseDoubleClickEvent(self, evt) -> bool:
        w,h = self.size()
        if evt.x <= w-7:
            self._lineEdit.setText(self._text)
            self._lineEdit.setGeometry(1,0,w-7,1)
            self._lineEdit.show()
            self._lineEdit.setFocus()
        return True

    def expandMenuItem(self):
        subMenuEditor = _SubMenuEditor(size=(20,10), menuButton=self._menuButton, designer=self._designer)
        subMenuEditor.itemsChanged.connect(self.update)
        wi = subMenuEditor.widgetItem()
        wi.setLayer(wi.LAYER1)
        w = self.width()
        ttk.TTkHelper.overlay(self, subMenuEditor, w-3, 0)

    def mouseReleaseEvent(self, evt) -> bool:
        w = self.width()
        if evt.x > w-4:
            self.closeClicked.emit(self)
        elif evt.x > w-7:
            self.expandMenuItem()
        else:
            self._designer.thingSelected.emit(self._menuButton,self._superMenuButton)
        return True

    def paintEvent(self, canvas: TTkCanvas):
        w = self.width()
        text = (
                ttk.TTkString( "[",        ttk.TTkColor.fg("#FFFF66"))+
                ttk.TTkString( self._text, ttk.TTkColor.RST))
        canvas.drawText(text=text)
        expandIcon = ">" if len(self._menuButton._submenu)> 0 else "+"
        text = (
                ttk.TTkString( "[",        ttk.TTkColor.fg("#AAAA44"))+
                ttk.TTkString( expandIcon, ttk.TTkColor.fg("#00FF00"))+
                ttk.TTkString( "][",       ttk.TTkColor.fg("#AAAA44"))+
                ttk.TTkString( "x",        ttk.TTkColor.fg("#FF0000"))+
                ttk.TTkString( "]",        ttk.TTkColor.fg("#FFFF66")))
        canvas.drawText(text=text, pos=(w-6,0))


class _SubMenuSpacer(ttk.TTkWidget):
    ''' Generic Control Splitter for the MenuEditor

        ---------[x]

    '''
    __slots__ = ('closeClicked', '_menuButton')
    def __init__(self, menuSpacer, *args, **kwargs):
        self._menuButton = menuSpacer
        self.closeClicked  = ttk.pyTTkSignal(_MenuItem)
        super().__init__(*args, **kwargs)

    def mouseReleaseEvent(self, evt) -> bool:
        w = self.width()
        if evt.x > w-4:
            self.closeClicked.emit(self)
        return True

    def paintEvent(self, canvas):
        w = self.width()
        canvas.drawText(pos=(0,0), text="-"*self.width())
        text = (
                ttk.TTkString( "[",       ttk.TTkColor.fg("#AAAA44"))+
                ttk.TTkString( "x",        ttk.TTkColor.fg("#FF0000"))+
                ttk.TTkString( "]",        ttk.TTkColor.fg("#FFFF66")))
        canvas.drawText(text=text, pos=(w-3,0))


class _SubMenuAreaWidget(ttk.TTkAbstractScrollView):
    '''
        ┌────────┤Left├────────╥────────
        │╿+╿[menu[>]┌──────────────────┐
        │╽+╽<XXXXXXX│[menu1      [+][x]│
        └───────────│[menu2      [+][x]│
        ════════════│---------------[x]│
                    │[menu3      [+][x]│
        ────────────│[menu4      [+][x]│
                    │[    Add Menu    ]│
        ────────────│[   Add Spacer   ]│
        ────────────│                  │
                    └──────────────────┘
    '''
    __slots__ = ('_items', '_menuButton', '_minWith',
                 '_btnAddSpacer', '_btnAddMenu', '_designer',
                 #Signals
                 'itemsChanged')
    def __init__(self, menuButton, designer, **kwargs):
        self.itemsChanged = ttk.pyTTkSignal(list)
        self._items = []
        self._designer = designer
        self._menuButton = menuButton
        self._minWidth = 0
        self._btnAddSpacer = ttk.TTkButton(text="Add Spacer")
        self._btnAddMenu   = ttk.TTkButton(text="Add Menu")
        super().__init__(**kwargs)
        self.layout().addWidget(self._btnAddSpacer)
        self.layout().addWidget(self._btnAddMenu  )
        self.setFocusPolicy(ttk.TTkK.ClickFocus + ttk.TTkK.TabFocus)
        self.viewChanged.connect(self._viewChangedHandler)
        self._btnAddSpacer.clicked.connect(self.addSpacer)
        self._btnAddMenu.clicked.connect(self.addMenu)
        for item in self._menuButton._submenu:
            self._importMenuItem(item)

    def close(self):
        self.itemsChanged.clear()
        return super().close()

    def _resizeEvent(self):
        w,h = self.size()
        w = max(w,self._minWidth)
        for i,wid in enumerate(self._items):
            wid.setGeometry(0,i,w,1)
        yy = len(self._items)
        self._btnAddMenu.setGeometry(  0, yy,   w, 1)
        self._btnAddSpacer.setGeometry(0, yy+1, w, 1)

    def resizeEvent(self, w, h):
        self._resizeEvent()

    def _importMenuItem(self,item):
        if issubclass(type(item),ttk.TTkMenuButton):
            item = _MenuItem(menuButton=item, autoResize=True, designer=self._designer)
        else:
            item = _SubMenuSpacer(menuSpacer=item)
        self._items.append(item)
        self._addMenuItem(item)

    @ttk.pyTTkSlot(_MenuItem)
    def removeMenuItem(self, item):
        self._items.pop(self._items.index(item))
        self.layout().removeWidget(item)
        self._menuButton.removeMenuItem(item._menuButton)
        item.closeClicked.disconnect(self.removeMenuItem)
        self._resizeEvent()
        self.itemsChanged.emit(self._items)
        self._designer.weModified.emit()

    def _addMenuItem(self, item):
        item.closeClicked.clear()
        item.closeClicked.connect(self.removeMenuItem)
        self.layout().addWidget(item)
        self._minWidth = max(self._minWidth,item.minimumWidth())
        self._resizeEvent()
        self.itemsChanged.emit(self._items)
        self._designer.weModified.emit()

    def addMenuItem(self, item):
        self._items.append(item)
        self._addMenuItem(item)

    @ttk.pyTTkSlot()
    def addMenu(self):
        mb = self._menuButton.addMenu(text="menu")
        mb.setName("menuButton")
        self.addMenuItem(_MenuItem(menuButton=mb, autoResize=False, designer=self._designer))

    @ttk.pyTTkSlot()
    def addSpacer(self):
        self._menuButton.addSpacer()
        ms = self._menuButton._submenu[-1]
        self.addMenuItem(_SubMenuSpacer(menuSpacer=ms))

    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewFullAreaSize(self) -> tuple:
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w , h

    def viewDisplayedSize(self) -> tuple:
        return self.size()

    def maximumWidth(self):   return 0x10000
    def maximumHeight(self):  return 0x10000
    def minimumWidth(self):   return 0
    def minimumHeight(self):  return 0


class _SubMenuEditor(ttk.TTkResizableFrame):
    __slots__ = ('_scrollView'
                 # Forwarded Signals
                 'itemsChanged')
    def __init__(self, menuButton, designer, **kwargs):
        super().__init__(**kwargs|{'layout':ttk.TTkGridLayout()})
        sa = ttk.TTkScrollArea(parent=self)
        self._scrollView = _SubMenuAreaWidget(menuButton=menuButton, designer=designer)
        sa.setViewport(self._scrollView)

        self.itemsChanged = self._scrollView.itemsChanged


class _MenuBarItemEditorView(ttk.TTkAbstractScrollView):
    '''
        ┌────────┤Left├────────╥──────┤Center├───────╥───────┤Right├───────┐
        │╿+╿[menu[+][x]        ║╿+╿                  ║╿+╿                  │
        │╽+╽                   ║╽+╽                  ║╽+╽                  │
        └──────────────────────╨─────────────────────╨─────────────────────┘
    '''
    __slots__ = ('_itemsLayout', '_items', '_designer')
    def __init__(self, itemsLayout, designer, *args, **kwargs):
        self._items = []
        self._itemsLayout = itemsLayout
        self._designer = designer
        super().__init__(*args, **kwargs)
        self.viewChanged.connect(self._viewChangedHandler)
        for item in self._itemsLayout.children():
            self._importMenuItem(item.widget())

    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewFullAreaSize(self) -> (int, int):
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w, h

    def viewDisplayedSize(self) -> (int, int):
        return self.size()

    def _importMenuItem(self,menuButton):
        item = _MenuItem(menuButton=menuButton, autoResize=True, designer=self._designer)
        self._items.append(item)
        self._addMenuItem(item)

    @ttk.pyTTkSlot(_MenuItem)
    def removeMenuItem(self, item:_MenuItem):
        item.sizeChanged.disconnect(self._refreshItems)
        item.closeClicked.disconnect(self.removeMenuItem)
        self._itemsLayout.removeWidget(item._menuButton)
        self.layout().removeWidget(item)
        self._items.pop(self._items.index(item))
        self._refreshItems()
        self._designer.weModified.emit()

    def _addMenuItem(self, item):
        item.sizeChanged.clear()
        item.closeClicked.clear()
        item.sizeChanged.connect(self._refreshItems)
        item.closeClicked.connect(self.removeMenuItem)
        self.layout().addWidget(item)
        self._refreshItems()
        self._designer.weModified.emit()

    @ttk.pyTTkSlot()
    def addMenuItem(self):
        button = ttk.TTkMenuButton(text="menu", name="menuButton")
        self._itemsLayout.addWidget(button)
        self._importMenuItem(button)

    def _refreshItems(self):
        x = 0
        for mi in self._items:
            w = mi.width()
            mi.move(x,0)
            x+=w
        _,__,w,h = self.layout().fullWidgetAreaGeometry()
        self.resize(w,h)


class _MenuItemEditor(ttk.TTkGridLayout):
    __slots__ = ('_addButton', '_scrollPart','_menuBarView')
    def __init__(self, itemsLayout, designer):
        super().__init__()
        self._addButton =ttk.TTkButton(text="+\n+",border=False, maxWidth=3, minWidth=3, minHeight=2, maxHeight=2)
        self._scrollPart = ttk.TTkAbstractScrollArea(
                verticalScrollBarPolicy   = ttk.TTkK.ScrollBarAlwaysOff ,
                horizontalScrollBarPolicy = ttk.TTkK.ScrollBarAlwaysOn  )
        self._menuBarView = _MenuBarItemEditorView(itemsLayout, designer=designer)
        self._scrollPart.setViewport(self._menuBarView)
        self.addWidget(self._addButton,0,0)
        self.addWidget(self._scrollPart,0,1)
        self._addButton.clicked.connect(self._menuBarView.addMenuItem)


class MenuBarEditor(ttk.TTkWindow):
    __slots__ = ('_editorMenuBar', '_frameOptions', '_widget', '_designer',
                 '_btnTop', '_btnBottom', '_cbTop', '_cbBottom',
                 '_itemsTop', '_itemsBottom', '_mbTop', '_mbBottom')
    def __init__(self, widget:ttk.TTkFrame, designer):
        self._widget = widget
        self._designer = designer
        ttk.TTkUiLoader.loadFile(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),"../tui/menuBarEditor.tui.json"),
            self)
        self._editorMenuBar        = self.getWidgetByName('EditorMenuBar')
        self._cbTop    = self.getWidgetByName('CbTop')
        self._cbBottom = self.getWidgetByName('CbBottom')
        self._btnTop    = self.getWidgetByName('BtnEditTop')
        self._btnBottom = self.getWidgetByName('BtnEditBottom')
        self._frameOptions = self.getWidgetByName("FrameOptions")

        self._btnTop.clicked.connect(   lambda : self._showEditor(ttk.TTkK.TOP))
        self._btnBottom.clicked.connect(lambda : self._showEditor(ttk.TTkK.BOTTOM))

        self._cbTop.clicked.connect(lambda en: self._enableMenuBar(en, ttk.TTkK.TOP))
        self._cbBottom.clicked.connect(lambda en: self._enableMenuBar(en, ttk.TTkK.BOTTOM))

        self._mbTop    = self._widget.menuBar(ttk.TTkK.TOP)
        self._mbBottom = self._widget.menuBar(ttk.TTkK.BOTTOM)

        if self._mbTop:
            self._cbTop.setChecked(True)
            self._btnTop.setEnabled(True)
        if self._mbBottom:
            self._cbBottom.setChecked(True)
            self._btnBottom.setEnabled(True)

        if self._mbTop:
            self._showEditor(ttk.TTkK.TOP)
        elif self._mbBottom:
            self._showEditor(ttk.TTkK.BOTTOM)

    def _enableMenuBar(self, enable, place):
        if enable:
            if place==ttk.TTkK.TOP:
                self._mbTop = mb = self._mbTop if self._mbTop else ttk.TTkMenuBarLayout()
            else:
                self._mbBottom = mb = self._mbBottom if self._mbBottom else ttk.TTkMenuBarLayout()
            self._widget.setMenuBar(mb, place)
        else:
            self._widget.setMenuBar(None, place)
        self._designer.weModified.emit()

    def _showEditor(self, place):
        if place==ttk.TTkK.TOP:
            self._btnTop.setChecked(True)
            self._btnBottom.setChecked(False)
            self.setTitle("MenuBar Editor (TOP)")
            mb = self._mbTop if self._mbTop else ttk.TTkMenuBarLayout()
        else:
            self._btnTop.setChecked(False)
            self._btnBottom.setChecked(True)
            self.setTitle("MenuBar Editor (BOTTOM)")
            mb = self._mbBottom if self._mbBottom else ttk.TTkMenuBarLayout()

        meL = _MenuItemEditor(mb._mbItems(ttk.TTkK.LEFT_ALIGN),   designer=self._designer)
        meC = _MenuItemEditor(mb._mbItems(ttk.TTkK.CENTER_ALIGN), designer=self._designer)
        meR = _MenuItemEditor(mb._mbItems(ttk.TTkK.RIGHT_ALIGN),  designer=self._designer)

        self._editorMenuBar.replaceItem(0,meL,title="Left")
        self._editorMenuBar.replaceItem(1,meC,title="Center")
        self._editorMenuBar.replaceItem(2,meR,title="Right")


    @staticmethod
    def spawnMenuBarEditor(designer):
        def _spawnMenuBarEditor(widget):
            menuBarEditor = MenuBarEditor(widget=widget, designer=designer)
            ttk.TTkHelper.overlay(None, menuBarEditor, 10, 5, toolWindow=True)
        return _spawnMenuBarEditor
