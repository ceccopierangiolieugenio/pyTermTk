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
    var = yield
    print(f"{var=}")
    yield

yf1 = yieldFunc1()

for x in yf1:
    print(f"{x=}")
    yf1.send(123)

class testWrite():
    def __init__(self) -> None:
        self.loopGenerator = self._loop()

    def _loop(self):
        _run = True
        while _run:
            var = yield
            yield
            print(f"Loop: {var=}")
            if not var:
                return

    def write(self, data):
        print(f"Writing {data=}")
        n = next(self.loopGenerator)
        self.loopGenerator.send(data)

tw = testWrite()
tw.write(123)
tw.write(345)
tw.write(567)
tw.write(None)
tw.write(890)


