#!/bin/sh

__check(){
    grep -r -e "^import" -e "^from" TermTk |
        grep -v -e "from TermTk" -e "import TermTk" |
        grep -v "from typing import" |
        grep -v "__init__.py:from \.[^ ]* *import" |
        grep -v -e "import re" -e "import os" -e "import datetime" |
        grep -v \
            -e "from dataclasses" \
            -e "signal.py:from inspect import getfullargspec" \
            -e "signal.py:from types import LambdaType" \
            -e "signal.py:from threading import Lock" \
            -e "signal.py:import asyncio" \
            -e "signal.py:import importlib.util" \
            -e "colors.py:from .colors_ansi_map" \
            -e "log.py:import inspect" \
            -e "log.py:import logging" \
            -e "log.py:from collections.abc import Callable, Set" \
            -e "term.py:import importlib.util" \
            -e "term.*.py:import sys, os, signal" \
            -e "term.*.py:from .term_base import TTkTermBase" \
            -e "timer.py:import importlib" \
            -e "timer_unix.py:import threading" \
            -e "timer_pyodide.py:import pyodideProxy" \
            -e "ttk.py:import signal" \
            -e "ttk.py:import time" \
            -e "ttk.py:import queue" \
            -e "ttk.py:import threading" \
            -e "ttk.py:import platform" \
            -e "clipboard.py:import importlib.util" \
            -e "filebuffer.py:import threading" \
            -e "texedit.py:from math import log10, floor" \
            -e "string.py:import unicodedata" \
            -e "string.py:from types import GeneratorType" \
            -e "progressbar.py:import math" \
            -e "uiloader.py:import json" \
            -e "uiproperties.py:from .properties.* import" \
            -e "util.py:import zlib, pickle, base64" \
            -e "propertyanimation.py:from inspect import getfullargspec" \
            -e "propertyanimation.py:from types import LambdaType" \
            -e "propertyanimation.py:import time, math" \
            -e "savetools.py:import importlib.util" \
            -e "savetools.py:import json" |
        grep -v \
            -e "TTkTerm/input_mono.py:from time import time" \
            -e "TTkTerm/input_mono.py:import platform" \
            -e "TTkTerm/input_mono.py:from ..drivers import TTkInputDriver" \
            -e "TTkTerm/input_thread.py:from time import time" \
            -e "TTkTerm/input_thread.py:import threading, queue" \
            -e "TTkTerm/input_thread.py:from ..drivers import TTkInputDriver" \
            -e "TTkTerm/input.py:from .input_thread import *" |
        grep -v \
            -e "TTkGui/__init__.py:import importlib.util" \
            -e "TTkGui/textdocument.py:from threading import Lock" \
            -e "TTkGui/textdocument_highlight_pygments.py:from pygments" |
        grep -v \
            -e "TTkTerm/term.py:from ..drivers import *" \
            -e "drivers/unix_thread.py:import sys, os" \
            -e "drivers/unix_thread.py:from select import select" \
            -e "drivers/unix_thread.py:import threading" \
            -e "drivers/unix_thread.py:import queue" \
            -e "drivers/unix.py:import sys, os, re" \
            -e "drivers/unix.py:import signal" \
            -e "drivers/unix.py:from select import select" \
            -e "drivers/windows.py:import signal" \
            -e "drivers/windows.py:from ctypes import Structure, Union, byref, wintypes, windll" \
            -e "drivers/pyodide.py:from pyodide import __version__ as pyodideVersion" \
            -e "drivers/term_windows.py:import sys, os" \
            -e "drivers/term_windows.py:from threading import Thread, Lock" \
            -e "drivers/term_windows.py:from ..TTkTerm.term_base import TTkTermBase" \
            -e "drivers/term_windows.py:from .windows import *" \
            -e "drivers/term_unix.py:from ..TTkTerm.term_base import TTkTermBase" \
            -e "drivers/term_unix.py:from threading import Thread, Lock" \
            -e "drivers/term_unix_serial.py:from ..TTkTerm.term_base import TTkTermBase" \
            -e "drivers/term_unix_serial.py:from .term_unix import *" \
            -e "drivers/unix_gpm.py:import sys" \
            -e "drivers/unix_gpm.py:import os" \
            -e "drivers/unix_gpm.py:import re" \
            -e "drivers/unix_gpm.py:import ctypes" \
            -e "drivers/unix_gpm.py:import signal" \
            -e "drivers/unix_gpm.py:from select import select" \
            -e "drivers/term_pyodide.py:import pyodideProxy" \
            -e "drivers/term_pyodide.py:from ..TTkTerm.term_base import TTkTermBase" \
            -e "drivers/__init__.py:import importlib.util" \
            -e "drivers/__init__.py:import platform" |
        grep -v \
            -e "TTkTerminal/debugterminal.py:import struct, fcntl, termios" \
            -e "TTkTerminal/debugterminal.py:from select import select" \
            -e "TTkTerminal/terminalview.py:import struct, fcntl, termios" \
            -e "TTkTerminal/terminalview.py:from select import select" \
            -e "TTkTerminal/terminalview.py:from .terminalview_CSI_DEC import _TTkTerminal_CSI_DEC" \
            -e "TTkTerminal/terminal.py:import struct, fcntl, termios" \
            -e "TTkTerminal/terminal.py:from .terminalview_CSI_DEC import _TTkTerminal_CSI_DEC" \
            -e "TTkTerminal/terminal_screen.py:import collections" \
            -e "TTkTerminal/terminal_screen.py:import unicodedata" \
            -e "TTkTerminal/terminal_screen.py:from .terminal_screen_CSI import _TTkTerminalScreen_CSI" \
            -e "TTkTerminal/terminal_screen.py:from .terminal_screen_C1  import _TTkTerminalScreen_C1" \
            -e "TTkTerminal/terminalhelper.py:import struct, fcntl, termios" \
            -e "TTkTerminal/terminalhelper.py:from select import select" \
            -e "TTkTerminal/__init__.py:import importlib.util" \
            -e "TTkTerminal/__init__.py:import platform" |
        grep -v \
            -e "TTkModelView/__init__.py:from importlib.util import find_spec" \
            -e "TTkModelView/tablemodelcsv.py:import csv" \
            -e "TTkModelView/tablemodelsqlite3.py:import sqlite3" \
            -e "TTkModelView/tablemodelsqlite3.py:import threading"
} ;

if __check ;  then
    echo "Failed Dependencies verification!!!" ;
    echo "Please check:" ;
    echo "#######################"
    __check ;
    echo "#######################"
    exit 1 ;
else
    echo "Dependencies Verified!!!"
    exit 0 ;
fi ;
