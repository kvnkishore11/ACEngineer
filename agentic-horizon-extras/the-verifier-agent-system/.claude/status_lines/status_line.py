#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Debug status line - report width detection."""

import json
import os
import shutil
import subprocess
import sys


def tty_width():
    try:
        with open("/dev/tty") as tty:
            r = subprocess.run(["stty", "size"], stdin=tty, capture_output=True, text=True, timeout=1)
        return int(r.stdout.split()[1])
    except Exception:
        return -1


def main():
    sys.stdin.read()
    cols_env = os.environ.get("COLUMNS", "?")
    shutil_w = shutil.get_terminal_size((-1, -1)).columns
    tty_w = tty_width()
    print(f"COLUMNS={cols_env}  shutil={shutil_w}  /dev/tty={tty_w}")


if __name__ == "__main__":
    main()
