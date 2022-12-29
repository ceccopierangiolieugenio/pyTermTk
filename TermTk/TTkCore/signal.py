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

# ref: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
#      https://github.com/ceccopierangiolieugenio/pyCuT/blob/master/cupy/CuTCore/CuSignal.py

'''
Signals & Slots [`Tutorial <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_]
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

import weakref

class WeakrefSlot:
    '''
    A WeakrefSlot instance saves a slot as weakref (or WeakMethod).

    Hence the slots may be garbage collected, leaving this WeakrefSlot
    without a referent.

    WeakrefSlots are callable. They call the referent slot (if available).

    WeakrefSlots have no __eq__ method hence they are compared with
    python's "is" operator (identitiy check). This is important for
    WekrefSlots inside lists.

    WeakrefSlots have the _referent_gone flag which is set after the
    WeakrefSlot has detected that the referent was already garbage
    collected. This flag may be used to easily delete WeakrefSlots
    without referents.
    '''
    __slots__ = ('_weak_slotref', '_referent_gone')

    def __init__(self, slot):
        '''
        initialize WekrefSlot for the input argument slot (which must be callable).

        WeakMethod is used for bounded methods.

        Attention:
        A slot object which has no (other) references than the given
        slot may be garbage collected immediately after this call.
        They are "dead on arrival". A typical example for this is a
        inline lambda function. That's *the* feature of WeakrefSlots.
        '''
        if not callable(slot):
            raise TypeError(f'slot must be callable; I found {type(slot)=}')
        self._referent_gone = False
        bound_method = hasattr(slot, '__self__')  and  hasattr(slot, '__func__')
        self._weak_slotref = (
            weakref.WeakMethod(slot) if bound_method else weakref.ref(slot))

    def __str__(self):
        '''show target (if avail).'''
        target = None if self._referent_gone else self._weak_slotref()
        target_str = 'dead' if target is None else f'to {str(target)}'
        return f'<{self.__class__.__name__} at {hex(id(self))}; {target_str}>'

    def __call__(self, *args, **kwargs):
        '''
        If the referent of _weak_slotref was not garbage collected, then
        call the referent.

        Checks and updates _referent_gone flag.
        '''
        if self._referent_gone:
            return  # Nothing to do; we already know the referent is gone
        func = self._weak_slotref()
        if func is None:
            # referent was gargabe collected (since the last test)
            self._referent_gone = True
            return # Nothing to do
        func(*args, **kwargs)  # call referent slot
        # throw away the (strong) reference "func" now


def pyTTkSlot(*args, **kwargs):
    def pyTTkSlot_d(func):
        # Add signature attributes to the function
        func._TTkslot_attr = args
        return func
    return pyTTkSlot_d

def pyTTkSignal(*args, **kwargs):
    return _pyTTkSignal_obj(*args, **kwargs)

class _pyTTkSignal_obj():
    _signals = []
    __slots__ = ('_types', '_name', '_revision', '_connected_slots')
    def __init__(self, *args, **kwargs):
        # ref: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html#PyQt5.QtCore.pyqtSignal

        # PyQt5.QtCore.pyqtSignal(types[, name[, revision=0[, arguments=[]]]])
        #    Create one or more overloaded unbound signals as a class attribute.

        #    Parameters:
        #    types - the types that define the C++ signature of the signal. Each type may be a Python type object or a string that is the name of a C++ type. Alternatively each may be a sequence of type arguments. In this case each sequence defines the signature of a different signal overload. The first overload will be the default.
        #    name - the name of the signal. If it is omitted then the name of the class attribute is used. This may only be given as a keyword argument.
        #    revision - the revision of the signal that is exported to QML. This may only be given as a keyword argument.
        #    arguments - the sequence of the names of the signal's arguments that is exported to QML. This may only be given as a keyword argument.
        #    Return type:
        #        an unbound signal
        self._types = args
        self._name = kwargs.get('name', None)
        self._revision = kwargs.get('revision', 0)
        self._connected_slots = []
        _pyTTkSignal_obj._signals.append(self)

    def connect(self, slot, use_weak_ref=False):
        # ref: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html#connect

        # connect(slot[, type=PyQt5.QtCore.Qt.AutoConnection[, no_receiver_check=False]]) -> PyQt5.QtCore.QMetaObject.Connection
        #    Connect a signal to a slot. An exception will be raised if the connection failed.

        #    Parameters:
        #    slot - the slot to connect to, either a Python callable or another bound signal.
        #    type - the type of the connection to make.
        #    no_receiver_check - suppress the check that the underlying C++ receiver instance still exists and deliver the signal anyway.
        #    Returns:
        #        a Connection object which can be passed to disconnect(). This is the only way to disconnect a connection to a lambda function.
        if hasattr(slot, '_TTkslot_attr'):
            if len(slot._TTkslot_attr) != len(self._types):
                error = "Decorated slot has no signature compatible: "+slot.__name__+str(slot._TTkslot_attr)+" != signal"+str(self._types)
                raise TypeError(error)
            for a,b in zip(slot._TTkslot_attr, self._types):
                if not issubclass(a,b):
                    error = "Decorated slot has no signature compatible: "+slot.__name__+str(slot._TTkslot_attr)+" != signal"+str(self._types)
                    raise TypeError(error)
        if use_weak_ref:
            slot = WeakrefSlot(slot)  # replace slot with WeakrefSlot
        if slot not in self._connected_slots:
            self._connected_slots.append(slot)
        return slot # may return WeakrefSlot which may be used for disconnect

    def disconnect(self, *args, **kwargs):
        for slot in args:
            if slot in self._connected_slots:
                self._connected_slots.remove(slot)

    def emit(self, *args, **kwargs):
        if len(args) != len(self._types):
            error = "func"+str(self._types)+" signal has "+str(len(self._types))+" argument(s) but "+str(len(args))+" provided"
            raise TypeError(error)

        need_weakref_cleanup = False  # have we seen WeakrefSlots without referent?
        for slot in self._connected_slots:
            slot(*args, **kwargs)
            if isinstance(slot, WeakrefSlot)  and  slot._referent_gone:
                need_weakref_cleanup = True

        if need_weakref_cleanup:
            # remove WeakrefSlots where referent was gone
            for slot in self._connected_slots[:]: # do a slice for safe removal
                if isinstance(slot, WeakrefSlot)  and  slot._referent_gone:
                    self._connected_slots.remove(slot)

    def clear(self):
        self._connected_slots = []

    @staticmethod
    def clearAll():
        for s in _pyTTkSignal_obj._signals:
            s.clear()

    def forward(self):
        def _ret(*args, **kwargs):
            self.emit(*args, **kwargs)
        return _ret
