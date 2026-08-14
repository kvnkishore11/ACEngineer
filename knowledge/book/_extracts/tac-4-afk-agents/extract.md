# TAC-4 · AFK Agents — Master Teaching Notes

> Source of truth for the expanded chapter. Video 46:25 · Intermediate · Tactic #4: **Stay Out The Loop**
> Lesson artifact: a full **agentic layer** — 9 ADW files + 13 reusable prompts + 5 hooks — wrapped around an untouched app. Two live runs on camera: a documentation chore (issue #31 → PR #32, ~5 min) and a real feature (issue #33 "Jsonl Support" → PR #34, ~17 min).

**Lesson thesis in one sentence:** Most engineering work doesn't need you in the loop — so assemble the four PITER elements (Prompt input, Trigger, Environment, Review) around AI Developer Workflows that chain your lesson-3 templates through Claude Code in programmable mode, and let chores, bugs, and features become pull requests while you're away from the keyboard.

**The chapter must land ten ideas.** Each below follows: Hook → Picture → Worked example (course codebase) → Dan's term → Failure mode → Retrieval Q.

---

## Idea 1 — Two loops: in-loop vs out-loop agentic coding

**Hook.** You already stopped typing code (TAC-1). But you're still *there* — sitting at the device, prompting back and forth, back and forth. Dan's claim: the tech ecosystem is obsessed with human-in-the-loop systems and misses the trend that *increasingly more chores, bugs, and features don't require your expertise at all*. There is a second kind of agentic coding, and it hands off exponentially more work.

**Picture.** Frame t0240 (4:00): the **Agentic Coding KPIs** slide — Size ↑ (1480 Ops), Attempts ↓ (8), Streak ↑ (7 runs), Presence ↓ (10, "want to minimize") — the scoreboard the tactic exists to move. (The 2:55 "IN LOOP AGENTIC CODING" kinetic-text beat sets the contrast; the chapter can render the in/out comparison as a designed two-column diagram.)

**Worked example.** Demo 2's punchline: a real feature (JSONL upload support) shipped from a GitHub issue with zero mid-run interaction — "this was a feature that an engineer may have picked up themselves, and it was completely unnecessary."

**Dan's term.** *In-loop* (classical human-in-the-loop) vs ***Outloop* agentic coding** — "off-device agentic coding... you go AFK, away from keyboard. You walk away from your keyboard, or maybe you were never there in the first place. Maybe you sent the prompt right from your phone on GitHub, Slack, Notion, Jira, a text message." The honest split: in-loop stays great for *experimentation, exploring new territory, and very, very hard, very specific problems* — "but let's be real, most of engineering is not that." The trend bet: *models will improve and tools will change*, so an out-loop system solves more every month for free. And the KPI tie-in: "we want presence down, size up, streak up, attempts down."

**Failure mode.** Binary thinking in either direction: "everything out-loop" (then the one genuinely hard problem produces a garbage PR and trust collapses) or "nothing out-loop until it's perfect" (the tactic dies waiting). The lesson's routing rule is class-based, not all-or-nothing.

**Retrieval Q.** Define out-loop agentic coding in one phrase, and name the three kinds of work Dan keeps in-loop. *(Off-device agentic coding — prompt in, you're AFK; experimentation, new territory, very hard specific problems.)*

---

## Idea 2 — Own your pipeline: the anti-cloud-tools argument

**Hook.** Copilot, Devin, Jules, Codex — Dan has used them all, and the lesson opens by promising you'll *replace and outperform* them. Not because they're bad: because they're "literally designed for everyone's codebases, not yours."

**Picture.** Designed pull-quote territory (the beat is spoken over B-roll): "Just like the prompt, your agentic pipeline is too valuable to outsource to a third party tool, especially this early in phase two of the generative AI age."

**Worked example.** The JSONL feature demo *is* the argument: the issue encodes house rules (std lib only, `__` delimiter *stored in a constants file*, `_0` list indexing, fixtures in the test dir) and the templates encode how this codebase plans, validates (`cd app/server && uv run pytest`), commits, and PRs. No rented agent knows those rules; this pipeline runs on nothing else.

**Dan's term.** *Own your agentic pipeline* / "**this one size does not fit all**, especially as your product grows and becomes unique and differentiated." Late-lesson restatement: "these tools are not running your templates... not built to solve your problems."

**Failure mode.** Hearing "never use cloud tools" (Dan doesn't say that) — or the opposite: evaluating this lesson's DIY stack on convenience alone ("GitHub already has agents") and missing that the *pipeline* — templates + workflows + standards — is the asset being built, whoever hosts the compute.

**Retrieval Q.** Why do cloud agentic tools have "natural limits" for your codebase, per Dan? *(Designed for everyone's codebases, not yours — they don't run your templates/prompts/practices, and one size does not fit all as your product differentiates.)*

---

## Idea 3 — PITER: the four elements of AFK agents

**Hook.** "Staying out the loop sounds great — how does it actually work?" Four elements. Miss any one and the system isn't AFK: no prompt input → nothing to do; no trigger → someone must press go; no environment → it runs where you're working; no review → you can't trust what shipped.

**Picture.** Frame t0521 (8:41): the four colored letter-cards **PI · T · E · R** over the keyboard — the lesson's mnemonic image. Frame t0605 (10:05): T+E made flesh — the screen-shared Mac mini running `uv run adws/trigger_webhook.py` (port 8001, `POST /gh-webhook`) beside GitHub's new-issue form.

**Worked example.** Demo 1's full instantiation: **P** = GitHub issue #31 (title + description are the prompt) · **T** = GitHub webhook → `adws/trigger_webhook.py` (fires on `issues:opened` or a comment that is exactly `adw`; responds instantly and `Popen`s the workflow to beat GitHub's 10-second timeout) · **E** = "IndyDevDanAgents's Mac mini," exposed via a Cloudflare tunnel (`scripts/expose_webhook.sh`) · **R** = PR #32 plus the live issue-comment feed. Demo 2 swaps T and E (manual command, local device) *without touching P or R* — proving the elements are independently swappable.

**Dan's term.** The *four elements of AFK agents*, remembered with **PITER** — "prompt input, trigger, environment, review. With this setup, your agents can run while you're AFK." Tool-agnosticism is explicit: "these four elements can be anything... Don't read into how this is configured too much. Focus on the composable units." Recommended defaults: GitHub issues + GitHub PRs; start trigger/environment local, then offload to another device.

**Failure mode.** Config fixation — "I don't own a Mac mini / we use Jira, so this isn't for me." The tell of a student who missed the abstraction: they can't re-map the four elements onto their own stack in one minute. Second failure: forgetting a trigger is still live (webhook/cron listening) and burning tokens on every stray issue.

**Retrieval Q.** Expand PITER and give the lesson's tool for each element; then name the two elements demo 2 swapped. *(Prompt input=GitHub issues; Trigger=webhook [also cron/manual]; Environment=dedicated Mac mini; Review=PRs + comment feed. Demo 2: trigger→manual command, environment→local device.)*

---

## Idea 4 — The ADW: AI Developer Workflow

**Hook.** Between trigger and review something has to *run the work*. Not a mega-prompt — a workflow: the highest leverage point and highest composition level of agentic coding, with a name pulled forward from Principled AI Coding so you take it seriously as a unit of engineering.

**Picture.** Frame t1630 (27:10): the anatomy in five docstring lines at the top of `adws/adw_plan_build.py` — Fetch GitHub issue → Create branch → Plan Agent → Build Agent → Create PR — plus environment requirements. (Note for accuracy: that docstring's `feature/issue-{number}-{slug}` branch example predates the real `/generate_branch_name` contract — the code's own comments drift; see Idea 9.)

**Worked example.** `adws/adw_plan_build.py` (536 lines, a uv single-file script — "these can be Bun scripts if you want, shell scripts, whatever you want; the whole point is that they're a layer on top of your codebase"). One issue number in; classification, branch, committed plan, implementation, commits, PR out.

**Dan's term.** ***ADW — AI Developer Workflow***: "a reusable agentic workflow that combines code, agentic prompts, and agents to deliver results autonomously... the synthesis of previous generation deterministic code and new generation non-deterministic language models, prompt chains, and now agents." The future claim: "in the future these will just be known as scripts, and we'll fully expect agentic behavior by default." Aliases on camera: agentic pipeline, agentic workflow, compositional workflow — "so many names for the same thing."

**Failure mode.** Treating the ADW as "a script that calls an API" and rewriting it as one giant prompt — losing the deterministic error handling, the per-step observability, and the ability to improve any single step. Opposite failure: over-engineering an orchestration framework instead of one 500-line file ("don't get too meta, let's keep it simple" — said when noting ADWs can operate on ADWs).

**Retrieval Q.** Recite the ADW definition and the five workflow steps of `adw_plan_build.py`. *(Reusable agentic workflow combining code + agentic prompts + agents to deliver results autonomously; fetch issue → branch → plan agent → build agent → PR.)*

---

## Idea 5 — The agentic layer: two essential directories, app untouched

**Hook.** Where does all this live? Not in your app. The entire out-loop machine is two directories you could drop into any codebase you operate.

**Picture.** Frame t1460's left rail (24:20): the repo tree with `adws/`, `.claude/`, `app/`, `scripts/`, `specs/`, `ai_docs/`, `logs/` — the layer visibly *around* the product. (Chapter may add a designed ring diagram: app core, agentic layer, GitHub surface.)

**Worked example.** "Notice how `app/` is completely untouched here. We're not combining or conflating the functionality between these two. The ADWs combined with your prompts... these two directories and their content form the agentic layer around your codebase." Supporting cast in-repo: `specs/` holds four pre-existing plans (worked examples of each template's output shape), `ai_docs/` pins reference docs agents can read (Claude Code CLI, SDK, E2B, provider quick-starts), `scripts/` holds start/stop/reset utilities the templates call.

**Dan's term.** *The agentic layer* — built "by dedicating and focusing really hard on these two essential directories: `.claude/commands`, aka wherever your prompts are stored, and ADWs, [where] compositional workflows are stored." The improvement loop: "you're gonna run some ADWs... that don't fully solve the problem. Then you'll spend some time, you'll invest in your templates, and then you'll compose them into your ADWs and you'll improve."

**Failure mode.** Conflating the layers — importing app code from ADWs, or letting the app depend on the agentic layer. The discipline (layer wraps app; app never knows) is what makes the layer portable and the app shippable without it.

**Retrieval Q.** Name the two essential directories of the agentic layer and the rule about `app/`. *(.claude/commands/ for prompts, adws/ for workflows; the app stays completely untouched by the layer.)*

---

## Idea 6 — Micro-agents: isolate the big three, one problem each

**Hook.** How does a 46-minute lesson chain *eight* agent invocations without the whole thing derailing? By refusing to build one big agent. Every step gets its own agent, its own template, its own fresh context window, its own model.

**Picture.** Frame t2020 (33:40): `agents/cb881e79/` expanded — `adw_plan_build`, `branch_generator`, `issue_classifier`, `plan_finder`, `pr_creator`, `sdlc_implementor`, `sdlc_implementor_committer`, `sdlc_planner`, `sdlc_planner_committer` — nine folders, nine isolated jobs from one feature run.

**Worked example.** From `adw_plan_build.py`: `issue_classifier` runs `/classify_issue` on the issue JSON; `branch_generator` runs `/generate_branch_name`; `sdlc_planner` runs the class template (`/chore`, `/bug`, or `/feature`); `plan_finder` extracts the plan path; `{agent}_committer` runs `/commit`; `sdlc_implementor` runs `/implement <plan-file>` — "its context window is completely free. We can select a more powerful model, which I recommend you do for the implementation... and we can use the plan that was created by our planner as the prompt for our implementer." On camera all steps pass `model="sonnet"` "just 'cause it's going to be a little faster, but you're going to want to throw top models into the most complex steps, which are going to be your plan and your build step."

**Dan's term.** "By separating our agents, we're able to **isolate the big three — context, model, prompt — to solve one problem and solve one problem well**." Also: "several micro agents doing their work" and the classify switch: "we can **target specific classes of problems**... this is a very important pattern of agentic coding."

**Failure mode.** The mega-prompt reflex — classify+plan+build in one run "to save tokens," producing context bleed (plan pollution in the implementation), unattributable failures, and no per-step model policy. Second failure: putting the expensive model on glue steps and the cheap one on the build — exactly backwards from the stated policy.

**Retrieval Q.** List the micro-agents of a feature run in firing order, and state Dan's model policy. *(issue_classifier → branch_generator → sdlc_planner → plan_finder → sdlc_planner_committer → sdlc_implementor → sdlc_implementor_committer → pr_creator; cheap/fast on glue, most powerful on plan and build.)*

---

## Idea 7 — Programmable mode: Claude Code as a pipeline primitive

**Hook.** tac-1 planted "the agent is a function you can call." tac-4 shows what that seed grows into: every micro-agent above is *one subprocess call* built by ~30 lines of Python.

**Picture.** Frame t1930 (32:10): `agent.py`'s `prompt_claude_code` on screen — `cmd = [CLAUDE_PATH, "-p", request.prompt]` + `--model` + `--output-format stream-json` + `--verbose`, with the `--dangerously-skip-permissions` branch highlighted.

**Worked example.** `execute_template()` composes `prompt = f"{slash_command} {' '.join(args)}"` (slash commands resolve to `.claude/commands/*.md` with `$ARGUMENTS`/`$1..$n` substitution), archives the exact prompt to `agents/{adw_id}/{agent}/prompts/`, streams output to `raw_output.jsonl`, converts to a readable `.json`, and parses the final `result` message for `success`/`session_id`/text. A minimal env allowlist (`get_claude_env`) passes only what's needed — `ANTHROPIC_API_KEY`, `CLAUDE_CODE_PATH`, PATH/HOME/etc., `GITHUB_PAT→GH_TOKEN` when present. Permissions: `--dangerously-skip-permissions` is always on for template runs — "it is running dangerously, but because it's in its own environment, this is going to be safe."

**Dan's term.** *Programmable mode* — "this is the value of programmable mode... It lets us use Claude Code as a **new agentic coding primitive**, where we can call our agent with any prompt at any step of our workflow that we need to automate engineering work."

**Failure mode.** Copying the dangerous flag without the E of PITER — yolo-permissions on a daily-driver machine with production credentials. The safety argument is *environmental isolation*, not model trust. Secondary: ignoring the JSONL result line (num_turns, duration, cost, is_error) and flying blind on what each step actually did.

**Retrieval Q.** Write the full command shape agent.py executes, and justify the dangerous flag in one sentence. *(claude -p "<slash_command> <args>" --model <sonnet|opus> --output-format stream-json --verbose --dangerously-skip-permissions; safe because the run is confined to a dedicated environment — the permission boundary is the environment.)*

---

## Idea 8 — Contracts + loud failure: how code chains non-deterministic agents

**Hook.** Deterministic code can't `if` on an apology paragraph. Every glue step in the ADW ends with a one-line output contract — and every step's result is checked, reported, or fatal.

**Picture.** Frame t1540 (25:40): the kickoff terminal — `issue_command: /feature`, `Created branch: feat-33-cb881e79-jsonl-support`, prompts saved per agent — machine-consumable outputs landing in code. (Also visible: Dan's real `Failed to spawn` error from running in the wrong directory — the honest 30 seconds every student will reproduce.)

**Worked example.** The contracts, verbatim from `.claude/commands/`: `classify_issue` — "Respond exclusively with '/' followed by the command... or `0` if the issue isn't any of the above"; `generate_branch_name` — "Return ONLY the branch name"; `commit` — "Return ONLY the commit message" (format `<agent_name>: <issue_class>: <message>`, ≤50 chars, present tense); `pull_request` — "Return ONLY the PR URL"; `find_plan_file` — "the path or '0' if not found." Python-side: `classify_issue()` validates membership in `["/chore","/bug","/feature"]`; `get_plan_file()` validates path-shape; `check_error()` posts `❌ {prefix}: {error}` to the issue and `sys.exit(1)`. Extension point: "you just add them here in your classify issue step, and then you update your data types" (`IssueClassSlashCommand` Literal).

**Dan's term.** "**No ad hoc prompts as strings inside of the codebase.** We're isolating all of our prompts so that we can improve them... Run either non-deterministic intelligence or a deterministic step. We then check for issues, do some logging, do some reporting, and then we continue."

**Failure mode.** Prompts that end with "explain what you did" feeding code that expects a bare token — the #1 self-built-ADW bug. Equally fatal: swallowing failures instead of failing loudly to the review surface; a silent half-run is worse than a visible dead one.

**Retrieval Q.** What may the classifier output, and what happens when any step's contract breaks? *(Exactly /chore, /bug, /feature, or 0; check_error logs it, comments ❌ on the issue, and exits the run.)*

---

## Idea 9 — Observe, report, log, monitor — then fix the SYSTEM

**Hook.** An agent that ships work you can't see is worthless: "It doesn't matter if our agent can solve every problem **if we don't know that it's solved**." And when you *do* see a mistake, the move that makes this tactic compound is refusing to fix the artifact.

**Picture.** Frame t0700 (11:40): issue #31's live feed — `5615f7c8_ops: ✅ Starting ADW workflow` → `✅ Issue classified as: /chore` → `✅ Working on branch: chore-31-5615f7c8-document-adw-directory` → `5615f7c8_sdlc_planner: ✅ Building implementation plan`. Frame t0890 (14:50): PR #32 with plan link, ADW Tracking ID `5615f7c8`, `Closes #31` — and the agent's real errors on screen (it expands ADW as "Agentic **Developer** Workflow" and describes plausible-but-nonexistent files). Frame t2245 (37:25): review's final form — the feature *working in the app*, `profile__location`/`profile__skills_0` columns proving the issue's conventions were honored.

**Worked example.** Four observability layers, all in-repo: (1) issue comments prefixed `{adw_id}_{agent_name}:` from `format_issue_message()`; (2) `agents/{adw_id}/` — saved prompts + `raw_output.jsonl` + `execution.log`; (3) `logs/{session_id}/` via the five Claude Code hooks in `.claude/settings.json` ("we activated this thanks to Claude Code hooks"); (4) the committed plan — "the planner created the plan and outputted a **concrete asset**... it's not enough to just run a random ad hoc prompt, because how will you know how to improve that? And more importantly, how will your agents know?" Then the doctrine, delivered over the PR's mistakes: "You don't fix the issue. **You fix the system that caused the issue.** You fix your templates, you fix your ADW." Bonus in-repo exhibit: `adws/README.md` itself carries agent-flavored inaccuracies (a wrong "edit agent.py line 129" model pointer; a commit-format section that doesn't match `commit.md`) — reviewing agent output is not optional.

**Dan's term.** *Observe / report / log / monitor*; *fix the system, not the issue*; *solve problem classes* — "ADWs and the prompt templates you build out for your codebase, they solve classes of problems that you no longer have to solve."

**Failure mode.** Watching the live feed like television and never opening `agents/{adw_id}/` — then a failed run is a mystery instead of a diff. And the artifact reflex: hand-editing the bad PR (the fix evaporates on the next run) instead of upgrading the template (the fix compounds forever).

**Retrieval Q.** Name all four observability surfaces of a run, and state the fix-the-system rule as policy. *(Issue-comment live feed, agents/{adw_id} artifacts, logs/{session_id} hook logs, committed plan file — plus the PR. Policy: when output is wrong, improve the template/ADW that produced it; never just patch the output.)*

---

## Idea 10 — The adoption path: health-check first, chores first, then climb

**Hook.** "I recommend you take action on this now. Like don't wait — **the ROI here is insane**." But the lesson is equally specific about *how* to start: validate the environment before every run, and climb the trust ladder from the bottom.

**Picture.** Frame t1460 (24:20): the health check — `Overall Status: HEALTHY`, the built-in "Repository still points to 'disler'" warning (aimed at YOU, the viewer), gh installed/authenticated, a live Claude Code 2+2 test, and the ✅ posted to issue #33. Frame t1355 (22:35): what a good first *feature* prompt looks like when you get there — constraints, not plans.

**Worked example.** `adws/health_check.py` — "something I highly recommend you build into your ADWs before you run your complex or simplistic workflow. You just want to know that everything's configured properly." Then the ladder: issue #31's two-line chore ("chores are the simplest unit of engineering work that your agent should be taking off your plate **with no debate at all**") before issue #33's constrained feature. Setup is itself agentic: `/install` removes the course remote, copies env samples, installs deps, and *reports* the actions you must take (push to your own repo — you can't PR the course repo). Between reruns: `scripts/clear_issue_comments.sh`, `scripts/delete_pr.sh`.

**Dan's term.** The *health check* pattern; the ladder — "start with low hanging fruit... **start templating out the chore** for your codebase, then move up to bugs, and then eventually you'll get to the feature level"; the goal state — "after the upfront install... you have an agent operating its own environment you can call using an out-loop system. This is massive impact." Closing frame: this tactic + lesson 3 are the hinge of the course — "this lesson is pivotal. Your ability to internalize lesson three and four will decide if you come out on top here. **Template and stay out the loop.**"

**Failure mode.** Skipping the health check and debugging its findings one mystery at a time (the disler-remote failure is near-universal); starting at the feature rung "to really test it" and rage-quitting on a mediocre PR; treating the ~5-min/~17-min demo timings as promises rather than one codebase's data points.

**Retrieval Q.** What does the health check verify, and what's the adoption ladder? *(Env vars, git remote [warns on disler], gh CLI auth, live Claude Code round-trip — optionally posting to an issue; chores → bugs → features.)*

---

## Timeline map (VTT-verified)

| Time | Beat |
|---|---|
| 0:14–1:26 | Cold open: step out of the loop; let your product build itself; replace Copilot/Devin/Jules/Codex; own your pipeline |
| 1:26–2:09 | Tactics 1–3 recap → Tactic #4: stay out the loop |
| 2:09–3:30 | Two types: in-loop (obsession, back-and-forth) vs Outloop (off-device, AFK, prompt from your phone) |
| 3:30–4:12 | Models improve/tools change; build the system that builds the system; KPIs: presence↓ size↑ streak↑ attempts↓ |
| 4:12–5:44 | Net-new agentic layer; "not playing today's game"; if you're not wrong now, you will be; PMF/TAM stakes |
| 5:44–6:40 | How it works; automate ~half the SDLC, prompt → PR; lesson-3 templates are mission critical; one size does not fit all |
| 6:40–8:18 | **ADW defined**; synthesis of deterministic code + non-deterministic models; "will just be known as scripts"; term from Principled AI Coding |
| 8:18–9:09 | **AFK agents; four elements; PITER** |
| 9:09–10:29 | Demo-1 element choices: issues / webhook (loot box for setup; watch first) / Mac mini (screen share) / PRs |
| 10:29–11:11 | Demo 1 prompt input: issue #31 `/chore` document adws/ |
| 11:11–12:50 | Webhook fires; live feed; classified /chore; branch `chore-31-5615f7c8-...`; planner → spec committed; implementor fresh context; model advice |
| 12:50–14:20 | Fundamentals never leave; "success is absolutely planned"; PR lands; **five minutes** total |
| 14:20–15:56 | PR #32 review; plan as implementer's prompt; **errors found → improve the prompt**; "ADWs can operate on your ADWs — don't get too meta" |
| 15:56–17:03 | PITER recap (webhook URL blurred); halfway through TAC = plan+build automated end to end |
| 17:03–17:55 | Elements can be anything; opinions encouraged; focus on composable units; kill the webhook for demo 2 |
| 17:55–20:17 | Fresh clone; Yolo mode + check settings file; **/install** walk-through; report → push to YOUR repo |
| 20:17–21:08 | Root .env: ANTHROPIC_API_KEY ("agent SDK currently only runs with the API key"), CLAUDE_CODE_PATH via `which claude` |
| 21:08–22:57 | App tour (NL→SQL, :8000/:5173); only .csv/.json today; **issue #33 Jsonl Support** written with constraints |
| 22:57–24:31 | **Health check** on issue 33: HEALTHY + disler warning + live 2+2 test + ✅ comment |
| 24:31–26:05 | Manual trigger; wrong-dir stumble; ADW ID `cb881e79`; classified /feature; branch `feat-33-...`; "agent has taken the wheel"; what-not-how |
| 26:05–26:59 | Feature template ≠ chore template; target classes of problems |
| 26:59–31:51 | Code walkthrough: docstring workflow; main(); report-or-check-error; classify prompt; data-types mapping; branch step; build_plan request shape; **model policy** |
| 31:51–32:43 | `agent.py`: build/log/execute; **programmable mode = new agentic coding primitive**; dangerous-but-safe |
| 32:43–34:28 | Observability: hook session logs; `agents/{adw_id}` per-agent folders; commit plan → implement → commit → PR creator (JSONL + JSON logs) |
| 34:28–35:47 | Workflow complete: PR #34, **~17 minutes**; review; **170-line plan** as concrete asset; "how will your agents know how to improve?" |
| 35:47–38:41 | Verify in-app: regression query; CSV/JSON/**JSONL** UI; fixture upload; `__`/`_0` honored; "completely unnecessary" work; **fix the system** |
| 38:41–40:16 | Tool-agnostic recap; cloudflared tunnel; dedicated environment; two agentic units shipped; KPIs start mediocre → invest → improve |
| 40:16–42:30 | In-loop's remaining role; "most of engineering is not that"; classes solved forever; the two essential directories; add logging/observability |
| 42:30–44:30 | Always-on device demo re-trigger; **take action now, ROI insane**; defaults; local → offload; **chores → bugs → features** |
| 44:30–46:25 | Recap: planning velocity up; the massive issue = review load; lesson-5 teaser (close the loops, agents validate their own work); "template and stay out the loop" |

## Terminology glossary (Dan-isms, canonical spellings)

- **Stay Out The Loop** — Tactic #4; leave the prompting loop (not the review loop)
- **In-loop / Outloop agentic coding** — human-in-the-loop at the device vs off-device agentic coding
- **AFK agents** — agents that run while you're Away From Keyboard; "run the loop while you stay out of it"
- **PITER** — Prompt input, Trigger, Environment, Review (transcript says "Peter")
- **ADW — AI Developer Workflow** — reusable agentic workflow combining code, agentic prompts, and agents to deliver results autonomously (term carried from Principled AI Coding); aka agentic pipeline / compositional workflow
- **Agentic layer** — `.claude/commands/` + `adws/` wrapped around an untouched app
- **Programmable mode** — `claude -p ... --output-format stream-json` as a callable pipeline primitive
- **Micro agents** — per-step agents isolating the big three; **target specific classes of problems**
- **ADW ID** — 8-char run ID threading comments → branch → `agents/{id}/` → commits → PR
- **Live feed** — `{adw_id}_{agent}: ✅/❌ message` issue comments
- **Health check** — pre-flight ADW validating env/repo/gh/Claude before runs
- **Fix the system, not the issue** — improve the template/ADW, never just the artifact
- **KPIs** — presence↓ · size↑ · streak↑ · attempts↓ (from TAC-2)
- Transcript corrections: "Devon"→Devin, "Cloud Code"→Claude Code, "Cloud Flared"→cloudflared, "on L support"→JSONL support, "reasonable prompts"→reusable prompts, "from principle to decoding"→from Principled AI Coding, "feel the ADWs"→fuel the ADWs

## Bridge to the rest of TAC (as trailed in-lesson)

- **From lesson 3:** templates are "mission critical for outloop agentic coding" — the ADW is templates *chained*; the chore→plan expansion is exactly the tac-3 pattern running headless.
- **To lesson 5 (Close the Loops):** the named "massive issue" — these workflows require lots of reviewing; next lesson teaches agents to validate their own work on multiple dimensions ("what's better than one test? Yes — two, three, or ten"), raising review velocity to match planning/building velocity.
- **Further out:** "obviously, we're gonna take this a lot further. We're gonna push this" — more SDLC steps, more triggers, always-on environments ("this device now is always running for me... listening for any codebase").
- **Halfway checkpoint:** "your ability to internalize lesson three and four will decide if you come out on top here. Template and stay out the loop."
