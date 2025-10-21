2. Persistent State Management (state.py:15-173)
ADWState Class with file persistence:
Storage: agents/{adw_id}/adw_state.json
Core fields: adw_id, issue_number, branch_name, plan_file, worktree_path, backend_port, frontend_port, model_set
Workflow tracking: all_adws list tracks which workflows have run
Validation: Uses Pydantic ADWStateData model for type safety
3. Isolated Worktree Architecture (worktree_ops.py:15-200)
Worktree Creation (create_worktree():):
Location: trees/{adw_id}/ directory
Branch creation: git worktree add -b {branch_name} {path} origin/main
Isolation: Complete repository copy for parallel execution
Port Allocation System:
Deterministic: backend_port = 9100 + (hash(adw_id) % 15)
Range: Backend 9100-9114, Frontend 9200-9214
Environment: Creates .ports.env with BACKEND_PORT, FRONTEND_PORT, VITE_BACKEND_URL
Three-way Validation (validate_worktree()):
State has worktree_path
Directory exists on filesystem
Git recognizes the worktree
ADW Substages Breakdown
1. 📋 PLAN Phase (adw_plan_iso.py)
Substages:
State Initialization (66-95)

Load/create ADW state with ensure_adw_id()
Track workflow execution in all_adws list
Environment Setup (108-127)

Port Allocation: Deterministic backend/frontend ports (9100-9114/9200-9214)
Worktree Creation: Isolated git worktree in trees/{adw_id}/
Environment Files: Create .ports.env with port configuration
Issue Analysis (128-158)

Issue Classification: Use /classify_issue → /chore|/bug|/feature
Branch Generation: Create standardized branch name via /generate_branch_name
Plan Generation (179-218)

Worktree Installation: Run /install_worktree command for environment setup
Plan Creation: Execute classified command (/chore, /bug, /feature) in worktree
Plan Validation: Ensure plan file exists in worktree
Git Operations (285-328)

Commit Creation: Generate semantic commit message
Plan Commit: Commit plan to isolated branch
PR Creation: Push and create/update pull request
2. 🔨 BUILD Phase (adw_build_iso.py)
Substages:
Prerequisites Validation (63-134)

State Loading: Require existing ADW ID and state
Worktree Validation: Three-way check (state, filesystem, git)
Plan File Verification: Ensure plan exists from previous phase
Implementation Execution (162-183)

Plan Implementation: Execute /implement command with plan file
Code Generation: Generate solution based on plan in isolated worktree
Quality Assurance (185-231)

Issue Classification: Retrieve or re-classify issue type
Commit Generation: Create implementation commit message
Implementation Commit: Commit changes to isolated branch
Integration (233-249)

Git Finalization: Push changes and update PR
3. 🧪 TEST Phase (adw_test_iso.py)
Substages:
Test Environment Setup (671-725)

State Validation: Verify worktree and dependencies exist
Test Configuration: Configure unit and E2E test flags
Unit Test Execution (346-453)

Test Execution: Run /test command in worktree
Result Parsing: Parse JSON test results with pass/fail counts
Failure Resolution: Use /resolve_failed_test for automatic fixes
Retry Logic: Up to 4 retry attempts with resolution
E2E Test Execution (530-645)

E2E Test Execution: Run /test_e2e with isolated ports
Screenshot Capture: Capture UI test screenshots
E2E Resolution: Use /resolve_failed_e2e_test for UI fixes
Retry Logic: Up to 2 retry attempts for E2E tests
Test Reporting (781-863)

Comprehensive Summary: Post detailed test results to GitHub
Test Commit: Commit test results regardless of outcome
Status Tracking: Track test success/failure for downstream decisions
4. 👀 REVIEW Phase (adw_review_iso.py)
Substages:
Review Preparation (385-410)

Spec File Discovery: Find plan file from state or git diff
Review Configuration: Set resolution and retry parameters
Implementation Review (71-115)

Code Review: Execute /review command against specification
Screenshot Analysis: Capture visual evidence of implementation
Issue Detection: Identify blockers, tech debt, and skippable issues
Issue Resolution (202-251, 413-458)

Blocker Resolution: Auto-create patch plans for critical issues
Patch Implementation: Implement resolutions automatically
Retry Logic: Up to 3 review attempts with automatic fixes
Review Reporting (144-200, 461-470)

Screenshot Upload: Upload to R2 storage with public URLs
Summary Generation: Create markdown summary with embedded images
Review Commit: Commit review results and resolutions
5. 📚 DOCUMENT Phase (adw_document_iso.py)
Substages:
Documentation Analysis (63-97)

Change Detection: Check for changes vs origin/main
Spec File Location: Find specification from state
Documentation Generation (99-184)

Doc Creation: Execute /document command with spec file
Content Validation: Verify documentation files were created
Conditional Updates: Update conditional docs based on changes
KPI Tracking (186-286)

Metrics Collection: Track agentic performance metrics
KPI Updates: Update agentic_kpis.md with workflow statistics
Commit KPIs: Commit metrics (never fails main workflow)
Documentation Finalization (456-515)

Doc Commit: Commit documentation changes
Git Finalization: Push and update PR
6. 🚢 SHIP Phase (Composite Workflows)
Zero Touch Execution (ZTE) (adw_sdlc_ZTE_iso.py):
Sequential Chain: Plan → Build → Test → Review → Document → Ship
Failure Gates: Stop on any phase failure (especially tests)
Auto-Merge: Automatically approve and merge PR if all phases pass
Other Composite Workflows:
adw_plan_build_iso: Plan + Build only
adw_plan_build_test_iso: Plan + Build + Test
adw_plan_build_test_review_iso: Plan + Build + Test + Review
adw_plan_build_document_iso: Plan + Build + Document
Key Technical Features
Failure Recovery Mechanisms:
Test Resolution: Automatic test fixing with up to 4 retry attempts
Review Resolution: Auto-patch blocker issues with up to 3 retries
E2E Resolution: UI test fixing with screenshot analysis
Quality Gates:
Test Phase: Must pass unit tests to continue ZTE
Review Phase: Must resolve blocker issues before proceeding
Documentation Phase: Conditional generation based on actual changes
State Management:
Persistent State: agents/{adw_id}/adw_state.json tracks all workflow progress
Workflow Tracking: all_adws field tracks which workflows have executed
Port Management: Deterministic port allocation for parallel execution
Isolation Architecture:
Git Worktrees: Complete repository isolation in trees/{adw_id}/
Port Isolation: Each ADW gets unique backend/frontend ports
Environment Isolation: Separate .ports.env and dependencies per worktree