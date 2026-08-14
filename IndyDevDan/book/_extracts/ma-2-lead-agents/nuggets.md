# Nuggets — Multi-Team Agentic Coding / Lead Agents (`ma-2-lead-agents`)

Distilled, teachable ideas from the lesson — the "loot box" of insights. Each is a one-line hook + a short expansion grounded in the transcript, `README.md`, `OPUS.md`, or the source. Use them for pull-quotes, section epigraphs, and retrieval prompts.

---

## The thesis

1. **One agent is a ceiling.** No single agent, however smart, escapes it. The upgrade isn't a smarter agent — it's a *team* of specialized agents behind one interface.

2. **If you re-prompt one agent all day, YOU are the orchestrator.** That's the bottleneck. The whole system exists to move the classify/route/synthesize work off of you and onto an orchestrator agent.

3. **Outperform the normal distribution of results.** Specialized teams don't just match a single agent's average output — they push past it. That's the entire value proposition, and it's why it's "not for cost-min-maxers."

4. **This is agentic coding *beyond* Claude Code.** Multi-agent orchestration is today's frontier; multi-team agentic coding on a fully customizable harness is the next step past it.

## Architecture

5. **Depth-2 delegation maps to a real org.** User → Orchestrator → Team Leads → Workers. Two levels of delegation, no more. "Most systems either go flat or go too deep — two levels hits the sweet spot." (OPUS.md)

6. **You only ever talk to the orchestrator.** That single interface is what keeps *your* cognitive load flat as the number of specialists grows. Adding a team is a config edit, not a new thing for you to manage.

7. **Leads think; workers do.** Leads and the orchestrator *route, coordinate, and synthesize* — they never write, edit, or run bash. "You're a leader — delegate, never execute."

8. **The block is the feature.** When the Engineering Lead gets rejected from touching files, that's not waste — it forces the work to the specialist who has the right tools *and* the compounding domain memory.

9. **Only the workers touch the code.** Workers are the sole tier with `bash` + write/edit. That's what makes the hierarchy safe: coordination and execution are physically separated.

## Domain & safety

10. **Domain locking is the holy grail of large codebases.** Per-agent `read` / `upsert` / `delete` permissions per path. "No one should be touching the DevOps files except the DevOps agent."

11. **Two locks, not one.** A *soft* lock (the `zero-micro-management` skill in the prompt) and a *hard* lock (the `domain-enforcer` extension that structurally blocks out-of-domain tool calls and bash writes). The prompt can be argued with; the enforcer cannot.

12. **Boundary enforcement makes autonomy safe.** You can hand an agent full autonomy precisely *because* its blast radius is near zero. Autonomy without domain locking is how agents step on each other's files.

13. **No matching rule = deny.** The enforcer's default is closed: if nothing in the domain grants access to a path, the tool call is blocked. Safe by construction.

## Expertise & memory

14. **Agent experts always beat generic agents.** Same reason you trust the teammate who's shipped it a dozen times over the new hire. Specialization compounds; generality plateaus.

15. **Agents that remember are a competitive advantage over agents that forget.** Every agent keeps a personal mental-model file it reads on boot and updates after work. Session over session, knowledge stacks.

16. **This is NOT "remember everything I ever said."** Dan is explicit: global chat memory "is not going to go well." Specialized agents with *specific purposes* building *domain-relevant* memory — that's what goes well.

17. **You can't have your fingers on everything.** The journey to becoming an agentic engineer is learning to *let go* — teach the agent how to build a good mental model (the skill is ~76 lines), then don't touch the file.

18. **Read-only expertise is a load-bearing pattern.** `updatable: false` gives a billing/migrations/DevOps agent a playbook no one can corrupt — highly opinionated knowledge you never want an agent to "improve."

19. **Empty by default, rich over time.** The shipped repo ships all 10 mental models *empty*. They're meant to be grown per-codebase — the value is in the compounding, not the starter file.

## Skills & config

20. **Skills are the control surface.** Compose small markdown behaviors; share one to change many agents, remove one line to change one. `active-listener` lives in all 10 agents; `conversational-response` is deliberately withheld from workers so they stay verbose.

21. **The whole team is one YAML.** Add a team, prune a team, swap a member — one file, picked up on next launch. Colors, routing hints, roster. (But model/tools/skills/domain live in each agent's `.md`, not the config.)

22. **Config is where you scale horizontally.** The `plan-and-scale` preset runs *three parallel Engineering teams* from the same agent definitions — team count is a config knob.

23. **The model tier is a knob too.** Config `model:` overrides frontmatter `model:`. The `opensource` preset points 9 agents at 9 different providers — one interface, many brains.

## The mindset (spend, trust, scale)

24. **Spend to win.** "We are not afraid to spend to win here. We're not afraid to give our agents all the relevant context they need." 1M-token windows make deep specialization + memory viable — *if* you're willing to use the tokens.

25. **The $8 objection is a failure of imagination.** "You're thinking about right now. You're not thinking far enough into the future. Models will improve, costs are going down." The complaint dates you.

26. **You are not spending enough tokens.** Dan says it about himself too. The scarce resource isn't tokens — it's the willingness to reallocate work to compute.

27. **Where the ball is going, not where it is.** Build for the converging trends (rising intelligence, bigger context windows, cheaper tokens, customizable harnesses), not for today's constraints.

28. **2026 is trust and scale.** First raise trust until you *know* the team ships the result when you hit enter. Then scale — how big, how surgical. In that order.

29. **Systems that build systems.** The payoff of agentic coding: agents that plan, build, test, and validate your application so you compound your advantage instead of typing.

## Under the hood (for the "this is real" box)

30. **The nuclear UI pattern.** Three array assignments replace Pi's entire display layer while keeping the agent brain intact — the kind of hack only possible on a fully customizable harness.

31. **Every tier is the same binary, spawned as a subprocess.** `pi --mode json -p` with three extensions loaded; each self-exits unless its trigger env var is present. Elegant and uniform.

32. **Depth is capped by deleting an env var.** A lead strips `LEAD_MEMBERS_JSON` before spawning members, so the members' copy of the delegate tool self-disables. That's the whole recursion guard.

33. **The hardest problem is routing.** "Everything downstream only matters if the right team gets the right question." (OPUS.md) Teaching the orchestrator *when to delegate, what to delegate, and when to just answer* is the skill that compounds.

34. **The next frontier is parallel delegation.** `Promise.allSettled` already wraps the loop; the hard part is teaching the orchestrator when work is parallel-safe vs dependent. "Plan then build — sequential. Review from two angles — parallel."

35. **Track your spend or the footer lies.** The real `fix-worker-cost-tracking` bug: the TUI showed $8.79 while the API dashboard showed $34.28 — worker costs were silently dropped. Spend to win, *and* measure what you spend.
