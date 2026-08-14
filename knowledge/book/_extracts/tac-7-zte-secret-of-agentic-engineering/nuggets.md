# TAC-7 Nuggets — ranked for the struggling learner

Ordering rule: how much of the lesson collapses if this nugget is missing. Tier 1 is the tactic, the scale it lives on, and the secret it ends on; Tier 2 is the machinery that earns the right to drop your presence; Tier 3 is the posture that keeps ZTE a disciplined target instead of a reckless YOLO. This is the second-to-last lesson — nothing here is new machinery, it's TAC-4/5/6 composed and run in parallel, with the last human step removed.

---

## Tier 1 — If you remember nothing else

**1. Tactic #7 is Target Zero-Touch Engineering — and the word "Target" is load-bearing.**
TAC-1 told you to stop coding. TAC-7 comes for the thing you replaced it with: reviewing. ZTE = presence drops from two touchpoints (prompt + review) to one (prompt only); work flows prompt → production, auto-merged, untouched. But it's a North Star you *target* one problem class at a time (chores → bugs → features), not a switch you flip on day one. "This is the ultimate agentic coding North Star." Missing the word "Target" is how students hear "auto-merge everything" and correctly conclude that's insane.

**2. The Agentic Engineering Velocity Scale is a gradient, not a switch: In-Loop → Out-Loop → ZTE.**
Dan's exact framing: "It's not in loop versus out loop. It's in loop moving toward out loop." He *deliberately* steps back in-loop (22:59) to hand-review the drag-and-drop PR. You move along the scale per-problem-class, "one day at a time" — never a global mode flip. If you think of these as three settings on a dial you turn once, you've misread the spine of the whole lesson.

**3. Presence is the one number that tracks the entire course arc.**
It's the KPI under both TAC-1 and TAC-7: how many human touchpoints per shipped unit. In-loop = continuous; out-loop best = 2 (prompt, then review + merge); ZTE = 1 (prompt only). TAC-1 removed typing; TAC-7 removes reviewing; presence is what goes down both times. When you can't decide whether a run "counts" as ZTE, you're really asking what its presence was.
*Test yourself:* open `app_docs/agentic_kpis.md` — a real committed run (cc73faf1, issue #47, /chore) shows `average presence 1.0, streak 1`. If you can't read that row as "a real ZTE ship already happened in this repo," the KPI isn't real to you yet.

**4. The secret: it was never about the SDLC. It's composable agentic primitives.**
Stated verbatim, twice: "The secret of tactical agentic coding is that it's not about the software developer lifecycle at all. It's about composable agentic primitives you can use to solve any engineering problem class." The slide (t2765) reads Agentic Primitives → ADW steps → **ANY WORKFLOW**. This isn't a rug-pull: the SDLC still works, it's just *one arbitrary arrangement* — "a package for me to deliver a message." The failure is enshrining any fixed arrangement instead of owning the primitives and recomposing per problem class.

---

## Tier 2 — The machinery that earns the presence drop

**5. Git worktrees (or Docker, or E2B) — N agents, one device, zero collisions. The tool is not the point.**
Every workflow in tac-7 is `_iso`: it runs in `trees/<adw_id>/`, a *complete copy of the app* with deterministic ports (base-36 hash of the ADW ID % 15 → backend 9100–9114, frontend 9200–9214, socket-checked with fallback). That's how five agents run in parallel without fighting over branch, dev server, or DB. But Dan pre-empts worktree fixation twice: "I don't care how you scale up your agent environments, it only matters that you can." The repo even ships an E2B cloud-sandbox PoC. Fixating on worktrees-specifically is missing the concept for the implementation.

**6. The ADW state object is pipeline memory that lives OUTSIDE the context window.**
`agents/<adw_id>/adw_state.json`, ten load-bearing fields (adw_id, issue_number, branch_name, plan_file, issue_class, worktree_path, backend_port, frontend_port, model_set, all_adws). Every phase does load → contribute → save, so a fresh single-purpose agent in phase 5 knows the branch phase 1 created without you re-prompting it. Stuffing that bookkeeping into the agent's context instead breaks TAC-6's one-agent-one-prompt-one-purpose ("has not been broken. This is really important for scaling") and makes runs unreplayable.

**7. Model sets are compute allocation encoded as one information-dense keyword.**
Type `model_set heavy` in the issue → `/classify_adw` parses it into state → each `execute_template` resolves its model from `SLASH_COMMAND_MODEL_MAP` in `agents.py`. On heavy, exactly **8 of 18** commands escalate sonnet→opus (implement, resolve_failed_test, resolve_failed_e2e_test, document, chore, bug, feature, patch); classification/branch/test/review/commit/PR stay sonnet. The map's *selectivity* is the lesson. `model_set heavy` on everything "to be safe" = paying opus prices to extract JSON.

**8. Review = proof of value, and it's the trigger for everything downstream (including ZTE).**
Review is not re-testing. Testing asks "does it work?"; review asks "is what we built what we asked for?" — and it *proves it*: the review agent boots the app in its own worktree, drives it with Playwright MCP, takes 1–5 numbered screenshots of critical paths, classifies findings `skippable / tech_debt / blocker` (only **blocker** flips `success=false`), uploads to R2, posts to the issue, and auto-patches blockers ("attempt 1/3"). Dropping your review presence is only legitimate *because* this proof lands without you. Never opening the screenshots is how you fool yourself into ZTE.
*Test yourself:* three severity levels — which one blocks? *(Only `blocker`. If you said "all of them," your review will cry wolf and never let you reach presence 1.)*

**9. The ZTE pipeline is engineered to REFUSE to merge — count the gates before you fear it.**
`adw_sdlc_zte_iso.py` = SDLC + ship. Test failure → "ZTE Aborted." Review failure → "ZTE Aborted." Documentation failure → warn but continue ("shouldn't block shipping"). Ship itself: validate all 8 state fields non-null → validate the worktree three ways → in the repo root fetch → checkout main → pull → `git merge --no-ff` → push, *restoring the original branch on every failure path*. And upstream: `/classify_adw` refuses `adw_sdlc_ZTE_iso` unless **ZTE is literally uppercase** — lowercase silently downgrades to reviewed SDLC. "Agents auto-merging to main" is guarded at five distinct points, not zero.

**10. Both SDLC orchestrators hardcode `--skip-e2e`. Do not assume the browser E2E ran.**
Unit tests gate the pipeline; browser E2E is a separate standalone run (`adw_test_iso.py` without `--skip-e2e`). Assuming E2E ran on your ZTE ship is exactly the kind of unverified belief the lesson trains you out of. (Verified in source, both `adw_sdlc_iso.py` and `adw_sdlc_zte_iso.py`.)

---

## Tier 3 — Posture that keeps ZTE disciplined, not reckless

**11. ZTE is earned per problem class, and the "toy app" objection is named and answered in-lesson.**
Dan says it for you (32:37): "this isn't a real production application, you're pushing way too far." He agrees the app is a toy, then redirects: start with chores → bugs → features, and *target* ZTE so you discover when it's real for each class — "how else will you know unless you're trying?" The example being a background-color change is the point, not a weakness: ZTE is earned on exactly this low-stakes class first.

**12. Nothing in lesson 7 is new. The delta is scale + removing the last human.**
Five pieces of work shipped in parallel from six minutes of issue-writing is not new machinery — it's TAC-4's PITER + TAC-5's loops + TAC-6's focused agents, *composed and run in parallel*. "Once you've built the system that builds the system, it's going to pay you back massively." If you're hunting for the new trick, there isn't one; there's composition and the courage to drop the R.

**13. Verify countable claims against source, not the README. Docs drift; code ships.**
`adws/README.md` says ship "approves the PR, squash method." The code does a manual `git merge --no-ff` + push — and Dan's *narration* matches the code, not the README. Same lesson as the uppercase-`zte` interlock: if you type lowercase and it downgrades, that's the safety working, not a bug. When a claim is countable (how many workflows, which merge strategy, did E2E run), read the source.

**14. The real blocker is belief, not technology — and the lesson's ask is one concrete step.**
"The real challenge... is about your belief. You have to believe that the agentic layer is worth investing into... If you don't believe that your agents can run your codebase, you're cooked." "It's not about being right. It's about being prepared to win." Consuming this as motivation-content and changing nothing is the failure. The ask: pick one chore class this week, encode it, instrument it, and let the KPIs argue.

**15. Own the primitives; the arrangement is yours. "The one way is the way that ships in your codebase."**
"This arrangement of ADWs is completely arbitrary." The 14 workflow scripts are just *compositions* of the same phase modules — the CSV bug took `patch`, the features took `sdlc`, on identical infrastructure. Every org's arrangement "is going to look a bit different." Hearing "SDLC is dead, delete my pipeline" is the misread; the transferable skill is recomposing primitives per problem class.

---

## Micro-quiz (close the book first)

1. Name the three levels of the velocity scale and your presence count at each. Why is it a gradient, not a switch — and what did Dan do at 22:59 that proves it?
2. Why is the word "Target" in the tactic name load-bearing? What sequence of problem classes does Dan give for approaching ZTE?
3. State the secret in one sentence. If it's true, why isn't "seven lessons of SDLC" a rug-pull?
4. Give the ZTE pipeline's gates in order: which failing phase does NOT abort the ship, and what runs before any git command in the ship step? What silently downgrades a ZTE run?
5. `model_set heavy` — which phase reads it off the raw issue, where is it stored, and how many of the 18 commands actually escalate to opus?
6. Review found no blockers, only `tech_debt`. Did the pipeline ship? What did review compare against — and why is that a different question from "did the tests pass"?

*(Answers: extract.md ideas 2, 8, 11, 9, 5, 6.)*
