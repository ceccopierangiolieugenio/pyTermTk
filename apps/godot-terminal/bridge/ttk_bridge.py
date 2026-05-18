#!/usr/bin/env python3
"""Godot <-> pyTermTk terminal bridge.

This process runs a local pty-backed shell using pyTermTk terminal parsing and
streams a JSON grid frame to a TCP client (Godot).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import select
import socket
import sys
import threading
from dataclasses import dataclass
from typing import Any


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PYTERMTK_PATH = os.path.join(ROOT_DIR, "libs", "pyTermTk")
if PYTERMTK_PATH not in sys.path:
    sys.path.insert(0, PYTERMTK_PATH)

from TermTk.TTkWidgets.TTkTerminal.terminalhelper import TTkTerminalHelper
from TermTk.TTkWidgets.TTkTerminal.terminalview import TTkTerminalView


DEFAULT_FG = (220, 220, 220)
DEFAULT_BG = (10, 10, 10)


@dataclass
class BridgeConfig:
    host: str = "127.0.0.1"
    port: int = 18081
    cols: int = 100
    rows: int = 32
    shell: str | None = None


class TerminalModel:
    def __init__(self, cols: int, rows: int, shell: str | None) -> None:
        self._lock = threading.Lock()
        self._dirty = threading.Event()
        self._closed = threading.Event()

        self._cols = cols
        self._rows = rows

        self.view = TTkTerminalView(size=(cols, rows))
        self.helper = TTkTerminalHelper()

        self.helper.dataOut.connect(self._on_data)
        self.helper.terminalClosed.connect(self._on_terminal_closed)

        if shell:
            self.helper.runShell(shell)
        else:
            self.helper.runShell()

        self.resize(cols, rows)
        self._dirty.set()

    def _on_data(self, data: str) -> None:
        with self._lock:
            self.view.termWrite(data)
            self._dirty.set()

    def _on_terminal_closed(self) -> None:
        self._closed.set()
        self._dirty.set()

    def is_closed(self) -> bool:
        return self._closed.is_set()

    def consume_dirty(self) -> bool:
        if self._dirty.is_set():
            self._dirty.clear()
            return True
        return False

    def push_input(self, raw: bytes) -> None:
        self.helper.push(raw)

    def resize(self, cols: int, rows: int) -> None:
        cols = max(3, int(cols))
        rows = max(1, int(rows))
        with self._lock:
            self._cols = cols
            self._rows = rows
            self.view._screen_alt.resize(cols, rows)
            self.view._screen_normal.resize(cols, rows)
            self.helper.resize(cols, rows)
            self._dirty.set()

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            screen = self.view._screen_current
            cursor = list(screen.getCursor())
            data = screen._canvas._data
            colors = screen._canvas._colors

            cells: list[list[list[Any]]] = []
            for y in range(self._rows):
                row: list[list[Any]] = []
                for x in range(self._cols):
                    ch = data[y][x]
                    if ch == "":
                        ch = " "

                    color = colors[y][x]
                    fg = color.fgToRGB() if color.hasForeground() else DEFAULT_FG
                    bg = color.bgToRGB() if color.hasBackground() else DEFAULT_BG
                    flags = (
                        (1 if color.bold() else 0)
                        | (2 if color.italic() else 0)
                        | (4 if color.underline() else 0)
                        | (8 if color.strikethrough() else 0)
                        | (16 if color.blinking() else 0)
                    )

                    row.append([ch, fg[0], fg[1], fg[2], bg[0], bg[1], bg[2], flags])
                cells.append(row)

            return {
                "type": "frame",
                "cols": self._cols,
                "rows": self._rows,
                "cursor": cursor,
                "cells": cells,
                "closed": self._closed.is_set(),
            }


class BridgeServer:
    def __init__(self, config: BridgeConfig) -> None:
        self.config = config
        self.model = TerminalModel(config.cols, config.rows, config.shell)
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()

    @staticmethod
    def _send_json(conn: socket.socket, payload: dict[str, Any]) -> None:
        data = (json.dumps(payload, separators=(",", ":")) + "\n").encode("utf-8")
        view = memoryview(data)
        while len(view):
            try:
                sent = conn.send(view)
                if sent == 0:
                    raise ConnectionError("socket connection broken")
                view = view[sent:]
            except (BlockingIOError, InterruptedError):
                # In non-blocking mode the socket may temporarily refuse writes.
                _, writable, _ = select.select([], [conn], [], 0.25)
                if not writable:
                    continue

    def _handle_message(self, message: dict[str, Any]) -> dict[str, Any] | None:
        mtype = message.get("type")

        if mtype == "resize":
            self.model.resize(int(message.get("cols", 80)), int(message.get("rows", 24)))
            return {"type": "ack", "event": "resize"}

        if mtype == "text":
            txt = str(message.get("text", ""))
            if txt:
                self.model.push_input(txt.encode("utf-8"))
            return None

        if mtype == "input":
            encoded = str(message.get("data", ""))
            if encoded:
                self.model.push_input(base64.b64decode(encoded))
            return None

        if mtype == "ping":
            return {"type": "pong"}

        return {"type": "error", "message": f"Unknown message type: {mtype}"}

    def serve_forever(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.config.host, self.config.port))
            server.listen(1)
            print(f"[bridge] listening on {self.config.host}:{self.config.port}")

            while not self._stop.is_set():
                conn, addr = server.accept()
                print(f"[bridge] client connected: {addr[0]}:{addr[1]}")
                try:
                    self._serve_client(conn)
                except Exception as exc:  # pragma: no cover - best effort logging
                    print(f"[bridge] client error: {exc}")
                finally:
                    try:
                        conn.close()
                    except OSError:
                        pass
                    print("[bridge] client disconnected")

    def _serve_client(self, conn: socket.socket) -> None:
        # Send initial handshake in blocking mode
        self._send_json(
            conn,
            {
                "type": "hello",
                "protocol": "ttk-godot-bridge-v1",
                "cols": self.config.cols,
                "rows": self.config.rows,
            },
        )
        self._send_json(conn, self.model.snapshot())

        # Switch to non-blocking for event loop
        conn.setblocking(False)

        recv_buffer = ""
        while not self._stop.is_set():
            if self.model.consume_dirty() or self.model.is_closed():
                self._send_json(conn, self.model.snapshot())

            readable, _, _ = select.select([conn], [], [], 0.03)
            if not readable:
                continue

            try:
                chunk = conn.recv(65536)
            except (BlockingIOError, InterruptedError):
                continue
            if not chunk:
                return

            recv_buffer += chunk.decode("utf-8", errors="ignore")
            while "\n" in recv_buffer:
                line, recv_buffer = recv_buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    self._send_json(conn, {"type": "error", "message": "Bad JSON"})
                    continue

                response = self._handle_message(message)
                if response is not None:
                    self._send_json(conn, response)


def parse_args() -> BridgeConfig:
    parser = argparse.ArgumentParser(description="Godot/pyTermTk terminal bridge")
    parser.add_argument("--host", default="127.0.0.1", help="TCP listen host")
    parser.add_argument("--port", type=int, default=18081, help="TCP listen port")
    parser.add_argument("--cols", type=int, default=100, help="Initial terminal columns")
    parser.add_argument("--rows", type=int, default=32, help="Initial terminal rows")
    parser.add_argument("--shell", default=None, help="Optional shell/program path")

    args = parser.parse_args()
    return BridgeConfig(
        host=args.host,
        port=args.port,
        cols=args.cols,
        rows=args.rows,
        shell=args.shell,
    )


def main() -> None:
    config = parse_args()
    server = BridgeServer(config)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()


if __name__ == "__main__":
    main()
