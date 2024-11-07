.. _pyTermTk:  https://github.com/ceccopierangiolieugenio/pyTermTk
.. _TermTk:    https://github.com/ceccopierangiolieugenio/pyTermTk

.. _TTkLog:       https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkCore.log.html
.. _TTkLogViewer: https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkTestWidgets.logviewer.html

.. _TTkLabel:      https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.label.html
.. _TTkButton:     https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.button.html
.. _TTkGridLayout: https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkLayouts.gridlayout.html

===================
pyTermTk_ - Your first Calculator
===================

Intro
=====

This example shows how to use `signals and slots <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_ to implement the functionality of a calculator widget, and how to use TTkGridLayout_ to place child widgets in a grid.
Due to the modular nature of pyTermTk_, the same result may be achieved in multiple ways, for the sack of simplicity I will use a procedural approach avoiding to create a calculator widget.

Design
======

First of all we need a rough idea about the layout we want to achieve.
Thanks to my amazing `paint.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/paint.py>`_ I draw my idea and I used it to check the grid placement of any widget

::

    Col:  0      1       2       3
     |-------|-------|-------|-------|   Row:
    ╔═════════════════════════════════╗ ---
    ║ ┌─────────────────────────────┐ ║  |
    ║ │ r:0,c:0,  rspan:1, cspan:4  │ ║  | 0
    ║ └─────────────────────────────┘ ║ ---
    ║ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ║  |
    ║ │ 1,0 │ │ 1,1 │ │ 1,2 │ │ 1,3 │ ║  | 1
    ║ └─────┘ └─────┘ └─────┘ └─────┘ ║ ---
    ║ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ║  |
    ║ │ 2,0 │ │ 2,1 │ │ 2,2 │ │ 2,3 │ ║  | 2
    ║ └─────┘ └─────┘ └─────┘ └─────┘ ║ ---
    ║ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ║  |
    ║ │ 3,0 │ │ 3,1 │ │ 3,2 │ │ 3,3 │ ║  | 3
    ║ └─────┘ └─────┘ └─────┘ │     │ ║ ---
    ║ ┌─────────────┐ ┌─────┐ │ 2,1 │ ║  |
    ║ │ 4,0   1,2   │ │ 4,2 │ │     │ ║  | 4
    ║ └─────────────┘ └─────┘ └─────┘ ║ ---
    ╚═════════════════════════════════╝

Start Coding
============

Initialize the window
---------------------

From `calculator.001.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/calculator/calculator.001.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=tutorial/calculator/calculator.001.py>`__):

.. code:: bash

    # If you want to try without installation, run from the pyTermTk root folder
    PYTHONPATH=`pwd` tutorial/calculator/calculator.001.py

First thing first I need a parent widget with a grid layout that I can use to place the elements of my calculator

.. code:: python

    import TermTk as ttk

        # Create a root object (it is a widget that represent the terminal)
    root = ttk.TTk()

        # Create a window and attach it to the root (parent=root)
    calculatorWin = ttk.TTkWindow(parent=root, pos=(1,1), size=(30,17), title="My first Calculator")

        # Create a grid layout and set it as default for the window
    winLayout = ttk.TTkGridLayout()
    calculatorWin.setLayout(winLayout)

Once we have out layout object (**winLayout**) ready we can add all the widgets of calculator to it


Add all the widgets of calculator to it
---------------------------------------

From `calculator.002.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/calculator/calculator.002.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=tutorial/calculator/calculator.002.py>`__):

Based on the positions and sizes defined in the `design layout <#design>`_, I place all the widgets on the TTkGridLayout_ (**winLayout**)

.. code:: bash

    # If you want to try without installation, run from the pyTermTk root folder
    PYTHONPATH=`pwd` tutorial/calculator/calculator.002.py

.. code:: python

        # Define the Label and attach it to the grid layout at
        # Position (Row/Col) (0,0) and (Row/Col)Span (1,4)
        # I force the Max Height to 1 in order to avoid this widget to resize vertically
    resLabel = ttk.TTkLabel(text="Results", maxHeight=1)
    winLayout.addWidget(resLabel, 0,0, 1,4)

        # Define the Numeric Buttons and attach them to the grid layout
    btn1 = ttk.TTkButton(border=True, text="1")
    btn2 = ttk.TTkButton(border=True, text="2")
    btn3 = ttk.TTkButton(border=True, text="3")
    btn4 = ttk.TTkButton(border=True, text="4")
    btn5 = ttk.TTkButton(border=True, text="5")
    btn6 = ttk.TTkButton(border=True, text="6")
    btn7 = ttk.TTkButton(border=True, text="7")
    btn8 = ttk.TTkButton(border=True, text="8")
    btn9 = ttk.TTkButton(border=True, text="9")

    winLayout.addWidget(btn1, 1,0) # Colspan/Rowspan are defaulted to 1 if not specified
    winLayout.addWidget(btn2, 1,1)
    winLayout.addWidget(btn3, 1,2)
    winLayout.addWidget(btn4, 2,0)
    winLayout.addWidget(btn5, 2,1)
    winLayout.addWidget(btn6, 2,2)
    winLayout.addWidget(btn7, 3,0)
    winLayout.addWidget(btn8, 3,1)
    winLayout.addWidget(btn9, 3,2)

        # Adding the "0" button on the bottom which alignment is
        # Position (Row/Col) (4,0) (Row/Col)span (1,2)
        # Just to show off I am using another way to attach it to the grid layout
    winLayout.addWidget(btn0:=ttk.TTkButton(border=True, text="0"), 4,0, 1,2)

        # Define the 2 algebraic buttons
    winLayout.addWidget(btnAdd:=ttk.TTkButton(border=True, text="+"), 1,3)
    winLayout.addWidget(btnSub:=ttk.TTkButton(border=True, text="-"), 2,3)

        # The Enter "=" button (2 rows wide )
    winLayout.addWidget(btnRes:=ttk.TTkButton(border=True, text="="), 3,3, 2,1)

        # Last but not least an extrabutton just for  fun
    winLayout.addWidget(mysteryButton:=ttk.TTkButton(border=True, text="?"), 4,2)

This code will produce this result:

::

    ╔════════════════════════════╗
    ║ My first Calculator        ║
    ╟────────────────────────────╢
    ║Results                     ║
    ║┌─────┐┌─────┐┌─────┐┌─────┐║
    ║│  1  ││  2  ││  3  ││  +  │║
    ║╘═════╛╘═════╛╘═════╛╘═════╛║
    ║┌─────┐┌─────┐┌─────┐┌─────┐║
    ║│  4  ││  5  ││  6  ││  -  │║
    ║╘═════╛╘═════╛╘═════╛╘═════╛║
    ║┌─────┐┌─────┐┌─────┐┌─────┐║
    ║│  7  ││  8  ││  9  ││     │║
    ║╘═════╛╘═════╛╘═════╛│  =  │║
    ║┌────────────┐┌─────┐│     │║
    ║│     0      ││  ?  ││     │║
    ║╘════════════╛╘═════╛╘═════╛║
    ╚════════════════════════════╝

Cool isn't it?


Numeric Button Events
---------------------------------------

From `calculator.003.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/calculator/calculator.003.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=tutorial/calculator/calculator.003.py>`__):

.. code:: bash

    # If you want to try without installation, run from the pyTermTk root folder
    PYTHONPATH=`pwd` tutorial/calculator/calculator.003.py

.. code:: python

        # I am defining a simlpe structure that can be used to store
        # the mathematical elements of the formulae
    mathElements = {'a':None, 'b':None, 'operation':None}

        # This is a simple callback that I can use to store the numbers
        # I didn't include extra logic because out of the scope of this tutorial
    def setFactor(value):
        if mathElements['operation'] is None:
            mathElements['a'] = mathElements['a']*10+value
            # Display the value in the label
            resLabel.setText(f"{mathElements['a']}")
        else:
            mathElements['b'] = mathElements['b']*10+value
            # Display the value in the label
            resLabel.setText(f"{mathElements['b']}")

        # I am using a lambda function to redirect the click event to the
        # proper "setFactor" callback, this is due to the fact that the
        # "clicked" signal does not return any object or information that
        # can be used to identify which button has been pressed
        # different approaches are possible, i.e. create a separate function
        # for each button
    btn0.clicked.connect(lambda : setFactor(0))
    btn1.clicked.connect(lambda : setFactor(1))
    btn2.clicked.connect(lambda : setFactor(2))
    btn3.clicked.connect(lambda : setFactor(3))
    btn4.clicked.connect(lambda : setFactor(4))
    btn5.clicked.connect(lambda : setFactor(5))
    btn6.clicked.connect(lambda : setFactor(6))
    btn7.clicked.connect(lambda : setFactor(7))
    btn8.clicked.connect(lambda : setFactor(8))
    btn9.clicked.connect(lambda : setFactor(9))


Operation and results events
----------------------------

From `calculator.004.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/calculator/calculator.004.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=tutorial/calculator/calculator.004.py>`__):

.. code:: bash

    # If you want to try without installation, run from the pyTermTk root folder
    PYTHONPATH=`pwd` tutorial/calculator/calculator.004.py

.. code:: python

        # Define 2 slots to handle the Add and Sub operations
    @pyTTkSlot()
    def setOperationAdd():
        mathElements['operation'] = "ADD"

    @pyTTkSlot()
    def setOperationSub():
        mathElements['operation'] = "SUB"

        # Connect them to the clicked signal of the buttons
    btnAdd.clicked.connect(setOperationAdd)
    btnSub.clicked.connect(setOperationSub)

        # Same for the "=" button
    @pyTTkSlot()
    def executeOperation():
        if mathElements['operation'] is not None:
            if mathElements['operation'] == "ADD":
                res = mathElements['a'] + mathElements['b']
                resLabel.setText(f"{mathElements['a']} + {mathElements['b']} = {res}")
            else: # "SUB" Routine
                res = mathElements['a'] - mathElements['b']
                resLabel.setText(f"{mathElements['a']} - {mathElements['b']} = {res}")
            # reset the values
            mathElements['a'] = res
            mathElements['b'] = 0
            mathElements['operation'] = None

    btnRes.clicked.connect(executeOperation)


Beware the Mystery Button
-----------------------------------------

From `calculator.005.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/calculator/calculator.005.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=tutorial/calculator/calculator.005.py>`__):

.. code:: bash

    # If you want to try without installation, run from the pyTermTk root folder
    PYTHONPATH=`pwd` tutorial/calculator/calculator.005.py

.. code:: python

    @pyTTkSlot()
    def showAboytWindow():
        # I am using the overlay helper to show the
        # About window on top of the screen
        # it will be closed once the focus is lost
        ttk.TTkHelper.overlay(mysteryButton, ttk.TTkAbout(), -2, -1)

    mysteryButton.clicked.connect(showAboytWindow)

Press the Mystery "?" Button if you dare!!!

::

    ╔═══════════════════════════════════════════╗
    ║ My first Calculator                       ║
    ╟───────────────────────────────────────────╢
    ║1 + 2 = 3                                  ║
    ║┌─────────┐┌────────┐┌─────────┐┌─────────┐║
    ║│    1    ││   2    ││    3    ││    +    │║
    ║╘═════════╛╘════════╛╘═════════╛╘═════════╛║
    ║┌─────────┐┌────────┐┌─────────┐┌─────────┐║
    ║│    4    ││   5    ││    6    ││    -    │║
    ║│         ││  ╔═════════════════════════════════════════════════════╗
    ║╘═════════╛╘══║ About...                                            ║
    ║┌─────────┐┌──╟─────────────────────────────────────────────────────╢
    ║│    7    ││  ║   ▝▀▄           ████████╗            ████████╗      ║
    ║│         ││  ║ ▗▄▀▜▀▘▄▄▖       ╚══██╔══╝            ╚══██╔══╝      ║
    ║╘═════════╛╘══║▐▐▛▄▐▀▌▝▘▀          ██║  ▄▄  ▄ ▄▄ ▄▄▖▄▖  ██║ █ ▗▖    ║
    ║┌─────────────║▝▀▌▜▝▀▘▌▌   ▞▀▚ ▖▗  ██║ █▄▄█ █▀▘  █ █ █  ██║ █▟▘     ║
    ║│         0   ║ ▗▗▞▜▀▌▗▌▖  ▙▄▞▐▄▟  ██║ ▀▄▄▖ █    █ ▝ █  ██║ █ ▀▄    ║
    ║│             ║ ▝▐▙▟▟▌▟▌▌  ▌    ▐  ╚═╝                  ╚═╝         ║
    ║╘═════════════║  ▐▐▌▗▌▘▌▌    ▚▄▄▘   Version: 0.7.0a16               ║
    ╚══════════════║  ▝▐▌▐▖▜▌▌                                           ║
                   ║  ▝▐▀▝▘▀▘▘ Powered By, Eugenio Parodi                ║
                   ║   ▝▀▀▀▀▘                                            ║
                   ║ https://github.com/ceccopierangiolieugenio/pyTermTk ║
                   ╚═════════════════════════════════════════════════════╝

Well, with colors is another thing!!!
