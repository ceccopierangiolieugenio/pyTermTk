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

__all__ = ['TTkUiProperties']

from TermTk.TTkLayouts import *
from TermTk.TTkWidgets import *

# from .properties.about import
from .properties.button import *
from .properties.checkbox import *
from .properties.combobox import *
from .properties.container import *
from .properties.frame import *
# from .properties.graph import
# from .properties.image import
from .properties.label import *
from .properties.lineedit import *
from .properties.list_ import *
# from .properties.listwidget import
# from .properties.menubar import
from .properties.menu import *
# from .properties.progressbar import
from .properties.radiobutton import *
from .properties.resizableframe import *
# from .properties.scrollarea import
from .properties.scrollbar import *
from .properties.slider import *
# from .properties.spacer import
from .properties.spinbox import *
from .properties.splitter import *
# from .properties.tabwidget import
from .properties.texedit import *
from .properties.widget import *
from .properties.window import *

from .properties.table import *
from .properties.tree import *
from .properties.filetree import *
# from .properties.terminal import *

# Pickers
from .properties.colorpicker import *
from .properties.filepicker import *

# Layouts
from .properties.layout import *

TTkUiProperties = {
    # Widgets
        TTkButton.__name__         : TTkButtonProperties,
        TTkCheckbox.__name__       : TTkCheckboxProperties,
        TTkContainer.__name__      : TTkContainerProperties,
        TTkComboBox.__name__       : TTkComboBoxProperties,
        TTkFrame.__name__          : TTkFrameProperties,
        TTkLabel.__name__          : TTkLabelProperties,
        TTkLineEdit.__name__       : TTkLineEditProperties,
        TTkList.__name__           : TTkListProperties,
        TTkMenuButton.__name__     : TTkMenuButtonProperties,
        TTkRadioButton.__name__    : TTkRadioButtonProperties,
        TTkResizableFrame.__name__ : TTkResizableFrameProperties,
        TTkScrollBar.__name__      : TTkScrollBarProperties,
        TTkSpinBox.__name__        : TTkSpinBoxProperties,
        TTkSplitter.__name__       : TTkSplitterProperties,
        TTkTextEdit.__name__       : TTkTextEditProperties,
        TTkWidget.__name__         : TTkWidgetProperties,
        TTkWindow.__name__         : TTkWindowProperties,
    # Pickers
        TTkColorButtonPicker.__name__ : TTkColorButtonPickerProperties,
        TTkFileButtonPicker.__name__  : TTkFileButtonPickerProperties,
    # Layouts
        TTkLayout.__name__   : TTkLayoutProperties,
    # Models
        TTkTable.__name__    : TTkTableProperties,
        TTkTree.__name__     : TTkTreeProperties,
        TTkFileTree.__name__ : TTkFileTreeProperties,
}
