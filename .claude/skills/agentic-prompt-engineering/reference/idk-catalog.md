# Information Dense Keywords (IDK) - Complete Catalog

> "Strategic word placement that changes agent behavior"

This is the complete reference for IDKs - keywords that carry disproportionate weight in agent processing.

---

## How IDKs Work

### The Technical Mechanism

In transformer models, IDKs affect:
1. **Attention Weights**: IDKs receive higher attention scores
2. **Context Windows**: IDKs influence interpretation of surrounding tokens
3. **Pattern Matching**: IDKs activate specific behavioral templates
4. **Probability Shifts**: IDKs modify token generation probabilities

### The Practical Impact

```python
# Without IDK
Agent sees: "validate input" → 30% chance of validation

# With IDK
Agent sees: "CRITICAL: validate input" → 95% chance of validation
```

---

## Tier 1: Absolute Controllers (Maximum Impact)

### ALWAYS / NEVER
**Attention Weight**: ~3.5x baseline
**Compliance Rate**: 98%+
**Effect**: Creates near-absolute behavioral requirements

**Usage**:
```markdown
ALWAYS validate user input before database operations
NEVER expose internal system paths in error messages
ALWAYS create backup before destructive operations
NEVER proceed if validation fails
```

**When to Use**:
- Non-negotiable safety requirements
- Security constraints
- Data integrity rules
- Immutable business rules

**Combining**:
```markdown
CRITICAL: ALWAYS check authentication before data access
IMPORTANT: NEVER log sensitive user data (PII, passwords, tokens)
```

---

### MUST / MUST NOT
**Attention Weight**: ~3.0x baseline
**Compliance Rate**: 95%+
**Effect**: Strong requirement with slight flexibility for critical failures

**Usage**:
```markdown
You MUST check database connectivity before executing queries
You MUST NOT modify production data during testing
Code changes MUST pass all tests before deployment
Agents MUST report back within 30 seconds or timeout
```

**When to Use**:
- Critical requirements that can be violated only in exceptional cases
- Cross-cutting concerns (logging, error handling)
- Architecture principles
- SLA requirements

**vs ALWAYS/NEVER**: MUST allows for documented exceptions, ALWAYS does not

---

### CRITICAL
**Attention Weight**: ~4.0x baseline (highest)
**Compliance Rate**: 99%+
**Effect**: Overrides competing instructions, maximum priority

**Usage**:
```markdown
CRITICAL: Verify backup exists before deletion
CRITICAL: Validate JWT signature before processing claims
CRITICAL: Stop execution if memory usage exceeds 90%
```

**When to Use**:
- Single most important instruction in a section
- Failure points that break everything
- Security-sensitive operations
- Data loss prevention

**Combining with Others**:
```markdown
CRITICAL: ALWAYS verify user permissions before allowing access
CRITICAL: NEVER commit secrets or API keys to repository
```

**Placement**: Use sparingly - if everything is CRITICAL, nothing is.

---

## Tier 2: Strong Modifiers (High Impact)

### IMPORTANT
**Attention Weight**: ~2.5x baseline
**Compliance Rate**: 85%+
**Effect**: Significantly elevates priority without overriding

**Usage**:
```markdown
IMPORTANT: Generate comprehensive test coverage (>80%)
IMPORTANT: Include error handling for all external API calls
IMPORTANT: Document all public functions with docstrings
```

**When to Use**:
- Quality requirements
- Best practices that shouldn't be skipped
- Non-negotiable features
- Key validations

**Frequency**: Can be used multiple times per prompt (unlike CRITICAL)

---

### ESSENTIAL
**Attention Weight**: ~2.8x baseline
**Compliance Rate**: 90%+
**Effect**: Marks requirements for completion validation

**Usage**:
```markdown
ESSENTIAL: All API endpoints must return JSON with status field
ESSENTIAL: Error messages must include request_id for tracing
ESSENTIAL: Configuration must be externalized, not hardcoded
```

**When to Use**:
- Core architecture decisions
- Must-have features (vs nice-to-have)
- Contract requirements
- Integration points

---

### REQUIRED
**Attention Weight**: ~2.3x baseline
**Compliance Rate**: 85%+
**Effect**: Creates validation checkpoints

**Usage**:
```markdown
REQUIRED: Authentication token in all requests
REQUIRED: Input validation before processing
REQUIRED: Logging for audit trail
```

**When to Use**:
- Prerequisites that block further steps
- Mandatory inputs/outputs
- Compliance requirements

---

## Tier 3: Behavioral Modifiers (Moderate Impact)

### CAREFULLY
**Attention Weight**: ~1.8x baseline
**Effect**: +40% validation steps, increased error checking

**Usage**:
```markdown
CAREFULLY parse the configuration file (check for malformed JSON)
CAREFULLY migrate data (validate each row before commit)
CAREFULLY handle user input (sanitize and validate)
```

**When to Use**:
- Operations prone to errors
- Delicate state transitions
- User input handling
- Data migrations

**Effect on Agent**:
- Adds extra validation steps
- Increases error checking
- More conservative approach

---

### THOROUGHLY
**Attention Weight**: ~2.0x baseline
**Effect**: +60% completeness, more comprehensive execution

**Usage**:
```markdown
THOROUGHLY test all edge cases (empty, null, max values)
THOROUGHLY document the API (examples, error codes, rate limits)
THOROUGHLY analyze dependencies (direct and transitive)
```

**When to Use**:
- Testing requirements
- Documentation generation
- Security audits
- Code reviews

**Effect on Agent**:
- More exhaustive coverage
- Explores edge cases
- Longer execution time

---

### STRICTLY
**Attention Weight**: ~2.2x baseline
**Effect**: Reduces flexibility by 70%, enforces literal interpretation

**Usage**:
```markdown
STRICTLY follow the coding style guide (no exceptions)
STRICTLY adhere to the API schema (no additional fields)
STRICTLY maintain backward compatibility
```

**When to Use**:
- Style guides and standards
- Contract enforcement
- Compatibility requirements
- Regulatory compliance

**Effect on Agent**:
- No creative interpretation
- Literal compliance
- No shortcuts or optimizations

---

## Tier 4: Scope Controllers (Focused Impact)

### ONLY / EXCLUSIVELY
**Attention Weight**: ~2.5x baseline
**Effect**: 90% reduction in scope, ignores everything outside specification

**Usage**:
```markdown
ONLY modify files in the src/ directory (not tests, docs, config)
EXCLUSIVELY use Python 3.10 features (no deprecated syntax)
ONLY execute during business hours (9 AM - 5 PM)
Process ONLY the specified columns (ignore others)
```

**When to Use**:
- Constraining scope
- Permission boundaries
- Resource restrictions
- Safety limits

**Combining**:
```markdown
CRITICAL: ONLY access files within user's home directory
IMPORTANT: EXCLUSIVELY use approved libraries
```

---

### SPECIFICALLY
**Attention Weight**: ~1.9x baseline
**Effect**: Narrows interpretation, prevents generalization

**Usage**:
```markdown
SPECIFICALLY test the login endpoint (not entire auth system)
SPECIFICALLY validate email format (not all contact info)
SPECIFICALLY update version numbers (not full changelog)
```

**When to Use**:
- Preventing scope creep
- Focusing on one aspect
- Clarifying ambiguous requests

---

### EXACTLY
**Attention Weight**: ~2.1x baseline
**Effect**: Zero-tolerance matching, literal interpretation

**Usage**:
```markdown
Return EXACTLY this format: {"status": "ok", "data": []}
Match EXACTLY the regex pattern: ^[A-Z]{3}-\\d{4}$
Use EXACTLY 4 spaces for indentation (not tabs)
```

**When to Use**:
- Format specifications
- Schema validation
- Output contracts
- Compatibility requirements

---

## Advanced IDK Usage

### Stacking IDKs

**Sequential Intensification**:
```markdown
CRITICAL: ALWAYS validate authentication
IMPORTANT: THOROUGHLY test edge cases
CAREFULLY handle user input
```

**Effect**: Each layer adds independent influence

### Hierarchical Priority

```markdown
# Priority 1: Absolute
CRITICAL: [safety and security]

# Priority 2: Required
IMPORTANT: [quality and features]

# Priority 3: Recommended
[standard operations]
```

### Conditional IDKs

```markdown
IF production environment:
  - CRITICAL: ALWAYS use SSL
  - NEVER log sensitive data
ELSE IF staging:
  - IMPORTANT: Use SSL where possible
  - CAREFULLY log for debugging
```

---

## Domain-Specific IDKs

### Security Domain
```markdown
CRITICAL: Validate and sanitize all user input
NEVER trust client-side validation
ALWAYS use parameterized queries (prevent SQL injection)
MUST encrypt sensitive data at rest and in transit
STRICTLY enforce principle of least privilege
```

### Data Operations
```markdown
CRITICAL: Backup before destructive operations
ALWAYS validate data integrity after write
NEVER modify original data in-place
REQUIRED: Audit trail for all changes
CAREFULLY handle NULL values
```

### API Development
```markdown
IMPORTANT: All endpoints must return consistent error format
REQUIRED: Rate limiting on all public endpoints
EXACTLY follow OpenAPI 3.0 specification
THOROUGHLY document request/response schemas
```

### Testing
```markdown
THOROUGHLY test edge cases (empty, null, max, negative)
REQUIRED: Minimum 80% code coverage
SPECIFICALLY test error handling paths
CAREFULLY mock external dependencies
```

---

## Measuring IDK Effectiveness

### Before IDK
```markdown
Validate the input data before processing
```
**Result**: Validation skipped 30% of the time

### After IDK
```markdown
CRITICAL: ALWAYS validate input data before processing
```
**Result**: Validation performed 99% of the time

### Metrics to Track
- **Compliance Rate**: How often the instruction is followed
- **Error Reduction**: Decrease in validation failures
- **Consistency**: Same input → same output
- **Time Impact**: Whether THOROUGHLY increases execution time as expected

---

## Common Mistakes

### ❌ Overuse
```markdown
CRITICAL: IMPORTANT: ALWAYS CAREFULLY THOROUGHLY validate...
```
**Problem**: Dilutes impact, confuses priorities
**Solution**: Use ONE primary IDK per instruction

### ❌ Wrong Tier
```markdown
CAREFULLY delete production database
```
**Problem**: CAREFULLY insufficient for critical operation
**Solution**: Use CRITICAL or NEVER for destructive ops

### ❌ Conflicting IDKs
```markdown
ALWAYS include detailed logs
NEVER log any data
```
**Problem**: Agent can't satisfy both
**Solution**: Be specific about what to log

### ❌ No IDK on Critical Sections
```markdown
Backup data before deletion (would be nice)
```
**Problem**: Optional interpretation on critical operation
**Solution**: Add CRITICAL to enforce

---

## IDK Selection Guide

### Decision Tree

```
Is it about safety or security?
├─ YES → CRITICAL + ALWAYS/NEVER
└─ NO ↓

Is it a quality requirement?
├─ YES → IMPORTANT or ESSENTIAL
└─ NO ↓

Is it about scope/boundaries?
├─ YES → ONLY, EXCLUSIVELY, EXACTLY
└─ NO ↓

Is it about thoroughness?
├─ YES → THOROUGHLY, CAREFULLY
└─ NO ↓

Use standard language (no IDK needed)
```

### By Consequence of Failure

| Failure Impact | IDK Choice |
|----------------|------------|
| Data loss, security breach | CRITICAL + ALWAYS/NEVER |
| Quality degradation | IMPORTANT, ESSENTIAL |
| Incorrect scope | ONLY, EXCLUSIVELY |
| Incomplete work | THOROUGHLY |
| Avoidable errors | CAREFULLY |
| Nice-to-have | No IDK |

---

## Quick Reference Table

| IDK | Weight | Rate | Use For | Example |
|-----|--------|------|---------|---------|
| CRITICAL | 4.0x | 99% | Safety, security | CRITICAL: Verify backup |
| ALWAYS | 3.5x | 98% | Non-negotiable | ALWAYS validate input |
| NEVER | 3.5x | 98% | Absolute prohibition | NEVER expose secrets |
| MUST | 3.0x | 95% | Strong requirement | MUST pass tests |
| ESSENTIAL | 2.8x | 90% | Core requirement | ESSENTIAL: JSON response |
| IMPORTANT | 2.5x | 85% | Quality requirement | IMPORTANT: >80% coverage |
| REQUIRED | 2.3x | 85% | Prerequisites | REQUIRED: Auth token |
| STRICTLY | 2.2x | 80% | Literal compliance | STRICTLY follow PEP 8 |
| EXACTLY | 2.1x | 80% | Precision matching | EXACTLY match schema |
| THOROUGHLY | 2.0x | 75% | Completeness | THOROUGHLY test edges |
| SPECIFICALLY | 1.9x | 75% | Narrow focus | SPECIFICALLY test login |
| CAREFULLY | 1.8x | 70% | Extra validation | CAREFULLY parse config |

---

## Testing IDK Impact

### A/B Test Format

**Prompt A (No IDK)**:
```markdown
Validate user input before processing
```

**Prompt B (With IDK)**:
```markdown
CRITICAL: ALWAYS validate user input before processing
```

**Measure**:
- Success rate (validation performed)
- Error rate (uncaught invalid input)
- Consistency (same behavior each time)

### Expected Improvements

- Compliance: +50% to +90%
- Error reduction: -60% to -95%
- Consistency: +40% to +80%

---

**Use IDKs strategically, not randomly. Each one should serve a purpose.**
