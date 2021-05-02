.. _pyTermTk:   https://github.com/ceccopierangiolieugenio/pyTermTk
.. _TTk:        https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkCore.ttk.html#TermTk.TTkCore.ttk.TTk
.. _mainloop(): https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkCore.ttk.html#TermTk.TTkCore.ttk.TTk.mainloop
.. _TTkLabel:   https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.label.html#TermTk.TTkWidgets.label.TTkLabel

=============================================================================
pyTermTk_ - Hello World
=============================================================================

Intro
=====

Creating a simple GUI application using pyTermTk_ involves the following steps:

  - Import TermTk package.
  - Create an TTk_ object.
  - Add a TTkLabel_ object in it with the caption "**hello world**" in the position (x=5,y=2).
  - Enter the mainloop of application by `mainloop()`_  method.

Examples
========

Example 1
---------

Following is the code to execute `helloworld.001.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/helloworld/helloworld.001.py>`_ in pyTermTk_:

.. code:: python

    import TermTk as ttk

    root = ttk.TTk()
    ttk.TTkLabel(parent=root, pos=(5,2), text="Hello World")
    root.mainloop()

The above code produces the following output

::

    Hello World

Example 2 - Your first Window
-----------------------------

Following is the code to execute `helloworld.002.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/helloworld/helloworld.002.py>`_ in pyTermTk_:

.. code:: python

    import TermTk as ttk

        # Create a root object (it is a widget that represent the terminal)
    root = ttk.TTk()

        # Create a window and attach it to the root (parent=root)
    helloWin = ttk.TTkWindow(parent=root,pos = (1,1), size=(30,10), title="Hello Window", border=True)

        # Define the Label and attach it to the window (parent=helloWin)
    ttk.TTkLabel(parent=helloWin, pos=(5,5), text="Hello World")

        # Start the Main loop
    root.mainloop()


The above code produces the following output (yuhuuuuu!!!)

::

    ╔════════════════════════════╗
    ║ Hello Window               ║
    ╟────────────────────────────╢
    ║                            ║
    ║                            ║
    ║    Hello World             ║
    ║                            ║
    ║                            ║
    ║                            ║
    ╚════════════════════════════╝

