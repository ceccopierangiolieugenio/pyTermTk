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

import TermTk as ttk

from .cfg  import *
from .about import *

dWidgets = {
    'Layouts':{
        "Layout"       : { "class":ttk.TTkLayout    , "params":{}},
        "H Box Layout" : { "class":ttk.TTkHBoxLayout, "params":{}},
        "V Box Layout" : { "class":ttk.TTkVBoxLayout, "params":{}},
        "Grid Layout"  : { "class":ttk.TTkGridLayout, "params":{}},
        "Splitter"     : { "class":ttk.TTkSplitter  , "params":{'size':(40,10)}},
    },
    'Buttons':{
        "Button"       : { "class":ttk.TTkButton,      "params":{'size':(20,3), 'text':'Button', 'border':True, }},
        "Button Slim"  : { "class":ttk.TTkButton,      "params":{'size':(20,1), 'text':'Button', 'border':False, }},
        "Checkbox"     : { "class":ttk.TTkCheckbox,    "params":{'size':(20,1), 'text':'Checkbox' }},
        "Radio Button" : { "class":ttk.TTkRadioButton, "params":{'size':(20,1), 'text':'Radio b.' }},
    },
    'Input Widgets':{
        "ComboBox"    : { "class":ttk.TTkComboBox,  "params":{'size':(20,1)} },
        "LineEdit"    : { "class":ttk.TTkLineEdit,  "params":{'size':(20,1)} },
        "TextEdit"    : { "class":ttk.TTkTextEdit,  "params":{'size':(20,5)} },
        "SpinBox"     : { "class":ttk.TTkSpinBox,   "params":{'size':(20,1)} },
        "H ScrollBar" : { "class":ttk.TTkScrollBar, "params":{'size':(10,1), "orientation":ttk.TTkK.HORIZONTAL} },
        "V ScrollBar" : { "class":ttk.TTkScrollBar, "params":{'size':(1,5),  "orientation":ttk.TTkK.VERTICAL} },
    },
    'Widgets':{
        "Label"           : { "class":ttk.TTkLabel,          "params":{'size':(20,1), 'text':'Label'}},
        "List"            : { "class":ttk.TTkListWidget,     "params":{'size':(20,1)}},
        "Scroll Area"     : { "class":ttk.TTkScrollArea,     "params":{'size':(20,5)}},
        "Spacer"          : { "class":ttk.TTkSpacer,         "params":{'size':(10,5)}},
        "Tab Widget"      : { "class":ttk.TTkTabWidget,      "params":{'size':(20,3)}},
        "Window"          : { "class":ttk.TTkWindow,         "params":{'size':(20,10)}},
        "Widget"          : { "class":ttk.TTkWidget,         "params":{'size':(20,5)}},
        "Frame"           : { "class":ttk.TTkFrame,          "params":{'size':(20,5), 'border':True}},
        "Resizable Frame" : { "class":ttk.TTkResizableFrame, "params":{'size':(20,5)}},
    },
    'Debug':{
        "Log Viewer"       : { "class":ttk.TTkLogViewer,       "params":{'size':(60,10)}},
        "Input View"       : { "class":ttk.TTkKeyPressView,    "params":{'size':(60,3)}},
        "Tom Inspector"    : { "class":ttk.TTkTomInspector,    "params":{'size':(40,10)}},
        # "Test Widget"      : { "class":ttk.TTkTestWidgets,     "params":{'size':(40,10)}},
        "Test Widget info" : { "class":ttk.TTkTestWidgetSizes, "params":{'size':(40,10)}},
    }
}

class DragDesignItem(ttk.TTkWidget):
    _objNames = {}
    def __init__(self, itemName, widgetClass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumHeight(3)
        self.setMinimumSize(max(15,len(itemName)+2),3)
        self._itemName = itemName
        self._widgetClass = widgetClass

    def mouseDragEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Start DnD -> {self._itemName}")
        wc = self._widgetClass
        name = wc['class'].__name__
        if not name in DragDesignItem._objNames:
            DragDesignItem._objNames[name] = 1
        else:
            DragDesignItem._objNames[name] += 1
        name = f"{name}-{DragDesignItem._objNames[name]}"
        drag = ttk.TTkDrag()
        data = wc['class'](**(wc['params']|{'name':name}))
        drag.setPixmap(data)
        drag.setData(data)
        drag.exec()
        return True

    def paintEvent(self):
        self._canvas.drawText(text=self._itemName, pos=(1,1))
        self._canvas.drawBox(pos=(0,0),size=self.size())

class WidgetBox(ttk.TTkVBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for tw in dWidgets:
            self.addWidget(ttk.TTkLabel(text=tw, color=ttk.TTkColor.fg('#FFFF88')+ttk.TTkColor.bg('#0000FF')))
            for ww in dWidgets[tw]:
                self.addWidget(DragDesignItem(ww, dWidgets[tw][ww]))
        # self.setGeometry(0,0,self.minimumWidth(), self.minimumHeight())

class WidgetBoxScrollArea(ttk.TTkScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewport().setLayout(WidgetBox())
