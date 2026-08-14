# Hints — 10 o-agent

## Hint 1

Read `worker.py` top to bottom before writing a line — the orchestrator only makes sense from the worker's perspective. Notice: the worker reads `fleet/<name>/inbox.txt`, appends to `fleet/<name>/status.jsonl`, and exits on the literal command `shutdown`. Every blank in `oagent.py` is just a file operation or one `subprocess.Popen`. The fleet directory IS the database.

## Hint 2

Per function:

- `create_agent`: `subprocess.Popen([sys.executable, str(WORKER), name], ...)` with `stdin`, `stdout`, and `stderr` all set to `subprocess.DEVNULL` (otherwise callers hang on the worker's inherited pipes). Then `(home / "manifest.json").write_text(json.dumps({...}))`.
- `command_agent`: `(home / "inbox.txt").write_text(text, encoding="utf-8")` — that's the entire command channel.
- `status`: `trail.read_text().splitlines()[-1]` → `json.loads` → print `f"{n}: {last['event']} — {last['detail']}"`.
- `delete_agent`: write `"shutdown"` to the inbox, then a `while` loop polling `pid_alive(pid)` with a 2-second deadline; finally `shutil.rmtree(home)`.

## Hint 3

Near-answer — the six blanks in order:

```python
# create_agent, blank 1
proc = subprocess.Popen(
    [sys.executable, str(WORKER), name],
    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
# create_agent, blank 2
(home / "manifest.json").write_text(
    json.dumps({"name": name, "purpose": purpose, "pid": proc.pid}, indent=2),
    encoding="utf-8",
)
# command_agent
(home / "inbox.txt").write_text(text, encoding="utf-8")
# status
last = json.loads(trail.read_text(encoding="utf-8").splitlines()[-1])
print(f"{n}: {last['event']} — {last['detail']}")
# delete_agent, blank 1
(home / "inbox.txt").write_text("shutdown", encoding="utf-8")
deadline = time.time() + 2
while time.time() < deadline and pid_alive(pid):
    time.sleep(0.05)
# delete_agent, blank 2
shutil.rmtree(home)
```
