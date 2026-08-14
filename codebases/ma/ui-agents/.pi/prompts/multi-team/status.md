---
description: Show product health overview
argument-hint: <brand> <product>
---

# Purpose
Read-only status report for a product — no generation, no validation.

## Variables
BRAND: $1
PRODUCT: $2

## Instructions
- Read `trees.yaml` only — no team delegation needed
- Display tree counts, branch counts, status breakdown
- Use status icons: ✓ validated, ● generating/validating, ✗ failed, ○ draft

## Workflow
1. Read `apps/infinite-ui/src/brands/$BRAND/products/$PRODUCT/trees.yaml`
2. Parse and display:
   - Brand name, total tree count, total branch count
   - Per-tree: name, branch count
   - Per-branch: slug, status icon, created date
   - Summary counts by status
3. No teams needed — this is a read-only operation

## Report
Brand: $BRAND
Trees: N | Branches: N
[Per-tree breakdown]
Summary: N validated | N generating | N failed | N draft
