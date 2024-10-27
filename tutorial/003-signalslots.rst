.. _pyTermTk:  https://github.com/ceccopierangiolieugenio/pyTermTk
.. _TermTk:    https://github.com/ceccopierangiolieugenio/pyTermTk

.. _`TermTk Signal&Slots`: https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkCore.signal.html
.. _`Qt5 Signal&Slots`:    https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html

.. _TTkWidgets: https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.html

.. _windows:        https://ceccopierangiolieugenio.github.io/pyTermTk/TTkWidgets/window.html
.. _TTkLabel:       https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.label.html#TermTk.TTkWidgets.label.TTkLabel
.. _TTkLayouts:     https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/index.html
.. _TTkLayout:      https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/layout.html#TermTk.TTkLayouts.layout.TTkLayout
.. _TTkHBoxLayout:  https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/boxlayout.html#TermTk.TTkLayouts.boxlayout.TTkHBoxLayout
.. _TTkVBoxLayout:  https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/boxlayout.html#TermTk.TTkLayouts.boxlayout.TTkVBoxLayout
.. _TTkGridLayout:  https://ceccopierangiolieugenio.github.io/pyTermTk/TTkLayouts/gridlayout.html#TermTk.TTkLayouts.gridlayout.TTkGridLayout

.. _Layout Example:         https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/layout/example1.simple.layout.py
.. _VBox Example:           https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/layout/example2.simple.vbox.py
.. _HBox Example:           https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/layout/example3.simple.hbox.py
.. _Grid Example:           https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/layout/example4.simple.grid.py
.. _Nested Layouts Example: https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/layout/example5.nested.layouts.py
.. _`row/colspan Example`:  https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/layout/example6.grid.span.py

=============================================================================
pyTermTk_ - Signal & Slots
=============================================================================

Signals and slots are used for communication between objects.

Intro
=====

|  The `TermTk Signal&Slots`_ is more than heavily inspired by `Qt5 Signal&Slots`_
|  https://doc.qt.io/qt-5/signalsandslots.html

|  In GUI programming, when we change one widget, we often want another widget to be notified.
|  More generally, we want objects of any kind to be able to communicate with one another.
|  For example, if a user clicks a Close button, we probably want the window's close() function to be called.

Signal and Slots
================

|  A signal is emitted when a particular event occurs.
|  A slot is a function that is called in response to a particular signal.
|  TermTk_'s TTkWidgets_ have many predefined signals/slots, but it is possible to subclass any TTkWidgets_ and add our own signals/slots to them.

.. image:: https://ceccopierangiolieugenio.github.io/pyTermTk/_images/Signal.Slots.001.svg

Examples
========

Example 1 - basic signal slots
------------------------------

From `example1.basic.signalslots.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/signalslots/example1.basic.signalslots.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=tutorial/signalslots/example1.basic.signalslots.py>`__):

.. code:: python

    import TermTk as ttk

    ttk.TTkLog.use_default_stdout_logging()

        # define 2 signals with different signatures
    signal = ttk.pyTTkSignal()
    otherSignal = ttk.pyTTkSignal(int)


        # Define a slot with no input as signature
    @ttk.pyTTkSlot()
    def slot():
        ttk.TTkLog.debug("Received a simple signal")

        # Define 2 slots with "int" as input signature
    @ttk.pyTTkSlot(int)
    def otherSlot(val):
        ttk.TTkLog.debug(f"[otherSlot] Received a valued signal, val:{val}")

    @ttk.pyTTkSlot(int)
    def anotherSlot(val):
        ttk.TTkLog.debug(f"[anootherSlot] Received a valued signal, val:{val}")


        # connect the signals to the proper slot
    signal.connect(slot)
    otherSignal.connect(otherSlot)
    otherSignal.connect(anotherSlot)

        # Test the signals
    ttk.TTkLog.debug("Emit a simple signal")
    signal.emit()
    ttk.TTkLog.debug("Emit a valued signal")
    otherSignal.emit(123)

The above code produces the following output

::

     $  tutorial/signalslots/example1.basic.signalslots.py
    DEBUG:(MainThread) tutorial/signalslots/example1.basic.signalslots.py:54 Emit a simple signal
    DEBUG:(MainThread) tutorial/signalslots/example1.basic.signalslots.py:37 Received a simple signal
    DEBUG:(MainThread) tutorial/signalslots/example1.basic.signalslots.py:56 Emit a valued signal
    DEBUG:(MainThread) tutorial/signalslots/example1.basic.signalslots.py:42 [otherSlot] Received a valued signal, val:123
    DEBUG:(MainThread) tutorial/signalslots/example1.basic.signalslots.py:45 [anootherSlot] Received a valued signal, val:123


Example 2 - Use widgets signals and slots
-----------------------------------------

From `example2.widgets.signalslots.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/signalslots/example2.widgets.signalslots.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=tutorial/signalslots/example2.widgets.signalslots.py>`__):

.. code:: python

    import TermTk as ttk

    root = ttk.TTk()

        # Create a window with a logviewer
    logWin = ttk.TTkWindow(parent=root,pos = (10,2), size=(80,20), title="LogViewer Window", border=True, layout=ttk.TTkVBoxLayout())
    ttk.TTkLogViewer(parent=logWin)

        # Create 2 buttons
    btnShow = ttk.TTkButton(parent=root, text="Show", pos=(0,0), size=(10,3), border=True)
    btnHide = ttk.TTkButton(parent=root, text="Hide", pos=(0,3), size=(10,3), border=True)

        # Connect the btnShow's "clicked" signal with the window's "show" slot
    btnShow.clicked.connect(logWin.show)
        # Connect the btnHide's "clicked" signal with the window's "hide" slot
    btnHide.clicked.connect(logWin.hide)

    root.mainloop()

A screenshot is totally useless for this example but for the sack of completemess, the above code produces the following output

::

    ┌────────┐
    │  Show  │
    ╘════════╛╔══════════════════════════════════════════════════════════════════════════════╗
    ┌────────┐║ LogViewer Window                                                             ║
    │  Hide  │╟──────────────────────────────────────────────────────────────────────────────╢
    ╘════════╛║                                                                              ║
              ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:70 Starting M║
              ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:80 Signal Eve║
              ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:65 fps: 33   ║
              ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:65 fps: 34   ║
              ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:65 fps: 34   ║
              ║                                                                              ║
              ║                                                                              ║
              ║                                                                              ║
              ║                                                                              ║
              ║                                                                              ║
              ║                                                                              ║
              ║                                                                              ║
              ║                                                                              ║
              ║                                                                              ║
              ║◀▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┄┄┄┄┄┄┄┄┄┄┄▶║
              ╚══════════════════════════════════════════════════════════════════════════════╝
