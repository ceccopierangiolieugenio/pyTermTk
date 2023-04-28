.. _pyTermTk:    https://github.com/ceccopierangiolieugenio/pyTermTk
.. _TermTk:      https://github.com/ceccopierangiolieugenio/pyTermTk
.. _ttkDesigner: https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/ttkDesigner

.. _Widget:        https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.widget.html
.. _Textedit:      https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.texedit.html
.. _window:        https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.window.html
.. _button:        https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.button.html
.. _buttons:       https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.button.html

.. _layout:         https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkLayouts.html
.. _TTkLayouts:     https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkLayouts.html
.. _TTkLayout:      https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkLayouts.layout.html#ttklayout
.. _TTkHBoxLayout:  https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkLayouts.boxlayout.html#ttkhboxlayout
.. _TTkVBoxLayout:  https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkLayouts.boxlayout.html#ttkvboxlayout
.. _grid:           https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkLayouts.gridlayout.html#ttkgridlayout
.. _TTkGridLayout:  https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkLayouts.gridlayout.html#ttkgridlayout

===================
ttkDesigner_ - Your first TextEditor
===================


Start a new project
===================

- Create a new Window (**File** -> **New** -> **New Window**)
- Set the window params required:

  - Resize
  - title
  - Name - (This is the unique name that will be used to identify this Widget_)
  - Window flags (i.e. Maximize)
  - Layout to TTkGridLayout_ (This will allow all the components to be placed in a grid aligned to the content of the window_)
  - Add the "Maximize Button" through the Window Flags (I forgot to add this step in the video)

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/234842682-1ecd40dd-6829-47ff-bfb7-eae397553879.webm"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/234842682-1ecd40dd-6829-47ff-bfb7-eae397553879.webm"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

`textEdit.01.tui.json <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.01.tui.json>`_

.. code:: bash

    # You can quickly open this file using:
    ttkDesigner tutorial/ttkDesigner/textEdit/textEdit.01.tui.json



Add The first buttons (Undo,redo - Cut,Copy,Paste)
==================================================

- Define the **Undo**, **Redo** commands

 - Drag 2 buttons_ inside the window_ aligning them in the preferred grid_ position
 - Define the proper button Text ("**Undo**","**Redo**")
 - Choose a proper unique name (This step is not mandatory but useful to identify this Widget_)
 - Disable those buttons by default because at the beginning the Text Editor is not going to have any Undo/Redo Buffers (I forgot to add this step in the video)

- Define the **Cut**, **Copy**, **Paste** commands

  - Well, try to guess...

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/234842705-0252d988-047f-46a1-8241-7a4e710c3791.webm"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/234842705-0252d988-047f-46a1-8241-7a4e710c3791.webm"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

`textEdit.02.tui.json <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.02.tui.json>`_



Add the TextEdit widget
=======================

- Drag the TextEdit_ aligning it in the grid_ below any of the buttons_ previously placed

- | Expand the TextEdit_ widget in order to fill the entire area below the buttons_
  | Use the rainbow [🟥🟨🟩🩵🟦🦄] button to help identify the different widgets in the main window
- | Force the top grid to a fixed size (3 Chars)
  | In order to achieve this it is enough to force the MaxSize of any of the buttons in the top row to 3 Chars

- Check the line number, this will show the line number in the TextEdit_ when used

- Choose a proper unique name (This step is not mandatory but useful to identify this Widget_)

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/234842721-f9ae924e-0047-4ce3-b1e6-3e0c7d27cb38.webm"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/234842721-f9ae924e-0047-4ce3-b1e6-3e0c7d27cb38.webm"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

`textEdit.03.tui.json <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.03.tui.json>`_



Link the Events/Slots for the basic functionalities
===================================================

- | Connect the TextEdit `undo <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.texedit.html#TermTk.TTkWidgets.texedit.TTkTextEdit.undoAvailable>`__ / `redo <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.texedit.html#TermTk.TTkWidgets.texedit.TTkTextEdit.redoAvailable>`__ availability signals with the `setEnabled <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.widget.html#TermTk.TTkWidgets.widget.TTkWidget.setEnabled>`__ slots of the undo/redo buttons
  | This allow the TextEdit to control directly the availability status of the Buttons

- Connect the undo/redo buttons `clicked <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.button.html#TermTk.TTkWidgets.button.TTkButton.clicked>`__ event to the `undo <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.texedit.html#TermTk.TTkWidgets.texedit.TTkTextEdit.undo>`__ / `redo <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.texedit.html#TermTk.TTkWidgets.texedit.TTkTextEdit.redo>`__ slots of the TextEditor

- Same for the `Cut <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.texedit.html#TermTk.TTkWidgets.texedit.TTkTextEdit.cut>`__, `Copy <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.texedit.html#TermTk.TTkWidgets.texedit.TTkTextEdit.copy>`__, `Paste <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.texedit.html#TermTk.TTkWidgets.texedit.TTkTextEdit.paste>`__

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/234842736-fdf73508-2ef1-419e-9b30-6d262a0ff514.webm"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/234842736-fdf73508-2ef1-419e-9b30-6d262a0ff514.webm"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

`textEdit.04.tui.json <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.04.tui.json>`_



Add few extra controls (Open/Save/Color)
========================================

I used those emoji as file open/save text 📂 💾

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/234842758-dbd647ba-2596-4ec8-9a76-135435504505.webm"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/234842758-dbd647ba-2596-4ec8-9a76-135435504505.webm"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

`textEdit.05.tui.json <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.05.tui.json>`_



Link the Events/Slots for the color feature
===========================================

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/234842774-cf8c3fc3-4bb7-45ff-8e04-30a93aa343c6.webm"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/234842774-cf8c3fc3-4bb7-45ff-8e04-30a93aa343c6.webm"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

`textEdit.06.tui.json <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.06.tui.json>`_



Preview and Quick Export
========================

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/234842788-208e271a-e0b1-44f6-94b4-a62db00fd45a.webm"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/234842788-208e271a-e0b1-44f6-94b4-a62db00fd45a.webm"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

Exported: `texteditor.01.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/texteditor.01.py>`_
(`Try Online <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?fileUri=https://raw.githubusercontent.com/ceccopierangiolieugenio/pyTermTk/main/tutorial/ttkDesigner/textEdit/texteditor.01.py>`__)

.. code:: bash

    # If you want to try without installation, run from the pyTermTk root folder
    PYTHONPATH=`pwd`  python3  tutorial/ttkDesigner/textEdit/texteditor.01.py


Imclude the Open/Save routine
-------------------------------

Once (quick)exported the code, we need to define the appropriate routines and link them to the file(open/save) pickers `signals <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.TTkPickers.filepicker.html#TermTk.TTkWidgets.TTkPickers.filepicker.TTkFileButtonPicker.filePicked>`__

`texteditor.02.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/texteditor.02.py>`_
(`Try Online <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?fileUri=https://raw.githubusercontent.com/ceccopierangiolieugenio/pyTermTk/main/tutorial/ttkDesigner/textEdit/texteditor.02.py>`__)

.. code:: bash

    # If you want to try without installation, run from the pyTermTk root folder
    PYTHONPATH=`pwd`  python3  tutorial/ttkDesigner/textEdit/texteditor.02.py


.. code:: python

    # Retrieve the widgets we need to use
    btnOpen  = textEditWindow.getWidgetByName("BtnOpen")
    btnSave  = textEditWindow.getWidgetByName("BtnSave")
    textEdit = textEditWindow.getWidgetByName("TextEdit")


    # This is a generic routine to open/read a file
    # and push the content to the "TextEdit" widget
    pyTTkSlot(str)
    def openRoutine(fileName):
        with open(fileName) as fp:
            textEdit.setText(fp.read())

    # Connect the open routine to the (open)"filePicked" event
    btnOpen.filePicked.connect(openRoutine)


    # This is a generic routine to save the content of
    # the "TextEdit" widget to the chosen file
    pyTTkSlot(str)
    def saveRoutine(fileName):
        with open(fileName, 'w') as fp:
            fp.write(textEdit.toPlainText())

    # Connect the save routine to the (save)"filePicked" event
    btnSave.filePicked.connect(saveRoutine)
