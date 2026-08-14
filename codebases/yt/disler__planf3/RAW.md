# Planf3: Mythos Class Planning Meta-Skill
> Planf3 = Plans For Fable Five

## What is this?

There are two constraints of `Agentic Engineering`

1. Planning
2. Reviewing

Initial investment in a great plan is the difference between a great engineer and a mid engineer. By investing more effort upfront in planning, we improve on both constraints because `great planning, is great engineering`. 

Great planning also yields less reviewing as model capability increases.

The recently banned `Fable 5 and Mythos-class` models unlock the next level of planning ability which lets us specify the `EXACT outcomes we're looking for`.

Of the trade-off trifecta (perf, speed, cost) this new plan template trades speed and cost (tokens) for optimal performance.

## Priorities

`Performance > Speed >= Cost`

## Properties

To capture the intelligence ceiling of mythos-class models we need to improve our plan skill/template to have specific properties aka sections.

The output of our plan will be created, updated, and consumed by the agent trifecta: `The you (engineer), the engineering team, and ai agents`

> This will roughly be the new prompt template for the new planf3 meta-skill

- [x] h1 Title
- [x] Purpose, Problem, Solution
- [x] New vs Existing files section
- [x] HTML first
- [x] Questions and Answers section (toggleable)
- [x] Focused Images Embedded
- [x] Dedicated Workflows
- [x] Rich, updatable header metadata: created, modified[], commits[], agent name[], session id[], back references[] and forward references[]
- [x] Synced html and image styles
- [x] Per phase and per task per phase breakdown of work
- [x] Embedded checklist per task/phase
- [x] Validation & Testing sections that prevent completion until done (loops)

## API

`/planf3 <user prompt> <questionable>`

## Workflows

- Create Plan
- Update Plan
- Update References
- Build Plan
- Image Generation