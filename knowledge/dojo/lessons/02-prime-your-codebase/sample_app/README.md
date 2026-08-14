# TaskTrail

A tiny task tracker. Add tasks, list them, mark them done. Tasks persist to a JSON file
next to the code (path set in `config.json`).

## Usage

```bash
python3 app.py add "write the prime command"
python3 app.py list
python3 app.py done 1
```

## Layout

- `app.py` — CLI entry point: parses argv and routes commands to the store.
- `db.py` — storage layer: load/save tasks as JSON.
- `config.json` — settings: app name, database path, limits.
