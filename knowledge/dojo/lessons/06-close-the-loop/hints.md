# Hints — 06 close-the-loop

## Hint 1

Open `fixtures/payload_good.json` and read it as the hook will: it is exactly what arrives on your script's stdin. Find where the file path lives in that structure — that is your first blank. Then remember the protocol: exit 0 means "silent pass", exit 2 means "block, and stderr becomes feedback the agent reads". Only one other exit code in this file is ever correct, and it appears twice.

## Hint 2

Blank by blank in `hooks/validate_json.py`:
- The path nests two levels deep: get `tool_input` (a dict, default `{}`), then `file_path` (default `""`). Chain two `.get()` calls.
- The applicability test is the *inverse* — you exit 0 when the file is NOT ours: suffix is not `.json`, **or** `"data"` is not in `path.parts`.
- `missing` is a list comprehension over `REQUIRED_KEYS`, keeping each key that is `not in doc`.
- Both blocking exits are the literal `2`.

In `settings.sample.json`, the event that fires *after* a tool call is named exactly like its pre-call sibling — swap the prefix.

## Hint 3

Near-answers:

```python
file_path = payload.get("tool_input", {}).get("file_path", "")

if path.suffix != ".json" or "data" not in path.parts:
    sys.exit(0)

missing = [key for key in REQUIRED_KEYS if key not in doc]

sys.exit(2)   # both blocking exits
```

And in `settings.sample.json`, the blank key is `"PostToolUse"`. Sanity-check your hook by hand from the lesson directory:

```
python3 hooks/validate_json.py < fixtures/payload_good.json; echo "exit=$?"   # exit=0
python3 hooks/validate_json.py < fixtures/payload_bad.json;  echo "exit=$?"   # exit=2 + stderr
```
