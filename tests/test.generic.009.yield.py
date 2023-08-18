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

def yieldFunc1():
    for i in range(10):
        print(f"V {i}")
        yield f"{i=}"
        print(f"^ {i}")

for v in ( k:=yieldFunc1()):
    print(f"{v=} {k=}")
    for vv in k:
        print(f"{vv=}")
        break

print(f"----- {v=} {vv=}")

# Example adapted from:
#   https://www.pythonforbeginners.com/basics/create-generator-from-a-list-in-python
myList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
mygen = (i for i in myList)

for v in mygen:
    print(f"{v=} {k=}")
    for vv in mygen:
        print(f"{vv=}")
        break

print(f"----- {v=} {vv=}")

