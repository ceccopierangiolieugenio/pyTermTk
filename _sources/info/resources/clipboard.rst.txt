.. _clipboard:

=========
Clipboard
=========

.. _pyTermTk:  https://github.com/ceccopierangiolieugenio/pyTermTk


pyTermTk_ include a clipboard wrapper :class:`~TermTk.TTkGui.clipboard.TTkClipboard`, around any of the following libraries:

- `copykitten <https://github.com/klavionik/copykitten>`_ - Robust, dependency-free way to use the system clipboard in Python.
- `pyperclip <https://github.com/asweigart/pyperclip>`_ - Python module for cross-platform clipboard functions.
- `pyperclip3 <https://pypi.org/project/pyperclip3>`_ / `pyclip <https://github.com/spyoungtech/pyclip>`_  - Cross-platform Clipboard module for Python with binary support.
- `clipboard <https://github.com/terryyin/clipboard>`_  - A cross platform clipboard operation library of Python. Works for Windows, Mac and Linux.

.. raw:: html

    <video width="800"
        src="https://github.com/ceccopierangiolieugenio/pyTermTk/assets/8876552/55978bef-be18-4912-a4f1-4b26845325fa"
        data-canonical-src="https://github.com/ceccopierangiolieugenio/pyTermTk/assets/8876552/55978bef-be18-4912-a4f1-4b26845325fa"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

The basic pyTermTk_ does not include any of those clipboard managers.
An internal implementation whitin the scope of the app itself is still available.

If any of the previous listed clipboard managers are installed, pyTermTk_ is able to automatically detect and use them.

i.e.

.. code:: bash

    # Assuming no clipboard managers are installed
    # you can still copy/paste between editors in this session
    # but no text is copied to/from the system clipboard
    python3 demo/showcase/textedit.py

    # if pyperclip is installed,
    # pyTermTk defaults the clipboard manager to this tool
    # any copy/paste is synced with the system clipboard
    # it is possible to copy/paste from/to an external editor
    pip install pyperclip
    python3 demo/showcase/textedit.py

-----
Usage
-----

Once initialized the clipboard manager, 2 apis are provided that can be used to access the clipboard (:class:`~TermTk.TTkGui.clipboard.TTkClipboard.setText`, :class:`~TermTk.TTkGui.clipboard.TTkClipboard.text`)

    .. code:: python

        from TermTk import TTkClipboard

        # Initialize the clipboard manager
        clipboard = TTkClipboard()

        # Push some text to the clipboard
        clipboard.setText("Example")

        # Get the text from the clipboard
        text = clipboard.text()