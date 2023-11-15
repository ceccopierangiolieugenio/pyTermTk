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


def diff(docA, docB):
        i1 = min(len(docA),len(docB))
        for i,(a,b) in enumerate(zip(docA,docB)):
            if a!=b:
                i1 = i
                break

        i2 = min(len(docA),len(docB))-i1
        for i,(a,b) in enumerate(zip(reversed(docA[i1:]),reversed(docB[i1:]))):
            if a!=b:
                i2 = i
                break

        if i2 == 0:
            sliceB = docB[i1:]
            sliceA = docA[i1:]
        else:
            sliceB = docB[i1:-i2]
            sliceA = docA[i1:-i2]

        print(f"           {i1=}     {i2=}")
        print( "        0    1    2    3    4    5    6    7    8    9    10   11   12")
        print(f"o {docA=}")
        print(f"o {docB=}")
        print(f"sliceA {'     '*i1}{sliceA}")
        print(f"sliceB {'     '*i1}{sliceB}")
        if i2 == 0:
            docA[i1:] = sliceB
            docB[i1:] = sliceA
        else:
            docA[i1:-i2] = sliceB
            docB[i1:-i2] = sliceA
        print(f"n {docA=}")
        print(f"n {docB=}")

docA = ['a','b','c','d','e','f','g','h','i','j','k','l']
docB = ['a','b','c','d','e','f','g','h','i','j','k','l']
diff(docA, docB)

# Same Size
docA = ['a','b','c','d','e','f','g','h','i','j','k','l']
docB = ['a','b','c','d','x','y','g','h','i','j','k','l']
diff(docA, docB)
diff(docB, docA)
docA = ['a','b','c','d','e','f','g','h','i','j','k','l']
docB = ['1','2','c','d','e','f','g','h','i','j','k','l']
diff(docA, docB)
diff(docB, docA)
docA = ['a','b','c','d','e','f','g','h','i','j','k','l']
docB = ['a','b','c','d','e','f','g','h','i','X','Y','l']
diff(docA, docB)
diff(docB, docA)
docA = ['a','b','c','d','e','f','g','h','i','j','k','l']
docB = ['a','b','c','d','e','f','g','h','i','j','1','2']
diff(docA, docB)
diff(docB, docA)

# Diff Size
docA = ['a','b','c','d',        'g','h','i','j','k','l']
docB = ['a','b','c','d','X','Y','g','h','i','j','k','l']
diff(docA, docB)
diff(docB, docA)
docA = [        'c','d','e','f','g','h','i','j','k','l']
docB = ['X','Y','c','d','e','f','g','h','i','j','k','l']
diff(docA, docB)
diff(docB, docA)
docA = ['a','b','c','d','e','f','g','h','i','j'        ]
docB = ['a','b','c','d','e','f','g','h','i','j','X','Y']
diff(docA, docB)
diff(docB, docA)

# Diff Size
docA = ['a','b','c','d','Z',    'g','h','i','j','k','l']
docB = ['a','b','c','d','X','Y','g','h','i','j','k','l']
diff(docA, docB)
diff(docB, docA)
docA = ['Z',    'c','d','e','f','g','h','i','j','k','l']
docB = ['X','Y','c','d','e','f','g','h','i','j','k','l']
diff(docA, docB)
diff(docB, docA)
docA = ['a','b','c','d','e','f','g','h','i','j','Z'    ]
docB = ['a','b','c','d','e','f','g','h','i','j','X','Y']
diff(docA, docB)
diff(docB, docA)


docA = [  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12]
docB = ['a','b','c','d','e','f','g','h','i','j','k','l']
diff(docA, docB)
diff(docB, docA)

docA = []
docB = ['a','b','c','d','e','f','g','h','i','j','k','l']
diff(docA, docB)
diff(docB, docA)

docA = []
docB = []
diff(docA, docB)
diff(docB, docA)