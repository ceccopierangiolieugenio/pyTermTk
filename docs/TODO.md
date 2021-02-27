# TODO
- [ ] Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style
- [x] Move the Global Constants outside TTk object
- [ ] Add Typing (good luck) https://docs.python.org/3/library/typing.html
- [ ] Remove Duplicate functionalities (i.e. Widget)
  - [ ] Use @property/@setter when possible
  - [ ] Uniform the setter/getter/signal/slots
  - [ ] [UTF-8] Handle "Fullwidth" forms characters
        https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms
        https://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms_(Unicode_block)

## Terminal Helper
- [ ] Events
  - [x] Window : SIGWINCH triggered when the terminal is resized

## Input Class
- [ ] Return Error if Mouse RE does not match
- [x] Handle the Paste Buffer
- [ ] Investigate the middle mouse button paste
  *note: It works only in "INSERT" mode on Vim*
- [x] Handle Special Keys (UP, Down, . . .)
- [ ] Events
  https://tkinterexamples.com/events/events.html
  https://www.pythontutorial.net/tkinter/tkinter-event-binding/
  - [x] Keyboard
  - [x] Mouse

## Colors
- [ ] Allow dynamic depth change
- [x] Define a gradient feature
## Canvas Class
- [ ] Have a look to the Unicode chartable: https://www.utf8-chartable.de/unicode-utf8-table.pl

## Signal/Slots
- [x] Implement Signal/Slots

## Logs
- [x] Log Class
- [ ] Run Logger on a separate thread (push sring to a queue)
  - [ ] Include option to force print
- [ ] Log helpers
  - [x] File and Stdout logger
- [ ] logger auto integration
  - [ ] stdout until mainLoop

### Layout
- [ ] Add Weight in V and H Layout
- [ ] Add addLayout method - Nested layouts
- [x] Add Grid Layout

### Overlay widget
- [ ] Rewrite the Handling (ttk.py)
      It would be nice to have it as child outside the layour
- [ ] Enable mouse move on overlay
## Widgets
- [ ] Add Size Policy (fixed minimum maximum expanding)
- [x] Add Show/Hide
- [ ] Clean the way the parent is assigned, propagated
      *Widget \[setParent, addWidget, . . ], GridLayout \[addWidget]*
#### Button Widget
 - [x] Basic Implementation
 - [x] Events (Signal/Slots)
 - [x] Themes
#### Line Edit Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [x] Themes
 - [x] Input Type Numbers/Password
#### Text Edit Widget
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
 #### Table Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
 #### Window Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
 #### CheckBox Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [x] Themes
#### Radio button Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [x] Themes
#### ComboBox (dropdown) Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [x] Themes
#### Splitter widget
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
#### Tab Widget
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
#### Spin Box
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
#### Progress Bar
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
#### Graph Widget
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
#### Header Menu
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
