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

import time, multiprocessing

print(1)

def task(a,b,c,d,shared_results):
    print(2,a,b,c,d,shared_results)
    process = multiprocessing.current_process()
    print(f"Task: {process.daemon=}")
    for i in range(15):
        print(f"{i=}",flush=True)
        time.sleep(0.1)
    shared_results['pippo'] = (5,6,7,8)
    return 3,4,5,6

print(3)

if __name__ == '__main__':
    print(4)
    manager = multiprocessing.Manager()
    shared_results = manager.dict()

    process = multiprocessing.Process(target=task, daemon=True, args=(1,2,3,4,shared_results))

    process.start()
    process.join()

    print(shared_results)

    print(f"Main Process exit...")



