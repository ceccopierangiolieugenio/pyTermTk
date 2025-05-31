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

__all__ = ['main']

import argparse

import appdirs

from TermTk import TTk, TTkTerm, TTkTheme
from TermTk import TTkLog

from ttkode import TTkodeHelper
from ttkode import ttkodeProxy
from ttkode.app.cfg import TTKodeCfg


def main():
    TTKodeCfg.pathCfg = appdirs.user_config_dir("ttkode")

    parser = argparse.ArgumentParser()
    # parser.add_argument('-f', help='Full Screen', action='store_true')
    parser.add_argument('-c', help=f'config folder (default: "{TTKodeCfg.pathCfg}")', default=TTKodeCfg.pathCfg)
    parser.add_argument('filename', type=str, nargs='*',
                    help='the filename/s')
    args = parser.parse_args()

    # TTkLog.use_default_file_logging()

    TTKodeCfg.pathCfg = args.c
    TTkLog.debug(f"Config Path: {TTKodeCfg.pathCfg}")

    TTKodeCfg.load()

    # if 'theme' not in TTKodeCfg.options:
    #     TTKodeCfg.options['theme'] = 'NERD'
    # optionsLoadTheme(TTKodeCfg.options['theme'])

    TTkTheme.loadTheme(TTkTheme.NERD)

    TTkodeHelper._loadPlugins()

    root = TTk( layout=ttkodeProxy.ttkode(),
                title="TTkode",
                mouseTrack=True,
                sigmask=(
                    # TTkTerm.Sigmask.CTRL_C |
                    TTkTerm.Sigmask.CTRL_Q |
                    TTkTerm.Sigmask.CTRL_S |
                    TTkTerm.Sigmask.CTRL_Y |
                    TTkTerm.Sigmask.CTRL_Z ))

    for file in args.filename:
        ttkodeProxy.openFile(file)

    TTkodeHelper._runPlugins()

    root.mainloop()

if __name__ == '__main__':
    main()