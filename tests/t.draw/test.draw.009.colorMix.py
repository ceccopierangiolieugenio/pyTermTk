#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

def testColor(prefix:str,c1:ttk.TTkColor, c2:ttk.TTkColor):
    str1 = ttk.TTkString('Eugenio',c1)
    str2 = ttk.TTkString('Parodi' ,c2)
    rst  = "\033]8;;\033\\"
    print(prefix + (str1+str2).toAnsi() + rst)

fg_r = ttk.TTkColor.FG_RED
fg_g = ttk.TTkColor.FG_GREEN
fg_b = ttk.TTkColor.FG_BLUE
bg_r = ttk.TTkColor.BG_RED
bg_g = ttk.TTkColor.BG_GREEN
bg_b = ttk.TTkColor.BG_BLUE
fg_r_l = ttk.TTkColor.fg('#FF0000',link='https://github.com/ceccopierangiolieugenio/pyTermTk')
fg_g_l = ttk.TTkColor.fg('#00FF00',link='https://github.com/ceccopierangiolieugenio/pyTermTk')
fg_b_l = ttk.TTkColor.fg('#0000FF',link='https://github.com/ceccopierangiolieugenio/pyTermTk')
bg_r_l = ttk.TTkColor.bg('#FF0000',link='https://github.com/ceccopierangiolieugenio/pyTermTk')
bg_g_l = ttk.TTkColor.bg('#00FF00',link='https://github.com/ceccopierangiolieugenio/pyTermTk')
bg_b_l = ttk.TTkColor.bg('#0000FF',link='https://github.com/ceccopierangiolieugenio/pyTermTk')
testColor("r  ",fg_r,   bg_r)
testColor("g  ",fg_g,   bg_g)
testColor("b  ",fg_b,   bg_b)
testColor("rl ",fg_r_l, bg_r_l)
testColor("gl ",fg_g_l, bg_g_l)
testColor("bl ",fg_b_l, bg_b_l)

c1 = fg_r + bg_g
c2 = fg_r | bg_g
testColor("T1 ",c1,c2)

m1 = bg_b + fg_g
m2 = bg_b | fg_g
testColor("T2 ",m1,m2)

m3 = ttk.TTkColor.FG_YELLOW + m1
m4 = m1 + ttk.TTkColor.FG_YELLOW
m5 = ttk.TTkColor.FG_YELLOW | m1
m6 = m1 | ttk.TTkColor.FG_YELLOW
testColor("M1 ",m3,m4)
testColor("M1 ",m5,m6)

m3 = ttk.TTkColor.BG_YELLOW + m1
m4 = m1 + ttk.TTkColor.BG_YELLOW
m5 = ttk.TTkColor.BG_YELLOW | m1
m6 = m1 | ttk.TTkColor.BG_YELLOW
testColor("M2 ",m3,m4)
testColor("M2 ",m5,m6)

m3 = ttk.TTkColor.RST + m1
m4 = m1 + ttk.TTkColor.RST
m5 = ttk.TTkColor.RST | m1
m6 = m1 | ttk.TTkColor.RST
testColor("M3 ",m3,m4)
testColor("M3 ",m5,m6)