# Opus on Multi-Team Agentic Coding
> A conversation with opus, upon the completion of building the multi-team agentic coding system.

## What do you think about this system?

This is one of the most well-architected multi-agent systems I've seen. A few things stand out:

**The nuclear UI pattern is brilliant.** Three array assignments to replace Pi's entire display layer while keeping the agent brain intact. That's the kind of hack that only comes from deeply understanding a framework's internals — and it's documented well enough that others can maintain it.

**Depth-2 delegation is the right abstraction.** User → Orchestrator → Lead → Worker maps directly to how real engineering orgs operate. The Orchestrator doesn't micromanage — it classifies and routes. Leads synthesize, they don't execute. Workers are domain-locked. Each layer has a clear job. Most multi-agent systems I see either go flat (one agent calls many) or go too deep (agents calling agents calling agents). Two levels hits the sweet spot.

**Domain locking is the real unlock for scaling.** Giving each agent explicit read/write/delete permissions per path is what makes this safe for mid-to-large codebases. Without it, you'd have agents stepping on each other's files. The per-file expertise upsert scoping we did today (each lead can only write to *their own* mental model) is the right granularity.

**The mental model pattern compounds.** Agents that build their own expertise files session over session is a genuine competitive advantage over stateless agents. The key insight is that these aren't generic memories — they're *specialized knowledge for a specific domain in a specific codebase*. Backend dev remembers backend patterns. QA remembers failure modes. That's how human teams work.

**What I'd watch for going forward:**

- **Context window pressure.** With the conversation log, mental models, skills, and system prompts all loading per agent, you'll hit context limits on long sessions. The compaction story will matter.
- **Cost at scale.** Opus for the orchestrator + 3 leads, Sonnet for 6 workers — a single delegation chain can touch 3-4 models. "Ping each team" alone is 7+ API calls. Engineers should know the cost profile before going all-Opus.
- **The session persistence model.** JSONL session files mean agents resume where they left off — powerful, but stale sessions can accumulate context that drifts from the current codebase state. A session rotation or staleness check would help.

Overall — this is production-grade multi-agent orchestration. The configuration-driven team structure, the skills composition, the domain enforcement, the streaming subprocess protocol — it's all real engineering, not a demo. Engineers who study this will understand how to build agent systems that actually scale.

## Whats the one most important thing to get right for this to provide max leverage for engineers?

The orchestrator's ability to classify and route correctly.

Everything downstream — leads, workers, domain locking, mental models — only matters if the right team gets the right question. A misrouted request wastes tokens, time, and context window. A well-routed request triggers a cascade of specialized expertise that no single agent can match.

Right now the orchestrator decides based on its system prompt and the `consult-when` descriptions in the team config. That works for clear-cut requests. But the hard cases — requests that span domains, requests that need sequential team handoffs, requests where the orchestrator should just answer directly — those are where leverage is won or lost.

The engineers who get the most out of this system will be the ones who invest in teaching their orchestrator *when* to delegate, *what* to delegate, and *when to just answer the question itself*. That's the skill that compounds. Everything else is plumbing.

## What's the next most important direction to take this tool?

Parallel delegation.

Right now the orchestrator delegates sequentially — one team at a time. "Plan this feature, then build it, then validate it" is three serial round trips through Opus leads and Sonnet workers. That's the right default for dependent work. But a lot of real requests are independent across teams.

"Review this PR" could hit Engineering (architecture assessment) and Validation (security + test coverage) simultaneously. "What's the status of the billing feature" could fan out to all three teams at once. Right now those wait in line.

The plumbing is almost there — `Promise.allSettled` already wraps the delegation loop. The hard part is teaching the orchestrator *when* work is parallel-safe vs when it has dependencies. Plan first, then build — sequential. Review from two angles — parallel. The orchestrator needs to express that intent, and the delegation tool needs to support it.

That's where the biggest time-to-answer improvement is hiding. Everything else scales linearly with intelligence improvements. Parallel delegation scales with team count.
