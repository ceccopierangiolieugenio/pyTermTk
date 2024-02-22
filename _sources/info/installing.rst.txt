.. _pyTermTk:  https://github.com/ceccopierangiolieugenio/pyTermTk
.. _TermTk:    https://github.com/ceccopierangiolieugenio/pyTermTk

.. _install-installation:

============
Installation
============

pyTermTk_ is a self contained  library,
it does not require extra libraries to be used
and can be installed through :ref:`install-pypi`
or just :ref:`copying the TermTk folder<install-copy>` in the root folder of your project.



.. _install-pypi:

PyPi
----

It is possible to install pyTermTk with PyPi also inside a venv environment

User Install
~~~~~~~~~~~~

.. code:: bash

    # User/Global Install
    pip3 install --upgrade pyTermTk

`Venv <https://docs.python.org/3/library/venv.html>`_ Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    # Create a venv environment in the ".venv" folder
    python3 -m venv .venv
    . .venv/bin/activate

    # Install inside the venv environment
    pip3 install --upgrade pyTermTk

    # ... Do you Stuff

    # Clear/Erase/GetRidOf the venv
    rm -rf .venv


.. _install-copy:

Copy TermTk folder
------------------

.. code:: bash

    git clone https://github.com/ceccopierangiolieugenio/pyTermTk.git
    cp -a pyTermTk/TermTk  <DEST_FOLDER>


.. _install-quickstart:

==========
Quickstart
==========

There are a number of demo apps and examples that can be executed in the repository

Demos
-----

Inside the `demo <https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/demo>`_
and `demo/showcase <https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/demo/showcase>`_
folders there are a number of examples that can be executed out of the box.

Prerequisites
~~~~~~~~~~~~~

Clone or `Download <https://github.com/ceccopierangiolieugenio/pyTermTk/releases>`_ the pyTermTk_ repo:

.. code:: bash

    # Clone and enter the folder
    git clone https://github.com/ceccopierangiolieugenio/pyTermTk.git
    cd pyTermTk


Demos
~~~~~

* Main demo        `demo.py   <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/demo.py>`_   (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/demo.py>`_)
* paint demo       `paint.py  <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/paint.py>`_  (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/paint.py>`_)
* ttkode prototype `ttkode.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/ttkode.py>`_ (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/ttkode.py>`_)

.. code:: bash

    # Run the main demo
    python3 demo/demo.py

    # Run the paint demo
    python3 demo/paint.py

    # Run the ttkode demo
    python3 demo/ttkode.py


Showcase
~~~~~~~~

**Highlight:**

* Text Editor   `textedit.py      <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/textedit.py>`_       (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/textedit.py>`_)
* Animation     `animation.01.py  <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/animation.01.py>`_   (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/animation.01.py>`_)
* color picker  `colorpicker.py   <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/colorpicker.py>`_    (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/colorpicker.py>`_)
* file picker   `filepicker.py    <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/filepicker.py>`_     (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/filepicker.py>`_)
* drag & drop   `dragndrop.py     <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/dragndrop.py>`_      (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/dragndrop.py>`_)
* d&d with tabs `dndtabs.py       <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/dndtabs.py>`_        (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/dndtabs.py>`_)
* d&d with list `list.py          <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/list.py>`_           (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/list.py>`_)
* base widgets  `formwidgets02.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/formwidgets02.py>`_  (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/formwidgets02.py>`_)
* messagebox    `messagebox.py    <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/messagebox.py>`_     (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/messagebox.py>`_)
* splitter      `splitter.py      <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/splitter.py>`_       (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/splitter.py>`_)
* Windows       `windowsflags.py  <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/windowsflags.py>`_   (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/windowsflags.py>`_)
* AppTemplate   `apptemplate.py   <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/apptemplate.py>`_    (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?filePath=demo/showcase/apptemplate.py>`_)
* Tooltip       `test.ui.026.toolTip.py  <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/tests/t.ui/test.ui.026.toolTip.py>`_   (`tryItOnline <https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html?fileUri=https://raw.githubusercontent.com/ceccopierangiolieugenio/pyTermTk/main/tests/t.ui/test.ui.026.toolTip.py>`_)

.. code:: bash

    # Demo - Text Editor
    python3 demo/showcase/textedit.py
    # Demo - Animation
    python3 demo/showcase/animation.01.py
    # Demo - color picker
    python3 demo/showcase/colorpicker.py
    # Demo - file picker
    python3 demo/showcase/filepicker.py
    # Demo - drag & drop
    python3 demo/showcase/dragndrop.py
    # Demo - d&d with tabs
    python3 demo/showcase/dndtabs.py
    # Demo - d&d with list
    python3 demo/showcase/list.py
    # Demo - base widgets
    python3 demo/showcase/formwidgets02.py
    # Demo - messagebox
    python3 demo/showcase/messagebox.py
    # Demo - splitter
    python3 demo/showcase/splitter.py
    # Demo - Windows
    python3 demo/showcase/windowsflags.py
    # Demo - AppTemplate
    python3 demo/showcase/apptemplate.py
    # Demo - Tooltip
    python3 tests/t.ui/test.ui.026.toolTip.py

    # Text edit with "Pygments" highlight integrated
    # it require pygments
    #   pip install pygments
    python3 tests/t.ui/test.ui.018.TextEdit.Pygments.py README.md