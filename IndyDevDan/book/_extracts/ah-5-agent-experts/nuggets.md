# AH-5 Nuggets — ranked for the struggling learner

Ordering rule: how much of the lesson collapses if this nugget is missing. **Tier 1** is the load-bearing idea; **Tier 2** is the working machinery you'll actually type; **Tier 3** is the framing that keeps you honest about *when* to reach for this.

---

## Tier 1 — If you remember nothing else

**1. Agents forget, so they don't learn — that's the whole problem.**
Normal software improves with use; agents start cold every session. No prompt or context trick fixes this because it's *structural*. Agent experts fix it by **storing** what was learned.
*Why weak learners lose it:* it sounds obvious, so they skip the consequence — everything else in the lesson exists only because of this.

**2. Agent expert = a normal agent in an Act → Learn → Reuse loop over a mental model.**
Not a smarter model, not a longer system prompt, not custom tools (the two demos have none). The magic is the loop + a persistent expertise file. *"One executes and forgets, the other executes and learns."*
*Test yourself:* define it in one sentence without the words "smart" or "model."

**3. The expertise file is a MENTAL MODEL, not a source of truth.**
The code is the only source of truth. The file is a fast, fuzzy index the agent **re-validates against the code every time** ("validate against the codebase" literally appears twice in the question prompt). Your own head works the same way.
*Say it Dan's way:* "This is not a source of truth. This is your agent's mental model."

**4. Act · Learn · Reuse — memorize the loop.**
**Act:** take a *useful* action. **Learn:** store it (the self-improve prompt updates the expertise file). **Reuse:** read the mental model first next time. If you keep one image from this lesson, keep the Act/Learn/Reuse graphic sitting on top of a real expert prompt.

---

## Tier 2 — The working machinery

**5. Mechanically, an expert is a "self-improving template meta prompt."**
Decompose the mouthful: *meta prompt* (a prompt that builds prompts) + *template* (fixed purpose/structure) + *self-improving* (updates an isolated file for next time). That's it. If you understand meta prompts, you understand experts.

**6. Reuse is "read expertise → validate → answer." Never search blind.**
Watch the database question prompt: its first action is `Read(expertise.yaml)`, *then* it reads `models.py` and the migrations to confirm. Instant, no hunting. That first read is the entire differentiator.

**7. Learn is a prompt, not magic — and it's a closed loop.**
`self-improve.md`: (git diff) → read current expertise → validate vs code → list discrepancies → update → **enforce a hard line limit (wc -l, trim)** → **compile the YAML**. And it's allowed to find nothing: *"after your thorough search, there may be nothing to be done — this is perfectly acceptable."*

**8. The Act step is what separates a partial expert from a complete one.**
Database expert = Reuse + Learn, **no Act** (nothing changes) → a fine *partial* expert. WebSocket expert adds Act (a `build` step that edits code) → complete. `plan_build_improve.md` chains **plan (reuse) → build (act) → self-improve (learn)** as one one-shot prompt.

**9. Golden rule: never hand-edit the expertise file. Fix the self-improve prompt.**
See something wrong in the mental model? Don't open the file. Change the *learning rubric* so the agent produces the fix itself. *"Build the system that builds the system. Do not work on the application layer."* Editing the file by hand silently puts you back to manual memory maintenance.

**10. Delegate context; scale compute for confidence.**
`plan_build_improve` fires three **fresh sub-agents** so the top agent's context stays protected (plan ~81.8k tokens, build ~61.4k / 41 tools, then self-improve). Separately: fire the same question at 3–5 experts and compose the survivors — *"more compute equals more confidence"* (one may fail; one may find what others missed).

**11. Seed loosely; cap hard.**
Start from a **blank** expertise file and let the agent define the structure via self-improve; rerun until it stops finding new things. Then keep it under ~1000 lines with a `MAX_LINES` the agent enforces on itself.

**12. Meta-agentics are the atoms — but they're not experts.**
Meta prompt → new prompt, meta agent → new sub-agent, meta skill → new skill. They *act* but never *learn*. *"Every codebase must have meta agentics"* — just don't mistake them for experts.

---

## Tier 3 — Framing that keeps you honest

**13. Build experts in your scariest code, not your safest.**
Billing, security, the database, gnarly integrations, types-in-sync across services. *"My Agentic Experts have caught revenue changing details."* The higher the risk/complexity and the more it grows, the more an expert is worth.

**14. Don't build one when there's nothing to learn — or when *you* can't judge it.**
Static problems, simple/brand-new codebases (the model has seen their shape), or domains where **you** lack a mental model → use a plain generic agent. Building an expert you can't evaluate makes things worse.

**15. Product experts are a *seed*, not a shipping recommendation engine.**
Nile shows Act/Learn/Reuse per user (viewed/added/checked-out → personalized generative UI). Dan is explicit: agents are too slow for real-time recommendations today; study the pattern, expect to hide latency with UI hacks.

**16. False expertise is permanent — design for it.**
Agents make the same kinds of mistakes we do (they're trained on us). Error rates fall as models improve and fact-checkers get better, but it never fully goes away. Treat a self-improve diff like a PR in high-stakes systems.

**17. Everything is still the core four.**
Skill, sub-agent, MCP server, custom system prompt — pick by ergonomics. Underneath, an expert is just **context, model, prompt, tools** with a little structure. Stay close to bare metal.

---

## Micro-quiz (close the book first)

1. Why is "agents forget" a *structural* problem, and what does an expert add to fix it?
2. Define an agent expert in one sentence. Which three files/steps make the loop?
3. Is the expertise file a source of truth? What is — and what does the expert do with the file first?
4. The database expert is "partial." Which step is missing, and what supplies it in the websocket expert?
5. The mental model is wrong. What do you change, and what do you refuse to touch — and why?
6. Why fire three experts at one question? Why isolate plan/build/self-improve into separate sub-agents?
7. Name two systems you'd build an expert for and one you wouldn't. What makes the "wouldn't" case a trap?

*(Answers live in extract.md — Ideas 1, 2/9, 3, 9, 8, 10, 12.)*
