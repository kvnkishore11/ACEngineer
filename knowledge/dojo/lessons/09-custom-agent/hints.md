# Hints — 09 custom-agent

## Hint 1

Read `run_session()` before filling anything — it shows you the two denial paths and their exact reasons: a tool missing from `TOOLS` is denied with "not in registry", and a call the hook rejects is denied with "blocked by hook". Now look at `fixtures/session.jsonl`: which of the four scripted calls should hit which gate? That tells you what to register and what to block.

## Hint 2

The registry wants exactly two entries — `"read_file": read_file` and `"list_files": list_files` — and pointedly not `run_bash`; the whole lesson is that you never register it. For the hook: `target` is already resolved for you. `Path.is_relative_to(WORKSPACE)` answers "is this inside the workspace?" — return `False` when it isn't. For the system prompt, the check looks for: "read-only", "QA", a cite-your-paths rule, and the literal `ANSWER:` prefix rule.

## Hint 3

Near-answer. Role line: `You are a read-only codebase QA agent. You answer questions about the files in workspace/ and you never modify anything.` Format rule: `Cite every workspace file path you read, and end every response with a final line that starts with "ANSWER:".` The hook:

```python
if not target.is_relative_to(WORKSPACE):
    return False
```

Registry:

```python
TOOLS: dict = {
    "read_file": read_file,
    "list_files": list_files,
}
```
