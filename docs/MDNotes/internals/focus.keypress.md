# Current

## Current Status of the focus/keypress logic

```
<INPUT>
  └─▶ KeyEvent
        └─▶ TTk._key_event()
              try 1 ─▶ send KeyEvent to Focus Widget
              try 2 ─▶ send KeyEvent to Shortcut Engine
              try 3 ─▶ Check and handle for next Focus
              try 4 ─▶ check and handle for prev focus
```

## Reworked Status of the focus/keypress logic

1) Add default KeyPress handler

   This handler is supposed to switch the focus (next/prev) or return False

1) Add focus proxy/orchestrator/helper in TTkContainer (New Class? or internally Managed?)

   ####ß Require (so far)

   * Next Focus
   * Prev Focus
   * First Focus
   * Last Focus
   * Get Focussed
   * Focus Widget
   * UnFocus Widget
   * Add Widget(s)
   * Remove Widget(s)
   * Insert Widget(s)

1) Key Propagation

    ```
    <INPUT>
    └─▶ KeyEvent
            └─▶ TTk.keyEvent(kevt)
                try 1 ─▶ send KeyEvent to
                            └─▶ super().keyEvent(kevt) (TTkContainer)
                                try 1 : send key event to the focussed
                                  if return False;
                                try 2 : if  Tab/Right focus Next
                                try 3 : if ^Tab/Left  focus Prev
                                If nothing execute return False
                  if not handled, the tab/direction key switch reached the last/first widget:
                try 3 ─▶  Tab/Right focus the first
                try 4 ─▶ ^Tab/Left  focus the last
    ```

2) Focus Propagation

    ```
    ```

# TODO

[x] - Implement root handler to handle overlay widgets where the focus switch should be contained in the overlay
[x] - Remove nextFocus,prevFocus from the helper
[ ] - Investigate other widgets focus propagation
[ ] - Switch Focus to the menu
[ ] - Type TTkLayout and add docstrings
[ ] - Add deprecated methods in ttkhelper
[x] - Investigate lineedit of the combobox
[x] - Tab Widget: Adapt to the new logic
[x] - DateTime: Adapt to the new logic
[ ] - Tab Widget: Apply Highlight colors
