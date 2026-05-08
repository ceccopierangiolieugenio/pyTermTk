---
applyTo: "tutorial/examples/**/*.py,tutorial/examples/README.rst,tutorial/000-examples.rst"
description: Rules for authoring concise, practical pyTermTk examples with per-file introductions, web runnable links, quick run commands, and broad area coverage.
---
# Tutorial Examples Authoring Rules (Path Scoped)

These rules apply when creating or editing tutorial examples and their example index pages.

## Goal

- Examples must be small, focused, and easy to read.
- Prefer practical usage snippets over full featured tutorials.
- Each example should teach one main concept and at most one secondary concept.

## Python Example File Requirements

- Keep files short and clear; avoid large frameworks or excessive helper abstractions.
- Preserve executable style (`#!/usr/bin/env python3`) and MIT license header used by existing examples.
- Prefer explicit, readable widget setup over compact clever code.
- Use signal/slot examples with `@ttk.pyTTkSlot(...)` where relevant.
- Ensure examples are runnable as standalone scripts.
- The file should start with, in order:
  1 - shebang
    ```python
    #!/usr/bin/env python3
    ```
  2 - MIT License with the copyright aligned to the year of the file creation, where the copyright is in the format:
    ```python
    # Copyright (c) YYYY Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
    ```
  3 - standard pyTermTk direct-from-repo bootstrap, adjusted to reach the `libs/pyTermTk` folder from the example file nesting level
    ```python
    ##########
    # Those 2 lines are required to use the TermTk library straight from the main folder
    import sys, os
    sys.path.append(os.path.join(sys.path[0],'../../../libs/pyTermTk'))
    ##########
    ```
  4 - short module docstring at the top describing:
      - what the example demonstrates,
      - the key feature(s),
      - related API concepts.
  5 - imports and root initialization
    ```python
    import TermTk as ttk

    root = ttk.TTk()
    ```

## Widget Sizing and Layout Positioning

- **Button heights**: TTkButton widgets are typically 3 rows tall by default (accounting for borders and padding).
  - When positioning elements in a grid or vertical arrangement, account for this height.
  - Example: if a button is at `y=2`, the next element should start at `y=5` or later to avoid overlap.
- **Multi-column layouts**: When using multiple side-by-side columns, position the second column starting at `x=45` or further right to prevent text overlap.
  - Left column typically starts at `x=2`; ensure labels and widgets don't extend beyond `x=24`.
  - Use consistent x-positioning across vertically-aligned elements in the same column.
- **Label spacing**: Place informational labels at least 1 row before or after interactive widgets to improve visual clarity.
- **Avoid overlap**: Always verify spacing visually when using absolute positioning with `pos=(x, y)` parameters.

## Scope and Coverage

- Add examples across many library areas instead of overfocusing one widget mode.
- Favor representative coverage such as:
  - initialization/basic usage,
  - set/get APIs,
  - events and signals,
  - stateful widgets (checkable/toggle),
  - layout integration,
  - focus/keyboard navigation,
  - styling/theming,
  - practical mini form/workflow integration.
- Keep each file narrowly scoped; split into multiple files rather than one long example.

## Naming and Structure

- Use stable sequential naming: `<Topic>.<NN>.py` (for example, `Init.01.py`, `Events.01.py`).
- Place examples under topic folders (for example `tutorial/examples/TTkButton/`).
- Use descriptive topic names that match the concept being shown.

## Example Index Documentation (`README.rst`, `000-examples.rst`)

- Each example section should include:
  - a one-line human-readable purpose,
  - a runnable link using existing directives (`:ttk:sbIntLink:` / `:ttk:ghIntLink:` as appropriate),
  - a quick run command block.
- Keep section text concise and scannable.
- Keep `tutorial/examples/README.rst` and `tutorial/000-examples.rst` aligned in content and ordering.
- Note: `docs/source/tutorial/` is a symlink to the root `tutorial/` folder. Edits in either location affect the same files; no manual sync needed.

## Web Interface / Online Run Link

- Use the project sandbox convention when writing explicit links:
  - `https://ceccopierangiolieugenio.github.io/pyTermTk-Docs/sandbox/sandbox.html?filePath=<repo-relative-path>`
- Prefer existing rst directives in example index files where available.
- Ensure `filePath` is repository-relative and points to the exact example file.

## Quick Run Commands

- Provide minimal commands that work from repository root.
- Prefer executable path and `python3` fallback pattern:

  - `tutorial/examples/<Topic>/<Example>.py`
  - `python3 tutorial/examples/<Topic>/<Example>.py`

## Quality Bar

- No dead code or placeholder text in shipped examples.
- Avoid hidden side effects; behavior should be observable in the UI.
- Keep comments purposeful and sparse.
- Validate syntax before finalizing changes.
