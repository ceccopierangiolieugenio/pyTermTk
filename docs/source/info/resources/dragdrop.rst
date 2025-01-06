.. _DnD:

=============
Drag and Drop
=============

Drag and drop provides a simple visual mechanism which users can use to transfer 
information between and within widgets. 
Drag and drop is similar in function to the clipboard's cut and paste mechanism.


.. image:: https://github.com/user-attachments/assets/857fd144-7a2a-4173-80b3-d135e62b8235


This document describes the basic drag and drop mechanism and outlines the 
approach used to enable it in custom controls. 
Drag and drop operations are also supported by many of TermTk's controls, 
such as :py:class:`TTkList` or :py:class:`TTkTabWidget`.


---------------------
Drag and Drop Classes
---------------------

These classes deal with drag and drop and the necessary mime type encoding and decoding.

.. currentmodule:: TermTk

.. autosummary::
   :caption: Classes:
   :template: custom-class-template.01.rst

   TTkGui.TTkDrag
   TTkGui.TTkDropEvent


--------
Dragging
--------

To start a drag, create a :py:class:`TTkDrag` object, and call its :py:meth:`TTkDrag.exec` function. 
In most applications, it is a good idea to begin a drag and drop operation only 
after a mouse button has been pressed and the cursor has been moved a certain distance. 
However, the simplest way to enable dragging from a widget is to reimplement 
the widget's :py:meth:`TTkWidget.mouseDragEvent` and start a drag and drop operation:

.. code:: python

    def mouseDragEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        if evt.key == ttk.TTkMouseEvent.LeftButton:
            drag = ttk.TTkDrag()
            drag.setData("LeftClick Drag")
            drag.exec()
        return True

Note that the :py:meth:`TTkDrag.exec` function does not block the main event loop.

.. seealso::

    * :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.01.basic.py`

--------
Dropping
--------

To be able to receive the content dropped on a widget, reimplement 
the :py:meth:`TDragEvents.dropEvent` event handler functions.

.. code:: python

    def dropEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        ttk.TTkLog.debug(f"Drop data: {evt.data()}, Position: {evt.pos()}")
        return True

.. seealso::

    * :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.01.basic.py`


------
Events
------

There are several events that can be used to customize the drag and drop operation:

* :py:meth:`TDragEvents.dropEvent`      - Called when a drag is dropped on the widget.
* :py:meth:`TDragEvents.dragEnterEvent` - Called when a drag enters the widget.
* :py:meth:`TDragEvents.dragMoveEvent`  - Called when a drag moves over the widget.
* :py:meth:`TDragEvents.dragLeaveEvent` - Called when a drag leaves the widget if :py:meth:`TDragEvents.dragEnterEvent` or :py:meth:`TDragEvents.dragMoveEvent` are andled inside the widget.

.. code:: python

    def dragEnterEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        ttk.TTkLog.debug(f"Drag Enter: {evt.data()}, Position: {evt.pos()}")
        return True

    def dragLeaveEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        ttk.TTkLog.debug(f"Drag Leave: {evt.data()}, Position: {evt.pos()}")
        return True

    def dragMoveEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        ttk.TTkLog.debug(f"Drag Move: {evt.data()}, Position: {evt.pos()}")
        return True

    def dropEvent(self, evt:ttk.TTkDnDEvent) -> bool:
        ttk.TTkLog.debug(f"Drop: {evt.data()}, Position: {evt.pos()}")
        return True

.. seealso::

    * :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.02.events.01.py`
    * :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.02.events.02.py`


------
Pixmap
------

The visual representation of the drag can be customized by setting a pixmap with :py:meth:`TTkDrag.setPixmap`.
By default the pixmap is initialized as a simple text string ("[...]") 
but it can be customized by using 
a :py:class:`TTkWidget` or :py:class:`TTkCanvas` as a pixmap.

.. image:: https://github.com/user-attachments/assets/7a23f5a9-444b-4e5a-878b-91c4b35ee8d8

You can use the same object as pixmap to have a visual feedback of the widget being dragged:

.. code:: python

    def mouseDragEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        drag = ttk.TTkDrag()
        drag.setPixmap(self)
        drag.exec()
        return True

Or define another :py:class:`TTkWidget` as pixmap:

.. code:: python

    def mouseDragEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        button = ttk.TTkButton(text=f"DnD", border=True, size=(25,5))
        drag = ttk.TTkDrag()
        drag.setPixmap(button)
        drag.exec()
        return True

Or use a :py:class:`TTkCanvas` as pixmap and draw the required content on it:

.. code:: python

    def mouseDragEvent(self, evt:ttk.TTkMouseEvent) -> bool:
        pixmap = ttk.TTkCanvas(width=17,height=5)

        pixmap.drawText(pos=(0,0),text="╭╼ TXT ╾────────╮")
        pixmap.drawText(pos=(0,1),text="│Lorem ipsum dol│")
        pixmap.drawText(pos=(0,2),text="│consectetur adi│")
        pixmap.drawText(pos=(0,3),text="│sed do eiusmod │")
        pixmap.drawText(pos=(0,4),text="╰────────╼ End ╾╯")

        drag = ttk.TTkDrag()
        drag.setPixmap(pixmap)
        drag.exec()
        return True

.. seealso::

    * :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.03.pixmap.01.py`
    * :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.03.pixmap.02.py`
    * :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.03.pixmap.03.py`
    * :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.03.pixmap.04.py`


-------
HotSpot
-------

The hotspot is the offset of the pixmap related to the cursor position.
It can be set using :py:meth:`TTkDrag.setHotSpot`. 
It is useful when the pixmap is not centered on the cursor or when you want to define an offset to allow 
the object being dragged from the clicked position:

.. image:: https://github.com/user-attachments/assets/8d999365-c787-4eff-84f2-03ef2b22c37a

.. code:: python

    def mouseDragEvent(self, evt:ttk. TTkMouseEvent) -> bool:
        drag = ttk.TTkDrag()
        drag.setHotSpot((evt.x, evt.y))
        drag.setPixmap(self)
        drag.exec()
        return True

.. seealso::

    * :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.04.hotSpot.01.py`

--------
Examples
--------

* :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.01.basic.py`
* :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.02.events.01.py`
* :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.02.events.02.py`
* :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.03.pixmap.01.py`
* :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.03.pixmap.02.py`
* :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.03.pixmap.03.py`
* :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.03.pixmap.04.py`
* :ttk:sbIntLink:`tutorial/examples/DragAndDrop/dnd.04.hotSpot.01.py`
