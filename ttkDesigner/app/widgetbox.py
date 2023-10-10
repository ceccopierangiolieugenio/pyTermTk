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
        "Layout"       : { "class":ttk.TTkLayout    , "params":{'size':(30,10)}},
        "H Box Layout" : { "class":ttk.TTkHBoxLayout, "params":{'size':(30,10)}},
        "V Box Layout" : { "class":ttk.TTkVBoxLayout, "params":{'size':(30,10)}},
        "Grid Layout"  : { "class":ttk.TTkGridLayout, "params":{'size':(30,10)}},
        "Splitter"     : { "class":ttk.TTkSplitter  , "params":{'size':(40,10)}},
    },
    'Containers':{
        "Container"       : { "class":ttk.TTkContainer,      "params":{'size':(20,10)}},
        "Window"          : { "class":ttk.TTkWindow,         "params":{'size':(20,10)}},
        "Frame"           : { "class":ttk.TTkFrame,          "params":{'size':(20,5), 'border':True}},
        "Resizable Frame" : { "class":ttk.TTkResizableFrame, "params":{'size':(20,5)}},
   },
    'Buttons':{
        "Button"       : { "class":ttk.TTkButton,      "params":{'size':(20,3), 'text':'Button', 'border':True, }},
        "Button Slim"  : { "class":ttk.TTkButton,      "params":{'size':(20,1), 'text':'Button', 'border':False, }},
        "Checkbox"     : { "class":ttk.TTkCheckbox,    "params":{'size':(20,1), 'text':'Checkbox' }},
        "Radio Button" : { "class":ttk.TTkRadioButton, "params":{'size':(20,1), 'text':'Radio b.', 'radiogroup':'DefaultGroup' }},
    },
    'Input Widgets':{
        "ComboBox"    : { "class":ttk.TTkComboBox,  "params":{'size':(20,1)} },
        "LineEdit"    : { "class":ttk.TTkLineEdit,  "params":{'size':(20,1)} },
        "TextEdit"    : { "class":ttk.TTkTextEdit,  "params":{'size':(20,5), 'readOnly':False, 'multiline':True } },
        "TextEditLine": { "class":ttk.TTkTextEdit,  "params":{'size':(20,1), 'readOnly':False, 'multiLine':False, 'maxHeight':1 } },
        "SpinBox"     : { "class":ttk.TTkSpinBox,   "params":{'size':(20,1)} },
        "H ScrollBar" : { "class":ttk.TTkScrollBar, "params":{'size':(10,1), "orientation":ttk.TTkK.HORIZONTAL} },
        "V ScrollBar" : { "class":ttk.TTkScrollBar, "params":{'size':(1,5),  "orientation":ttk.TTkK.VERTICAL} },
    },
    'Widgets':{
        "Label"           : { "class":ttk.TTkLabel,          "params":{'size':(20,1), 'text':'Label'}},
        "List"            : { "class":ttk.TTkList,           "params":{'size':(20,5)}},
        # "List Widget"     : { "class":ttk.TTkListWidget,     "params":{'size':(20,5)}},
        "Scroll Area"     : { "class":ttk.TTkScrollArea,     "params":{'size':(20,5)}, "disabled": True},
        "Spacer"          : { "class":ttk.TTkSpacer,         "params":{'size':(10,5)}},
        "Tab Widget"      : { "class":ttk.TTkTabWidget,      "params":{'size':(20,3)}, "disabled": True},
        "Widget"          : { "class":ttk.TTkWidget,         "params":{'size':(20,5)}},
    },
    'Pickers':{
        "Color Picker"     : { "class":ttk.TTkColorButtonPicker, "params":{'size':( 6,3), 'border':True}},
        "File Picker"      : { "class":ttk.TTkFileButtonPicker,  "params":{'size':(20,3), 'border':True}},
        "Date Picker"      : { "class":ttk.TTkButton, "params":{'size':(20,3)}, "disabled": True},
        "TtkString Picker" : { "class":ttk.TTkButton, "params":{'size':(20,3)}, "disabled": True},
    },
    'Debug':{
        "Log Viewer"       : { "class":ttk.TTkLogViewer,       "params":{'size':(60,10)}},
        "Input View"       : { "class":ttk.TTkKeyPressView,    "params":{'size':(60,3)}},
        # "Tom Inspector"    : { "class":ttk.TTkTomInspector,    "params":{'size':(40,10)}, "disabled": True},
        "Test Widget"      : { "class":ttk.TTkTestWidgets,     "params":{'size':(40,10)}, "disabled": True},
        "Test Widget info" : { "class":ttk.TTkTestWidgetSizes, "params":{'size':(40,10)}},
    }
}

class DragDesignItem(ttk.TTkWidget):
    classStyle = {
                'default':     {'color': TTkColor.fg("#dddd88")+TTkColor.bg("#000044"),
                                'borderColor': TTkColor.RST,
                                'shadow': TTkColor.RST+TTkColor.bg('#444444')},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'borderColor': TTkColor.fg('#888888'),
                                'shadow': TTkColor.RST},
                'hover':       {'color': TTkColor.fg("#dddd00")+TTkColor.bg("#004488")+TTkColor.BOLD,
                                'borderColor': TTkColor.fg("#FFFF00")+TTkColor.bg("#000088")+TTkColor.BOLD,
                                'shadow': TTkColor.fg("#FFFF00")+TTkColor.bg('#444444')},
                'clicked':     {'color': TTkColor.fg("#FFFFDD")+TTkColor.BOLD,
                                'borderColor': TTkColor.fg("#DDDDDD")+TTkColor.BOLD,
                                'shadow':  TTkColor.fg("#DDDDDD")+TTkColor.bg('#444444')},
            }
    __slots__ = ('_itemName', '_widgetClass', '_designer')
    def __init__(self, itemName, widgetClass, designer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumHeight(3)
        self.setMinimumSize(max(15,len(itemName)+2),3)
        self._itemName = itemName
        self._widgetClass = widgetClass
        self._designer = designer
        self.setEnabled('disabled' not in widgetClass)

    def mouseDragEvent(self, evt) -> bool:
        ttk.TTkLog.debug(f"Start DnD -> {self._itemName}")
        wc = self._widgetClass

        # Gen unique name for the new widget
        basename = wc['class'].__name__
        name = basename
        index = 1
        names = {w.name() for w in self._designer.getWidgets()}
        while name in names:
            name = f"{basename}-{index}"
            index += 1

        drag = ttk.TTkDrag()
        data = wc['class'](**(wc['params']|{'name':name}))
        if issubclass(wc['class'], ttk.TTkWidget):
            drag.setPixmap(data)
        else:
            w,h = wc['params']['size']
            pm = ttk.TTkCanvas(width=w, height=h)
            pm.drawBox(pos=(0,0),size=(w,h), color=ttk.TTkColor.fg('#888888'))
            drag.setPixmap(pm)
        drag.setData(data)
        drag.exec()
        return True

    def paintEvent(self, canvas):
        style = self.currentStyle()

        textColor   = style['color']
        borderColor = style['borderColor']
        shadowColor = style['shadow']

        w,h = self.size()

        canvas.drawText(text=self._itemName, pos=(1,1), width=w-2, color=textColor)
        canvas.drawBox(pos=(0,0),size=self.size(), color=borderColor)

        # canvas.drawText(text=self._itemName, pos=(2,1), width=w-2, color=textColor)
        # txt = '▗' + ('▄'*(w-2)) + '▖'
        # canvas.drawText(text=txt, pos=(0,0), color=borderColor)
        # txt = '▝' + ('▀'*(w-2))
        # canvas.drawText(text=txt, pos=(0,2), color=shadowColor)
        # canvas.drawText(text='▐', pos=(0,  1), color=shadowColor)
        # canvas.drawText(text='▌', pos=(w-1,1), color=borderColor)
        # canvas.drawText(text='▘', pos=(w-1,2), color=borderColor)


class WidgetBox(ttk.TTkVBoxLayout):
    def __init__(self, designer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for tw in dWidgets:
            self.addWidget(ttk.TTkLabel(text=tw, color=ttk.TTkColor.fg('#FFFF88')+ttk.TTkColor.bg('#0000FF')))
            for ww in dWidgets[tw]:
                self.addWidget(DragDesignItem(ww, dWidgets[tw][ww], designer))
        # self.setGeometry(0,0,self.minimumWidth(), self.minimumHeight())

class WidgetBoxScrollArea(ttk.TTkScrollArea):
    def __init__(self, designer,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewport().setLayout(WidgetBox(designer))
