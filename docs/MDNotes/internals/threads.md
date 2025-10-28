Summary of the main pyTermTk Threading (26/Oct/2025) [8148cf0a]
```text

MainThread (mainlop)
│   └─▶ Wait on inputQueue ─> Signal ┬─▶ inputEvent
│                      ▲             └─▶ pasteEvent
│                      │
│                      (push to inputQueue)
├─▶ TTkInput Thread    │
│      └─▶ Wait on select(Stdin)
│
└─▶ TTk (Draw)
       └─▶ Wait on timeout (~65 fps) ──▶ Refresh Screen

```