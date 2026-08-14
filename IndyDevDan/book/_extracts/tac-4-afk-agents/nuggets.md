# TAC-4 Nuggets — ranked for the struggling learner

Ordering rule: how much of the rest of the course breaks if this nugget is missing. Tier 1 is non-negotiable; Tier 2 is the working machinery; Tier 3 is framing that keeps you motivated and honest.

---

## Tier 1 — If you remember nothing else

**1. PITER: the four elements of AFK agents.**
**P**rompt input · **T**rigger · **E**nvironment · **R**eview. In the lesson: GitHub issues · GitHub webhook (also cron, manual command) · a dedicated Mac mini · pull requests. Remove any element and it stops being AFK. The tools are swappable; the elements never are — "it doesn't matter if you use GitHub issues, Jira tasks, Notion boards... the key is that these four elements are always there."
*Why weak learners lose it:* they memorize Dan's tools instead of the elements, then stall on "I don't have a Mac mini."

**2. The ADW is the unit: code chaining agents chaining templates.**
An **AI Developer Workflow** is "a reusable agentic workflow that combines code, agentic prompts, and agents to deliver results autonomously." `adws/adw_plan_build.py` is the whole lesson in one file: fetch issue → classify → branch → plan → find plan → commit → implement → commit → PR. Your lesson-3 templates are its building blocks. "In the future these will just be known as scripts."

**3. Two loops exist — route work by class, keep both.**
In-loop (you at the device, back and forth) is for experimentation, new territory, and very hard specific problems. Out-loop (off-device: prompt in from anywhere, PR comes back) is for the growing majority — "increasingly more chores, bugs, and features don't require your expertise at all... let's be real, most of engineering is not that [hard]."

**4. Fix the system, not the issue.**
Dan's demo PR contains real mistakes (it calls ADW "Agentic Developer Workflow") and he narrates the only correct response: "You don't fix the issue. You fix the system that caused the issue. You fix your templates, you fix your ADW." Hand-patching output fixes one artifact once; upgrading the template fixes the class forever. This single habit is what makes the whole tactic compound.

---

## Tier 2 — The working machinery

**5. The issue IS the prompt — what, not how.**
Title + description become the agent's prompt. Chores need two lines; features get a "high to mid-level prompt" with constraints (issue #33: std lib only, `__` delimiter in a constants file, `_0` list indexing, update the UI, add fixtures). "All I have to do is write the prompt, the high level prompt — not even the plan." The planner expands it, exactly like tac-3.

**6. Micro-agents: isolate the big three per step.**
Eight specialized invocations per feature run — classifier, branch generator, planner, plan finder, two committers, implementor, PR creator — each with a fresh context window, one template, one job: "solve one problem and solve one problem well." Model policy: fast/cheap on glue steps (Dan runs Sonnet on camera), "throw top models into the most complex steps — your plan and your build step."

**7. Glue prompts end in contracts; code fails loudly.**
"Respond exclusively with /chore, /bug, /feature — or 0." "Return ONLY the branch name / commit message / PR URL / path-or-0." The Python validates every output and, on breach, comments `❌` on the issue and exits. "No ad hoc prompts as strings inside of the codebase. Everything's isolated so that we can improve it."

**8. Programmable mode is the primitive.**
Every agent call is: `claude -p "<slash_command> <args>" --model <m> --output-format stream-json --verbose --dangerously-skip-permissions`. ~30 lines in `agent.py` wrap it: save the prompt, stream JSONL to `agents/{adw_id}/{agent}/`, parse the result line (success, session_id, cost, turns). "It lets us use Claude Code as a new agentic coding primitive."

**9. Dangerous is safe only because of E.**
`--dangerously-skip-permissions` is paired with a dedicated environment the agent fully controls: "it is running dangerously, but because it's in its own environment, this is going to be safe." Move the permission boundary to the environment — never yolo your daily driver.

**10. Observability is load-bearing, in four layers.**
(1) Issue-comment live feed (`{adw_id}_{agent}: ✅ ...`); (2) `agents/{adw_id}/` — exact prompts + raw JSONL per agent; (3) `logs/{session_id}/` via Claude Code hooks; (4) the committed plan file. "It doesn't matter if our agent can solve every problem if we don't know that it's solved."

**11. The plan is a committed artifact so the system can improve.**
The planner outputs a concrete `specs/*.md` (the feature run's was 170 lines) that becomes the implementor's entire prompt — and your improvement diff: "it's not enough to just run a random ad hoc prompt, because how will you know how to improve that? And more importantly, how will your agents know?"

**12. Health-check before every run.**
`uv run adws/health_check.py <issue>` validates env vars, git remote (it literally warns if you still point at disler's repo), gh auth, and does a live Claude Code round-trip — then posts ✅ to the issue. "Something I highly recommend you build into your ADWs before you run your complex or simplistic workflow."

---

## Tier 3 — Framing that keeps you going

**13. Own your pipeline — one size does not fit all.**
Copilot/Devin/Jules/Codex are "designed for everyone's codebases, not yours"; they don't run your templates or standards. "Just like the prompt, your agentic pipeline is too valuable to outsource to a third party tool, especially this early in phase two."

**14. The KPIs are the scoreboard: presence↓ size↑ streak↑ attempts↓.**
Staying out the loop is the single best lever on all four at once. Score your own runs; the worst number tells you which element or template to fix.

**15. Climb the trust ladder: chores → bugs → features.**
"Chores are the simplest unit of engineering work that your agent should be taking off your plate with no debate at all." You won't start with top-tier KPIs — run, invest in templates, compose, improve.

**16. Bet on the future — you only have to be early once.**
"If you are not wrong now, you will be. It's only a matter of time. Tools will change and models will improve" — every model release upgrades your out-loop system for free. "Take action on this now... the ROI here is insane."

**17. This is the hinge of the course.**
"This lesson is pivotal. Your ability to internalize lesson three and four will decide if you come out on top here. Template and stay out the loop." Named cost: these workflows require lots of reviewing — lesson 5 exists to fix exactly that.

---

## Micro-quiz (close the book first)

1. Expand PITER and give Dan's tool choice for each element — then your own stack's version.
2. Recite the ADW definition and the five workflow steps of `adw_plan_build.py`.
3. What are the classifier's only legal outputs, and what does the code do when a contract breaks?
4. Write the full programmable-mode command shape from memory, and justify its dangerous flag in one sentence.
5. Name the four observability layers of a run and the file that becomes the implementor's entire prompt.
6. Your ADW's PR has a factual error. What do you do — precisely?
7. Which work stays in-loop, per Dan? Which KPIs move when you stay out?

*(Answers: extract.md ideas 3, 4, 8, 7, 9, 9, 1.)*
