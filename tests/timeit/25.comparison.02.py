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

import timeit, pickle

lll = ('ab','cd')

def test1():  return      'ab' in     ('ab','cd') ,     'ab' in     ('ab','cd') ,     'ab' in     ('ab','cd') ,     'ab' in     ('ab','cd') ,     'ab' in     ('ab','cd') ,     'ab' in     ('ab','cd') ,     'ab' in     ('ab','cd') ,     'ab' in     ('ab','cd') ,     'ab' in     ('ab','cd') ,     'ab' in     ('ab','cd')
def test2():  return  not 'ab' in     ('ab','cd') , not 'ab' in     ('ab','cd') , not 'ab' in     ('ab','cd') , not 'ab' in     ('ab','cd') , not 'ab' in     ('ab','cd') , not 'ab' in     ('ab','cd') , not 'ab' in     ('ab','cd') , not 'ab' in     ('ab','cd') , not 'ab' in     ('ab','cd') , not 'ab' in     ('ab','cd')
def test3():  return      'ab' not in ('ab','cd') ,     'ab' not in ('ab','cd') ,     'ab' not in ('ab','cd') ,     'ab' not in ('ab','cd') ,     'ab' not in ('ab','cd') ,     'ab' not in ('ab','cd') ,     'ab' not in ('ab','cd') ,     'ab' not in ('ab','cd') ,     'ab' not in ('ab','cd') ,     'ab' not in ('ab','cd')
def test4():  return      'az' in     ('ab','cd') ,     'az' in     ('ab','cd') ,     'az' in     ('ab','cd') ,     'az' in     ('ab','cd') ,     'az' in     ('ab','cd') ,     'az' in     ('ab','cd') ,     'az' in     ('ab','cd') ,     'az' in     ('ab','cd') ,     'az' in     ('ab','cd') ,     'az' in     ('ab','cd')
def test5():  return  not 'az' in     ('ab','cd') , not 'az' in     ('ab','cd') , not 'az' in     ('ab','cd') , not 'az' in     ('ab','cd') , not 'az' in     ('ab','cd') , not 'az' in     ('ab','cd') , not 'az' in     ('ab','cd') , not 'az' in     ('ab','cd') , not 'az' in     ('ab','cd') , not 'az' in     ('ab','cd')
def test6():  return      'az' not in ('ab','cd') ,     'az' not in ('ab','cd') ,     'az' not in ('ab','cd') ,     'az' not in ('ab','cd') ,     'az' not in ('ab','cd') ,     'az' not in ('ab','cd') ,     'az' not in ('ab','cd') ,     'az' not in ('ab','cd') ,     'az' not in ('ab','cd') ,     'az' not in ('ab','cd')
def test7():  return      'ab' in     lll         ,     'ab' in     lll         ,     'ab' in     lll         ,     'ab' in     lll         ,     'ab' in     lll         ,     'ab' in     lll         ,     'ab' in     lll         ,     'ab' in     lll         ,     'ab' in     lll         ,     'ab' in     lll
def test8():  return  not 'ab' in     lll         , not 'ab' in     lll         , not 'ab' in     lll         , not 'ab' in     lll         , not 'ab' in     lll         , not 'ab' in     lll         , not 'ab' in     lll         , not 'ab' in     lll         , not 'ab' in     lll         , not 'ab' in     lll
def test9():  return      'ab' not in lll         ,     'ab' not in lll         ,     'ab' not in lll         ,     'ab' not in lll         ,     'ab' not in lll         ,     'ab' not in lll         ,     'ab' not in lll         ,     'ab' not in lll         ,     'ab' not in lll         ,     'ab' not in lll
def test10(): return      'az' in     lll         ,     'az' in     lll         ,     'az' in     lll         ,     'az' in     lll         ,     'az' in     lll         ,     'az' in     lll         ,     'az' in     lll         ,     'az' in     lll         ,     'az' in     lll         ,     'az' in     lll
def test11(): return  not 'az' in     lll         , not 'az' in     lll         , not 'az' in     lll         , not 'az' in     lll         , not 'az' in     lll         , not 'az' in     lll         , not 'az' in     lll         , not 'az' in     lll         , not 'az' in     lll         , not 'az' in     lll
def test12(): return      'az' not in lll         ,     'az' not in lll         ,     'az' not in lll         ,     'az' not in lll         ,     'az' not in lll         ,     'az' not in lll         ,     'az' not in lll         ,     'az' not in lll         ,     'az' not in lll         ,     'az' not in lll


loop = 500000

a = {}

iii = 1
while (testName := f'test{iii}') and (testName in globals()):
    result = timeit.timeit(f'{testName}(*a)', globals=globals(), number=loop)
    # print(f"test{iii}) fps {loop / result :.3f} - s {result / loop:.10f} - {result / loop} {globals()[testName](*a)}")
    print(f"test{iii:02}) | {result / loop:.10f} sec. | {loop / result : 15.3f} Fps ╞╡-> {globals()[testName](*a)}")
    iii+=1
