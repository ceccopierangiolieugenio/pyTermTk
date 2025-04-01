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

# ref: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
#      https://github.com/ceccopierangiolieugenio/pyCuT/blob/master/cupy/CuTCore/CuSignal.py

'''
Signals & Slots [:ref:`Tutorial <Signal and Slots>`]
=========================================================================================================================

  Signals and slots are used for communication between objects.

Intro
=====

|  The :mod:`TermTk.TTkCore.signal` is more than heavily inspired by `Qt5 Signal&Slots <(https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html>`_
|  https://doc.qt.io/qt-5/signalsandslots.html

|  In GUI programming, when we change one widget, we often want another widget to be notified.
|  More generally, we want objects of any kind to be able to communicate with one another.
|  For example, if a user clicks a Close button, we probably want the window's close() function to be called.

Signal and Slots
================

|  A signal is emitted when a particular event occurs.
|  A slot is a function that is called in response to a particular signal.
|  `TermTk <https://github.com/ceccopierangiolieugenio/pyTermTk>`_'s :mod:`~TermTk.TTkWidgets` have many predefined signals/slots, but it is possible to subclass any :mod:`~TermTk.TTkWidgets` and add our own signals/slots to them.

.. image:: /../_images/Signal.Slots.001.svg

Methods
=======

.. autofunction:: TermTk.pyTTkSignal
.. autodecorator:: TermTk.pyTTkSlot
'''

__all__ = ['pyTTkSlot', 'pyTTkSignal']

# from typing import TypeVar, TypeVarTuple, Generic, List
from inspect import getfullargspec, iscoroutinefunction
from types import LambdaType
from threading import Lock
import asyncio

import importlib.util

if importlib.util.find_spec('pyodideProxy'):
    def _run_coroutines(coros):
        for call in coros:
            asyncio.create_task(call)
else:
    from threading import Thread
    import asyncio

    def _async_runner(coros):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.gather(*coros))
        loop.close()

    def _run_coroutines(coros):
        Thread(target=_async_runner, args=(coros,)).start()

def pyTTkSlot(*args):
    def pyTTkSlot_d(func):
        # Add signature attributes to the function
        func._TTkslot_attr = args
        return func
    return pyTTkSlot_d

# Ts = TypeVarTuple("Ts")
# class pyTTkSignal(Generic[*Ts]):
class pyTTkSignal():
    _signals = []
    __slots__ = ('_types', '_connected_slots', '_connected_async_slots', '_mutex')
    def __init__(self, *args, **kwargs) -> None:
        # ref: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html#PyQt5.QtCore.pyqtSignal

        # PyQt5.QtCore.pyqtSignal(types[, name[, revision=0[, arguments=[]]]])
        #    Create one or more overloaded unbound signals as a class attribute.

        #    Parameters:
        #    types - the types that define the C++ signature of the signal. Each type may be a Python type object or a string that is the name of a C++ type. Alternatively each may be a sequence of type arguments. In this case each sequence defines the signature of a different signal overload. The first overload will be the default.
        #    arguments - the sequence of the names of the signal's arguments that is exported to QML. This may only be given as a keyword argument.
        #    Return type:
        #        an unbound signal
        self._types = args
        self._connected_slots = {}
        self._connected_async_slots = {}
        self._mutex = Lock()
        pyTTkSignal._signals.append(self)

    def connect(self, slot):
        # ref: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html#connect

        # connect(slot[, type=PyQt5.QtCore.Qt.AutoConnection[, no_receiver_check=False]]) -> PyQt5.QtCore.QMetaObject.Connection
        #    Connect a signal to a slot. An exception will be raised if the connection failed.

        #    Parameters:
        #    slot - the slot to connect to, either a Python callable or another bound signal.
        #    type - the type of the connection to make.
        #    no_receiver_check - suppress the check that the underlying C++ receiver instance still exists and deliver the signal anyway.
        #    Returns:
        #        a Connection object which can be passed to disconnect(). This is the only way to disconnect a connection to a lambda function.
        spec = getfullargspec(slot)
        if isinstance(slot, LambdaType) and slot.__name__ == "<lambda>":
            nargs = len(spec.args)
        elif spec.varargs:
            nargs = len(self._types)
        else:
            nargs = len(spec.args) - (1 if (hasattr(slot, '__self__')) else 0)
        ndef = 0 if not spec.defaults else len(spec.defaults)
        if nargs-ndef > len(self._types):
                error = f"Decorated slot has no signature compatible: {slot.__name__} {spec} != signal{self._types}"
                raise TypeError(error)
        if hasattr(slot, '_TTkslot_attr'):
            if len(slot._TTkslot_attr) > len(self._types):
                error = "Decorated slot has no signature compatible: "+slot.__name__+str(slot._TTkslot_attr)+" != signal"+str(self._types)
                raise TypeError(error)
            else:
              for a,b in zip(slot._TTkslot_attr, self._types):
                if a!=b and not issubclass(a,b):
                    error = "Decorated slot has no signature compatible: "+slot.__name__+str(slot._TTkslot_attr)+" != signal"+str(self._types)
                    raise TypeError(error)
        if iscoroutinefunction(slot):
            if slot not in self._connected_async_slots:
                self._connected_async_slots[slot]=slice(nargs)
        else:
            if slot not in self._connected_slots:
                self._connected_slots[slot]=slice(nargs)

    def disconnect(self, *args, **kwargs) -> None:
        for slot in args:
            if slot in self._connected_slots:
                del self._connected_slots[slot]

    def emit(self, *args, **kwargs) -> None:
        if not self._mutex.acquire(False): return
        if len(args) != len(self._types):
            error = "func"+str(self._types)+" signal has "+str(len(self._types))+" argument(s) but "+str(len(args))+" provided"
            raise TypeError(error)
        for slot,sl in self._connected_slots.copy().items():
            slot(*args[sl], **kwargs)
        if self._connected_async_slots:
            coros = [slot(*args[sl], **kwargs) for slot,sl in self._connected_async_slots.copy().items()]
            _run_coroutines(coros)
        self._mutex.release()

    def clear(self):
        self._connected_slots = {}

    @staticmethod
    def clearAll():
        for s in pyTTkSignal._signals:
            s.clear()

    def forward(self):
        def _ret(*args, **kwargs) -> None:
            self.emit(*args, **kwargs)
        return _ret