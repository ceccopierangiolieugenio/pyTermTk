.. _pyTermTk:    https://github.com/ceccopierangiolieugenio/pyTermTk
.. _TermTk:      https://github.com/ceccopierangiolieugenio/pyTermTk
.. _ttkDesigner: https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/apps/ttkDesigner

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

.. _TTkUILoader:    https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkUiTools.uiloader.html#TermTk.TTkUiTools.uiloader.TTkUiLoader

.. contents::


.. _TextEdit_ttkDesigner-Tutorial_Intro:


===================
ttkDesigner_ - Your first TextEditor
===================


Start a new project
===================

- Create a new Window (**File** -> **New** -> **New Window**)
- Set your favourite window params:

  - Your preferred size
  - Some catcy Title
  - An Amazing Name - (This is the unique name that will be used to identify this Widget_)
  - Change the Layout to TTkGridLayout_ (This will allow all the components to be placed in a grid aligned to the content of the window_)
  - Add the "Maximize Button" through the Window Flags (I forgot to add this step in the video)

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/236455166-7c4905b9-572e-49e6-9f71-12fa5545fd90.mp4"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/236455166-7c4905b9-572e-49e6-9f71-12fa5545fd90.mp4"
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
        src="https://user-images.githubusercontent.com/8876552/236455152-4f7440c3-868c-47ce-9c6c-56047b9348ea.mp4"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/236455152-4f7440c3-868c-47ce-9c6c-56047b9348ea.mp4"
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
        src="https://user-images.githubusercontent.com/8876552/236455144-dae0cae7-42f0-4db9-983d-cedc980a8dad.mp4"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/236455144-dae0cae7-42f0-4db9-983d-cedc980a8dad.mp4"
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
        src="https://user-images.githubusercontent.com/8876552/236455133-2f13549a-5096-4ae0-87f7-55d419b220dd.mp4"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/236455133-2f13549a-5096-4ae0-87f7-55d419b220dd.mp4"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

`textEdit.04.tui.json <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.04.tui.json>`_



Add few extra controls (Open/Save/Color)
========================================

I used those emoji as file open/save text 📂 💾

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/236455116-57cfe842-e581-4dc7-ac74-dead0e440793.mp4"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/236455116-57cfe842-e581-4dc7-ac74-dead0e440793.mp4"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

`textEdit.05.tui.json <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.05.tui.json>`_



Link the Events/Slots for the color feature
===========================================

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/236455110-faac9646-e025-43bd-8833-624b9339db1b.mp4"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/236455110-faac9646-e025-43bd-8833-624b9339db1b.mp4"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

`textEdit.06.tui.json <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/textEdit.06.tui.json>`_



Preview and Quick Export
========================

.. raw:: html

    <video width="800"
        src="https://user-images.githubusercontent.com/8876552/236455105-25cd73a3-901f-4b96-a729-0723d9f80a93.mp4"
        data-canonical-src="https://user-images.githubusercontent.com/8876552/236455105-25cd73a3-901f-4b96-a729-0723d9f80a93.mp4"
        controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" ></video>

Exported: `texteditor.01.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/texteditor.01.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=tutorial/ttkDesigner/textEdit/texteditor.01.py>`__):

.. code:: bash

    # If you want to try without installation, run from the pyTermTk root folder
    PYTHONPATH=`pwd`  python3  tutorial/ttkDesigner/textEdit/texteditor.01.py


Import this widget in your project
==================================

The TTkUiLoader_ provide different methods to use the content generated by ttkDesigner_

Each method is capable of (1) returning a new Widget_ or (2) extending a custom defined widget

Option 1) Include the Open/Save routine and link them to the widget
-------------------------------------------------------------------

Once (quick)exported the code, we need to define the appropriate routines and link them to the file(open/save) pickers `signals <https://ceccopierangiolieugenio.github.io/pyTermTk/autogen.TermTk/TermTk.TTkWidgets.TTkPickers.filepicker.html#TermTk.TTkWidgets.TTkPickers.filepicker.TTkFileButtonPicker.filePicked>`__

`texteditor.02.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/texteditor.02.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=tutorial/ttkDesigner/textEdit/texteditor.02.py>`__):

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

Option 2) Extend a custom widget including the open/save methods
----------------------------------------------------------------

`texteditor.03.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tutorial/ttkDesigner/textEdit/texteditor.03.py>`_
(`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=tutorial/ttkDesigner/textEdit/texteditor.03.py>`__):

.. code:: bash

    # If you want to try without installation, run from the pyTermTk root folder
    PYTHONPATH=`pwd`  python3  tutorial/ttkDesigner/textEdit/texteditor.03.py


.. code:: python

    class MyTextEditor(TTkWindow):
        def __init__(self):
            # The "TTkUiLoader" is responsible to init this custom object
            # and extend it to the "textEditWindow" created in this tutorial
            # NOTE: no "super().__init__()" is required
            TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(
                #  <Copy here the Compressed string representing the object>
                ), self)

            # Connect the open routine to the (open)"filePicked" event
            self.getWidgetByName("BtnOpen").filePicked.connect(self.openRoutine)
            # Connect the save routine to the (save)"filePicked" event
            self.getWidgetByName("BtnSave").filePicked.connect(self.saveRoutine)

        # This is a generic routine to open/read a file
        # and push the content to the "TextEdit" widget
        pyTTkSlot(str)
        def openRoutine(self, fileName):
            textEdit = self.getWidgetByName("TextEdit")
            with open(fileName) as fp:
                textEdit.setText(fp.read())

        # This is a generic routine to save the content of
        # the "TextEdit" widget to the chosen file
        pyTTkSlot(str)
        def saveRoutine(self, fileName):
            textEdit = self.getWidgetByName("TextEdit")
            with open(fileName, 'w') as fp:
                fp.write(textEdit.toPlainText())
