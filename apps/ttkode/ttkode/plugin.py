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

__all__ = ['TTkodePlugin', 'TTkodePluginActivity']

from dataclasses import dataclass
from typing import Callable, List, Optional, Union
from enum import Enum

import TermTk as ttk

class TTkodePlugin():
    instances: List = []
    def __init__(
            self,
            name   : str,
            init   : Optional[Callable[[],None]] = None,
            apply  : Optional[Callable[[],None]] = None,
            run    : Optional[Callable[[],None]] = None ):
        self.name = name
        self.init = init
        self.apply = apply
        self.run = run
        self.instances.append(self)

class TTkodePluginActivity(TTkodePlugin):
    def __init__(
            self,
            activityName: str,
            widget: ttk.TTkWidget,
            icon:ttk.TTkString,
            **kwargs):
        self.activityName = activityName
        self.widget = widget
        self.icon = icon
        super().__init__(**kwargs)
