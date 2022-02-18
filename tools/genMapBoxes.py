#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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




from re import U


class ElemDef():
    def __init__(self, u, d, l, r):
        self.u = u
        self.d = d
        self.l = l
        self.r = r

    def __eq__(self, other):
        if other is None: return False
        return \
            self.u ==other.u and \
            self.d ==other.d and \
            self.l ==other.l and \
            self.r ==other.r

    def __add__(self, other):
        u = other.u if other.u else self.u
        d = other.d if other.d else self.d
        l = other.l if other.l else self.l
        r = other.r if other.r else self.r
        return ElemDef(u,d,l,r)

    def __hash__(self):
        return self.u + self.d*10 + self.l*100 + self.r*1000

    def __str__(self):
        return f"{self.u}_{self.d}_{self.l}_{self.r}"

e = {
    ElemDef(0,0,0,0) : ' ' ,
    ElemDef(1,1,0,0) : '│' ,
    ElemDef(0,0,1,1) : '─' ,
    ElemDef(0,1,0,1) : '┌' ,
    ElemDef(0,1,1,0) : '┐' ,
    ElemDef(1,0,0,1) : '└' ,
    ElemDef(1,0,1,0) : '┘' ,
    ElemDef(1,0,1,1) : '┴' ,
    ElemDef(0,1,1,1) : '┬' ,
    ElemDef(1,1,1,0) : '┤' ,
    ElemDef(1,1,0,1) : '├' ,
    ElemDef(1,1,1,1) : '┼' ,
    ElemDef(2,2,0,0) : '║' ,
    ElemDef(0,0,2,2) : '═' ,
    ElemDef(0,2,0,2) : '╔' ,
    ElemDef(0,2,2,0) : '╗' ,
    ElemDef(2,0,0,2) : '╚' ,
    ElemDef(2,0,2,0) : '╝' ,
    ElemDef(2,0,2,2) : '╩' ,
    ElemDef(0,2,2,2) : '╦' ,
    ElemDef(2,2,2,0) : '╣' ,
    ElemDef(2,2,0,2) : '╠' ,
    ElemDef(2,2,2,2) : '╬' ,
    ElemDef(1,0,2,2) : '╧' ,
    ElemDef(0,1,2,2) : '╤' ,
    ElemDef(2,2,0,1) : '╟' ,
    ElemDef(2,2,1,0) : '╢' ,
    ElemDef(2,0,1,1) : '╨' ,
    ElemDef(0,2,1,1) : '╥' ,
    ElemDef(1,1,0,2) : '╞' ,
    ElemDef(1,1,2,0) : '╡' ,
    ElemDef(0,2,1,0) : '╓' ,
    ElemDef(0,2,0,1) : '╖' ,
    ElemDef(2,0,1,0) : '╙' ,
    ElemDef(2,0,0,1) : '╜' ,
    ElemDef(0,1,2,0) : '╒' ,
    ElemDef(0,1,0,2) : '╕' ,
    ElemDef(1,0,2,0) : '╘' ,
    ElemDef(1,0,0,2) : '╛' ,
    ElemDef(2,2,1,1) : '╫' ,
    ElemDef(1,1,2,2) : '╪' ,
}

# Create table of combinations

for y in e:
    print(f"'{e[y]}' : " + '{ ', end='')
    for x in e:
        ch = e.get(y+x,'X')
        print(f"'{e[x]}':'{ch}', ", end='')
    print("} ,")
