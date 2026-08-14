# AH-2 Nuggets — ranked for the struggling learner

Ordering rule: how much of your agentic prompt engineering breaks if this nugget is missing. Tier 1 is non-negotiable; Tier 2 is the working machinery; Tier 3 is framing that keeps you consistent and honest.

---

## Tier 1 — If you remember nothing else

**1. The prompt is the fundamental unit of engineering.**
Not the function, not the file — the prompt. Because each line can fire tens to hundreds of tool calls and run for minutes to hours, one great prompt buys hundreds of hours of work and one bad prompt burns them the same way. Agentic prompt engineering is now a top-tier skill, not a joke.
*Say it Dan's way:* "The prompt is now the fundamental unit of engineering. And with agents, every prompt you create becomes a force multiplier."

**2. Every prompt is built from ~13 swappable Lego-block sections — add only what you need.**
`# Title · ## High Level Prompt · ## Metadata · ## Purpose · ## Variables · ## Instructions · ## Relevant Files · ## Codebase Structure · ## Workflow · ## Expertise · ## Template · ## Examples · ## Report`. Name them whatever you want; keep the names *consistent*. Composability + consistency = reuse.
*Why weak learners lose it:* they think they must use all the sections. You don't — drop Report if you don't care about output; drop Variables if nothing comes in.

**3. The Workflow section is the pillar: most useful, only medium skill.**
Graded **S usefulness / C skill.** It's the sequential numbered play that maps straight onto the agent's todo list, and it *hosts* control flow, loops, and delegation. Master this before anything "meta."
*Test yourself:* which is more useful, `## Workflow` or `## Template`? (Both S-useful — but Template costs S-skill, Workflow only C. Workflow is the bargain.)

**4. Seven levels, each adds exactly ONE capability — reach for the lowest that works.**
1 High Level → 2 Workflow → 3 Control Flow → 4 Delegate → 5 Higher Order → 6 Template Metaprompt → 7 Self-Improving. They stack (each inherits the sections below). "Usually level three, level four is all you need." Levels 1–4 = 80–90% of real work.

**5. You're writing for the trifecta — you, your team, your agents.**
Most importantly your agents. The coworker test: *"If I handed this to a coworker, could they complete this work top to bottom?"* If yes, it's probably a high-quality prompt — and your agent will run it just as cleanly.

---

## Tier 2 — The working machinery

**6. Input → Workflow → Output.** Design any prompt as Variables (in) → Workflow (work) → Report (out). Input and output are for you and your team; the workflow is for the agent. Drop any of the three you don't need.

**7. Static vs dynamic variables — one edit, everywhere.**
Dynamic = runtime input (`$1/$2/$ARGUMENTS`), changes each run (`USER_PROMPT: $1`). Static = fixed value referenced throughout, changed in one place (`PLAN_OUTPUT_DIRECTORY: \`specs/\``). Change `specs/` → `prd/` once and every reference follows. Convention: dynamic first, static second; prefer `$1/$2` over `$ARGUMENTS` for multiple args.

**8. Two pairs people confuse — learn the difference cold.**
- **Workflow vs Instructions:** Workflow is the play-by-play the agent *executes*; Instructions are auxiliary *notes about* the steps. Often you can fold Instructions into nested Workflow bullets.
- **Codebase Structure vs Relevant Files:** Codebase Structure is a *map you do NOT read* (find files fast, save tokens); Relevant Files is a set you *do* read.

**9. Delegation = your agent becomes the prompt engineer for its sub-agents.**
Level 4. `parallel_subagents.md` fires N stateless agents in one Task batch; the primary agent must *design self-contained prompts* with clear output expectations for each. Non-determinism is the point — five agents on five angles return five useful results. Ultra useful (S), hard to use (A-skill): you must manage information flow between agents.

**10. Control flow lives INSIDE the workflow.**
Early return: `build.md` line 17 — "If no `PATH_TO_PLAN`, STOP immediately and ask." Loop: `create_image.md`'s `<image-loop> … </image-loop>` block. Make branches/loops *visible* (numbered steps, XML delimiters) so your teammate and your agent both see where they start and stop.

**11. The peak move is a prompt that writes prompts (L6), then one that updates itself (L7).**
Template Metaprompt (`t_metaprompt_workflow.md`): a `## Specified Format` template the agent fills in — graded S/S. Self-Improving (`cc_hook_expert`): a dynamic `## Expertise` section that a *separate* `_improve` prompt rewrites — and it touches **only** the Expertise, never the Workflow.

**12. Everything in the tier list is graded for USER prompts.**
All your slash commands are user prompts (they enter the context window). System prompts are a different, higher-stakes game — see Tier 3.

---

## Tier 3 — Framing that keeps you consistent

**13. Consistency is king. Be *bored* of your own format.**
"Consistency is the greatest weapon against confusion for both you and your agent." Sameness is the feature: a predictable structure lets you CRUD reusable prompts at light speed and hand work to compute without friction. Novelty per prompt is a bug.

**14. "Three times marks a pattern."**
The trigger for writing a Level-1 prompt: the moment you do a thing a third time, copy it into a file and hand it to your agent. Then climb the levels only as the work demands.

**15. System prompts: scope and persistence — handle with care.**
Rules for *every* conversation; can't change mid-conversation; mistakes scale to every user prompt. "A bad system prompt is bad instructions for the whole job." You append (`background.md` → `--append-system-prompt`) or overwrite (SDK, AH-3) only when you build your own agents. Good sections: Purpose, Instructions, Examples, a *loose* Workflow ("workflows reduce agency to increase determinism"). Avoid: Variables, Report, Expertise, Templates, Metadata.

**16. This is the on-ramp to out-loop / ZTE.**
Reusable, consistent prompts → hand more to compute → move inside-loop → outside-loop → ZTE (TAC North Star), building AFK agents and ADW pipelines. "Invest in your prompts for the trifecta to achieve asymmetric engineering in the age of agents."

**17. Next move.** Finish TAC first (ZTE/AFK/ADWs). Then AH-3 (Claude Code SDK — build domain-specific agents with custom *system* prompts), the direct sequel to the system-vs-user section.

---

## Micro-quiz (close the book first)

1. Name the seven levels in order and the ONE capability each adds.
2. Which section is most useful, and what is its skill grade? Why is that combination the "bargain"?
3. Give a real static variable and a real dynamic variable from the codebase, and say why the split saves time.
4. Workflow vs Instructions — which does the agent execute? Codebase Structure vs Relevant Files — which do you NOT read?
5. In a delegate prompt, what job does the primary agent do for its sub-agents?
6. L6 vs L7: which writes a brand-new prompt, and which updates its own Expertise? What must the improve step never touch?
7. The tier-list grades apply to which kind of prompt — user or system? Name three sections that belong in a system prompt and three that don't.

*(Answers: extract.md §2, §3, §4, §3, §2 Level 4, §2 Levels 6–7, §5.)*
