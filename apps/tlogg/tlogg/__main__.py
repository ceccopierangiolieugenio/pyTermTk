#!/usr/bin/env python3

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

__all__ = []

import argparse
import appdirs

import TermTk as ttk

from tlogg.app.main import TLOGG
from tlogg.app.cfg import TloggCfg
from tlogg.app.options import optionsLoadTheme

from tlogg.proxy import tloggProxy
from tlogg.helper import TloggHelper

def main():
    TloggCfg.pathCfg = appdirs.user_config_dir("tlogg")

    parser = argparse.ArgumentParser()
    # parser.add_argument('-f', help='Full Screen', action='store_true')
    parser.add_argument('-c', help=f'config folder (default: "{TloggCfg.pathCfg}")', default=TloggCfg.pathCfg)
    parser.add_argument('filename', type=str, nargs='*',
                    help='the filename/s')
    args = parser.parse_args()

    # TTkLog.use_default_file_logging()

    TloggCfg.pathCfg = args.c
    ttk.TTkLog.debug(f"Config Path: {TloggCfg.pathCfg}")

    TloggCfg.load()

    if 'theme' not in TloggCfg.options:
        TloggCfg.options['theme'] = 'UTF8'
    optionsLoadTheme(TloggCfg.options['theme'])

    TloggHelper._loadPlugins()

    root = ttk.TTk(
            title="tlogg",
            layout=(tlogg:=TLOGG(tloggProxy=tloggProxy)),
            sigmask=(
                ttk.TTkTerm.Sigmask.CTRL_C |
                ttk.TTkTerm.Sigmask.CTRL_Q |
                ttk.TTkTerm.Sigmask.CTRL_S |
                ttk.TTkTerm.Sigmask.CTRL_Z ))
    TloggHelper._runPlugins()

    for file in args.filename:
        tlogg.openFile(file)

    root.mainloop()

if __name__ == '__main__':
    main()