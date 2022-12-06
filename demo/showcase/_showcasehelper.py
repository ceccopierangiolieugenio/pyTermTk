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

import random

import TermTk as ttk

zc1 = chr(0x07a6) # Zero width chars oަ
zc2 = chr(0x20D7) # Zero width chars o⃗
zc3 = chr(0x065f) # Zero width chars oٟ
utfwords = [
    f"--Zero{zc1}{zc2}{zc3}-1-", f"--Zero-2{zc1}{zc2}{zc3}-", f"--Ze{zc1}{zc2}{zc3}ro-3-", f"{zc1}{zc2}{zc3}--Zero-4-",
    "Lorem", "i🙻sum", "d😮l😱r", "sit", "am😎t,", "c😱nsectetur", "adi🙻iscing", "elit,", "sed", "do", "eiusmod", "t😜mpor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliq😞ip", "ex", "ea", "comm😞do", "cons😿quat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "cul🙻a", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]
words = ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit,", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua.", "Ut", "enim", "ad", "minim", "veniam,", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint", "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum."]

def randColor():
    return [
        ttk.TTkColor.RST,
        ttk.TTkColor.fg('#FFFF00'),
        ttk.TTkColor.fg('#00FFFF'),
        ttk.TTkColor.fg('#FF00FF'),
        ttk.TTkColor.fg('#0000FF')+ttk.TTkColor.bg('#00FF00'),
        ttk.TTkColor.fg('#00FF00')+ttk.TTkColor.UNDERLINE,
        ttk.TTkColor.fg('#FF0000')+ttk.TTkColor.STRIKETROUGH,
    ][random.randint(0,6)]

def getWord():
    return random.choice(words)
def getWords(n):
    www = [random.choice(words) for _ in range(n)]
    return " ".join(www)
def getSentence(a,b):
    return " ".join([getWords(random.randint(1,4)) for _ in range(0,random.randint(a,b))])

def getUtfWord():
    return random.choice(utfwords)
def getUtfWords(n):
    www = [random.choice(utfwords) for _ in range(n)]
    return " ".join(www)
def getUtfSentence(a,b):
    return " ".join([getUtfWords(random.randint(1,4)) for _ in range(0,random.randint(a,b))])

def getUtfColoredWords(n):
    www = [random.choice(utfwords) for _ in range(n)]
    return ttk.TTkString(" ".join(www), randColor())
def getUtfColoredSentence(a,b):
    return ttk.TTkString(" ").join([getUtfColoredWords(random.randint(1,4)) for _ in range(0,random.randint(a,b))])
