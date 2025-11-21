# Example: Meta-Prompt Pattern (Level 6)

A Level 6 Template Metaprompt - prompts that generate prompts for exponential leverage.

---

## What is a Meta-Prompt?

A meta-prompt is a prompt that **generates other prompts**. This is **massive leverage**:
- Write 1 meta-prompt → Generate 10+ domain-specific prompts
- Systematize prompt creation
- Ensure consistency across prompt library
- Capture patterns once, reuse infinitely

---

## Example: Generate CRUD Prompts

```markdown
---
description: Generate complete CRUD prompts for a data model
argument-hint: model-name
allowed-tools: Write
model: sonnet
---

# Generate CRUD Prompts

Generate a complete set of Create, Read, Update, Delete prompts for a data model.

## Purpose
Execute the `Workflow` to generate 4 prompts (create, read, update, delete) for {{MODEL_NAME}}

## Variables
MODEL_NAME: $1  # Name of the data model (e.g., "user", "product", "order")
OUTPUT_DIR: ./.claude/commands
MODEL_DIR: ./models
TIMESTAMP: $(date +%Y%m%d)

## Workflow
1. VALIDATE input:
   - REQUIRED: {{MODEL_NAME}} is provided
   - REQUIRED: {{OUTPUT_DIR}} exists
   - IF validation fails: Exit with usage message

2. Read model definition:
   ```bash
   cat {{MODEL_DIR}}/{{MODEL_NAME}}.ts
   # or {{MODEL_DIR}}/{{MODEL_NAME}}.py
   ```
   - Extract field names and types
   - Identify required vs optional fields
   - Note validation rules
   - Find relationships to other models

3. IMPORTANT: Generate CREATE prompt:

   **File**: `{{OUTPUT_DIR}}/create-{{MODEL_NAME}}.md`

   **Content**:
   ```markdown
   ---
   description: Create new {{MODEL_NAME}} record
   ---

   # Create {{MODEL_NAME}}

   Create a new {{MODEL_NAME}} record with validation

   ## Purpose
   Execute the `Workflow` to create and validate a new {{MODEL_NAME}}

   ## Variables
   [List all model fields as variables]

   ## Workflow
   1. VALIDATE required fields:
      - REQUIRED: [list required fields]
      - IF missing: Exit with error
   2. VALIDATE field formats:
      - [field]: [validation rule]
   3. Create record in database:
      ```[language]
      [ORM code to create record]
      ```
   4. CRITICAL: Verify creation:
      - Record exists in database
      - All fields saved correctly
   5. Return created record with ID

   ## Report
   ```json
   {
     "status": "success|failure",
     "{{MODEL_NAME}}_id": "generated-id",
     "created_at": "timestamp"
   }
   ```
   ```

4. Generate READ prompt:

   **File**: `{{OUTPUT_DIR}}/read-{{MODEL_NAME}}.md`

   **Content**:
   ```markdown
   ---
   description: Read {{MODEL_NAME}} records with filtering
   ---

   # Read {{MODEL_NAME}}

   Retrieve {{MODEL_NAME}} records by ID or filters

   ## Purpose
   Execute the `Workflow` to fetch {{MODEL_NAME}} data

   ## Variables
   QUERY_TYPE: $1  # "by-id" | "by-filter" | "all"
   QUERY_VALUE: $2  # ID or filter JSON

   ## Workflow
   1. Parse query type:
      - IF by-id: Fetch single record
      - IF by-filter: Query with filters
      - IF all: Return paginated list
   2. Execute database query:
      ```[language]
      [ORM code to query]
      ```
   3. VALIDATE results:
      - Check records exist
      - Verify field types
   4. Format output

   ## Report
   ```json
   {
     "status": "success|failure",
     "count": number,
     "{{MODEL_NAME}}s": [array of records]
   }
   ```
   ```

5. Generate UPDATE prompt:

   **File**: `{{OUTPUT_DIR}}/update-{{MODEL_NAME}}.md`

   **Content**:
   ```markdown
   ---
   description: Update existing {{MODEL_NAME}} record
   ---

   # Update {{MODEL_NAME}}

   Update {{MODEL_NAME}} record with validation and versioning

   ## Purpose
   Execute the `Workflow` to safely update a {{MODEL_NAME}}

   ## Variables
   {{MODEL_NAME.upper()}}_ID: $1  # Record to update
   UPDATES: $2  # JSON of field updates

   ## Workflow
   1. CRITICAL: Verify record exists:
      - Fetch current version
      - IF not found: Exit with 404
   2. VALIDATE updates:
      - Check field permissions
      - Validate new values
      - Ensure no required fields removed
   3. IMPORTANT: Create backup:
      - Save current version to audit log
   4. Apply updates:
      ```[language]
      [ORM code to update]
      ```
   5. CRITICAL: Verify update:
      - Changes persisted
      - No data loss
   6. Return updated record

   ## Report
   ```json
   {
     "status": "success|failure",
     "{{MODEL_NAME}}_id": "id",
     "updated_fields": [list],
     "previous_version": object
   }
   ```
   ```

6. Generate DELETE prompt:

   **File**: `{{OUTPUT_DIR}}/delete-{{MODEL_NAME}}.md`

   **Content**:
   ```markdown
   ---
   description: Delete {{MODEL_NAME}} record with safeguards
   ---

   # Delete {{MODEL_NAME}}

   Safely delete {{MODEL_NAME}} with backup and cascade handling

   ## Purpose
   Execute the `Workflow` to safely delete a {{MODEL_NAME}}

   ## Variables
   {{MODEL_NAME.upper()}}_ID: $1  # Record to delete
   CASCADE: $2  # "cascade" | "restrict" | "set-null"

   ## Workflow
   1. CRITICAL: Verify record exists:
      - Fetch current record
      - IF not found: Exit (already deleted)
   2. CRITICAL: Create backup before deletion:
      ```[language]
      [Code to backup to archive table]
      ```
   3. IMPORTANT: Check for dependencies:
      - Find related records
      - Handle according to CASCADE strategy
   4. CRITICAL: Perform deletion:
      ```[language]
      [ORM code to delete]
      ```
   5. CRITICAL: Verify deletion:
      - Record no longer in database
      - Backup exists in archive
      - Related records handled correctly

   ## Report
   ```json
   {
     "status": "success|failure",
     "{{MODEL_NAME}}_id": "id",
     "deleted_at": "timestamp",
     "backup_location": "path",
     "cascade_actions": [list]
   }
   ```
   ```

7. Create index file:

   **File**: `{{OUTPUT_DIR}}/{{MODEL_NAME}}-crud-index.md`

   **Content**: Links to all 4 CRUD prompts with usage examples

8. VALIDATE all generated prompts:
   - All 4 files exist
   - Follow Level 2 (Workflow) format
   - Include error handling
   - Have specific examples
   - Use appropriate IDKs

## Report

Provide summary of generated prompts:

```yaml
status: success|failure
model_name: {{MODEL_NAME}}
prompts_generated:
  - create-{{MODEL_NAME}}.md
  - read-{{MODEL_NAME}}.md
  - update-{{MODEL_NAME}}.md
  - delete-{{MODEL_NAME}}.md
total_prompts: 4
location: {{OUTPUT_DIR}}
index_file: {{MODEL_NAME}}-crud-index.md
ready_to_use: yes|no
```

## Error Handling
- IF {{MODEL_NAME}} not found in models directory:
  → Generate generic CRUD prompts with placeholders
  → Warn user to customize for specific model
- IF {{OUTPUT_DIR}} not writable:
  → Exit with permission error
  → Suggest alternative location
- IF prompt generation incomplete:
  → Save partial results
  → Report which prompts succeeded
  → Provide manual steps to complete

## Examples

### Example 1: Generate User CRUD
```bash
/generate-crud-prompts user
```

Expected output:
```yaml
status: success
model_name: user
prompts_generated:
  - create-user.md
  - read-user.md
  - update-user.md
  - delete-user.md
total_prompts: 4
location: ./.claude/commands
index_file: user-crud-index.md
ready_to_use: yes
```

**Result**: 4 new commands created
- `/create-user` - Creates user with email validation
- `/read-user` - Queries users by ID or filters
- `/update-user` - Updates user with audit trail
- `/delete-user` - Soft delete with backup

### Example 2: Generate Product CRUD
```bash
/generate-crud-prompts product
```

**Result**: 4 prompts for product management
- Includes inventory validation
- Handles SKU uniqueness
- Manages product variants
- Tracks price history
```

---

## Why This Works

### Exponential Leverage
- **1 meta-prompt** → **4 prompts per model** → **N models** = **4N prompts**
- For 10 models: 1 prompt generates 40 working prompts

### Consistency
- All CRUD prompts follow same pattern
- Same error handling approach
- Same validation strategy
- Same report format

### Maintainability
- Update meta-prompt once
- Regenerate all CRUD prompts
- Consistency across entire codebase

### Time Savings
- Manual: 30 min per CRUD set = 2 hours for 10 models
- Meta-prompt: 5 min one-time + 30 sec per model = 10 minutes total
- **92% time reduction**

---

## Advanced Meta-Prompt Patterns

### Pattern 1: Domain-Specific Generator

Generate prompts for specific domains:
```markdown
/generate-api-prompts [endpoint-name]
→ Creates prompts for: handler, validator, test, docs
```

### Pattern 2: Test Suite Generator

```markdown
/generate-test-suite [feature-name]
→ Creates: unit tests, integration tests, e2e tests
```

### Pattern 3: Documentation Generator

```markdown
/generate-docs [module-name]
→ Creates: API docs, usage guide, examples
```

### Pattern 4: Migration Generator

```markdown
/generate-migration [from-version] [to-version]
→ Creates: schema migration, data migration, rollback
```

---

## Meta-Prompt Best Practices

### ✅ DO

- **Generate complete, working prompts** (not templates)
- **Include validation in meta-prompt** (verify generated prompts)
- **Use consistent naming** (pattern-based filenames)
- **Add examples in generated prompts**
- **Include error handling**
- **Create index/navigation files**

### ❌ DON'T

- **Don't generate partial prompts** (requiring manual completion)
- **Don't skip validation** (ensure quality)
- **Don't hardcode values** (use variables)
- **Don't forget IDKs** (generated prompts need them too)
- **Don't create one-offs** (meta-prompts should be reusable)

---

## Integration with Workflow

### Standard SDLC with Meta-Prompts

```
1. Generate prompts for new feature:
   /generate-feature-prompts authentication

2. Run generated prompts:
   /plan-authentication
   /build-authentication
   /test-authentication
   /deploy-authentication

3. Update meta-prompt based on learnings

4. Regenerate for next feature
```

### Building Prompt Libraries

```
# Generate prompts for entire domain
for model in user product order payment; do
  /generate-crud-prompts $model
done

# Result: Complete CRUD library
# 4 models × 4 operations = 16 working prompts
```

---

## Measuring Meta-Prompt ROI

### Time Investment
- Create meta-prompt: 2 hours
- Generate prompts: 30 seconds each
- Manual creation: 30 minutes each

### Break-Even Point
- Break-even after: 4-5 prompt generations
- Thereafter: Pure profit

### Compound Value
- Each generated prompt used 10x → 10x leverage
- Meta-prompt used 10x → 100x total leverage

---

## Template for Your Own Meta-Prompts

```markdown
---
description: Generate [type] prompts for [domain]
---

# Generate [Type] Prompts

## Purpose
Execute the `Workflow` to generate N prompts for [purpose]

## Variables
DOMAIN: $1  # What to generate prompts for
OUTPUT_DIR: ./.claude/commands

## Workflow
1. VALIDATE input
2. Read domain definition/schema
3. FOR each prompt type:
   - Generate complete Level 2 (Workflow) prompt
   - Include all sections (Variables, Workflow, Report)
   - Add error handling
   - Use appropriate IDKs
   - Include examples
4. Create index file
5. VALIDATE all generated prompts

## Report
```yaml
status: success|failure
prompts_generated: [list]
total_count: N
location: [path]
```
```

---

**Meta-prompts are force multipliers. Master them, and you'll never manually write repetitive prompts again.**

**Key insight**: Time spent on one excellent meta-prompt returns 100x through generated prompts that each return 10x through agent execution = **1000x total leverage**.
