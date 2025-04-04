![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)
![Usage](https://img.shields.io/badge/Usage-Terminal%20User%20Interface-yellow)
![Python](https://img.shields.io/badge/Python-v3.8%5E-green?logo=python)
![tlogg_version](https://img.shields.io/github/v/tag/ceccopierangiolieugenio/tlogg?label=version)
[![pypi_version](https://img.shields.io/pypi/v/tlogg?label=pypi)](https://pypi.org/project/tlogg)
[![pypi_version](https://img.shields.io/twitter/follow/Pier95886803?style=social&logo=twitter)](https://twitter.com/hashtag/pyTermTk?src=hashtag_click&f=live)

# tlogg
A fast, advanced [text-based](https://en.wikipedia.org/wiki/Text-based_user_interface) log explorer written in [pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk), inspired by [glogg - the fast, smart log explorer](https://github.com/nickbnf/glogg) and [klogg - Faster log explorer](https://klogg.filimonov.dev)(fork of glogg)

[![screenshot](https://raw.githubusercontent.com/ceccopierangiolieugenio/binaryRepo/master/tlogg/screenshot.003.png)](https://pypi.org/project/tlogg)
## Features
- Search Panel
- Highlight
- Bookmarks
- Shiny ASCII Red Peppers

[![screenshot](https://raw.githubusercontent.com/ceccopierangiolieugenio/binaryRepo/master/tlogg/demo.001.gif)](https://pypi.org/project/tlogg)

- _Draggable_ **Tiling tabs**

[screenshot](https://github.com/ceccopierangiolieugenio/tlogg/assets/8876552/b3db13d9-48b4-485e-bc19-d655021479b6)

# Install from [pypi](https://pypi.org/project/tlogg)
```bash
pip install tlogg
```
## Enable the system Clipboard
[pyTermTk](https://github.com/ceccopierangiolieugenio/pyTermTk) automatically support the system clipboard through [pyperclip](https://pypi.org/project/pyperclip/)
```bash
pip install pyperclip
```
# QuickRun
```bash
 $ tlogg -h
usage: tlogg [-h] [-c C] filename [filename ...]

positional arguments:
  filename    the filename/s

optional arguments:
  -h, --help  show this help message and exit
  -c C        config folder (default: "/home/user/.config/tlogg")
```

# Test
### Clone
```bash
git clone https://github.com/ceccopierangiolieugenio/tlogg.git
cd tlogg
```
### Run
```
python3 -m tlogg  <File/s>
```

