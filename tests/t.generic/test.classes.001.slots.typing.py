#!/usr/bin/env python3
# vim:ts=4:sw=4:fdm=indent:cc=79:

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
import os,sys
from typing import get_type_hints
import inspect

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class A():
    __slots__ = ('a','b','c')
    def __init__(self,a,b,c) -> None:
        self.a=a
        self.b=b
        self.c=c

    def __str__(self) -> str:
        return f"A: {id(self)} -> {self.a=}, {self.b=}, {self.c}"
        # self.c=c

class B():
    __slots__ = ('a','b','c')
    a:int
    b:str
    c:A
    def __init__(self,a:int,b:str,c:A) -> None:
        self.a=a
        self.b=b
        self.c=c

    def __str__(self) -> str:
        return f"B: {id(self)} -> {self.a=}, {self.b=}, {self.c}"

b1 = B(123,'Eugenio',A(1,2,3))
b2 = B(456,'Parodi ',A(4,5,6))
b3 = B(789,'Pappala',A(7,8,9))

tw = ttk.TTkTableWidget
tm = inspect.getmembers(ttk.TTkTableWidget)
th = get_type_hints(ttk.TTkTableWidget)
th = get_type_hints(ttk.TTkConstant)

for i in th:
    print(i)

print(b1)
print(b2)
print(b3)
print(f"{B.a=}, {B.b=}, {B.c=}")
print(f"{A.a=}, {A.b=}, {A.c=}")
print(get_type_hints(B))
print(get_type_hints(B)[B.c.__name__])
print(get_type_hints(ttk.TTkTableWidget)[ttk.TTkTableWidget.cellChanged.__name__])
print(get_type_hints(ttk.TTkTableWidget))
print(inspect.getmembers(ttk.TTkTableWidget))

def template(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

baz = template
che = template

import ast
import inspect

# From
# https://stackoverflow.com/questions/3232024/introspection-to-get-decorator-names-on-a-method

class Foo(object):
    @baz
    @che
    def bar(self):
        pass

def get_decorators(cls):
    target = cls
    decorators = {}

    def visit_FunctionDef(node):
        decorators[node.name] = []
        for n in node.decorator_list:
            name = ''
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id

            decorators[node.name].append(name)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators

print(inspect.getsource(Foo))
print(get_decorators(Foo))