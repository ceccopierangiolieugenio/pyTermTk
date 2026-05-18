# Godot Terminal POC

This app is a proof-of-concept terminal emulator in Godot powered by pyTermTk terminal parsing.

## What this does

- Spawns a real local shell through pty (macOS/Linux).
- Uses pyTermTk terminal emulation (ANSI parsing, colors, cursor state).
- Streams a terminal cell grid to Godot over local TCP JSON lines.
- Renders glyphs in a fixed grid using a Nerd Font when available.
- Sends keyboard input and terminal resize events from Godot back to pty.

## Files

- `bridge/ttk_bridge.py`: Python bridge process.
- `scripts/terminal_bridge_client.gd`: Godot TCP client.
- `scripts/main.gd`: grid rendering and keyboard input mapping.
- `main.tscn`: runnable Godot scene.

## Font setup (Nerd Font)

Drop a Nerd Font file at:

- `assets/fonts/JetBrainsMonoNerdFontMono-Regular.ttf`

If the font is missing, the scene falls back to the default Godot font.


## Setup

Before running the project for the first time, you must initialize the environment and download all required assets:

```bash
./setup.sh
```

This script will set up dependencies and fetch any necessary fonts or resources.

## Run

1. Start the bridge from repository root:

```bash
cd apps/godot-terminal
../../.venv/bin/python bridge/ttk_bridge.py --cols 100 --rows 32
```

2. Open `apps/godot-terminal` in Godot 4.6 and run the project.

## Protocol (quick reference)

Client to bridge:

- `{"type":"resize","cols":120,"rows":40}`
- `{"type":"text","text":"ls\n"}`
- `{"type":"input","data":"<base64 bytes>"}`

Bridge to client:

- `{"type":"hello",...}`
- `{"type":"frame","cols":...,"rows":...,"cursor":[x,y],"cells":[...],"closed":false}`

Each cell is encoded as:

`[ch, fg_r, fg_g, fg_b, bg_r, bg_g, bg_b, flags]`

Flags bitfield:

- `1`: bold
- `2`: italic
- `4`: underline
- `8`: strikethrough
- `16`: blinking

## Notes

- This is a POC and currently sends full frames, not diffs.
- It is intended for local use (`127.0.0.1`).
- Wide/combining characters are parsed by pyTermTk; rendering quality depends on the selected font.
