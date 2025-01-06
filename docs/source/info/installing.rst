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

Windows10 Install
~~~~~~~~~~~~~~~~~

.. raw:: html

    <iframe width="600" height="450" src="https://www.youtube.com/embed/1nQ3P3bgKNY?si=aagKoOBKtMi8MT_1&cc_load_policy=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


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

* Main demo        :ttk:sbIntLink:`demo,demo.py`
* paint demo       :ttk:sbIntLink:`demo,paint.py`
* ttkode prototype :ttk:sbIntLink:`demo,ttkode.py`

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

* Text Editor   :ttk:sbIntLink:`demo/showcase,textedit.py`
* Animation     :ttk:sbIntLink:`demo/showcase,animation.01.py`
* color picker  :ttk:sbIntLink:`demo/showcase,colorpicker.py`
* file picker   :ttk:sbIntLink:`demo/showcase,filepicker.py`
* drag & drop   :ttk:sbIntLink:`demo/showcase,dragndrop.py`
* d&d with tabs :ttk:sbIntLink:`demo/showcase,dndtabs.py`
* d&d with list :ttk:sbIntLink:`demo/showcase,list.py`
* base widgets  :ttk:sbIntLink:`demo/showcase,formwidgets02.py`
* messagebox    :ttk:sbIntLink:`demo/showcase,messagebox.py`
* splitter      :ttk:sbIntLink:`demo/showcase,splitter.py`
* Windows       :ttk:sbIntLink:`demo/showcase,windowsflags.py`
* AppTemplate   :ttk:sbIntLink:`demo/showcase,apptemplate.py`
* ToolTip       :ttk:sbIntLink:`tests/t.ui,test.ui.026.toolTip.py`

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