# STATUS: COMPLETE ✅

LENS: agent-systems

`ma-4-verifier-agent` — **The Pi Verifier Agent** companion rebuilt as a teaching-first Agent OS field guide.

## Deliverables

- `code/ma-4-verifier-agent.html` — compact companion centered on the commander boundary, observer harness, verifier contracts, closed correction loop, scoped safety, operation, and an agent-ops lab.
- `code/ma-4-verifier-agent-STATUS.md` — this status and grounding record.

## Agent interfaces covered

- Human commander contract: choose domain, write claim-style intent, define proof, prompt only the builder, observe Reports, and handle bounded escalation.
- Setup/priming interfaces: `.claude/commands/install.md`, `.claude/commands/prime.md`, `just prime`, and `just primepi`.
- Runtime cast: builder Pi, verifier Pi, domain persona, launcher/supervisor, deterministic verifier script, and the deliberate absence of runtime subagents.
- Operator surface: `just`, `just v`, `just vsql`, `just vpy`, `just vimg`, `just clean`, and same-process `/verify` attachment.
- Context/memory: original user prompt, `~/.pi/agent/sessions/<sid>.jsonl`, per-turn line bounds, `.pi/settings.json`, and project-local `.env` loading.
- Prompt contracts: generic/SQLite/Python/image persona frontmatter and bodies, spawn-time full system-prompt replacement, active `verify_on_stop.md`, and the currently unwired `builder_error.md` template.
- Model contract: persona `model:` selection, current shipped `openai/gpt-5.5` values, and model swap as a stable harness dimension.
- Tool/permission contract: persona `tools:`, launcher `--tools`, automatic `verifier_prompt` inclusion, verifier `tool_call` gate, missing `write`/`edit`, and persona-specific bash-policy differences.
- Harness/launcher: builder socket server, tmux/OS-window child spawn, generated wrapper/system-prompt files, startup diagnostics, input lock, connection UI, liveness, cleanup, and one-verifier limit.
- IPC protocol: JSONL framing, enforced direction matrix, start/stop/error events, hello/ack, prompt/ack, Report, ping/pong, and bye.
- Verification oracles: read-only SQLite wrapper, Python checker routes, image vision/relevance/readability contract, generic read-only-by-prompt surface, and structured rejection messages.
- Report/recovery contract: atomic evidence, five Report sections, confidence ladder, corrective follow-up delivery, loop counting, and human escalation after `max_loops`.
- Builder interoperability: `cross-agent.ts` command/skill discovery is builder-only; the verifier child does not load arbitrary cross-harness skills.
- Agent-ops lab: lower the image persona’s `MAX_TEXT_ELEMENTS` budget or harden the harness’s bash-prefix acceptance boundary, with observable fail→feedback→repair criteria.

## Accuracy decisions

- The current files, not the stale README limitations paragraph, are treated as operational truth: four full personas ship, and bare `just v` selects the generic `verifier` persona.
- The recording’s GLM 5.1/GPT-5.5 mix is period detail; all four checked-in persona files currently declare `openai/gpt-5.5`.
- “Read-only by architecture” is scoped. SQLite has persona tool narrowing, a script-only bash policy, and a read-only domain checker; Python also has script-only bash but runs tests; generic and image have no script-only bash policy.
- The current bash gate is described exactly as implemented: `cmd.startsWith(expected)`. It is meaningful narrowing, not parsed-argv or shell-free enforcement.
- SQLite query/PRAGMA routes use `mode=ro&immutable=1`, while dot-commands go through `sqlite3 -readonly`; no universal sandbox claim is made.
- `/tmp/pi-verifier/` mode `0700` is described as same-user filesystem authorization, not cryptographic peer authentication.
- The builder model is not described as unaware at the harness level: the builder-side extension owns status, socket, spawn, and correction injection; the builder model does not decide to invoke verification.
- Multi-verifier fan-out is not claimed. The server refuses a second verifier connection for the same builder.
- `plan-w-team.md` is indexed as a separate planning/team interface, not presented as part of the verifier’s runtime control loop.

## Page structure

1. Compact site bar
2. Agent mission card
3. Cast of agents and non-agent control surfaces
4. Agent-surface infographic
5. Human-boundary / closed-system control loop and worked SQLite run
6. Prompt, permission, launcher, and verification contracts
7. README/justfile operating sequence
8. Agent OS failure modes
9. Agent-ops lab with observable pass criteria
10. Six-sentence teach-back
11. Collapsible one-line-per-file index
