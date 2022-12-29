#!/usr/bin/env python3
# vim:ts=4:sw=4:fdm=indent:cc=79:

# MIT License
#
# Copyright (c) 2022 Luchr  <https://github.com/luchr>
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

import datetime
import gc

import TermTk

WIN_COUNTER = 0

class ShowEventWindow(TermTk.TTkWindow):
    __slots__ = ('_win_number', '_event_info')

    def __init__(self, parent, event):
        global WIN_COUNTER
        WIN_COUNTER += 1
        win_number = WIN_COUNTER
        self._win_number = win_number
        win_layout = TermTk.TTkGridLayout(columnMinHeight=1)
        TermTk.TTkWindow.__init__(
            self, parent=parent, pos=(10, 18+win_number), size=(45, 5),
            title=f'Window {win_number}',
            layout=win_layout)
        if win_number == 1:
            self.setWindowFlag(0x0)
        self._event_info = TermTk.TTkLabel(
            text='updated if main button is clicked')
        win_layout.addWidget(self._event_info, 0, 0)
        event.connect(self.show_event, use_weak_ref=True)

    def show_event(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._event_info.setText(f'last seen event: {now}')
        TermTk.TTkLog.debug(f'show_event of window {self._win_number}')
        gc.collect()
        refs = gc.get_referrers(self)
        TermTk.TTkLog.debug(f'{len(refs)=}')
        for ref in refs:
            TermTk.TTkLog.debug(f'{id(ref)=}: {repr(ref)}')


class MainWindow(TermTk.TTkWindow):
    __slots__ = ('_main_button', '_slot_info', '_info_timer', '_timer_delay')

    def __init__(self, parent, timer_delay):
        self._timer_delay = timer_delay
        win_layout = TermTk.TTkGridLayout(columnMinHeight=1)
        TermTk.TTkWindow.__init__(
            self, parent=parent, pos=(1, 1), size=(50, 17), title='Main Window',
            layout=win_layout)
        self.setWindowFlag(0x0)

        main_button = TermTk.TTkButton(text='main test button', border=True)
        self._main_button = main_button
        win_layout.addWidget(main_button, 0, 0)

        new_win_button = TermTk.TTkButton(
            text='create new listener window', border=True)
        new_win_button.clicked.connect(
            lambda: create_show_event_window(parent, main_button.clicked))
        win_layout.addWidget(new_win_button, 2, 0)

        slot_info = TermTk.TTkLabel(text='')
        self._slot_info = slot_info
        win_layout.addWidget(slot_info, 4, 0)

        quit_button = TermTk.TTkButton(text='quit', border=True)
        quit_button.clicked.connect(parent.quit)
        win_layout.addWidget(quit_button, 6, 0)

        self._info_timer = TermTk.TTkTimer()
        self._info_timer.timeout.connect(self.show_info)
        self._info_timer.start(timer_delay)

        create_show_event_window(parent, main_button.clicked)

    def show_info(self):
        len_slots = len(self._main_button.clicked._connected_slots)
        self._slot_info.setText(f"Main button has {len_slots} slots/listeners ")
        self._info_timer.start(self._timer_delay)


def create_show_event_window(parent, event):
    win = ShowEventWindow(parent, event)
    win.setFocus()

def main():
    '''show main window and start event loop.'''
    root = TermTk.TTk()
    TermTk.TTkLog.use_default_file_logging()

    MainWindow(root, 0.5)

    root.mainloop()


if __name__ == '__main__':
    main()

# EOF
