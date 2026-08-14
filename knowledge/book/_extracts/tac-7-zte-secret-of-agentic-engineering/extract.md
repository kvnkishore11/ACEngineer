# TAC-7 · ZTE Secret of Agentic Engineering — Master Teaching Notes

**Tactic #7: Target Zero-Touch Engineering.** Video 53:20 (3200s), advanced, second-to-last lesson. Codebase `tac/tac-7` (loot box: `git clone https://github.com/disler/tac-7.git`) — the TAC-6 Natural Language SQL app wrapped in the finished agentic layer: 14 isolated ADW workflow scripts, 33 command prompts, worktree isolation, model sets, webhook + cron triggers, and the auto-shipping ZTE pipeline.

The lesson runs in an unusual shape: first ~28 minutes are a *dividend-collection demo* (five real pieces of work handed to the layer and shipped in parallel while Dan reviews), then the *velocity-scale reveal* (in-loop → out-loop → ZTE), a live ZTE run that merges to main untouched, and finally the course's *secret*. Teach it in that order — evidence first, doctrine second.

Teaching model per idea: **Hook → Picture → Worked example → Name (Dan's term) → Failure mode → Retrieval.**

---

## Idea 1 — Payday: five pieces of work, one engineer, zero typing

- **Hook:** This morning you have three features, a chore, and a bug in your queue. Estimate honestly: a week? Dan files all five as GitHub issues in six minutes and goes to review something else. All five ship.
- **Picture:** Frame t0250 (4:10) — a GitHub "Create new issue" form. The body is plain English plus two keywords: `/feature`, `adw_sdlc_iso`. Then frame t0372 (6:12) — the webhook terminal detecting the event, initializing state, allocating ports 9106/9206.
- **Worked example:** #51 drop-zone surface area (feature), #52 JSON export (feature), table random data (feature, `model_set heavy`), #54 bump the NL→SQL model to o4-mini (chore), and a CSV-text bug routed to the lightweight patch workflow instead of full SDLC (5:22). "Five issues getting tackled by our agentic pipelines... all happening in parallel" (7:25). "This is absurd levels of scale" (7:08).
- **Name:** Collecting the dividends of the agentic layer. "Once you've built the system that builds the system, it's going to pay you back massively."
- **Failure mode:** Believing something new was built for this demo. It's TAC-4's PITER + TAC-5's loops + TAC-6's focused agents, *composed and run in parallel*. The delta of lesson 7 is scale and the removal of the last human step — not new machinery.
- **Retrieval:** Which of the five pieces of work did NOT get the full SDLC, and what got it instead? *(The CSV-text bug → adw_patch_iso, a targeted patch plan + implement + PR.)*

## Idea 2 — The Agentic Engineering Velocity Scale (the lesson's spine)

- **Hook:** How present are you in your own engineering? Score yourself: driving every prompt (always present), showing up twice (prompt, review), or once (prompt only)?
- **Picture:** Frame t0100 (1:40) — the on-screen scale: **1 In-Loop → 2 Out-Loop → 3 ZTE**.
- **Worked example:** The whole lesson walks the scale left to right: interactive `claude` sessions (in-loop, the clone-and-/install ritual at 8:15), the five-issue parallel run (out-loop, presence two: Dan prompts, then reviews), and issue #62 (ZTE, presence one: prompt → production).
- **Name:** "There are three levels: in loop, out loop, and one additional level..." (1:28). Presence numbers from the course card: out-loop = two touchpoints, ZTE = one.
- **Failure mode:** Reading the scale as a switch. Dan's own words: "It's not in loop versus out loop. It's in loop moving toward out loop" (9:42) — and he *deliberately* goes back in-loop at 22:59 to hand-review the drag-and-drop PR. Progress is per-problem-class, "one day at a time."
- **Retrieval:** Name the three levels and your presence count at each. *(In-loop/continuous; out-loop/2; ZTE/1.)*

## Idea 3 — Git worktrees: N agents, one device, zero collisions

- **Hook:** Fire two agents in the same repo directory and watch them fight over the same branch, dev server, and database. Now fire five without a fight.
- **Picture:** Frame t0680 (11:20) — `trees/` expanded to a dozen 8-hex-char directories, each a *complete copy of the application* owned by one agent. Frame t0890 (14:50) — the state file that remembers which copy belongs to whom.
- **Worked example:** `adw_plan_iso.py` creates `trees/<adw_id>/` via `git worktree add -b <branch> ... origin/main`, allocates deterministic ports (base-36 hash of the ADW ID % 15 → backend 9100–9114, frontend 9200–9214, socket-checked with fallback), writes `.ports.env`, then runs `/install_worktree` *inside the worktree*: copy `.env`s, append ports, copy `.mcp.json` + Playwright config and rewrite paths to absolute, `uv sync`, `bun install`, reset the DB. At 12:58 Dan jumps into a live one: `code trees/<id>` — branch `chore-...-issue-39-...` in the status bar.
- **Name:** Isolated ADWs (`_iso` suffix — every workflow in tac-7 is iso). "In every tree, the application exists for a specific agent to build in. This is the easiest way to parallelize your workflows" (11:17).
- **Failure mode:** Worktree fixation. Dan pre-empts it twice: "It doesn't matter that you use Git work trees... Docker... I don't care how you scale up your agent environments, it only matters that you can" (~11:40). (The repo even ships an E2B cloud-sandbox PoC in `adws/adw_tests/sandbox_poc.py`.) Second failure: never running `scripts/purge_tree.sh` and discovering each worktree is a full repo copy the hard way.
- **Retrieval:** An ADW ID hashes to index 7. Which two ports does the run get, and what file records them? *(9107 and 9207 — `.ports.env` in the worktree, mirrored into `adw_state.json`.)*

## Idea 4 — The state object: pipeline memory outside the context window

- **Hook:** Phase 2 of your pipeline needs the branch name phase 1 created. Where does it live — in a prompt? In your head?
- **Picture:** Frame t0890 — `agents/e2ae7fad/adw_state.json` open in the editor: ten fields, every one load-bearing.
- **Worked example:** `adw_id, issue_number, branch_name, plan_file, issue_class, worktree_path, backend_port, frontend_port, model_set, all_adws`. Every phase does load → contribute → save. `all_adws` appends each workflow that ran (that's how KPI "attempts" is computed later). And `adw_ship_iso` turns state into a gate: all eight required fields non-null or no merge.
- **Name:** The ADW state object. "Expect to have to add some type of state object inside your dedicated agent environments... it frees your agent to do one thing extraordinarily well... and lets you jump in and replay what that agent has done" (14:55–15:06).
- **Failure mode:** Stuffing pipeline bookkeeping into the agent's context instead — which breaks TAC-6's one-agent-one-prompt-one-purpose ("has not been broken. This is really important for scaling," 14:29) and makes runs unreplayable.
- **Retrieval:** Ship aborts with "missing fields." Which mechanism caught it, and what does that tell you about the run? *(State-completeness validation — some phase never ran/never saved; the paper trail says which.)*

## Idea 5 — Model sets: compute allocation as one information-dense keyword

- **Hook:** One of your five issues is a big feature; another is a text rename. Should both burn your most expensive model?
- **Picture:** Frame t1010 (16:50) — `agents.py`'s `SLASH_COMMAND_MODEL_MAP` on screen: eighteen commands, each mapped for `base` and `heavy`.
- **Worked example:** Typing `model_set heavy` in the issue → `/classify_adw` parses it into state → every `execute_template` call resolves its model from the map. On heavy, exactly 8 commands escalate sonnet→opus (`/implement`, `/resolve_failed_test`, `/resolve_failed_e2e_test`, `/document`, `/chore`, `/bug`, `/feature`, `/patch`); classification, branch naming, test, review, commit, PR stay sonnet. Inside the prompts, "think hard" IDKs activate reasoning (17:25). The heavy random-data feature runs 27 minutes on opus and ships ~300 lines.
- **Name:** Model sets — "a knob to turn to increase the compute that our workflow uses" (16:45); IDK = information-dense keyword (from TAC-2/AH vocabulary): "You can encode any information dense keyword you want. You just have to make sure that your prompts recognize it and pick it up" (16:04).
- **Failure mode:** `model_set heavy` on everything "to be safe" — paying opus prices for JSON extraction. The map's selectivity IS the lesson: compute allocation is an engineering decision you encode once, then invoke with one word.
- **Retrieval:** Which phase reads `model_set` off the raw issue text, and where is the value stored so later phases agree? *(/classify_adw at trigger time; persisted in adw_state.json.)*

## Idea 6 — Review = proof of value (and the trigger for everything after)

- **Hook:** Your agent says "done." Your PM asks "is it though?" What arrives in your review system without you lifting a finger?
- **Picture:** Frame t1290 (21:30) — issue #51's thread: "📷 Screenshots — Captured 4 screenshots," the app visible with the new drop overlay.
- **Worked example:** The review agent boots the app *in the worktree on its own ports*, drives it with Playwright MCP, takes 1–5 numbered screenshots of critical paths only, classifies findings (`skippable` / `tech_debt` / `blocker` — success means *no blockers*), returns strict JSON, uploads images to Cloudflare R2, posts them to the issue. Blockers aren't just reported: the review workflow patches and re-reviews ("attempt 1/3" visible on #54's thread). Dan: "Our agents took images and gave us proof that the feature has shipped" (21:26). The named next step: video — "have your agents take video, upload it to a cloud bucket, and post the URLs" (26:12); the Playwright config already records 1920×1080 video per run.
- **Name:** Proof of value. "It's not 'does it work?' It's 'is what we built what we asked for?'" (21:40) — TAC-5's review question, now automated end-to-end. "Having a comprehensive review system is a massive, massive edge" (and "an entire product category," 25:40).
- **Failure mode:** Never opening the screenshots. The review system is how trust gets *earned*; skip it and your presence never legitimately drops. Opposite failure: treating review as re-testing — tests already gated the pipeline; review compares to the SPEC.
- **Retrieval:** Three severity levels, and which one flips `success` to false? *(skippable, tech_debt, blocker — only blocker.)*

## Idea 7 — The realization: your review is the bottleneck (KPIs prove it)

- **Hook:** Tenth time this month your pipeline shipped a chore flawlessly. You reviewed all ten. What did review #10 contribute? Be honest: latency.
- **Picture:** No frame — this beat is spoken over B-roll (render as a designed pull-quote). The instrument is `app_docs/agentic_kpis.md`: attempts, plan size, diff size, presence, streak.
- **Worked example:** The committed KPI table is a real run's receipt: ADW `cc73faf1`, issue #47, `/chore`, attempts 1, plan 39 lines, diff 274/5/10, average presence 1.0, streak 1 — a ZTE run whose committed spec still carries the trigger text `/chore adw_sdlc_ZTE_iso - update 'Upload Data' to be 'Upload'`. The KPI command recomputes streak/attempts with forced `python -c` arithmetic inside the document phase.
- **Name:** The bottleneck realization: "This human in the loop model is a bottleneck. I'm not catching any bugs anymore. I'm not adding any value outside of the agentic layer. I'm going to remove the human in the loop review process *for this class of problems*" (30:45). Foreshadowed at 2:06: "a bottleneck, not a safety net."
- **Failure mode:** Making the call on vibes in either direction — YOLO-merging without a streak, or refusing forever despite one. The KPIs exist precisely so this is an *evidence-gated* decision per problem class ("90% of the time there's no issues, and that number keeps going up," 39:52–40:06).
- **Retrieval:** Which KPI directly encodes "how touched" a run was, and what value does ZTE target? *(Presence; 1.)*

## Idea 8 — Tactic #7: Target Zero-Touch Engineering (PITER → PITE)

- **Hook:** TAC-1 told you to stop coding and you (eventually) did. The same argument now comes for the thing you replaced coding with: reviewing.
- **Picture:** Frame t1912 (31:52) — the course tactic card: definition (presence KPI 2 → 1) + daily actions, including "Go from PITER to PITE with one prompt agentic workflows."
- **Worked example:** The reveal sequence 30:45–32:30: bottleneck realization → "you'll drop yourself off the end of the out-loop PITER framework and it becomes PITE, not PITER. You'll drop off the review" (31:19) → "YOLO mode for your AI developer workflows... maximum confidence mode... Just like you've stopped coding, you'll stop reviewing" (31:33–31:46) → "This is the lesson seven tactic: Target zero touch engineering... the ultimate agentic coding North Star" (31:50) → KPI shape: "Attempts at one, size constantly scaling up, streak constantly increasing... drop your presence down to one" (31:56).
- **Name:** Zero-Touch Engineering (tactic; the *code* calls it Zero Touch Execution — same acronym, both appear in course artifacts). The word **Target** in the tactic name is load-bearing: it's a North Star, not a day-one state.
- **Failure mode:** The O-face objection, named in-lesson (32:37): "this isn't a real production application, you're pushing way too far." Dan agrees the app is a toy and redirects: start with chores → bugs → features (33:07); the tactic is *targeting* ZTE so you discover when it's real for each class — "how else will you know unless you're trying?" (37:25).
- **Retrieval:** What does PITER lose under ZTE, and what replaces it? *(The R/review; it's replaced by embedded pipeline gates — tests, agentic review with proof, state validation — not by nothing.)*

## Idea 9 — The ZTE pipeline in code: gates, ship mechanics, and one uppercase interlock

- **Hook:** "Agents auto-merging to main" sounds like a horror story. Read the 240 lines of `adw_sdlc_zte_iso.py` and count the ways it refuses to.
- **Picture:** Frame t2135 (35:35) — issue #62's initiation comment: six phases ending "🚢 Ship to production (approve & merge PR)" + "⚠️ Code will be automatically merged if all phases pass!"
- **Worked example:** ZTE = SDLC + ship. Gates in source: test failure → "ZTE Aborted"; review failure → "ZTE Aborted"; documentation failure → warn but continue ("shouldn't block shipping"); ship failure → report + manual-merge advice. Ship itself: validate all 8 state fields → validate worktree (state + filesystem + `git worktree list`) → in the repo root: fetch, checkout main, pull, `git merge --no-ff` (message "Merge branch '<branch>' via ADW Ship workflow"), push origin main — restoring the original branch on every failure path. Upstream, the interlock: `/classify_adw` refuses `adw_sdlc_ZTE_iso` unless **ZTE is explicitly uppercase**; lowercase silently downgrades to reviewed SDLC. Also verified: both SDLC orchestrators hardcode `--skip-e2e` — unit tests gate the pipeline, browser E2E is a separate standalone run.
- **Name:** Zero Touch Execution workflow; the ship phase; "our final approval step" (state validation, per the docstring).
- **Failure mode (three, all real):** (1) assuming E2E ran — it didn't; (2) trusting `adws/README.md`'s "approves the PR, squash method" — the code does a manual `--no-ff` merge + push (Dan's narration at 33:55 matches the code, the README is stale — verify countable claims against source); (3) typing lowercase `zte` and mistaking the working interlock for a bug.
- **Retrieval:** Which failing phase does NOT stop a ZTE run, and which check runs before any git command in ship? *(Documentation; the 8-field state completeness check + worktree validation.)*

## Idea 10 — The demo lands: one prompt to production

- **Hook:** What does presence-of-one actually look like on a Tuesday?
- **Picture:** Frame t2958 (49:18) — the app after `git pull origin main`, wearing the background color an agent shipped. Review evidence earlier: "Background is green" screenshots in the review step (44:16).
- **Worked example:** Issue #62 "Update the background color" with `/chore adw_sdlc_ZTE_iso` (34:38–34:58) → initiation (35:31) → plan/build/test/review/document on base models → auto-merge → "It's deployed to production. The issue is closed. All I did was write this prompt" (48:31). Dan's framing of the class: designer-whim styling changes — "this is not something you should ever spend your time on... low hanging fruit" (34:20).
- **Name:** "This is zero touch engineering. This is the future of engineering" (49:20). Prod here = main branch; "for you, this will be your deploy — staging, production, however your engineering is configured" (44:50).
- **Failure mode:** Scoffing at the example's size. The size is the point — ZTE is earned on exactly this class first. The committed repo carries the same class shipped for real (background: off-white → light-sky-blue `#E0F6FF`; button text "Upload Data" → "Upload").
- **Retrieval:** In tac-7, what concretely is "production," and where does Dan say your version of ship should point? *(Push to main; your deploy pipeline/staging/prod.)*

## Idea 11 — The secret: composable agentic primitives (SDLC demoted)

- **Hook:** Seven lessons of plan → build → test → review → document. Now the instructor tells you the SDLC was never the point. Why isn't that a rug-pull?
- **Picture:** Frame t2765 (46:05) — "The Secret: Composable Agentic Primitives": Agentic Primitives (ADWs, Templates, Plans, Architecture, Tests, Documentation, Types, Standard Out, Tools, Prompt, Model, Context) → ADW steps (Plan/Build/Test/Review/Document/Deploy) → Composed Workflows (Plan→Build→Test, Build→Review→Deploy, Test→Document, **ANY WORKFLOW**).
- **Worked example:** The repo already practices the secret: 14 workflow scripts are *arrangements* of the same phase modules — plan_build, plan_build_test, plan_build_review, plan_build_test_review, plan_build_document, sdlc, sdlc_zte, patch, ship — and the CSV bug took a different composition (patch) than the features (sdlc) on the same infrastructure.
- **Name:** Stated twice, verbatim (45:58–46:10): "The secret of tactical agentic coding is that it's not about the software developer lifecycle at all. It's about composable agentic primitives you can use to solve any engineering problem class." SDLC: "powerful, but... a remnant of the past" (46:26); "this arrangement of ADWs is completely arbitrary... The one way is the way that ships in your codebase" (47:20).
- **Failure mode:** Hearing "SDLC is dead, delete my pipeline." The SDLC "still works, it's still very relevant... a package for me to deliver a message" — the failure is enshrining ANY fixed arrangement instead of owning the primitives and recomposing per problem class ("it's going to look a bit different for every single organization").
- **Retrieval:** Give the secret in one sentence, and name four primitives from the slide. *(Not the SDLC — composable agentic primitives for any problem class; e.g. templates, plans, prompts, ADWs.)*

## Idea 12 — Belief, the four postures, and the closing arc

- **Hook:** Everything in this lesson is copy-able this weekend. Dan says the real blocker isn't technical. What is it?
- **Picture:** No frame — the futures monologue (38:55–39:20) plays over B-roll; render the four postures as a designed diagram: run away / stand still / move toward / **sprint**.
- **Worked example:** The two-engineer comparison (39:30–40:40): a few weeks of agentic-layer investment → "write a single prompt, hit enter, ship into production... 90% of the time no issues, and that number keeps going up — every tool release, every model release." Versus: open Jira, prompt in-loop, sit, wait, iterate, retest. "Tell me who wins this. Tell me who makes their business more money" (40:36).
- **Name:** "The real challenge... is about your belief. You have to believe that the agentic layer is worth investing into... If you don't believe that your agents can run your codebase, you're cooked" (41:10–41:18). "It's not about being right. It's about being prepared to win" (41:35). Career close: "you'll be the engineer they can't replace... because you understand and control the agentic layer... the area of highest leverage" (44:00→49:44: "1x input becomes 10x output, 10x becomes 100x").
- **Failure mode:** Consuming the monologue as motivation-content and changing nothing. The lesson's own ask is one concrete step: pick a chore class this week, encode it, instrument it, let the KPIs argue.
- **Retrieval:** The arc in one line: what did TAC-1 remove, what does TAC-7 remove, and what number tracks both? *(Typing, then reviewing; presence.)*

---

## Timeline map (VTT-verified, ±5s)

| Time | Beat |
|---|---|
| 0:00–2:30 | Cold open: "a codebase that nearly runs itself" (0:28); agenda; "bottleneck, not a safety net" (2:06) |
| 3:05–5:50 | Agent environment live; five issues filed (#51, #52, random-data heavy, #54, CSV patch) |
| 5:54–7:30 | All five fire; webhook terminal; "absurd levels of scale" (7:08) |
| 8:15–9:42 | Clone ritual; agentic-layer recap; ADWs = scripting layer (9:18); "in loop moving toward out loop" (9:42) |
| 10:30–13:30 | adw_sdlc_iso composition; worktrees (11:17); /install_worktree (12:06); `code trees/<id>` (12:58) |
| 14:29–15:10 | TAC-6 tactic intact; state.json (14:44) |
| 15:46–18:20 | Model sets; agents.py map (16:41); heavy→opus (16:59); think-hard IDK (17:25); /classify_adw (17:41) |
| 18:37–22:00 | Status sweep; o4-mini review + PR (18:50); screenshot proof (21:26); "is what we built what we asked for" (21:40) |
| 22:59–27:00 | In-loop review (/in_loop_review), browser testing, docs + conditional docs trail |
| 27:59–29:30 | "Can't vibe code this" (27:59); "orchestrating intelligence" (29:21) |
| 30:45–33:30 | Bottleneck realization; PITER→PITE (31:19); YOLO/max-confidence (31:33); tactic named (31:50); KPIs (31:56); presence of two (32:15); O-face + chores→bugs→features (32:37–33:07) |
| 33:46–35:35 | ZTE mechanics + ship (33:55); issue #62 filed (34:38); initiation comment (35:31) |
| 36:24–40:40 | Counter-narrative: parabolic (37:06); "work you do not have to do" (37:40); compounding (37:53); 90% scenario (39:52); "who wins" (40:36) |
| 41:00–43:45 | Belief section; "you're cooked" (41:18); "prepared to win" (41:35); career defensibility |
| 44:12–44:35 | ZTE review evidence ("Background is green"); documentation completes |
| 45:50–48:30 | THE SECRET ×2 (45:58); primitives slide (46:05); "remnant of the past" (46:26); stack recap (48:00–48:17) |
| 48:31–49:20 | Issue closed, deployed (48:31); "sprint into the future" (49:06); git pull shows it live (49:14) |
| 49:38–53:20 | Highest-leverage close (49:44); lesson-8 preview: atoms + compositions (51:37–52:30); final four-postures question |

## Terminology glossary (canonical spellings; transcript mishears in parens)

- **ZTE** — Zero-Touch Engineering (tactic) / Zero Touch Execution (code & bot comments). Level 3 of the scale.
- **Agentic Engineering Velocity Scale** — In-Loop (1) → Out-Loop (2) → ZTE (3).
- **Presence** — KPI: how many touchpoints you have per shipped unit. Out-loop best = 2 (prompt, review); ZTE = 1.
- **PITER → PITE** ("Peter → Pete") — Prompt input, Trigger, Environment, Review; ZTE drops the R.
- **ADW** — AI Developer Workflow; `adws/` is "a scripting layer that lets us construct pipelines of agents that solve specific classes of problems back to back to back."
- **_iso** — isolated: the workflow runs in its own git worktree with dedicated ports.
- **Worktree / trees/<adw_id>** — full repo copy per run; ports 9100–9114 / 9200–9214 (15 slots).
- **ADW state object** — `agents/<adw_id>/adw_state.json`, ten fields, pipeline memory + ship gate.
- **Model set** ("model set heavy") — base|heavy IDK re-mapping each slash command's model; heavy→opus for 8 of 18 commands.
- **IDK** — information-dense keyword (e.g. "think hard", "model_set heavy").
- **Proof of value** — review-step evidence: numbered screenshots (next: video) posted to the review system.
- **Composable agentic primitives** — the secret; SDLC is one arbitrary arrangement ("a package to deliver a message").
- **YOLO mode / maximum confidence mode** — Dan's names for ZTE's no-review posture ("yellow mode" = yolo mode; "o4 many" = o4-mini; "agent decoding" = agentic coding).

## Bridge to the rest of TAC

- Backward: TAC-4 built PITER and the first ADWs; TAC-5 built the loops ZTE's gates rely on (tests, review, resolution); TAC-6 made agents single-purpose and docs conditional — tac-7 runs all of it in parallel and removes the last human step.
- Forward (51:37–53:20): Lesson 8 revisits "the atoms of agentic engineering" and their compositions across codebase types (web app, CLI, notebooks) — "master them and you can build any molecular structure you need" — plus positioning for today's and tomorrow's engineering. Closing question of this lesson: run away, stand still, move toward, or sprint?
