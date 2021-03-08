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

import TermTk as ttk

ttk.TTkLog.use_default_stdout_logging()

    # define 2 signals with different signatures
signal = ttk.pyTTkSignal()
otherSignal = ttk.pyTTkSignal(int)


    # Define a slot with no input as signature
@ttk.pyTTkSlot()
def slot():
    ttk.TTkLog.debug("Received a simple signal")

    # Define 2 slots with "int" as input signature
@ttk.pyTTkSlot(int)
def otherSlot(val):
    ttk.TTkLog.debug(f"[otherSlot] Received a valued signal, val:{val}")

@ttk.pyTTkSlot(int)
def anotherSlot(val):
    ttk.TTkLog.debug(f"[anootherSlot] Received a valued signal, val:{val}")


    # connect the signals to the proper slot
signal.connect(slot)
otherSignal.connect(otherSlot)
otherSignal.connect(anotherSlot)

    # Test the signals
ttk.TTkLog.debug("Emit a simple signal")
signal.emit()
ttk.TTkLog.debug("Emit a valued signal")
otherSignal.emit(123)