# Chore: rename settings.py to config.py

## Chore description
The module `app/settings.py` is imported in three places, but every other project on the team calls this file `config.py`. Rename the file and update every import so the codebase stays consistent — consistency is a powerful actor against complexity, for humans and for agents.

## Relevant files
- `app/settings.py` — the module being renamed; no logic changes
- `app/main.py` — imports `from app.settings import load_settings` at the top of the file
- `app/db.py` — imports `settings` to build the connection string
- `tests/test_settings.py` — rename to `tests/test_config.py` so the test tree keeps mirroring the source tree

## Step-by-step tasks
1. `git mv app/settings.py app/config.py`
2. Update the import in `app/main.py` to `from app.config import load_settings`
3. Update the import in `app/db.py` to `from app.config import settings`
4. `git mv tests/test_settings.py tests/test_config.py` and update its imports
5. Grep the repo for any remaining `app.settings` references and fix stragglers

## Validation commands
- `uv run pytest` — full suite passes, zero regressions
- `grep -rn "app.settings" app/ tests/` — returns nothing
- `python -c "from app.config import load_settings"` — the module imports cleanly
