---
name: baotoq-projects
description: Repo inventory and activity for baotoq
---

## Repos

### baotoq/micro-commerce ★ DOMINANT (100% of sessions)

A personal showcase e-commerce microservices platform built over multiple milestones on .NET 10 + Next.js 14. Every session in this dataset touches this repo.

**What baotoq does here:** Designs and ships full milestones end-to-end — from DDD architecture to GitOps deployment — using his GSD workflow system to orchestrate Claude Code subagents in parallel waves.

**Tech stack:**
- Backend: .NET 10 / ASP.NET Core, MediatR, Entity Framework Core, MassTransit, .NET Aspire
- Frontend: Next.js 14 (App Router), TypeScript, shadcn/ui, Biome
- Auth: Keycloak OIDC (via NextAuth.js)
- Messaging: RabbitMQ (k8s) / Azure Service Bus (production)
- Database: PostgreSQL (StatefulSet with SealedSecrets)
- K8s: Kustomize base+overlay, ArgoCD app-of-apps, Kind cluster for local dev
- Observability: OpenTelemetry Collector, .NET Aspire Dashboard
- CI/CD: GitHub Actions (dotnet-test.yml, container-images.yml, release.yml), GHCR, 1Password

**Milestone history (inferred from session data):**
- **v1.0 MVP:** Full e-commerce flow — catalog, cart, checkout saga, orders, admin, 180 tests
- **v1.1 User Features:** Profiles, reviews, wishlists, cart merge, DDD audit
- **v2.0 DDD Foundation:** Vogen IDs, SmartEnum, FluentResults, Specifications, interceptors
- **v3.0 K8s & GitOps:** Docker images, Kustomize, ArgoCD, CI/CD pipeline, UI refresh (shadcn), OTEL
- **v3.1 (in-progress during dataset):** ArgoCD best practices (AppProject RBAC, sync waves, ignoreDifferences)

**Recurring themes:**
- Phase-based development with wave execution: plan → execute → verify → audit → complete
- Parallel subagent execution for independent plans (11 parallel UI plans in phase 25.1)
- Gap closure passes after milestones (`--gaps`, `--gaps-only` flags)
- Periodic deep audits of previous implementations (whole-repo code review with CRITICAL/WARNING/INFO/GOOD taxonomy)
- K8s security hardening: sealed secrets, security contexts, AppProject RBAC
- CI/CD maintenance: fixing .NET SDK version mismatches, stale project paths, caching gaps

**Planning structure:**
- `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, `.planning/PROJECT.md`
- `.planning/phases/NN-phase-name/NN-MM-PLAN.md` per plan
- `.planning/phases/NN-phase-name/NN-MM-SUMMARY.md` and `VERIFICATION.md` after execution
- `.planning/vX.Y-MILESTONE-AUDIT.md` after audit
- `.planning/milestones/` archive after completion

**GSD workflow system:**
- Located at `@/Users/baotoq/.claude/get-shit-done/workflows/*.md`
- References: `ui-brand.md`, `questioning.md`
- Templates: `project.md`, `requirements.md`, `milestone-archive.md`
- Commands: `plan-phase`, `execute-phase`, `audit-milestone`, `complete-milestone`, `new-milestone`, `plan-milestone-gaps`, `update`

**Paperclip integration:**
- Multi-agent platform with heartbeat execution model
- Typed sub-agents: Senior .NET Backend Engineer, Senior Next.js Frontend Engineer, CEO, Founding Engineer
- Skills injected at `/var/folders/.../paperclip-skills-*/`
- API: `PAPERCLIP_API_URL`, `PAPERCLIP_AGENT_ID`, `PAPERCLIP_RUN_ID`, `PAPERCLIP_TASK_ID`
