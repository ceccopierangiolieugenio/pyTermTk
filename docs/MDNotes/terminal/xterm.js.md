# Notes About Xterm.js

Those are the main api exported by xterm.js,

This is used as reference to build a platform agnostic terminal emulator (TTkTerminal)

```javascript
// Init
    var term = new Terminal({allowProposedApi: true});

// Write to the terminal
    term.write('xterm.js - Loaded\n\r')

// Resize Event
    term.onResize( (obj) => {
      term.reset()
      ttk_resize(obj.cols, obj.rows)
    });

// Input Event
    term.onData((d, evt) => { ttk_input(d) })
```