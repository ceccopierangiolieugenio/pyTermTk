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

import timeit

bigString1 = "abc"*10000+"a"
bigString2 = bigString1
bigString3 = "abc"*10000+"a"
bigString4 = "abc"*10000+"b"
bigString5 = "abc"*10000+"bc"

# print(bigString1)

def test1():  return (bigString1==bigString1,bigString1==bigString1,bigString1==bigString1,bigString1==bigString1)
def test2():  return (bigString1==bigString2,bigString1==bigString2,bigString1==bigString2,bigString1==bigString2)
def test3():  return (bigString1==bigString3,bigString1==bigString3,bigString1==bigString3,bigString1==bigString3)
def test4():  return (bigString1==bigString4,bigString1==bigString4,bigString1==bigString4,bigString1==bigString4)
def test5():  return (bigString1==bigString5,bigString1==bigString5,bigString1==bigString5,bigString1==bigString5)


loop = 100000

a = {}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1
