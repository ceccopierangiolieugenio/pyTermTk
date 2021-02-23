# pyTermTk
#### Python Terminal Toolkit
Text-based user interface library ([TUI](https://en.wikipedia.org/wiki/Text-based_user_interface))
Evolved from the discontinued project [pyCuT](https://github.com/ceccopierangiolieugenio/pyCuT)
and inspired by a mix of [Qt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/),[GTK](https://pygobject.readthedocs.io/en/latest/) and [tkinter](https://docs.python.org/3/library/tkinter.html) api definition with a touch of personal interpretation

## Quick Test/Try

#### Clone
```shell
clone git@github.com:ceccopierangiolieugenio/pyTermTk.git
cd pyTermTk
```

#### Run Basic input test
```shell
python3 tests/test.input.py
```

#### Run Terminal resize test
```shell
# Press CTRL-C to exit
# the logs are written to "session.log"
python3 tests/test.ui.002.py
python3 tests/test.ui.003.layout.py
python3 tests/test.ui.004.windowspy
```
#### Profiling
##### cProfile
```shell
python3 -m cProfile -o profiler.txt tests/test.ui.004.py

# install cprofilev:
#     pip3 install cprofilev
cprofilev -f profiler.txt
# open http://127.0.0.1:4000
```
##### pyroscope
[pyroscope](https://pyroscope.io/) can be used as well for profiling