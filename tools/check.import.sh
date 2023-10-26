#!/bin/sh

__check(){
    grep -r -e "^import" -e "^from" TermTk |
        grep -v -e "from TermTk" -e "import TermTk" |
        grep -v "__init__.py:from \.[^ ]* *import" |
        grep -v -e "import re" -e "import os" -e "import datetime" |
        grep -v \
            -e "from dataclasses" \
            -e "signal.py:from inspect import getfullargspec" \
            -e "signal.py:from types import LambdaType" \
            -e "signal.py:from threading import Lock" \
            -e "colors.py:from .colors_ansi_map" \
            -e "log.py:import inspect" \
            -e "log.py:import logging" \
            -e "log.py:from collections.abc import Callable, Set" \
            -e "input.py:import platform" \
            -e "input.py:from time import time" \
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
            -e "progressbar.py:import math" \
            -e "uiloader.py:import json" \
            -e "uiproperties.py:from .properties.* import" \
            -e "util.py:import zlib, pickle, base64" \
            -e "propertyanimation.py:from inspect import getfullargspec" \
            -e "propertyanimation.py:from types import LambdaType" \
            -e "propertyanimation.py:import time, math" |
        grep -v \
            -e "TTkTerm/input.py:from ..drivers import TTkInputDriver" \
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
            -e "drivers/term_pyodide.py:import pyodideProxy" \
            -e "drivers/term_pyodide.py:from ..TTkTerm.term_base import TTkTermBase" \
            -e "drivers/__init__.py:import importlib.util" \
            -e "drivers/__init__.py:import platform"
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
