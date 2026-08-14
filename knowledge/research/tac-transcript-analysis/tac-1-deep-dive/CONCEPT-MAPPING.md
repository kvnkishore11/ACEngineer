# TAC-1 Concept Mapping: Video to Code

## Mapping Spoken Concepts to Code Artifacts

This document connects what the instructor SAYS in the videos to what actually EXISTS in the codebase.

---

## 1. Core Conceptual Mapping

### "Stop Coding" → Programmable Execution

**What the Author Says:**
> "Throughout TAC, Tactical Agentic Coding, we're not going to type a single line of code."

**What the Code Shows:**
```python
# programmable/programmable.py
def main():
    with open("programmable/prompt.md", "r") as f:
        prompt_content = f.read()

    command = ["claude", "-p", prompt_content]
```

**The Connection:**
The entire codebase demonstrates automation through prompts, not manual coding. The Python/Shell/TypeScript files are minimal wrappers that invoke Claude to do the actual work.

---

### "The Big Three to Core Four" → Permission Model

**What the Author Says:**
> "Agentic Coding expands on the big three by adding one new dimension... tools."
> "Context → Model → Prompt → Tools (Core Four)"

**What the Code Shows:**
```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit",
      "Bash(uv run:*)",
      "Bash(git checkout:*)",
      "Bash(git branch:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "WebSearch"
    ]
  }
}
```

**The Connection:**
The permission file literally defines the "Tools" dimension - each permission is a tool that transforms a simple prompt into an agentic system.

---

### "AI Coding vs Agentic Coding" → README Prompts

**What the Author Says:**
> "This first prompt represents what can be done with AI coding at a foundational level."
> "This second prompt represents what can be done with agentic coding at a foundational level."

**What the Code Shows:**
```markdown
## AI Coding Prompt
CREATE main_aic.py:
    print goodbye ai coding

## Agentic Coding Prompt
RUN:
    checkout a new/existing "demo-agentic-coding" git branch
CREATE main_tac.py:
    print "hello agentic coding"
    print a concise explanation of the definition of ai agents
RUN:
    uv run main_aic.py
    uv run main_tac.py
    git add .
    git commit -m "Demo agentic coding capabilities"
```

**The Connection:**
The README provides the EXACT examples discussed in the video - simple file creation (AI) vs. multi-step workflows with git operations (Agentic).

---

## 2. Hidden Architecture Revealed

### "Programmable Agentic Coding Tool" → Multi-Language Support

**What the Author Says:**
> "Claude Code is also a programmable Agentic Coding tool... we can run it from any programming language that has terminal access."

**What the Code Shows:**
- `programmable/programmable.py` - Python implementation
- `programmable/programmable.sh` - Shell implementation
- `programmable/programmable.ts` - TypeScript/Bun implementation

**Deeper Insight:**
The author provides THREE implementations of the same concept, showing this isn't tied to a specific language but is a universal pattern. This redundancy is pedagogical - proving the concept works everywhere.

---

### "Long Chains of Tools" → Sequential Operations

**What the Author Says:**
> "The new element that transforms the big three of AI coding to Agentic Coding is prompts that can reliably execute long chains of tools."

**What the Code Shows in prompt.md:**
```markdown
RUN:
    checkout a new/existing "demo-agentic-coding" git branch
CREATE main_aic.py:
    print "goodbye ai coding"
CREATE main_tac.py:
    print "hello agentic coding"
RUN:
    uv run main_aic.py
    uv run main_tac.py
    git add .
    git commit -m "Demo agentic coding capabilities"
REPORT:
    respond with the exact output of both .py files
```

**The Connection:**
The prompt demonstrates a 7-step chain: branch management → file creation → execution → version control → reporting. This IS the "long chain" concept materialized.

---

## 3. Pedagogical Code Patterns

### Pattern 1: Minimal Viable Wrapper

**Video Context:** "We can embed our own agents, our own workflows, our own agentic prompts"

**Code Pattern:**
```python
# Entire implementation in ~30 lines
def main():
    with open("programmable/prompt.md", "r") as f:
        prompt_content = f.read()
    command = ["claude", "-p", prompt_content]
    result = subprocess.run(command, capture_output=True, text=True)
```

**Teaching Method:** Start with the absolute minimum to prove the concept works.

---

### Pattern 2: Declarative Task Definition

**Video Context:** "Engineering work across worlds"

**Code Pattern:**
```markdown
RUN:     # Imperative command
CREATE:  # File generation
REPORT:  # Output verification
```

**Teaching Method:** Introduce a domain-specific language (DSL) that maps directly to engineering workflows.

---

## 4. What's Said vs. What's Shown

### Explicit in Video, Implicit in Code

| Video Concept | Code Implementation | Gap Analysis |
|---------------|-------------------|--------------|
| "Stop coding" | No actual code writing examples | Proven by absence |
| "10x leverage" | Single prompt → Multiple operations | Demonstrated but not measured |
| "Self-operating machines" | Automated git workflow | Basic example, not fully autonomous |
| "Replace yourself" | Prompt-driven development | Conceptual, not literal |

### Implicit in Video, Explicit in Code

| Code Feature | Video Coverage | Significance |
|-------------|----------------|--------------|
| Permission granularity | Briefly mentioned | Critical for production safety |
| .env.sample file | Not discussed | Implies API key management |
| WebSearch permission | Not demonstrated | Hints at future capabilities |
| Error handling in scripts | Not mentioned | Shows production thinking |

---

## 5. The Meta-Pattern: Teaching Through Contrast

The entire TAC-1 structure is built on contrasts:

### File Structure Contrasts
- `main_aic.py` vs `main_tac.py` (old vs new)
- Single command vs workflow (simple vs complex)
- Manual vs programmable (human vs system)

### Prompt Structure Contrasts
```markdown
# AI Coding: Single directive
CREATE main_aic.py:
    print goodbye ai coding

# Agentic Coding: Multi-step workflow
RUN → CREATE → CREATE → RUN → RUN → git add → git commit → REPORT
```

### Execution Contrasts
- Interactive (human types) vs Programmatic (script runs)
- Synchronous (wait for each) vs Sequential (automated flow)
- Local (single file) vs Systemic (git integration)

---

## 6. Evolution Markers in Code

### What TAC-1 Sets Up for Future Lessons

1. **Permission System** → Will expand to more tools
2. **Prompt Templates** → Will become more complex
3. **Git Integration** → Foundation for CI/CD automation
4. **Multi-language Support** → Platform agnostic approach
5. **Report Directive** → Self-validation pattern

### Seeds Planted But Not Sprouted

```json
"WebSearch"  // Allowed but never used in TAC-1
```
This permission hints at future lessons involving external data fetching.

---

## 7. The Real Lesson Hidden in Plain Sight

**What the Author Really Teaches:**

The code isn't about Python, Shell, or TypeScript. It's about:

1. **Abstraction**: Hide complexity behind simple interfaces
2. **Composition**: Build complex behaviors from simple primitives
3. **Automation**: Replace human actions with systematic processes
4. **Verification**: Always validate outputs (REPORT directive)
5. **Evolution**: Start simple, enable complexity

**The Hidden Message:**
The actual code files (programmable.py/sh/ts) are throwaway. They're just proof that ANY language can invoke this pattern. The real asset is the PROMPT and the MENTAL MODEL.

---

## 8. What's Missing (Intentionally)

### Not in TAC-1 (Setting Up Future Lessons)

1. **No error handling in prompts** - Building confidence first
2. **No conditional logic** - Linear workflows only
3. **No data persistence** - Stateless operations
4. **No external APIs** - Local operations only
5. **No parallel execution** - Sequential thinking first

Each absence is pedagogical - complexity will be layered in future lessons.

---

## Summary: The Perfect Pedagogical Codebase

TAC-1's codebase is remarkably aligned with its video content:

- **Every file has purpose** - No bloat, no confusion
- **Every concept has code** - Concrete examples for abstract ideas
- **Every pattern has variants** - Proving universality
- **Every feature has permission** - Security-first thinking

The genius is in what's NOT there as much as what IS there. It's a minimal viable lesson that plants seeds for an entire curriculum.

The code literally demonstrates the transformation from "typing code" to "commanding systems" - the fundamental shift the author evangelizes throughout the video.