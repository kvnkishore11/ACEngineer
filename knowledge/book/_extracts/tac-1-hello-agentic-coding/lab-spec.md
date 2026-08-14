# TAC-1 Lab Spec — Hello Agentic Coding

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `tac/tac-1`; students: `git clone https://github.com/disler/tac-1.git`). No external repos, no extra dependencies beyond the lesson's prerequisite tools.
**Prime directive (graded throughout):** you type **zero** lines of application code by hand. Even file edits in the stretch drills go through Claude Code.
**Time box:** 45–75 minutes. Token cost: one interactive demo pair + 3–5 headless runs (small; but real — pay to play).

---

## 0 · Setup (10 min)

1. Fresh directory for TAC codebases → `git clone https://github.com/disler/tac-1.git && cd tac-1`
2. Verify the toolbelt: `claude --version`, `uv --version`, `git --version`; optional `bun --version` (TS variant). Windows: run everything inside WSL.
3. **Permissions audit (do not skip):** open `.claude/settings.json` and answer in writing:
   - Which three file tools may the agent use freely?
   - Which four git subcommands are allowed? Which git subcommands are NOT (e.g. `push`)?
   - What single non-local tool is enabled? (`WebSearch`)
4. Open the repo in your IDE, open the terminal (Cmd+J in VS Code), run `claude`.

**Checkpoint 0:** you can state, without looking, what the agent may do. If you can't, re-read the file — this habit is a graded outcome.

## 1 · Reproduce Dan — interactive A/B (15 min)

**A. Phase-1 prompt.** Copy the README **AI Coding Prompt** into Claude Code; fire.
- Verify: `main_aic.py` exists; `uv run main_aic.py` → `goodbye ai coding`.
- Note what did NOT happen: no branch, no commit, no execution by the agent.

**B. Phase-2 prompt.** Copy the README **Agentic Coding Prompt**; fire. Watch the todo checklist form, then drain.
- Verify all five engineering actions:
  1. `git branch --show-current` → `demo-agentic-coding`
  2. `main_tac.py` exists; `uv run main_tac.py` → `hello agentic coding` + one-line AI-agent definition
  3. both files were executed by the agent (outputs visible in its trace)
  4. `git log --oneline -1` → `Demo agentic coding capabilities`
  5. the agent reported what it did and cleaned up its todos

**Checkpoint 1 (write it down):** list the five actions prompt B performed that prompt A didn't. This list IS the AI-coding → agentic-coding delta.

## 2 · Reproduce Dan — programmable/headless (15 min)

1. Read `programmable/prompt.md`. Spot the two differences from the README agentic prompt *before* running anything: (a) it also CREATEs `main_aic.py` — self-contained, no dependency on drill 1; (b) it ends with a `REPORT:` block demanding the exact output of both .py files.
2. Clean slate exactly like Dan: `git checkout main && git branch -D demo-agentic-coding`
3. From a fresh terminal on `main`: `uv run python programmable/programmable.py` — hands off. No interaction allowed.
4. When it returns, verify: branch re-created, both files re-created, commit present, and the printed REPORT contains the exact outputs (cross-check by running both files yourself).
5. Run the same workflow via the other two launchers (reset the branch between runs):
   - `sh programmable/programmable.sh`
   - `bun run programmable/programmable.ts`

**Checkpoint 2:** all three launchers drove the identical workflow. Say in one sentence why the language didn't matter. *(Claude Code runs in the terminal; anything with terminal access can call `claude -p` — the agent is a function.)*

## 3 · Stretch drills (15–30 min, still zero hand-typing)

**S1 — Extend the REPORT (closed-loop thinking).** Using Claude Code (not your editor), edit `programmable/prompt.md` so REPORT also includes the current git branch name. Reset the branch; rerun the Python launcher; verify the report changed accordingly.

**S2 — Fourth launcher (prove the pattern).** Ask Claude Code to add a launcher in another language available on your machine (e.g. plain Node, Ruby, Go — anything with terminal access), following the existing three as style guides. Reset; run it; verify the identical workflow.

**S3 — Break the tool surface (permissions intuition).** Via Claude Code, remove `"Bash(git commit:*)"` from `.claude/settings.json`. Rerun the agentic prompt and observe precisely where and how the workflow halts or asks. Restore the permission. Write one sentence: what does this teach about the tools circle of the core four? *(The tool surface bounds what an agentic prompt can accomplish; permissions are part of the system design.)*

**S4 — Map to your job (transfer).** Time drill 1A and 1B. Then write two lists from your actual work: tasks that are AI-coding-prompt-shaped vs agentic-coding-prompt-shaped. Circle the one agentic-shaped task you'd automate first with the `programmable/` pattern.

## Pass criteria (all required)

- [ ] Zero application code typed by hand anywhere in the lab
- [ ] Permissions audit answers correct (checkpoint 0)
- [ ] Five-action delta list correct (checkpoint 1)
- [ ] `demo-agentic-coding` branch exists with commit `Demo agentic coding capabilities` containing `main_aic.py` + `main_tac.py`
- [ ] `uv run main_tac.py` prints "hello agentic coding" + a one-line AI-agent definition
- [ ] All three (or four, with S2) launchers completed headlessly with a REPORT matching the real outputs
- [ ] Closing oral check, no notes: the core four; the one-dimension delta; Claude Code's three essential elements; the contradicting truth resolved in one sentence

## Instructor / self-check notes

- **Most common stall:** the "new/existing branch" wording — if the branch already exists from a prior run, the agent may reuse it and the student thinks something broke. Fix: always `git branch -D demo-agentic-coding` between runs (Dan does exactly this on camera at ~17:56).
- **Second stall:** running the programmable script from inside the `demo-agentic-coding` branch instead of `main` — teaches why runbooks state their starting state.
- **Cost anxiety:** each headless run is a small number of agent turns; the lab total is modest. If a student can't run it at all, the budget conversation (pay to play) is the actual lesson surfacing early.
- **What this lab intentionally does NOT cover:** skills, triggers, parallelism, CI embedding — later lessons. Deflect scope creep to keep the primitive crisp.
