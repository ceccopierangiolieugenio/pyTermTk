Gnu Screen Escape 
https://www.gnu.org/software/screen/manual/html_node/Control-Sequences.html

The following is a list of control sequences recognized by `screen`. ‘(V)’ and ‘(A)’ indicate VT100-specific and ANSI- or ISO-specific functions, respectively.

```
ESC E                           Next Line
ESC D                           Index
ESC M                           Reverse Index
ESC H                           Horizontal Tab Set
ESC Z                           Send VT100 Identification String
ESC 7                   (V)     Save Cursor and Attributes
ESC 8                   (V)     Restore Cursor and Attributes
ESC [s                  (A)     Save Cursor and Attributes
ESC [u                  (A)     Restore Cursor and Attributes
ESC c                           Reset to Initial State
ESC g                           Visual Bell
ESC Pn p                        Cursor Visibility (97801)
    Pn = 6                      Invisible
         7                      Visible
ESC =                   (V)     Application Keypad Mode
ESC >                   (V)     Numeric Keypad Mode
ESC # 8                 (V)     Fill Screen with E's
ESC \                   (A)     String Terminator
ESC ^                   (A)     Privacy Message String (Message Line)
ESC !                           Global Message String (Message Line)
ESC k                           Title Definition String
ESC P                   (A)     Device Control String
                                Outputs a string directly to the host
                                terminal without interpretation.
ESC _                   (A)     Application Program Command (Hardstatus)
ESC ] 0 ; string ^G     (A)     Operating System Command (Hardstatus, xterm
                                title hack)
ESC ] 83 ; cmd ^G       (A)     Execute screen command. This only works if
                                multi-user support is compiled into screen.
                                The pseudo-user ":window:" is used to check
                                the access control list. Use "addacl :window:
                                -rwx #?" to create a user with no rights and
                                allow only the needed commands.
Control-N               (A)     Lock Shift G1 (SO)
Control-O               (A)     Lock Shift G0 (SI)
ESC n                   (A)     Lock Shift G2
ESC o                   (A)     Lock Shift G3
ESC N                   (A)     Single Shift G2
ESC O                   (A)     Single Shift G3
ESC ( Pcs               (A)     Designate character set as G0
ESC ) Pcs               (A)     Designate character set as G1
ESC * Pcs               (A)     Designate character set as G2
ESC + Pcs               (A)     Designate character set as G3
ESC [ Pn ; Pn H                 Direct Cursor Addressing
ESC [ Pn ; Pn f                 same as above
ESC [ Pn J                      Erase in Display
      Pn = None or 0            From Cursor to End of Screen
           1                    From Beginning of Screen to Cursor
           2                    Entire Screen
ESC [ Pn K                      Erase in Line
      Pn = None or 0            From Cursor to End of Line
           1                    From Beginning of Line to Cursor
           2                    Entire Line
ESC [ Pn X                      Erase character
ESC [ Pn A                      Cursor Up
ESC [ Pn B                      Cursor Down
ESC [ Pn C                      Cursor Right
ESC [ Pn D                      Cursor Left
ESC [ Pn E                      Cursor next line
ESC [ Pn F                      Cursor previous line
ESC [ Pn G                      Cursor horizontal position
ESC [ Pn `                      same as above
ESC [ Pn d                      Cursor vertical position
ESC [ Ps ;...; Ps m             Select Graphic Rendition
      Ps = None or 0            Default Rendition
           1                    Bold
           2            (A)     Faint
           3            (A)     Standout Mode (ANSI: Italicized)
           4                    Underlined
           5                    Blinking
           7                    Negative Image
           22           (A)     Normal Intensity
           23           (A)     Standout Mode off (ANSI: Italicized off)
           24           (A)     Not Underlined
           25           (A)     Not Blinking
           27           (A)     Positive Image
           30           (A)     Foreground Black
           31           (A)     Foreground Red
           32           (A)     Foreground Green
           33           (A)     Foreground Yellow
           34           (A)     Foreground Blue
           35           (A)     Foreground Magenta
           36           (A)     Foreground Cyan
           37           (A)     Foreground White
           39           (A)     Foreground Default
           40           (A)     Background Black
           ...                  ...
           49           (A)     Background Default
ESC [ Pn g                      Tab Clear
      Pn = None or 0            Clear Tab at Current Position
           3                    Clear All Tabs
ESC [ Pn ; Pn r         (V)     Set Scrolling Region
ESC [ Pn I              (A)     Horizontal Tab
ESC [ Pn Z              (A)     Backward Tab
ESC [ Pn L              (A)     Insert Line
ESC [ Pn M              (A)     Delete Line
ESC [ Pn @              (A)     Insert Character
ESC [ Pn P              (A)     Delete Character
ESC [ Pn S                      Scroll Scrolling Region Up
ESC [ Pn T                      Scroll Scrolling Region Down
ESC [ Pn ^                      same as above
ESC [ Ps ;...; Ps h             Set Mode
ESC [ Ps ;...; Ps l             Reset Mode
      Ps = 4            (A)     Insert Mode
           20           (A)     ‘Automatic Linefeed’ Mode.
           34                   Normal Cursor Visibility
           ?1           (V)     Application Cursor Keys
           ?3           (V)     Change Terminal Width to 132 columns
           ?5           (V)     Reverse Video
           ?6           (V)     ‘Origin’ Mode
           ?7           (V)     ‘Wrap’ Mode
           ?9                   X10 mouse tracking
           ?25          (V)     Visible Cursor
           ?47                  Alternate Screen (old xterm code)
           ?1000        (V)     VT200 mouse tracking
           ?1047                Alternate Screen (new xterm code)
           ?1049                Alternate Screen (new xterm code)
ESC [ 5 i               (A)     Start relay to printer (ANSI Media Copy)
ESC [ 4 i               (A)     Stop relay to printer (ANSI Media Copy)
ESC [ 8 ; Ph ; Pw t             Resize the window to ‘Ph’ lines and
                                ‘Pw’ columns (SunView special)
ESC [ c                         Send VT100 Identification String
ESC [ x                 (V)     Send Terminal Parameter Report
ESC [ > c                       Send Secondary Device Attributes String
ESC [ 6 n                       Send Cursor Position Report
```