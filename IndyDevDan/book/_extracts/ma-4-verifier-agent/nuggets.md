# MA-4 Nuggets — ranked for the struggling learner

Ordering rule: how much of the verifier's value collapses if this nugget is missing. Tier 1 is the load-bearing core; Tier 2 is the working machinery; Tier 3 is framing that keeps you honest and motivated.

---

## Tier 1 — If you remember nothing else

**1. The verifier attacks ONE of the only two constraints.**
Agentic engineering has two binding constraints: **planning** and **reviewing**. Everything else is downstream. The verifier collapses the *reviewing* side into a second agent that re-checks every turn for you. That's the entire reason it's high-leverage — it's not "another bot," it's an attack on the thing that actually eats your day.
*Why weak learners lose it:* they think the payoff is "more automation." The payoff is specifically **your review hours back**.

**2. Verification = decomposition into atomic claims.**
"I created the table" is not one thing to check — it's five (table exists, columns, primary key, FKs, defaults). The verifier's job is to pull every bundle apart into the smallest true/false propositions and prove each against *actual state*. The agent's summary is a **claim, never proof** — every PASS must cite a real tool output (a `PRAGMA` row, a `SELECT count(*)`, the image bytes).
*Test yourself:* a single green "✅ done" — is that verification? (No. It's exactly where silent bugs hide.)

**3. Spend tokens to save time.**
The verifier burns 2–5× the builder's tokens per turn. If you optimize tokens, that's waste. If you optimize **time**, it's the best trade on the board. Tokens are cheap and getting cheaper; your hours are not and never will be.
*Say it Dan's way:* "Quite literally spending 5x tokens to make sure that I spend less of my time."

**4. It runs UNPROMPTED, and you can't type at it.**
On the builder's stop event the verifier fires on its own — hands off the keyboard. And its input bar is **locked**: you literally cannot drop a one-off instruction into it. When it misses something, your only move is to edit the persona, the script, or the prompt template. That's not a limitation; it's the mechanism that forces you to fix the whole *class* of problem, not the one instance.

---

## Tier 2 — The working machinery

**5. Trust AND scale — the rare pattern that does both.**
Most agentic moves trade one for the other (review deeper → slower; more compute → less trust per output). The verifier does *more work* (scale) AND attaches a deterministic proof to every claim (trust), in the same run. If you can only keep one sentence about *why* the verifier matters, keep this one.

**6. The builder doesn't know the verifier exists (top-down observer).**
Only lifecycle ticks (start / stop / error) cross the private unix socket at `/tmp/pi-verifier/<sid>.sock`. No transcript content on the wire. The verifier pulls the turn's slice from the builder's session JSONL on disk (`~/.pi/agent/sessions/<sid>.jsonl`) and does its own checking. The one thing it can push back is a correction via the `verifier_prompt` tool.

**7. Read-only is enforced by ARCHITECTURE, not by prompt — three layers.**
(1) Persona `tools:` has no `write`/`edit`, so Pi never registers them. (2) A tool-call hook blocks any bash that isn't `uv run --script verify_sqlite.py`, and the block reason is a *teaching message* — "the error message is the documentation." (3) The script opens the DB `mode=ro&immutable=1` with a PRAGMA allowlist. All three must fail before anything mutates. "Please be read-only" in a prompt is **not** security.

**8. Bash is the most dangerous tool — lock it to one script.**
Dan's blunt version: the bash tool is "a ticking time bomb." Restricting it to a single allowed script is "the highest level of control you can give." This is the concrete, do-it-today takeaway even if you never build the full two-agent system.

**9. The Report is a flywheel: "what could you not verify / what do you need from me?"**
Every cycle ends with those two questions. Whatever the verifier couldn't prove is the *exact* next thing you template into the script or persona. Verifier accuracy **compounds** with every prompt you write — a positive feedback loop, not a one-off check.

**10. AND, not OR — a different model verifies.**
Builder = Opus 4.7; verifier = GPT-5.5 (image) or GLM 5.1 (SQLite). Two *different* models = two independent perspectives, each catching the other's misses. The persona's `model:` field pins the verifier's model, so a two-model system is one frontmatter line. Every benchmark tests one model alone; you don't have to.

---

## Tier 3 — Framing that keeps you going

**11. Two camps, and the gap is widening.**
Camp A prompts a single agent back and forth (in 2026 that feels like hand-typing code did in 2025). Camp B builds coordinated multi-agent systems. The verifier is the *simplest* door from A into B — the first multi-agent system Dan says most engineers can actually build.

**12. Work on the system that builds the system.**
"You don't want to be working on your application anymore... you work on the agentic system." The verifier is an *extension layer* of specialized validation you bolt onto whatever your primary agent is — and you can stack more than one.

**13. One agent, one prompt, one purpose.**
A focused agent is a performant agent. Each verifier does exactly one job (image readability, SQLite integrity, Python types/tests) and stays silent when its domain isn't engaged (relevance gate). Don't build one do-everything verifier; specialize and stack.

**14. Own your agent harness.**
The input lock, the tool narrowing, the bash override, the auto-spawn — none of it is possible without control over the harness. Stock tools (Claude Code / Codex / Gemini / open-code) change underneath your feet; a harness you own doesn't. The transferable point isn't "use Pi" — it's "you need control over the tool surface and lifecycle."

**15. 2026 is the year of trust.**
"Do you trust your agents to do what you ask them to? And then, how much? At what scale?" Trust and scale are the two knobs; the verifier is one of the few moves that turns both. That's why Dan says to dial into it rather than skip over it.

---

## Micro-quiz (close the book first)

1. What are the two constraints of agentic coding, and which one does the verifier attack?
2. What is an atomic claim, and why is one coarse PASS worse than three explicit FAILs?
3. State the core trade in one line, and name the two quantities exchanged.
4. Why can't you type at the verifier — and what must you do instead when it misses something?
5. Name the three read-only layers and where each one runs.
6. Why "AND, not OR," and what single line of config makes a two-model system real?
7. What two questions end every Report, and why are they a flywheel?

*(Answers: nuggets 1, 2, 3, 4, 7, 10, 9 — or extract.md ideas 2, 3, 4, 6, 7, 8, and the Report contract.)*
