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
import re
import argparse
import queue
import pickle
import threading

sys.path.append(os.path.join(sys.path[0],'../../demo'))
sys.path.append(os.path.join(sys.path[0],'../../libs/pyTermTk'))

import demo
import TermTk as ttk

class TTkRecord(ttk.TTk):
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

    __slots__ = ('_record', '_events', '_key_events', '_mouse_events', '_screen_events', '_glyphCount')
    _ansi_re = re.compile(r'\x1b\[[^a-zA-Z]*[a-zA-Z]')

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self._record = kwargs.get('record', True)
        self._glyphCount = 0
        self._events        = self._RecordQueue()
        self._key_events    = self._RecordQueue()
        self._mouse_events  = self._RecordQueue()
        self._screen_events = self._RecordQueue()

    MOUSE_EVENT  = 0x01
    KEY_EVENT    = 0x02
    SCREEN_EVENT = 0x04
    QUIT_EVENT   = 0x08
    TIME_EVENT   = 0x10

    def _mainloop(self):
        if self._record:
            return super()._mainloop()
        original_push = ttk.TTkTerm.push
        ansi_re = self._ansi_re
        record = self
        def _counting_push(*args):
            s = str(*args)
            stripped = ansi_re.sub('', s)
            record._glyphCount += len(stripped)
            original_push(*args)
        ttk.TTkTerm.push = _counting_push
        self.show()
        while (evt := self._events.get()) != self.QUIT_EVENT:
            mevt,kevt = None, None
            if evt == self.MOUSE_EVENT:
                mevt = self._mouse_events.get()
            if evt == self.KEY_EVENT:
                kevt = self._key_events.get()
            if evt == self.TIME_EVENT:
                self._paintEvent.set()
                super()._time_event()
                continue
            #if evt == self.SCREEN_EVENT:
            #    width, height = self._screen_events.get()
            #    super()._win_resize_cb(width, height)
            super()._processInput(kevt, mevt)
        ttk.TTkTerm.push = original_push
        return None

    def _processInput(self, kevt, mevt):
        if mevt:
            self._events.put(self.MOUSE_EVENT)
            self._mouse_events.put(mevt)
        if kevt:
            self._events.put(self.KEY_EVENT)
            self._key_events.put(kevt)
        super()._processInput(kevt,mevt)

    def _time_event(self):
        self._events.put(self.TIME_EVENT)
        super()._time_event()

    def _win_resize_cb(self, width, height):
        self._events.put(self.SCREEN_EVENT)
        self._screen_events.put((width, height))
        super()._win_resize_cb(width, height)

    def saveQueue(self, fd):
        self._events.put(self.QUIT_EVENT)
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
    parser.add_argument('-t', help='Track Mouse', action='store_true')
    args = parser.parse_args()
    mouseTrack = args.t

    print(args)

    if args.record:
        root = TTkRecord(title="pyTermTk Demo Record", record=True, mouseTrack=mouseTrack)
        winTabbed1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(80,24), title="pyTermTk Showcase", border=True, layout=ttk.TTkGridLayout())
        demo.demoShowcase(winTabbed1, True)
        root.mainloop()
        root.saveQueue(args.record)
        args.record.close()
        ttk.TTkHelper.quit()
        print(f"\n\nGlyph count: {root._glyphCount}")
    elif args.play:
        root = TTkRecord(title="pyTermTk Demo Record", record=False)
        root.loadQueue(args.play)
        winTabbed1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(80,24), title="pyTermTk Showcase", border=True, layout=ttk.TTkGridLayout())
        demo.demoShowcase(winTabbed1, True)
        root.mainloop()
        ttk.TTkHelper.quit()
        print(f"\n\nGlyph count: {root._glyphCount}")
    else:
        demo.main()
        ttk.TTkHelper.quit()

def test_demo():
    root = ttk.TTk(layout=ttk.TTkGridLayout())
    assert demo.demoShowcase(root) is not None
    ttk.TTkHelper.quit()

def message_handler(mode, context, message):
    msgType = "NONE"
    if   mode == ttk.TTkLog.InfoMsg:     msgType = "[INFO]"
    elif mode == ttk.TTkLog.WarningMsg:  msgType = "[WARNING]"
    elif mode == ttk.TTkLog.CriticalMsg: msgType = "[CRITICAL]"
    elif mode == ttk.TTkLog.FatalMsg:    msgType = "[FATAL]"
    elif mode == ttk.TTkLog.ErrorMsg:    msgType = "[ERROR]"
    print(f"{msgType} {context.file} {message}")

def test_recording1():
    # ttk.TTkLog.use_default_file_logging()
    ttk.TTkLog.installMessageHandler(message_handler)
    root = TTkRecord(title="pyTermTk Demo Record", record=False)
    root.loadQueue(open('tmp/test.input.001.bin', 'rb'))
    winTabbed1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(80,24), title="pyTermTk Showcase", border=True, layout=ttk.TTkGridLayout())
    demo.demoShowcase(winTabbed1, True)
    root.mainloop()
    ttk.TTkHelper.quit()
    print(f"\n\nGlyph count: {root._glyphCount}")

def test_recording2():
    # ttk.TTkLog.use_default_file_logging()
    ttk.TTkLog.installMessageHandler(message_handler)
    root = TTkRecord(title="pyTermTk Demo Record", record=False)
    root.loadQueue(open('tmp/test.input.002.bin', 'rb'))
    winTabbed1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(80,24), title="pyTermTk Showcase", border=True, layout=ttk.TTkGridLayout())
    demo.demoShowcase(winTabbed1, True)
    root.mainloop()
    ttk.TTkHelper.quit()
    print(f"\n\nGlyph count: {root._glyphCount}")

def test_recording3():
    # ttk.TTkLog.use_default_file_logging()
    ttk.TTkLog.installMessageHandler(message_handler)
    root = TTkRecord(title="pyTermTk Demo Record", record=False)
    root.loadQueue(open('tmp/test.input.003.bin', 'rb'))
    winTabbed1 = ttk.TTkWindow(parent=root,pos=(0,0), size=(80,24), title="pyTermTk Showcase", border=True, layout=ttk.TTkGridLayout())
    demo.demoShowcase(winTabbed1, True)
    root.mainloop()
    ttk.TTkHelper.quit()
    print(f"\n\nGlyph count: {root._glyphCount}")