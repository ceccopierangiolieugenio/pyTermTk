## Python Refactoring
* From [sourcery](https://sourcery.ai/blog)'s [Blog](https://sourcery.ai/blog/)
    [explaining-refactorings-1](https://sourcery.ai/blog/explaining-refactorings-1/)
    [explaining-refactorings-2](https://sourcery.ai/blog/explaining-refactorings-2/)
    [explaining-refactorings-3](https://sourcery.ai/blog/explaining-refactorings-3/)
    [explaining-refactorings-4](https://sourcery.ai/blog/explaining-refactorings-4/)
    [explaining-refactorings-5](https://sourcery.ai/blog/explaining-refactorings-5/)
    [explaining-refactorings-6](https://sourcery.ai/blog/explaining-refactorings-6/)
    [explaining-refactorings-7](https://sourcery.ai/blog/explaining-refactorings-7/)

## UTF-8
#### Unicode chartable
    https://www.utf8-chartable.de/unicode-utf8-table.pl
#### Fullsize/Halfsize forms
    https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms
    https://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms_(Unicode_block)
#### Ascii Fonts
    https://github.com/phpjsnerd/ascii-fonts
    https://github.com/phpjsnerd/ascii-fonts/blob/master/Calvin%20S.flf
    https://www.texttool.com/ascii-font#p=display&f=Calvin%20S&t=Type%20Something%20%2012345
    http://www.roysac.com/thedrawfonts-tdf.html#16

## Terminal
#### ANSI Escape Sequences
https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#file-ansi-md
https://conemu.github.io/en/AnsiEscapeCodes.html
#### Hyperlink
https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda
#### ANSI 16 256 24bit color conversion
https://www.calmar.ws/vim/256-xterm-24bit-rgb-color-chart.html
#### ANSI Colors
https://talyian.github.io/ansicolors/
http://pueblo.sourceforge.net/doc/manual/ansi_color_codes.html

#### Blinking Text
```bash
echo  -e "\033[5mBlinking Text\033[0m"
echo  -e "\033[33;5mBlinking Text\033[0m"
echo  -e "\033[33;7mBlinking Text\033[0m"
echo  -e "\033[33;5;7mBlinking Text\033[0m"
```

## Sphinx Doc
#### Domains - docstring syntax
https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#directive-py-class
#### ReStructuredText
https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#explicit-markup-blocks

## Disable SIGSTOP triggered by CTRL+S
```bash
# Disable
stty stop ''
# ReEnable = map stop top CTRL+S
stty stop '^s'
```

```python
import sys, termios

attr = termios.tcgetattr(sys.stdin)
# Save the value to be restored
bak = attr[6][termios.VSTOP]

# Disable SIGSTOP triggered by CTRL+S
attr[6][termios.VSTOP]=0
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, attr)

'''. . . do stuff . . .'''

# reEnable SIGSTOP triggered by CTRL+S
attr[6][termios.VSTOP]=bak
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, attr)
```
### Terminal Mapping:
 - CTRL-C -> termios.VINTR
 - CTRL-S -> termios.VSTOP
 - CTRL-Z -> termios.VSUSP
 - CTRL-Q -> termios.VSTART

Have a look at [test.termios.001.py](../../tests/test.termios.001.py)

### [GNU Nano](https://www.nano-editor.org) Terminal Initialization
https://git.savannah.gnu.org/cgit/nano.git/tree/src/nano.c#n1199

## Terminal Multiplexer

### Get Default shell

```python
import pwd, os
pwd.getpwuid(os.getuid()).pw_shell # values from /etc/passwd = '/bin/bash'
```

Check as reference:

 - https://github.com/tmux/tmux/blob/master/tmux.c#L63

Pty Demo:

 - https://docs.python.org/3/library/pty.html#example

## Screenshot editor (FREEEEEEEE)
https://screenshotr.app/

* presets:
  Canvas W = 1000
  Browser Width = 950
  Browser Scale = 1