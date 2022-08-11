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

import sys, os
import argparse
import queue
import pickle

sys.path.append(os.path.join(sys.path[0],'../../demo'))
sys.path.append(os.path.join(sys.path[0],'../..'))

import demo

class TTkRecord(demo.ttk.TTk):
    class _RecordQueue(queue.Queue):
        def __init__(self, *args, **kwargs):
            super().__init__( *args, **kwargs)
            self._saveQueue = queue.Queue()

        def put(self, *args, **kwargs):
            self._saveQueue.put( *args, **kwargs)
            super().put( *args, **kwargs)

        def get(self, *args, **kwargs):
            return super().get( *args, **kwargs)

        def getData(self):
            data = []
            while not self._saveQueue.empty():
                d = self._saveQueue.get()
                data.append(d)
            return data

        def putData(self, data):
            for d in data:
                self.put(d)

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkRecord' )
        self._events        = TTkRecord._RecordQueue()
        self._key_events    = TTkRecord._RecordQueue()
        self._mouse_events  = TTkRecord._RecordQueue()
        self._screen_events = TTkRecord._RecordQueue()

    def saveQueue(self, fd):
        data = {'events': self._events.getData(),
                'key':    self._key_events.getData(),
                'mouse':  self._mouse_events.getData(),
                'screen': self._screen_events.getData()}
        pickle.dump(data,fd)

    def loadQueue(self, fd):
        data = pickle.load(fd)
        self._events.putData(data['events'])
        self._key_events.putData(data['key'])
        self._mouse_events.putData(data['mouse'])
        self._screen_events.putData(data['screen'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--record', help='Record input to File', type=argparse.FileType('bw'))
    parser.add_argument('-p', '--play',   help='Play input from File', type=argparse.FileType('br'))
    parser.add_argument('-f', help='Full Screen (default)', action='store_true')
    parser.add_argument('-w', help='Windowed',    action='store_true')
    args = parser.parse_args()

    print(args)

    if args.record:
        root = TTkRecord(title="pyTermTk Demo Record")
        winTabbed1 = demo.ttk.TTkWindow(parent=root,pos=(0,0), size=(80,24), title="pyTermTk Showcase", border=True, layout=demo.ttk.TTkGridLayout())
        demo.demoShowcase(winTabbed1, True)
        root.mainloop()
        root.saveQueue(args.record)
        args.record.close()
    elif args.play:
        root = TTkRecord(title="pyTermTk Demo Record")
        root.loadQueue(args.play)
        winTabbed1 = demo.ttk.TTkWindow(parent=root,pos=(0,0), size=(80,24), title="pyTermTk Showcase", border=True, layout=demo.ttk.TTkGridLayout())
        demo.demoShowcase(winTabbed1, True)
        root.mainloop()
    else:
        demo.main()

def test_demo():
    root = demo.ttk.TTk(layout=demo.ttk.TTkGridLayout())
    assert demo.demoShowcase(root) != None
    root.quit()

def test_recording1():
    root = TTkRecord(title="pyTermTk Demo Record")
    root.loadQueue(open('tmp/test.input.bin', 'rb'))
    winTabbed1 = demo.ttk.TTkWindow(parent=root,pos=(0,0), size=(80,24), title="pyTermTk Showcase", border=True, layout=demo.ttk.TTkGridLayout())
    demo.demoShowcase(winTabbed1, True)
    root.mainloop()