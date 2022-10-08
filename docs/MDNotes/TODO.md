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
      https://stackoverflow.com/questions/68412744/count-length-of-value-within-a-cell-with-full-width-characters
- [ ] Support Hyperlink: (gnome-terminal)
      https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda
- [x] Process child events before parent
- [ ] Rewrite the way focus is handled
      https://doc.qt.io/qt-5/focus.html
      Ref: https://github.com/ceccopierangiolieugenio/scripts/blob/master/Programming/python/pyqt5/textedit.001.py

## Terminal Helper
- [ ] Events
  - [x] Window : SIGWINCH triggered when the terminal is resized

## Input Class
- [ ] Return Error if Mouse RE does not match
- [x] Handle the Paste Buffer
- [ ] Investigate the middle mouse button paste
  *note: It works only in "INSERT" mode on Vim*
- [x] Handle Special Keys (UP, Down, . . .)
- [x] Handle CTRL-Mouse
- [/] Handle CTRL,ALT,SHIFT + Key (Tab, UP, Down, . . .)
  - [x] Handle  SHIFT + Tab
    - [x] Handle Tab Focus
  - [x] Handle  CTRL,ALT,SHIFT + (F1 -> F12)
  - [/] Handle  CTRL,ALT,SHIFT + (Up, Down, Left Right)
- [ ] Events
  https://tkinterexamples.com/events/events.html
  https://www.pythontutorial.net/tkinter/tkinter-event-binding/
  - [x] Keyboard
  - [x] Mouse
    - [ ] Implement the different Escape codes
          (Check https://github.com/vercel/hyper)
          https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Mouse-Tracking

## Colors
- [ ] Allow dynamic depth change
- [x] Define a gradient feature
## Canvas Class
- [ ] Have a look to the Unicode chartable: https://www.utf8-chartable.de/unicode-utf8-table.pl

## Signal/Slots
- [x] Implement Signal/Slots

## Logs
- [x] Log Class
- [ ] Run Logger on a separate thread (push string to a queue)
  - [ ] Include option to force print
- [ ] Log helpers
  - [x] File and Stdout logger
- [ ] logger auto integration
  - [ ] stdout until mainLoop

### Layout
- [ ] Add Weight in V and H Layout
- [x] Add addLayout (adDItem) method - Nested layouts
- [x] Add Grid Layout
  - [x] Add ColSpan / RowSpan
- [x] Get rid of groupMoveTo
- [x] Get rid of addWidget

### AbstractScrollArea
- [x] Implement something that mimic the QAbstactScrollArea
  https://doc.qt.io/qt-5/qabstractscrollarea.html
  https://doc.qt.io/qt-5/qscrollarea.html
- [ ] Implement the focus policy

### Overlay widget
- [x] Use the nested layout for the overlay
- [x] Rewrite the Handling (ttk.py)
      It would be nice to have it as child outside the layout
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
 - [x] Themes
 #### Fancy Table Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes

 #### Tree Widget
 - [x] Basic Implementation
 - [ ] Implement cache/pagination for big data
 - [ ] Events (Signal/Slots)
 - [ ] Themes
 #### Window Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [x] Themes
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
 - [x] Basic Implementation
 - [x] Snap on min/max sizes
 - [ ] Events (Signal/Slots)
 - [x] Themes
 - [ ] Support addItem
#### Tab Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [x] Themes
 - [ ] Align Selected to center
 - [x] Add Menu
 - [ ] Keyboard events
#### Spin Box
 - [x] Basic Implementation
 - [x] Events (Signal/Slots)
 - [ ] Themes
#### Progress Bar
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
#### Graph Widget
 - [x] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [x] Themes
#### Header Menu
 - [x] Basic Implementation
 - [x] Events (Signal/Slots)
 - [x] Themes

### Pickers
#### Color Picker~/github/Varie/pyTermTk~/github/Varie/pyTermTk
 - [x] Basic Implementation
 - [x] Events (Signal/Slots)
 - [x] Themes
 - [x] Use Spinbox for R G B
#### Date Picker
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
#### File Picker
 - [x] Basic Implementation
 - [x] Events (Signal/Slots)
 - [x] Themes
#### Yes/No Ok/Cancel Picker
 - [ ] Basic Implementation
 - [ ] Events (Signal/Slots)
 - [ ] Themes
