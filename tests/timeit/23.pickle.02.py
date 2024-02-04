#!/usr/bin/env python3

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

import sys,os,io
import pickle

import timeit
import random


sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class MyPickler(pickle.Pickler):
    def reducer_override(self, obj):
        """Custom reducer for MyClass."""
        if issubclass(type(obj),ttk.TTkColor):
            return type, (obj.__class__.__name__, obj.__class__.__bases__,
                          {'_buffer': obj._buffer,
                           '_fg':obj._fg,
                           '_bg':obj._bg,
                           '_mod':obj._mod,
                           '_link':obj._link,
                           '_clean':obj._clean,
                           '_colorMod':obj._colorMod })
        else:
            return NotImplemented

f = io.BytesIO()
p = MyPickler(f)

# canvas = ttk.TTkCanvas(width=500,height=200)
# cp = ttk.TTkColorDialogPicker(size=(500,200),title="Test Color Picker")
cp = ttk.TTkWidgets.TTkPickers.colorpicker._TTkColorCanvas(size=(500,200))
canvas = cp.getCanvas()
cp.paintEvent(canvas)
cp.paintChildCanvas()
picklestring = pickle.dumps(canvas)

def test1():
    return len(pickle.dumps(canvas))

def test2():
    return len(pickle.dumps(canvas.serialize()))

def test3():
    p.dump(canvas)
    return len(f.getvalue())

def test4():
    c = pickle.loads(picklestring)
    return c._width * c._height


loop = 50

a = {}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1

