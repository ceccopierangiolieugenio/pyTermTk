https://www.x.org/docs/xterm/

# DCS - ESC P
ESC P + Pt + ESC \
Device Control String (DCS) xterm implements no DCS functions; Pt is ignored. Pt need not be printable characters.

vim initialization using DCS
vim -> src/term.c
```c
// 2. Check compatibility with xterm.
// We move the cursor to (2, 0), print a test sequence and then query
// the current cursor position. If the terminal properly handles
// unknown DCS string and CSI sequence with intermediate byte, the test
// sequence is ignored and the cursor does not move. If the terminal
// handles test sequence incorrectly, a garbage string is displayed and
// the cursor does move.
MAY_WANT_TO_LOG_THIS;
LOG_TR(("Sending xterm compatibility test sequence."));
// Do this in the third row. Second row is used by ambiguous
// character width check.
term_windgoto(2, 0);
// send the test DCS string.
out_str((char_u *)"\033Pzz\033\\");
// send the test CSI sequence with intermediate byte.
out_str((char_u *)"\033[0%m");
out_str(T_U7);
termrequest_sent(&xcc_status);
out_flush();
did_send = TRUE;
```