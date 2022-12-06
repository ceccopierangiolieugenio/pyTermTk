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

import urllib.request
import re

URI='http://www.unicode.org/Public/UCD/latest/ucd/DerivedAge.txt'

response = urllib.request.urlopen(URI)

# Matching:
#   "FE24..FE26    ; 5.1 #   [3] COMBINING MACRON LEFT HALF..COMBINING CONJOINING MACRON"
#   "10190..1019B  ; 5.1 #  [12] ROMAN SEXTANS SIGN..ROMAN CENTURIAL SIGN"
rangeMatch = re.compile(r'^([0-9A-F]+)\.\.([0-9A-F]+) *; ([0-9\.]+) (#.*)$')

# Matching:
#   "A95F          ; 5.1 #       REJANG SECTION MARK"
#   "1093F         ; 5.1 #       LYDIAN TRIANGULAR MARK"
singleMatch = re.compile(r'^([0-9A-F]+) *; ([0-9\.]+) (#.*)$')



for line in response.readlines():
    # print(line.decode('utf-8'))
    if m := rangeMatch.match(line.decode('utf-8')):
        rfr = m.group(1)
        rto = m.group(2)
        rver = m.group(3)
        rdesc = m.group(4)
        print(f"{rver=} {rfr=} {rto=} {rdesc=}")
    elif m := singleMatch.match(line.decode('utf-8')):
        rm = m.group(1)
        rver = m.group(2)
        rdesc = m.group(3)
        print(f"{rver=} {rm=} {rdesc=}")
