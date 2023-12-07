

![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)
![Usage](https://img.shields.io/badge/Usage-Terminal%20User%20Interface-yellow)
![Python](https://img.shields.io/badge/Python-v3.8%5E-green?logo=python)
![pyTermTk_version](https://img.shields.io/github/v/tag/ceccopierangiolieugenio/pyTermTk?label=version)
[![Test Status](https://img.shields.io/github/actions/workflow/status/ceccopierangiolieugenio/pyTermTk/testing.yml?branch=main&label=tests)](https://github.com/ceccopierangiolieugenio/pyTermTk/actions?query=workflow%3Atesting)
[![pypi_version](https://img.shields.io/pypi/v/pyTermTk?label=pypi)](https://pypi.org/project/pyTermTk)
[![pypi_version](https://img.shields.io/twitter/follow/Pier95886803?style=social&logo=twitter)](https://twitter.com/hashtag/pyTermTk?src=hashtag_click&f=live)

![screenshot](https://ceccopierangiolieugenio.github.io/binaryRepo/pyTermTk/images/pyTermTk.HERO.800.png)

## [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk)

(**py**thon **Term**inal **T**ool**k**it) is a Text-based user interface library ([TUI](https://en.wikipedia.org/wiki/Text-based_user_interface))
Evolved from the discontinued project [pyCuT](https://github.com/ceccopierangiolieugenio/pyCuT)
and inspired by a mix of [Qt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/),[GTK](https://pygobject.readthedocs.io/en/latest/), and [tkinter](https://docs.python.org/3/library/tkinter.html) api definition with a touch of personal interpretation

[pyTermTk.Showcase.002.webm](https://user-images.githubusercontent.com/8876552/206490679-2bbdc909-c9bc-41c1-9a50-339b06dabecd.webm)

## [Features](https://ceccopierangiolieugenio.github.io/pyTermTk/info/features/index.html)
- [Self Contained](https://ceccopierangiolieugenio.github.io/pyTermTk/info/installing.html) (no external lib required), Python 3.9 or above required.
- [Cross compatible](https://ceccopierangiolieugenio.github.io/pyTermTk/info/features/crosscompatible.html): [Linux](https://en.wikipedia.org/wiki/Linux)🐧, [MacOS](https://en.wikipedia.org/wiki/MacOS)🍎, [MS Windows](https://en.wikipedia.org/wiki/Microsoft_Windows)🪟, [HTML5](https://en.wikipedia.org/wiki/HTML5)🌍([Try](https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html))
- [Basic widgets](https://ceccopierangiolieugenio.github.io/pyTermTk/info/features/widgets.html#base-widgets) for [TUI](https://en.wikipedia.org/wiki/Text-based_user_interface) development (Button, Label, checkbox, ...)
- [Specialized widgets](https://ceccopierangiolieugenio.github.io/pyTermTk/info/features/widgets.html#specialised-widgets) to improve the usability (Windows, Frames, Tables, ...)
- QT Like Layout system to help arrange the widgets in the terminal
- True color support
- Ful/Half/Zero sized Unicode characters 😎
- I am pretty sure there is [something else...](https://ceccopierangiolieugenio.github.io/pyTermTk/info/features/index.html)

---

## Try the [Sandbox](https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html) straight from your browser

[![SandBox](https://user-images.githubusercontent.com/8876552/206438915-fdc868b1-32e0-46e8-9e2c-e29f4a7a0e75.png)](https://ceccopierangiolieugenio.github.io/pyTermTk/sandbox/sandbox.html)

Powered by [Pyodide](https://pyodide.org/) and [xterm.js](https://xtermjs.org/) and [CodeMirror5](https://codemirror.net/5/) and [w2ui](https://w2ui.com/)

---

## [the Tutorials](https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/tutorial) and [the Examples](https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/tutorial/000-examples.rst)
Be inspired by [the Tutorials](https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/tutorial) and [the Examples](https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/tutorial/000-examples.rst)

## [Api Definitions](https://ceccopierangiolieugenio.github.io/pyTermTk/)
Don't get bored by the [Api Definitions](https://ceccopierangiolieugenio.github.io/pyTermTk/)

## [ttkDesigner](https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/ttkDesigner)
Smell deliciousness with the official [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) tool for designing and building Text-based user interfaces ([TUI](https://en.wikipedia.org/wiki/Text-based_user_interface)s)

---

## [Install/Upgrade](https://ceccopierangiolieugenio.github.io/pyTermTk/info/installing.html)
[pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) is available on [PyPI](https://pypi.org/project/pyTermTk/)
```bash
pip3 install --upgrade pyTermTk
```

## Quick Test/Try - no install required

#### Clone
```bash
git clone https://github.com/ceccopierangiolieugenio/pyTermTk.git
cd pyTermTk
```

#### Demos
```bash
# Press CTRL-C to exit (CTRL-Break on Windows)

# Showcase Demo
python3 demo/demo.py -f

# run the ttkDesigner
python3 -m ttkDesigner

# Text edit with "Pygments" highlight integrated
# it require pygments
#   pip install pygments
python3 tests/test.ui.018.TextEdit.Pygments.py README.md
```

---

## Projects using [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk)
- [ttkDesigner](https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/ttkDesigner) - the official [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) tool for designing and building Text-based user interfaces ([TUI](https://en.wikipedia.org/wiki/Text-based_user_interface)s)
- [tlogg](https://github.com/ceccopierangiolieugenio/tlogg) - A fast, advanced log explorer.
- [ttkode](https://github.com/ceccopierangiolieugenio/ttkode) - TerminalToolKit (Studio) Code (editor)
- [pytest-fold](https://github.com/jeffwright13/pytest-fold) - A Pytest plugin to make console output more manageable when there are multiple failed tests
- [pytest-tui](https://github.com/jeffwright13/pytest-tui) - A Text User Interface (TUI) for Pytest, automatically launched after your test run is finished
- [breakoutRL](https://ceccopierangiolieugenio.itch.io/breakoutrl) - Breakout the Roguelike

## Related Projects
- Honourable mention
  - [bpytop](https://github.com/aristocratos/bpytop) - Linux/OSX/FreeBSD resource monitor <br>
    This was the base inspiration for my core library

- Python
  - [urwid](https://github.com/urwid/urwid) - Console user interface library for Python
  - [pyTermGUI](https://github.com/bczsalba/pytermgui) - A simple yet powerful TUI framework for your Python (3.7+) applications
  - [Textual](https://github.com/Textualize/textual) - TUI (Text User Interface) framework for Python inspired by modern web development
  - [Rich](https://github.com/Textualize/rich) - Python library for rich text and beautiful formatting in the terminal
  - [PyCuT](https://github.com/ceccopierangiolieugenio/pyCuT) - terminal graphic library loosely based on QT api (my previous failed attempt)
  - [pyTooling.TerminalUI](https://github.com/pyTooling/pyTooling.TerminalUI) - A set of helpers to implement a text user interface (TUI) in a terminal.

- Non Python
  - [Turbo Vision](http://tvision.sourceforge.net)
  - [ncurses](https://en.wikipedia.org/wiki/Ncurses)
  - [tui.el](https://github.com/ebpa/tui.el) - An experimental text-based UI framework for Emacs modeled after React
