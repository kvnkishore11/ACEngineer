# Hints — 03 · leverage-points

## Hint 1

Six marked sites, two leverage points. The three print sites open standard out — after every
action, say what happened and name the task. The three signature sites open types — annotate
every parameter and the return. Replace each marker comment with real code (for the loop in
`list_tasks`, the `pass` goes away too). Behavior must not change otherwise: same commands,
same tasks.json.

## Hint 2

- Stdout: `add` prints something like `added #<id>: <text>`; `list` prints one line per task
  with its id, a done/open marker, and its text; `done` prints a confirmation containing the
  word done and the id.
- Types: the task collection is `list[dict]`, task text is `str`, the id is `int`.
  `add_task` returns the new task (`dict`); `list_tasks` returns nothing (`None`);
  `complete_task` returns the task or nothing (`dict | None`).

## Hint 3

Near-answers:

- `def add_task(tasks: list[dict], text: str) -> dict:` with
  `print(f"added #{task['id']}: {task['text']}")` after the save.
- `def list_tasks(tasks: list[dict]) -> None:` with
  `print(f"#{task['id']} [{'done' if task['done'] else 'open'}] {task['text']}")` in the loop.
- `def complete_task(tasks: list[dict], task_id: int) -> dict | None:` with
  `print(f"done #{task['id']}: {task['text']}")` before the `return task`.
