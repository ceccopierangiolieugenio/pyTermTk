.. pyTermTk documentation master file, created by
   sphinx-quickstart on Wed Oct 23 16:32:12 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. Add your content using ``reStructuredText`` syntax. See the
   https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
   documentation for details.

Welcome to pyTermTk_'s documentation!
=====================================

.. image:: https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/images/pyTermTk.HERO.800.png

Intro
-----

| pyTermTk_ is a Text-based user interface library (TUI_)
| Evolved from the discontinued project pyCuT_ and inspired by
| a mix of Qt5_, GTK_, and tkinter_ api definition with a touch of personal interpretation

.. _pyTermTk:  https://github.com/ceccopierangiolieugenio/pyTermTk
.. _TermTk:    https://github.com/ceccopierangiolieugenio/pyTermTk

.. _TUI:     https://en.wikipedia.org/wiki/Text-based_user_interface
.. _pyCuT:   https://github.com/ceccopierangiolieugenio/pyCuT
.. _Qt5:     https://www.riverbankcomputing.com/static/Docs/PyQt5/
.. _GTK:     https://pygobject.readthedocs.io/en/latest/
.. _tkinter: https://docs.python.org/3/library/tkinter.html

:doc:`info/features/index`
   Main features of this library

:ref:`features-alpha`
   New Features available but being reviewed and prone of future changes that may break the compatibility with the previous releases

:doc:`info/installing`
   How to install,Quickstart,Use,Deliver pyTermTk_

**Web Exporter**
   TBD (sorry😭)

:doc:`info/debug`
   Notes on how to Debug/Profile

.. :ref:`supported-dependencies`
   Supported project dependencies, like Python and Sphinx.

.. toctree::
   :maxdepth: 1
   :caption: Tutorials

   tutorial/000-examples

   tutorial/001-helloworld
   tutorial/002-layout
   tutorial/003-signalslots
   tutorial/004-logging
   tutorial/005-calculator

   tutorial/ttkDesigner/textEdit/README

.. Hidden TOCs

.. toctree::
   :caption: Features
   :maxdepth: 1
   :hidden:

   info/features/index
   info/features/crosscompatible
   info/features/widgets

.. toctree::
   :caption: Dev
   :maxdepth: 1
   :hidden:

   info/installing
   info/debug
   info/resources/index

API Reference
=============

.. currentmodule:: TermTk

.. autosummary::
   :caption: API Reference
   :toctree: _autosummary
   :template: custom-module-template.01.rst

   TTkAbstract
   TTkCore
   TTkGui
   TTkLayouts
   TTkTemplates
   TTkTestWidgets
   TTkUiTools
   TTkWidgets
   TTkWidgets.TTkModelView
   TTkWidgets.TTkPickers
   TTkWidgets.TTkTerminal

.. #.. autosummary::
.. #   :caption: Classes:
.. #   :toctree: _autosummary
.. #   :template: custom-class-template.01.rst
.. #
.. #   TTkCore.pyTTkSignal
.. #   TTkCore.pyTTkSlot
.. #
.. #   TTkWidgets.TTkAppTemplate
.. #   TTkWidgets.TTkMenuBar
.. #   TTkWidgets.TTkMenuBarLayout

.. #   TTkWidgets.TTkWidget

.. #   TTkWidgets.TTkLineEdit
.. #   TTkWidgets.TTkScrollBar
.. #   TTkWidgets.TTkModelView.TTkTable

.. #
.. #    TTkCore.TTkK
.. #    TTkCore.TTkConstant
.. #    TTkWidgets.TTkWidget
.. #    TTkWidgets.TTkContainer
.. #    TTkWidgets.TTkScrollBar

.. #    | TTkCore.TTk
.. #    | TTkCore.TTkHelper
.. #    | TTkCore.TTkColor
.. #
.. # | TermTk.TTkAbstract
.. # | TermTk.TTkCore
.. # | TermTk.TTkCore.TTkTerm
.. # | TermTk.TTkGui
.. # | TermTk.TTkLayouts
.. # | TermTk.TTkTemplates
.. # | TermTk.TTkTestWidgets
.. # | TermTk.TTkTheme
.. # | TermTk.TTkTypes
.. # | TermTk.TTkUiTools
.. # | TermTk.TTkWidgets
.. # | TermTk.TTkWidgets.TTkModelView
.. # | TermTk.TTkWidgets.TTkPickers
.. # | TermTk.TTkWidgets.TTkTerminal
.. #
.. # | TTkAbstract
.. # | TermTk.TTkCore
.. # | TermTk.TTkCore.TTkTerm
.. # | TermTk.TTkGui
.. # | TermTk.TTkLayouts
.. # | TermTk.TTkTemplates
.. # | TermTk.TTkTestWidgets
.. # | TermTk.TTkTheme
.. # | TermTk.TTkTypes
.. # | TermTk.TTkUiTools
.. # | TermTk.TTkWidgets
.. # | TermTk.TTkWidgets.TTkModelView
.. # | TermTk.TTkWidgets.TTkPickers
.. # | TermTk.TTkWidgets.TTkTerminal

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`