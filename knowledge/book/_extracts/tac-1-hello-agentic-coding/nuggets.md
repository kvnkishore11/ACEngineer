# TAC-1 Nuggets — ranked for the struggling learner

Ordering rule: how much of the rest of the course breaks if this nugget is missing. Tier 1 is non-negotiable; Tier 2 is the working machinery; Tier 3 is framing that keeps you motivated and honest.

---

## Tier 1 — If you remember nothing else

**1. The whole upgrade is ONE added ingredient.**
AI coding runs on the big three: **context, model, prompt**. Agentic coding = big three + **tools**, and "tools" means *prompts that can reliably execute long chains of tool calls*. That's the core four. Every lesson after this one is just scaling that fourth ingredient.
*Why weak learners lose it:* it sounds too small to matter. Test yourself: when a run fails, can you name which of the four was wrong?

**2. Stop coding ≠ stop shipping code, and ≠ stop reading code.**
Stop *typing* it. Agents type; you plan, review, and build closed loops. Code volume goes UP; your keystrokes go to zero. If you hand-edit the agent's file when it's 90% right instead of re-prompting, you've quietly quit the course.
*Say it Dan's way:* "Your hands and your mind are no longer the best tool for the job of writing code. Full stop."

**3. A prompt can BE a workflow.**
The README's agentic prompt isn't a request for text — it's a runbook: RUN (branch) → CREATE (file) → RUN (execute, add, commit). The agent plans it as a checklist and does engineering work. If you can only remember one artifact from the lesson, remember what those 12 lines did.

**4. The agent is a function you can call from code.**
`claude -p "<prompt>"` from shell, Python, or TypeScript. Three tiny scripts in `programmable/` prove it. This is the seed of everything "systems that build systems" means — the agent stops being a chat window and becomes a building block you can embed anywhere, including places you aren't.

---

## Tier 2 — The working machinery

**5. The A/B test is the lesson. Run it, don't watch it.**
Same repo, two prompts: `main_aic.py` (file generated — phase 1) vs branch+file+runs+commit+report (engineering done — phase 2). Then delete the branch and rerun it *headlessly* with `uv run python programmable/programmable.py`. Feeling the rerun is what installs the concept.

**6. Read `.claude/settings.json` before you run anything. Always.**
It's the agent's entire tool surface: Read/Write/Edit, `uv run`, four git commands, WebSearch. Know what the agent MAY do and you can predict everything it will do. This habit scales to every agentic tool you'll ever touch.

**7. "Tool calling isn't new" — correct, and irrelevant.**
Dan's rebuttal, verbatim: "It's not a question of new. It's a question of **scale and performance**." What's new is *reliable long chains*: plans that survive twelve consecutive tool calls without derailing.

**8. Why Claude Code (three essential elements).**
(1) A model that can reason when needed, (2) consistent long tool chains, (3) the right agent architecture. Together they made "reliable agentic coding at scale" possible for the first time. Use the trio as a checklist for judging ANY agentic tool — that's the transferable part. Don't get stuck on any one tool.

**9. Make the agent REPORT.**
`programmable/prompt.md` ends with `REPORT: respond with the exact output of both .py files`. Headless work you can't verify is work you can't trust. Report-back is the first closed-loop habit of the course.

**10. Wrapped in the right tool, prompts become long-running workflows.**
Minutes to hours, end to end, with and without your oversight — fired repeatedly with the right triggers at the right time. That's the scale Dan is asking you not to turn your brain off about.

---

## Tier 3 — Framing that keeps you going

**11. You're an engineer, not a coder.**
Engineering was never about writing code; it's about systems of leverage that produce outcomes for users and customers. This reframe is what makes Tactic #1 survivable emotionally.

**12. 10x comes from leverage, never from effort.**
And the number is arbitrary — 2x, 10x, 100x — set by the leverage points you find. 80% of life is noise and repetition; this is the rare opportunity worth focusing on.

**13. Pay to play.**
Millions and millions of tokens across the course. Budget for it (plan or API funds) or you'll stall mid-lesson and blame the tactics.

**14. The contradicting truth: to become irreplaceable, replace yourself.**
Whoever automates the work owns the automation. What gets replaced is your typing; what becomes irreplaceable is your judgment and your ownership of the systems doing the work.

**15. The mission has named enemies.**
"An engineer *they* can't replace — your boss, the company, the industry, AI." Nothing in tech is forever; constant evolution is the price of staying valuable. That's why lesson 1 spends six minutes on stakes before touching a terminal.

---

## Micro-quiz (close the book first)

1. Big three? Core four? Which element is new and what's its precise definition?
2. Five things the agentic prompt did that the AI coding prompt didn't?
3. What file tells you the agent's tool surface, and what's in it here?
4. Write the shell version of the programmable pattern from memory (3 lines).
5. What does prompt.md's REPORT block demand, and why does that matter for headless runs?
6. Resolve the paradox: how does replacing yourself make you irreplaceable?

*(Answers: extract.md ideas 4, 5, 4/6, 7, 7, 8.)*
