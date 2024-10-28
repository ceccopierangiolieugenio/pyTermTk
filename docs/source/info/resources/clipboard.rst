.. _clipboard:

=========
Clipboard
=========

.. _pyTermTk:  https://github.com/ceccopierangiolieugenio/pyTermTk


pyTermTk_ include a clipboard wrapper :py:class:`TTkClipboard`, around any of the following libraries:

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

Once initialized the clipboard manager, 2 apis are provided that can be used to access the clipboard (:py:class:`TTkClipboard.setText`, :py:class:`TTkClipboard.text`)

.. code:: python

    from TermTk import TTkClipboard

    # Initialize the clipboard manager
    clipboard = TTkClipboard()

    # Push some text to the clipboard
    clipboard.setText("Example")

    # Get the text from the clipboard
    text = clipboard.text()

------------------
Clipboard over ssh
------------------

As reported in `234# <https://github.com/ceccopierangiolieugenio/pyTermTk/issues/234#issuecomment-1930919647>`_, it is possible to share the clipboard enabling the X11 forwarding.


Terminal (Linux,osx)
~~~~~~~~~~~~~~~~~~~~

You can forward X11 using `ssh <https://www.man7.org/linux/man-pages/man1/ssh.1.html>`_

.. code:: bash

    # Enable X11 forwarding
    ssh -X <IP>

or

.. code:: bash

    # Enable trusted X11 forwarding
    ssh -Y <IP>

putty
~~~~~

It is possible to forward X11 via putty through these settings

.. image:: https://github.com/ceccopierangiolieugenio/pyTermTk/assets/8876552/1b7fea21-74f2-4351-9a9c-548aaa1581ca
