# Product Overview — CodeLens

## What We Are
CodeLens is a code review platform for mid-market engineering teams. We integrate with GitHub/GitLab and provide automated code analysis, review assignment, and compliance tracking.

## How It Works
1. PR opens in GitHub/GitLab → CodeLens webhook fires
2. Static analysis runs (security, style, complexity, test coverage)
3. AI-assisted review suggestions surface in-line
4. Review routing assigns to appropriate reviewers based on code ownership
5. Compliance dashboard tracks review SLAs, approval chains, audit trails

## Core Differentiator
We're the only code review tool that combines automated analysis + intelligent routing + compliance tracking in one product. Competitors do one of these. We do all three.

## Product Stats
- Languages supported: 14 (JS/TS, Python, Go, Java, Rust, C#, etc.)
- Average PR review time with CodeLens: 2.4 hours (industry avg: 8.2 hours)
- False positive rate on security findings: 4.1%
- Integrations: GitHub, GitLab, Bitbucket, Jira, Slack, Linear

## Pricing
- Team: $15/seat/month (up to 25 seats)
- Business: $29/seat/month (unlimited seats, SSO, audit logs)
- Enterprise: custom pricing (SOC2 reports, on-prem option, dedicated support)
- Average deal size: $4,000/year

## Tech Stack
- Frontend: React + TypeScript
- Backend: Go microservices
- Analysis engine: Tree-sitter + custom AST analyzers
- AI layer: Claude API for review suggestions
- Infrastructure: AWS ECS, PostgreSQL, Redis
