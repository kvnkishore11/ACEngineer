# Test the Agentic Prompt Engineering Skill

This file tests whether the skill is working correctly.

## Test 1: Skill Discovery

Ask Claude:
> "I want to create a slash command that runs tests. Can you help?"

**Expected**: Claude should reference this skill automatically and guide you through creating a Level 2 Workflow prompt.

---

## Test 2: Format Selection

Ask Claude:
> "Should I use Level 1 or Level 2 format for a command that generates documentation?"

**Expected**: Claude should recommend Level 2 (Workflow) and explain why, referencing the 7 levels from SKILL.md.

---

## Test 3: IDK Recommendation

Ask Claude:
> "I have a command that deletes files. Where should I put CRITICAL?"

**Expected**: Claude should recommend placing CRITICAL on the backup verification step, referencing the IDK catalog.

---

## Test 4: Template Usage

Ask Claude:
> "Create a slash command that analyzes code complexity"

**Expected**: Claude should:
1. Use the workflow-prompt-template.md
2. Fill in all sections
3. Add appropriate IDKs
4. Include examples
5. Follow Level 2 format

---

## Test 5: Meta-Prompt Understanding

Ask Claude:
> "What's a meta-prompt and when should I use one?"

**Expected**: Claude should explain Level 6 prompts, give examples from meta-prompt-example.md, and explain the exponential leverage concept.

---

## Validation

If all 5 tests pass, the skill is working correctly!

The skill should activate automatically when you:
- Mention "slash command"
- Say "create a prompt"
- Ask about "agent instructions"
- Request "help with prompting"
