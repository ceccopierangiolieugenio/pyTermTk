

![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)
![Usage](https://img.shields.io/badge/Usage-Terminal%20User%20Interface-yellow)
![Python](https://img.shields.io/badge/Python-v3.8%5E-green?logo=python)
![pyTermTk_version](https://img.shields.io/github/v/tag/ceccopierangiolieugenio/pyTermTk?label=version)
[![Test Status](https://img.shields.io/github/workflow/status/ceccopierangiolieugenio/pyTermTk/Testing?label=tests)](https://github.com/ceccopierangiolieugenio/pyTermTk/actions?query=workflow%3Atesting)
[![pypi_version](https://img.shields.io/pypi/v/pyTermTk?label=pypi)](https://pypi.org/project/pyTermTk)
[![pypi_version](https://img.shields.io/twitter/follow/Pier95886803?style=social&logo=twitter)](https://twitter.com/hashtag/pyTermTk?src=hashtag_click&f=live)

[![screenshot](https://github.com/ceccopierangiolieugenio/binaryRepo/blob/master/pyTermTk/Logo.retroterm.001.png?raw=true)](https://pypi.org/project/pyTermTk)

## [python Terminal Toolkit](https://github.com/ceccopierangiolieugenio/pyTermTk)

Text-based user interface library ([TUI](https://en.wikipedia.org/wiki/Text-based_user_interface))
Evolved from the discontinued project [pyCuT](https://github.com/ceccopierangiolieugenio/pyCuT)
and inspired by a mix of [Qt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/),[GTK](https://pygobject.readthedocs.io/en/latest/), and [tkinter](https://docs.python.org/3/library/tkinter.html) api definition with a touch of personal interpretation

[![screenshot](https://github.com/ceccopierangiolieugenio/binaryRepo/blob/master/pyTermTk/demo.001.gif?raw=true)](https://pypi.org/project/pyTermTk)

## Features
- Basic widgets for [TUI](https://en.wikipedia.org/wiki/Text-based_user_interface) development (Button, Label, checkbox, ...)
- Specialized widgets to improve the usability (Windows, Frames, Tables, ...)
- QT Like Layout system to help arrange the widgets in the terminal
- True color support
- [TBD] Fullsize/Halfsize UTF-8 characters

## Limitations
- Only the key combinations forwarded by the terminal emulator used are detected (ALT,CTRL may not be handled)

## Try
[![screenshot](https://github.com/ceccopierangiolieugenio/binaryRepo/blob/master/pyTermTk/replit.pytermtk.banner.png?raw=true)](https://replit.com/@EugenioP/pyTermTk?v=1)

## [Tutorial](tutorial)
Be inspired by the [tutorial examples](https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/tutorial)

## [Api Definitions](https://ceccopierangiolieugenio.github.io/pyTermTk/)
Don't get bored by the [Api Definitions](https://ceccopierangiolieugenio.github.io/pyTermTk/)

## Install/Upgrade
[pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) is available on [PyPI](https://pypi.org/project/pyTermTk/)
```shell
pip3 install --upgrade pyTermTk
```
## Quick Test/Try - no install required

#### Clone
```shell
clone git@github.com:ceccopierangiolieugenio/pyTermTk.git
cd pyTermTk
```

#### Run Basic (non ui) input test
```shell
python3 tests/test.input.py
```

#### Run demo
```shell
# Press CTRL-C to exit
# the logs are written to "session.log"
make runDemo
  # or
python3 demo/demo.py -f

# Try gittk
make runGittk
```
#### Profiling
##### [cProfile](https://docs.python.org/3/library/profile.html), [cProfilev](https://github.com/ymichael/cprofilev)
```shell
python3 -m cProfile -o profiler.txt tests/test.ui.004.py

# install cprofilev:
#     pip3 install cprofilev
cprofilev -f profiler.txt
# open http://127.0.0.1:4000
```
##### pyroscope
[pyroscope](https://pyroscope.io/) can be used as well for profiling