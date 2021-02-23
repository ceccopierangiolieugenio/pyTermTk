# TODO
- [ ] Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style
- [ ] Use @property/@setter when possible
- [ ] Move the Global Constants outside TTk object

## Terminal Helper
- [ ] Events
  - [x] Window : SIGWINCH triggered when the terminal is resized

## Input Class
- [ ] Return Error if Mouse RE does not match
- [x] Handle the Paste Buffer
- [ ] Investigate the middle mouse button paste
  *note: It works only in "INSERT" mode on Vim*
- [ ] Handle Special Keys (UP, Down, . . .)
- [ ] Events
  https://tkinterexamples.com/events/events.html
  https://www.pythontutorial.net/tkinter/tkinter-event-binding/
  - [x] Keyboard
  - [x] Mouse

## Canvas Class
- [ ] Have a look to the Unicode chartable: https://www.utf8-chartable.de/unicode-utf8-table.pl

## Signal/Slots
- [ ] Implement Signal/Slots

## Logs
- [x] Log Class
- [ ] Run Logger on a separate thread (push sring to a queue)
  - [ ] Include option to force print
- [ ] Log helpers
  - [x] File and Stdout logger
- [ ] logger auto integration
  - [ ] stdout until mainLoop

## Widgets
- [ ] Add Size Policy (fixed minimum maximum expanding)
- [ ] Add Show/Hide
### Layout
- [ ] Add Weight in V and H Layout