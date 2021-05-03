.. _pyTermTk:  https://github.com/ceccopierangiolieugenio/pyTermTk
.. _TermTk:    https://github.com/ceccopierangiolieugenio/pyTermTk

.. _TTkLog:       https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkCore.log.html
.. _TTkLogViewer: https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkTestWidgets.logviewer.html

===================
pyTermTk_ - Logging
===================

Intro
=====

The TTkLog_ class provide a set of api to allow and configure the logging.

Examples
========

Example 1 - Log to file
-----------------------

From `example1.logtofile.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/logging/example1.logtofile.py>`_

.. code:: python

    import TermTk as ttk

        # session.log is used by default
    ttk.TTkLog.use_default_file_logging()

        # Push some Debug messages
    ttk.TTkLog.info(    "Test Info Message")
    ttk.TTkLog.debug(   "Test Debug Message")
    ttk.TTkLog.error(   "Test Error Message")
    ttk.TTkLog.warn(    "Test Warning Message")
    ttk.TTkLog.critical("Test Critical Message")


Example 2 - Log to stdout
-------------------------

From `example2.logtostdout.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/logging/example2.logtostdout.py>`_

.. code:: python

    import TermTk as ttk

    ttk.TTkLog.use_default_stdout_logging()

        # Push some Debug messages
    ttk.TTkLog.info(    "Test Info Message")
    ttk.TTkLog.debug(   "Test Debug Message")
    ttk.TTkLog.error(   "Test Error Message")
    ttk.TTkLog.warn(    "Test Warning Message")
    ttk.TTkLog.critical("Test Critical Message")
    ttk.TTkLog.fatal(   "Test Fatal Message")

Example 3 - custom logging
--------------------------

From `example3.customlogging.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/logging/example3.customlogging.py>`_

.. code:: python

    import TermTk as ttk

        # define the callback used to process the log message
    def message_handler(mode, context, message):
        msgType = "NONE"
        if mode == ttk.TTkLog.InfoMsg:       msgType = "[INFO]"
        elif mode == ttk.TTkLog.WarningMsg:  msgType = "[WARNING]"
        elif mode == ttk.TTkLog.CriticalMsg: msgType = "[CRITICAL]"
        elif mode == ttk.TTkLog.FatalMsg:    msgType = "[FATAL]"
        elif mode == ttk.TTkLog.ErrorMsg:    msgType = "[ERROR]"
        print(f"{msgType} {context.file} {message}")

        # Register the callback to the message handler
    ttk.TTkLog.installMessageHandler(message_handler)

        # Push some Debug messages
    ttk.TTkLog.info(    "Test Info Message")
    ttk.TTkLog.debug(   "Test Debug Message")
    ttk.TTkLog.error(   "Test Error Message")
    ttk.TTkLog.warn(    "Test Warning Message")
    ttk.TTkLog.critical("Test Critical Message")
    ttk.TTkLog.fatal(   "Test Fatal Message")

Example 4 - Use TTkLogViewer_ widget
--------------------------------------------------

From `example4.ttklogviewer.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/logging/example4.ttklogviewer.py>`_

.. code:: python

    import TermTk as ttk

    root = ttk.TTk()

        # Create a window and attach it to the root (parent=root)
    logWin = ttk.TTkWindow(parent=root,pos = (1,1), size=(80,20), title="LogViewer Window", border=True, layout=ttk.TTkVBoxLayout())

        # Attach the logViewer widget to the window
    ttk.TTkLogViewer(parent=logWin)

        # Push some Debug messages
    ttk.TTkLog.info(    "Test Info Message")
    ttk.TTkLog.debug(   "Test Debug Message")
    ttk.TTkLog.error(   "Test Error Message")
    ttk.TTkLog.warn(    "Test Warning Message")
    ttk.TTkLog.critical("Test Critical Message")
    ttk.TTkLog.fatal(   "Test Fatal Message")

        # Start the Main loop
    root.mainloop()

The above code produces the following output

::

    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║ LogViewer Window                                                             ║
    ╟──────────────────────────────────────────────────────────────────────────────╢
    ║                                                                              ║
    ║INFO : tutorial/logging/example4.ttklogviewer.py:36 Test Info Message         ║
    ║DEBUG: tutorial/logging/example4.ttklogviewer.py:37 Test Debug Message        ║
    ║ERROR: tutorial/logging/example4.ttklogviewer.py:38 Test Error Message        ║
    ║WARNING : tutorial/logging/example4.ttklogviewer.py:39 Test Warning Message   ║
    ║CRITICAL: tutorial/logging/example4.ttklogviewer.py:40 Test Critical Message  ║
    ║FATAL: tutorial/logging/example4.ttklogviewer.py:41 Test Fatal Message        ║
    ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:70 Starting M║
    ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:80 Signal Eve║
    ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:65 fps: 33   ║
    ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:65 fps: 34   ║
    ║DEBUG: _/.venv/lib/python3.8/site-packages/TermTk/TTkCore/ttk.py:65 fps: 34   ║
    ║                                                                              ║
    ║                                                                              ║
    ║                                                                              ║
    ║◀▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┄┄┄┄┄┄┄┄┄┄┄▶║
    ╚══════════════════════════════════════════════════════════════════════════════╝
