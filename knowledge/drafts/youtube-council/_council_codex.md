# A Personal Operating Plan for Engineering Like IndyDevDan

## 1. Thesis

To think, create, and write codebases like Dan is to treat software engineering as the design of a **reliable operating environment for agents**. Your primary output is not lines of application code; it is a set of contracts, context surfaces, specialized roles, deterministic workflows, safety boundaries, observability, and executable verification that lets agents produce correct code repeatedly. Dan-style repos are usually small because each isolates one leverage point. Copy that compression: choose one control surface, make it legible to a fresh agent, close its loop with evidence, and only then compose it with others.

Throughout this plan, `ROOT` means `/Users/kvnkishore/WebstormProjects/AgenticEngineer/IndyDevDan`.

## 2. Anti-goals

- Do not watch all 71 course/public videos in order. Consume a lesson only to answer the next engineering question.
- Do not copy thumbnail rhetoric, product names, model rankings, or repo naming patterns. Those are packaging, not the transferable system.
- Do not rebuild Dan's full stack before mastering one seam. A hook with a test is better than a half-working “software factory.”
- Do not confuse many agents with orchestration. Every agent needs one purpose, explicit inputs/outputs, a tool boundary, and a downstream check.
- Do not accept an agent's prose report as verification. Trust commands, artifacts, diffs, tests, screenshots, logs, and an independent read.
- Do not turn file archaeology into study. Prime an agent around a question, predict the answer, then inspect only the decisive paths.
- Do not use a new toy product as the lab. Work on the course codebases and the `disler/*` clones already under `ROOT/youtube/_repos/`.

## 3. Mental model: the three-layer operating system

### Engineer layer: intent and economics

You choose the problem, define “done,” allocate models, set the risk budget, and decide when evidence is sufficient. Hermes is the scheduler and intake desk; Claude Code/Opus is the high-reasoning planner or builder; Codex is the independent implementation/review instrument; local Gemma/MLX handles cheap classification, summarization, and log reduction. Model choice is a policy per role, not a bake-off hobby.

### Agent layer: bounded intelligence

Agents plan, build, review, test, or verify—one purpose per invocation. Context is deliberately retrieved; prompts have typed sections; fresh contexts separate plan from build; specialists own narrow domains; verifier agents challenge claims. Multi-agent value comes from different responsibilities and failure modes, not headcount.

### Code layer: deterministic control

The repo is the agent OS: `CLAUDE.md`/instructions, `specs/`, skills and commands, hooks, task state, scripts, sandboxes, tests, logs, and workflow code. Deterministic code owns ordering, persistence, permissions, retries, and status. Agents own ambiguous reasoning. The core loop is:

`contract -> agent action -> deterministic check -> independent verification -> encode the gap -> clean rerun`

The last two steps matter most. A correction that exists only in chat is lost; a correction added to a prompt, hook, test, verifier persona, or workflow improves the next run.

## 4. Curriculum path: phases 0–4

Assume **90 minutes Monday–Friday, two hours Saturday, 30 minutes Sunday**. Every session uses 10 minutes of retrieval, 55 minutes of operation, 20 minutes of verification, and 5 minutes to record the next gap. Read `ROOT/book/_extracts/<lesson>/nuggets.md` before a transcript and use the adjacent `lab-spec.md` as the executable syllabus.

### Phase 0 — Establish the baseline (week 1)

- Run the TAC-3 plan/build separation in `ROOT/tac-3-success-is-planned/codebase/`, following `ROOT/book/_extracts/tac-3-success-is-planned/lab-spec.md`.
- Plan in one fresh agent; implement in another. Before each run, write your prediction of files, tests, and likely failure.
- Record baseline numbers: interventions, elapsed time, autonomous minutes, failed checks, and defects you found after the agent stopped.
- Exit criterion: one change passes its specified validation from a clean checkout, with no hand-written application code.

### Phase 1 — Master closed single-agent loops (weeks 2–3)

- Anchor lessons: TAC-5, TAC-6, and TAC-7. Work from their `ROOT/book/_extracts/.../lab-spec.md` files; use the course codebase symlinks, not copies.
- In `ROOT/tac-5-close-the-loops/codebase/`, require every prompt to contain a validation block and trace `adws/adw_test.py`.
- Practice focus in `ROOT/tac-6-let-your-agents-focus/codebase/`: split mixed work into planner, implementer, and tester responsibilities.
- Practice zero-touch execution in `ROOT/tac-7-zte-secret-of-agentic-engineering/codebase/`: move recurring human nudges into code or prompt contracts.
- Exit criterion: three consecutive small tasks reach green checks without an in-run human correction.

### Phase 2 — Make repos agent-operable (weeks 4–5)

- Anchor lessons: TAC-8, AH-1, AH-2, and AH-3.
- Map the agentic layer in `ROOT/tac-8-the-agentic-layer/codebase/`; distinguish application files from agent-control files.
- Compare context and prompt formats using `ROOT/ah-1-rd-framework-context-window-mastery/codebase/` and `ROOT/ah-2-seven-levels-agentic-prompt-formats/codebase/`.
- Build one narrowly specialized role in `ROOT/ah-3-building-domain-specific-agents/codebase/` whose output is mechanically checkable.
- Exit criterion: a fresh agent can enter one chosen repo, locate the task contract, run the correct checks, and report evidence without you naming files.

### Phase 3 — Orchestrate and verify (weeks 6–7)

- Anchor lessons: AH-4, AH-6, MA-2, and MA-4.
- Trace one workflow end-to-end in `ROOT/ah-6-building-agentic-layers/codebase/adws/`: trigger, persisted state, agent step, log, check, terminal status.
- Run the verifier lab from `ROOT/book/_extracts/ma-4-verifier-agent/lab-spec.md` against `ROOT/ma-4-verifier-agent/codebase/`.
- Deliberately plant a bounded defect. Require the verifier to decompose the builder's claims and cite tool evidence.
- Exit criterion: builder and verifier close one defect loop without a human-authored follow-up prompt.

### Phase 4 — Compose a small software factory (weeks 8–10)

- Use `ROOT/ah-6-building-agentic-layers/codebase/` as the integration reference, not as a template to copy wholesale.
- Compose only the surfaces already mastered: plan contract, isolated builder, event log, deterministic tests, read-only verifier, bounded retry, final human gate.
- Run five real maintenance tasks on a Dan course/public repo. After each, improve exactly one OS surface based on the observed gap.
- Exit criterion: at least four of five tasks finish with replayable artifacts and no mid-run intervention; a fresh verifier can reconstruct why each task passed.

## 5. The 60–90 minute codebase study ritual

1. **Frame one question (5 min):** “Where is completion decided?” or “What prevents a dangerous command?” Never “understand the repo.”
2. **Predict (5 min):** write the likely control flow and decisive files from memory.
3. **Prime with an agent (10 min):** ask for a path-level map with entry point, state transitions, output artifacts, and verification commands. No edits.
4. **Trace one golden path (15 min):** follow a single trigger to terminal state. In an ADW, trace one ID through workflow state, agent prompt, raw output, logs, commit/PR, and tests.
5. **Trace one failure path (10 min):** locate timeout, non-zero exit, malformed output, permission denial, retry, and human escalation behavior.
6. **Operate it (20 min):** run the smallest safe example. Capture the exact command, artifact, duration, and exit status.
7. **Challenge it (10 min):** have a different model review the claims against the diff and checks. Seed one safe failure when possible.
8. **Teach back (5 min):** explain the seam without notes: what is deterministic, what is agentic, what proves success, and where you would encode the next fix.

## 6. Authoring a Dan-style codebase

### Checklist

- One-sentence problem and one named control surface.
- A 60-second README: purpose, architecture, install, one command, expected evidence.
- Small application core; agentic layer visibly separate from business logic.
- Task contract with goal, inputs, constraints, non-goals, acceptance criteria, and validation commands.
- One agent, one prompt, one purpose; explicit output path/schema.
- Least-privilege tools and a disposable branch, worktree, container, or sandbox.
- Structured events with run ID, step, status, timestamps, model, cost, and artifact paths.
- Deterministic checks at each boundary; no success status derived only from model prose.
- Read-only independent verifier for medium/high-risk claims.
- Bounded retry and explicit escalation; no infinite “keep trying” loop.
- Fixtures for happy path and a planted failure.
- A clean-start replay command and a short post-run scorecard.

### Minimum viable agent OS

Start with only six surfaces: `README.md`, an agent instruction file, `specs/`, one `plan -> build -> verify` runner, `scripts/verify.*`, and `runs/<run-id>.jsonl`. Add skills, experts, dashboards, or teams only after a recorded failure demonstrates the need. If a fresh agent cannot identify the next task and its proof of completion in under two minutes, the OS is not yet legible.

## 7. First four personal projects

Work on personal branches/forks; preserve the local catalog as reference.

1. **Hook flight recorder:** in `ROOT/youtube/_repos/disler__claude-code-hooks-mastery/`, reduce the broad demo to one seam: capture `PostToolUse`, `PostToolUseFailure`, and `Stop` into normalized JSONL keyed by run ID. Add fixture payloads and a command that proves ordering and redaction. Done means a fresh session produces a replayable event timeline.
2. **Plan contract:** in `ROOT/youtube/_repos/disler__planf3/`, author a compact project-local planning variant that must emit objective, non-goals, affected paths, risks, acceptance checks, and an evidence table. Test it on the same TAC-3 chore three times. Done means all plans satisfy a mechanical section/schema check and a fresh builder needs no clarification.
3. **Artifact verifier:** in `ROOT/youtube/_repos/disler__the-verifier-agent/`, follow its existing persona/script two-file pattern to verify filesystem deliverables: required paths, forbidden files, checksums or sizes, and test output. Done means it catches a planted missing artifact, sends one concrete correction, and passes after the builder repairs it without human prompting.
4. **Plan-build-verify ADW:** in `ROOT/ah-6-building-agentic-layers/codebase/`, add one workflow composition—not a new platform—that connects the plan contract, a builder, and the artifact verifier. Persist step state and cap correction cycles at two. Done means one safe maintenance issue completes AFK and one impossible issue terminates honestly with evidence.

## 8. Weekly operating loop

- **Monday — intake:** Hermes runs `ROOT/youtube/weekly_update.py`. Review only new/errored output, `ROOT/youtube/INDEX.json`, the new lesson's `STATUS.json`, `metadata/repos.json`, and `CODEBASE.md`. Admit at most one new idea to the week.
- **Tuesday — anchor:** pair that idea with one paid-course principle. Read its `nuggets.md`; retrieve the concept from memory before consulting the transcript.
- **Wednesday — reproduce:** run the relevant course `lab-spec.md` checkpoint unchanged. Save commands and evidence.
- **Thursday — mutate:** change one control surface in the course/public repo. State the expected behavioral difference before running.
- **Friday — verify:** use a different model as read-only verifier; rerun deterministic checks from clean state and plant one bounded failure.
- **Saturday — author:** rebuild the pattern in the same repo with fewer moving parts; write the 60-second README and teach-back.
- **Sunday — compound:** update the scorecard, promote one discovered gap into a reusable prompt/hook/test/verifier rule, and queue one question for Monday. New YouTube material never displaces an unfinished verification loop.

## 9. Metrics that indicate real transfer

Track a four-week rolling window:

- **Useful AFK ratio:** autonomous minutes that end in accepted evidence / total agent runtime.
- **First-pass closed-loop rate:** tasks reaching all checks without human correction.
- **Intervention density:** human nudges per agent hour; classify missing context, bad contract, unsafe tool, weak oracle, or infrastructure.
- **Evidence coverage:** acceptance claims backed by a deterministic check or independent observation / total claims.
- **Replay rate:** successful runs reproducible from clean state with one documented command.
- **Agent-operability latency:** minutes for a fresh agent to locate task, constraints, and validation.
- **Defect escape rate:** issues found by you after the verifier declared success.
- **System improvements:** observed failures converted into durable OS surfaces per week.

Do not score videos watched, prompts sent, tokens consumed, agents spawned, commits, or lines of code.

## 10. Risks and failure modes

- **Consumption gravity:** cap source study at 30% of weekly time; no lab, no next lesson.
- **Architecture cosplay:** adding orchestrators before one reliable loop. Earn every layer with a failure record.
- **False AFK:** an agent running unattended but producing unreviewable work. AFK counts only when evidence is accepted.
- **Verifier theater:** same context/model rubber-stamping the builder. Separate role, context, and preferably model; restrict verifier tools to read-only.
- **Prompt patching:** correcting a single run in chat. Move recurring corrections into the owning contract and rerun clean.
- **Unsafe autonomy:** permission skipping outside disposable environments. Use branches/worktrees/sandboxes, deny destructive commands, exclude production credentials, cap budget and retries.
- **Observability without decisions:** collecting logs nobody uses. Every event must support debugging, cost control, replay, or a gate.
- **Model churn:** changing models while the harness is unstable. Hold tasks and checks constant; swap a model only to answer a specific policy question.
- **Overfitting to Dan:** preserve the principles, but write your own smaller interfaces and explanations.

## 11. Immediate next seven days

### Day 1 — Baseline and retrieval

Read `ROOT/book/_extracts/tac-3-success-is-planned/nuggets.md` and the lab spec. Create a scorecard with the eight metrics above. Before opening code, draw the expected plan/build boundary.

### Day 2 — Plan, do not build

In `ROOT/tac-3-success-is-planned/codebase/`, run one `/chore` planning exercise in a fresh Opus session. Inspect the generated spec against its template and improve the template—not the plan—if a required check is missing.

### Day 3 — Build from cold context

Give only the spec to a fresh Codex or Claude builder. Run the repo's tests yourself. Ask the other strong model to review spec-versus-diff read-only. Record every intervention and escaped claim.

### Day 4 — Close the loop

Use `ROOT/book/_extracts/tac-5-close-the-loops/lab-spec.md` with `ROOT/tac-5-close-the-loops/codebase/`. Run one task with an explicit validation block; trace the produced logs and identify where success is actually decided.

### Day 5 — Start project 1

In a personal branch of `ROOT/youtube/_repos/disler__claude-code-hooks-mastery/`, specify the normalized three-event JSONL contract and fixture cases. Have an agent implement it. Do not expand beyond the flight recorder.

### Day 6 — Break and replay

Feed the recorder a failed tool payload and a secret-shaped value. Prove failure ordering and redaction, then run a clean real session. Use a second model to verify the timeline against raw inputs.

### Day 7 — Teach and decide

From memory, explain engineer/agent/code layers and demo the recorder in five minutes. Update the scorecard. Promote the largest observed gap into one durable surface. Start week 2 only if the TAC-3 change and hook recorder both replay from clean state; otherwise repeat the failing loop.
