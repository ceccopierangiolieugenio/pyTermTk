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

## Terminal
#### Hyperlink
https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda

## Sphinx Doc
#### Domains - docstring syntax
https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#directive-py-class
#### ReStructuredText
https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#explicit-markup-blocks

## Disable SIGSTOP triggered by CTRL+S
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