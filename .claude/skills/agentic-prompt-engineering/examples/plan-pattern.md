# Example: Plan Pattern

A Level 2 Workflow prompt for generating implementation plans.

---

```markdown
---
description: Generate detailed implementation plan from requirements
argument-hint: requirements-description
allowed-tools: Read, Write, Bash
model: sonnet
---

# Plan

Generate a comprehensive implementation plan for a new feature or change.

## Purpose
Execute the `Workflow` and `Report` sections to create a detailed, actionable implementation plan

## Variables
USER_REQUIREMENTS: $1  # Feature description or requirements
PLAN_OUTPUT_DIR: ./specs
PLAN_TEMPLATE: ./.claude/templates/plan-template.md
PROJECT_ROOT: .
TIMESTAMP: $(date +%Y%m%d-%H%M%S)

## Workflow
1. VALIDATE requirements:
   - REQUIRED: {{USER_REQUIREMENTS}} is not empty
   - REQUIRED: {{PLAN_OUTPUT_DIR}} exists or can be created
   - IF validation fails: Exit with clear error message

2. Analyze current project structure:
   ```bash
   git ls-files | head -50
   tree -L 2 -I 'node_modules|.git|dist|build'
   ```

3. Read relevant context files:
   - README.md for project overview
   - package.json or requirements.txt for dependencies
   - Existing similar features for patterns

4. IMPORTANT: Generate comprehensive plan with these sections:

   ### Overview
   - Clear problem statement
   - Proposed solution approach
   - Key benefits and trade-offs

   ### Technical Design
   - Architecture decisions
   - Data models and schemas
   - API contracts (if applicable)
   - Component interactions

   ### Implementation Phases
   - Phase 1: [Foundation work]
   - Phase 2: [Core features]
   - Phase 3: [Integration and polish]

   ### File Changes
   - Files to create: [list with purpose]
   - Files to modify: [list with changes]
   - Files to delete: [list with reason]

   ### Testing Strategy
   - Unit test requirements
   - Integration test scenarios
   - E2E test cases
   - Edge cases to cover

   ### Deployment Considerations
   - Migration requirements
   - Rollback procedures
   - Monitoring and alerts
   - Feature flags (if applicable)

   ### Success Criteria
   - Functional requirements met
   - Performance targets
   - Quality gates
   - Acceptance criteria

5. Write plan to file:
   ```bash
   mkdir -p {{PLAN_OUTPUT_DIR}}
   ```
   File path: `{{PLAN_OUTPUT_DIR}}/plan-{{TIMESTAMP}}.md`

6. CRITICAL: Validate generated plan:
   - ALL sections are present (not TBD or TODO)
   - File changes are specific (not "update as needed")
   - Success criteria are measurable
   - Testing strategy covers edge cases
   - IF any section is incomplete: Regenerate that section

7. Create GitHub issue (optional):
   ```bash
   gh issue create \
     --title "Plan: {{USER_REQUIREMENTS}}" \
     --body-file {{PLAN_OUTPUT_DIR}}/plan-{{TIMESTAMP}}.md \
     --label "plan"
   ```

## Report

Provide structured summary:

```yaml
status: success|failure
plan_file: [absolute path]
sections_generated: [count]
estimated_complexity: low|medium|high|epic
estimated_effort: [hours or story points]
breaking_changes: yes|no
dependencies:
  - [dependency 1]
  - [dependency 2]
risks:
  - [risk 1]
  - [risk 2]
github_issue: [URL if created]
next_steps:
  - [step 1]
  - [step 2]
```

REQUIRED fields:
- status, plan_file, estimated_complexity

## Error Handling
- IF {{USER_REQUIREMENTS}} is empty:
  → Exit with: "Error: Requirements description required. Usage: /plan 'feature description'"
- IF {{PLAN_OUTPUT_DIR}} cannot be created:
  → Exit with permission error and suggest alternative location
- IF project structure cannot be determined:
  → Generate plan with generic structure
  → Add WARNING note in plan
- IF plan generation is incomplete:
  → Retry incomplete sections once
  → IF still incomplete: Save partial plan with TODO markers
  → Report status as "partial"

## Examples

### Example 1: New Feature
```bash
/plan "Add user authentication with email/password and OAuth2 support for Google and GitHub"
```

Expected output:
```yaml
status: success
plan_file: /project/specs/plan-20240115-143022.md
sections_generated: 7
estimated_complexity: high
estimated_effort: 40 hours
breaking_changes: yes
dependencies:
  - OAuth2 library (passport.js or similar)
  - Email service provider (SendGrid/AWS SES)
  - Session management (Redis)
risks:
  - Security: OAuth token storage
  - Migration: Existing users need migration path
github_issue: https://github.com/user/repo/issues/123
next_steps:
  - Review and approve plan
  - Set up OAuth apps in Google/GitHub
  - Run /build with this plan
```

### Example 2: Bug Fix
```bash
/plan "Fix memory leak in background job processor causing OOM errors after 24h runtime"
```

Expected output:
```yaml
status: success
plan_file: /project/specs/plan-20240115-144513.md
sections_generated: 7
estimated_complexity: medium
estimated_effort: 8 hours
breaking_changes: no
dependencies: []
risks:
  - Diagnosis: May need profiling in production
  - Testing: Requires long-running test (24h+)
next_steps:
  - Profile memory usage in staging
  - Review plan with team
  - Run /build when approved
```

### Example 3: Refactoring
```bash
/plan "Refactor API layer to use GraphQL instead of REST, maintaining backward compatibility"
```

Expected output:
```yaml
status: success
plan_file: /project/specs/plan-20240115-150033.md
sections_generated: 7
estimated_complexity: epic
estimated_effort: 120 hours
breaking_changes: no
dependencies:
  - GraphQL server (Apollo/Express-GraphQL)
  - Schema generation tooling
  - GraphQL client libraries
risks:
  - Complexity: Maintaining two APIs during transition
  - Performance: GraphQL N+1 query issues
  - Timeline: Phased migration required
next_steps:
  - Get architectural approval
  - Prototype GraphQL schema
  - Define migration phases
  - Plan backward compatibility strategy
```
```

---

## Why This Works

### Clear Structure
- Every section has a purpose
- No ambiguity in what to do
- Validation ensures quality

### Comprehensive Planning
- Covers technical, testing, and deployment
- Identifies risks early
- Provides clear success criteria

### Actionable Output
- Plan can be directly used by /build command
- File paths are specific
- Dependencies are explicit

### Built-in Quality
- Validation step catches incomplete plans
- Forces specific file changes (not vague)
- Requires measurable success criteria

### Flexible Usage
- Works for features, bugs, refactoring
- Scales from hours to weeks of work
- Can integrate with GitHub issues

---

## Variations

### Quick Plan (Level 1 style)
```markdown
# Quick Plan

Generate a rapid 5-minute implementation outline for {{$1}}

## Purpose
Quick planning for small tasks under 2 hours
```

### Epic Plan (More detailed)
```markdown
# Epic Plan

Generate multi-sprint planning for large initiatives

## Additional Sections
- Stakeholder analysis
- Milestone breakdown
- Resource allocation
- Risk mitigation strategies
```

### Technical Deep Dive
```markdown
# Tech Plan

Focus exclusively on technical architecture and design patterns

## Emphasis
- System design diagrams
- Database schemas
- API contracts
- Performance considerations
```

---

## Integration Points

**Works with**:
- `/build` - Executes the plan
- `/test` - Validates implementation
- `/review` - Checks alignment with plan
- GitHub Issues - Track plan as issue

**ADW Integration**:
```bash
# Full SDLC
/plan "feature" → /build ./specs/plan-*.md → /test → /review
```

---

**This is the foundation of the TAC system - great plans lead to great implementations.**
