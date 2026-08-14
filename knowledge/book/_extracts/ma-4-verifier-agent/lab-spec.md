# MA-4 Lab Spec — The Pi Verifier Agent

**Scope rule:** every drill runs inside the course codebase only (`codebase/` → `agentic-horizon-extras/the-verifier-agent-system`; the free public build is `git clone https://github.com/disler/the-verifier-agent.git`). No external repos. This is an **advanced** lab — it assumes you ship production code and are comfortable in a terminal.
**Prime directive (graded throughout):** you **never type an instruction into the verifier window** — it's input-locked by design. Every behavior change goes into the persona (`.pi/verifier/agents/*.md`), the script (`.pi/verifier/scripts/*.py`), or the prompt template (`.pi/verifier/prompts/verify_on_stop.md`). If you catch yourself wanting to "just tell the verifier," that's the lesson firing.
**Time box:** 60–90 minutes. Token cost: several builder+verifier turns; the verifier spends 2–5× the builder — real money, on purpose (spend tokens to save time). The image drill additionally needs an `OPENAI_API_KEY` (gpt-image-2).

---

## 0 · Setup (15 min)

1. Open the repo in your agentic coding tool and run `/install` (or the README's Manual install). It verifies `node≥20`, `pi`, `tmux`, `uv`, `python3≥3.11`, `sqlite3`, `just` are on PATH; runs `npm install`; validates personas/scripts; checks a provider key; and runs `npx tsc --noEmit` (must exit 0).
2. `chmod +x .pi/verifier/scripts/verify_sqlite.py .pi/verifier/scripts/verify_python.py`
3. Drop a provider key into a project-local `.env`. `OPENAI_API_KEY` is canonical (the personas default to `openai/gpt-5.5`, and the gpt-image-2 skill also uses it). Confirm presence without printing the value.
4. **Read the guarantee before you run anything (do not skip):** open `README.md`'s "three independent layers" section and `.pi/verifier/agents/verify_sqlite.md`. Answer in writing:
   - Which tools does the verifier persona declare — and which two mutation tools are *absent*? (`read, grep, find, ls, bash, verifier_prompt`; no `write`, no `edit`.)
   - What single bash command may the SQLite verifier run? (`uv run --script .pi/verifier/scripts/verify_sqlite.py <db> "<cmd>"`.)
   - What makes the DB connection read-only even if a mutation reached the script? (`mode=ro&immutable=1` + PRAGMA allowlist.)
   - What is the socket-directory authentication? (`/tmp/pi-verifier/` at `chmod 0700` — only your UID connects.)

**Checkpoint 0:** you can state, without looking, the three read-only layers and where each runs. If you can't, re-read — this is a graded outcome.

## 1 · Reproduce Dan — the SQLite loop with a planted defect (25 min)

Goal: watch the verifier catch a real, deliberately-introduced defect and drive the fix — hands off the keyboard.

1. Create a fixture DB with a **planted flaw**. Ask the *builder* (do NOT hand-write SQL if you're honoring TAC's "stop coding") to create `tmp/mock_shop.db` with `users`, `products`, and `orders`, but deliberately introduce one of: (a) `orders` missing its `PRIMARY KEY`, or (b) `orders.user_id` declaring a foreign key to a **mistyped** table (`user` instead of `users`).
2. Boot the pair: `just vsql`. Confirm a second OS window (or sibling tmux window) opens with the **input-locked** SQLite verifier; confirm the builder's input-box border shows `verifier connected`.
3. Prompt the builder: *"Inspect the schema of tmp/mock_shop.db and confirm every table has a primary key and every foreign key references a real table and column."*
4. On the builder's stop, watch the verifier **auto-start** (you type nothing). Confirm in its window that it:
   - reads only the turn's session-JSONL slice (not the whole file),
   - decomposes into atomic claims, and
   - runs the allowed script (`PRAGMA foreign_key_list(...)`, `PRAGMA integrity_check`, `.schema`).
5. Confirm it **FAILS** the flawed claim (`STATUS: failed`, `CONFIDENCE: FEEDBACK`), calls `verifier_prompt` with a *concrete* fix (exact table/column, suggested DDL), and that the builder receives it as a follow-up and repairs the schema — **without you typing anything**.
6. Confirm the next cycle returns `STATUS: verified` / `CONFIDENCE: PERFECT`, a green bar, and `atomic_claims_failed: 0`.

**Checkpoint 1 (write it down):** paste the verifier's atomic-claim list for one cycle. Circle the atom that failed and the exact tool output that proved it false. That output — not the builder's prose — is what "verified" means.

## 2 · Reproduce Dan — the image readability contract (20 min, needs OPENAI_API_KEY)

1. Boot `just vimg`. Prompt the builder to generate an architecture diagram **deliberately dense with labels** (ask for bullet lists inside every node — > 10 distinct text blocks).
2. Confirm the image verifier reads the actual image bytes, decomposes into atomic *visual* claims, and **fails the readability claim** because it exceeds `MAX_TEXT_ELEMENTS: 10` (open `.pi/verifier/agents/verify_image.md` and find that literal value).
3. Confirm it calls `verifier_prompt` naming the offending labels and a concrete fix (simplify / combine / use icons), the builder regenerates, and the next cycle passes.

**Checkpoint 2:** find the `MAX_TEXT_ELEMENTS: 10` line in the persona and change it to `6`. Regenerate a borderline image and show the threshold now bites at 6 — proving the rule lives in the file, not the model.

## 3 · Stretch drills (20–40 min, still zero typing at the verifier)

**S1 — Author a new domain verifier (the two-file pattern).** Clone `verify_sqlite.py` → `verify_<domain>.py` (keep the shebang, the PEP 723 header, the `emit()`/`reject()` JSON contract, and the argparse skeleton) and `verify_sqlite.md` → `verify_<domain>.md` (keep the 6-section body, the literal `## Report` block, and a `bash_policy` pointing at your new script). Boot it with `pi -e ./apps/verifier/verifiable.ts -e ./apps/verifier/cross-agent.ts --verifiable --verifier-agent verify_<domain>`. Good starters: an HTTP/endpoint verifier or a filesystem-artifact verifier.

**S2 — Prove the bash lockdown (security intuition).** Inside a running SQLite verifier, engineer a situation where the model tries an off-policy bash command (e.g. it decides to `INSERT`, or to `cat` a file). Confirm two things: (a) the tool-call hook **blocks** it with the structured teaching message that names the allowed form; (b) even a raw `INSERT` passed *through* the script is refused by `mode=ro&immutable=1`. Write one sentence on why enforcement outside the model matters more than a "please be read-only" prompt.

**S3 — Feed the flywheel.** Find a real entry under the Report's "What could you not verify? / What do you need from me to verify this next time?" Template that exact check into the persona or script so the gap is covered next run. Re-run and show the gap closed. This is the compounding loop — verifier accuracy that grows with every prompt.

**S4 — AND, not OR (model swap).** Change the verifier persona's `model:` from `openai/gpt-5.5` to a different provider (e.g. `z-ai/glm-5.1`, matching the video). Re-run drill 1 and confirm the pattern is model-agnostic — a different verifier model, same mechanic. One sentence: why is a *different* model from the builder better than the same one?

**S5 — Try to break the input lock.** Attempt to type into the verifier window. Confirm the `CustomEditor` swallows your keystrokes AND `pi.on("input")` rejects non-extension input (two independent layers). One sentence: how does this lock *force* templated engineering?

## Pass criteria (all required)

- [ ] You never typed a single instruction into the verifier; every change went into a persona / script / prompt template (prime directive).
- [ ] The verifier spawned automatically and ran on the builder's stop event with NO prompt from you (checkpoint 1).
- [ ] A planted defect was caught, the verifier sent a *concrete* corrective prompt, and the builder auto-corrected within `max_loops` (verify by watching `atomic_claims_failed` go to 0).
- [ ] You produced a Report with `STATUS` + `CONFIDENCE` + all five sections, including at least one honest "what could you not verify / what do you need from me" entry that you then templated (S3).
- [ ] You demonstrated the bash lockdown blocking an off-policy command (S2) OR the `MAX_TEXT_ELEMENTS` threshold biting after you edited it (checkpoint 2).
- [ ] Closing oral check, no notes: the two constraints and which one the verifier attacks; the three read-only layers; why it's AND (builder + a different verifier model), not OR; and why spending 2–5× the tokens makes you faster.

## Instructor / self-check notes

- **Most common stall — no second window opens.** The launcher branches on `$TMUX`: inside tmux you get a *sibling window* (check `tmux list-windows`), not a new OS window. If neither appears, the spawn-hello timeout (~3s) surfaces pi's real stderr in the builder — read it; the usual cause is an invalid persona `model:` id or a missing dependency. `just clean` clears stale tmux sessions/sockets/breadcrumbs from a prior crash.
- **Second stall — "the verifier verified nothing."** Domain verifiers have a **relevance gate**: the image verifier no-ops (`PERFECT`, 0 claims) on a turn with no image work; the Python verifier no-ops on a turn that only touched `.html`/`.css`. That silence is correct behavior, not a bug — match the recipe to the work.
- **Third stall — the verifier can't run its check.** If it reports `unsure` / `FAILED` with "no fixture / no oracle," that IS the flywheel output (S3). Don't fight it — template the missing check.
- **Model expectation:** the shipped personas default to `openai/gpt-5.5`; the *video* used GLM 5.1 (SQLite) and GPT-5.5 (image). Both are fine — the model is one frontmatter line (S4).
- **Cost:** the verifier deliberately burns 2–5× the builder's tokens. If a student balks at the spend, the "spend tokens to save time" conversation is the actual lesson surfacing early — price your review hours in.
- **What this lab intentionally does NOT cover:** stacking multiple verifiers behind one builder, three-layer orchestration (teams), and the teased agentic-security deep-dive — later material. Keep the two-agent primitive crisp.
