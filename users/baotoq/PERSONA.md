---
name: baotoq-persona
description: Background, inferred role, domain expertise, and attitude toward the agent for baotoq
---

## Background (inferred)

baotoq is a **full-stack/platform engineer** (inferred) based in Vietnam (Asia/Saigon timezone confirmed from task output: `"You're out of extra usage · resets 3am (Asia/Saigon)"`). He works on macOS (`/Users/baotoq/`, `/var/folders/b7/gw3fn69x5l756sbkj8s5v7j40000gn/T/`). His GitHub username is `baotoq` and his primary project is a personal showcase/portfolio microservices platform.

## Seniority signals (inferred)

- Designed and ships a multi-milestone product with DDD, CQRS, outbox patterns, sealed secrets, ArgoCD GitOps — far beyond junior scope
- Chose chiseled .NET base images, MassTransit + EF Core outbox, Vogen strongly-typed IDs, FluentResults — deliberate architectural choices
- Built his own AI-agent workflow orchestration system (GSD + Paperclip) on top of Claude Code
- Knows the difference between sync waves, AppProject RBAC, and `ignoreDifferences` in ArgoCD
- Reviews CI/CD at the `.NET SDK version mismatch` level, not at a surface level

**Estimated seniority:** Senior engineer (4–8 years) who has worked on production .NET microservices and is now deliberately adding cloud-native DevOps skills (inferred).

## Domain expertise

- **Primary:** .NET 10 / ASP.NET Core (C#), microservices architecture, DDD patterns
- **Strong:** Next.js 14+ / TypeScript, shadcn/ui, React Server Components
- **Growing:** Kubernetes, ArgoCD GitOps, Kustomize overlays, SealedSecrets
- **Operational:** GitHub Actions CI/CD, Docker multi-stage builds, GHCR, multi-arch images
- **Data/Messaging:** PostgreSQL, RabbitMQ, MassTransit, Azure Service Bus, Entity Framework Core
- **Auth/Observability:** Keycloak OIDC, .NET Aspire, OpenTelemetry, Aspire Dashboard

## Role

Solo engineer on a personal showcase project (`baotoq/micro-commerce`). Acts simultaneously as CEO, architect, and IC — he uses his GSD system to simulate having a small engineering team by spawning typed sub-agents (Senior .NET Backend Engineer, Senior Next.js Frontend Engineer, Founding Engineer). He is both the orchestrator and the product owner.

## Attitude toward the agent

**Trusting, but corrects immediately when misrouted.** He accepts agent output ~82% of the time without pushback. When he does push back, corrections are blunt and minimal: he does not explain why the agent was wrong — he just restates what he wants or pastes the correct content directly. He does not apologize for interrupting, thank the agent, or soften corrections.

He treats the agent as an executor of his workflow system, not as a collaborator to reason with. He is comfortable giving the agent very little context (a phase number, a flag) and expecting it to load its own context files. When the agent asks clarifying questions he doesn't want to answer, he either pastes the answer content directly or issues a new command.

## Persona annotations

- 57.9% "Vague Requester": slash commands and short XML stubs with no explicit requirement text
- 36.8% "Expert Nitpicker": when he reviews output, he applies structured CRITICAL/WARNING/INFO/GOOD taxonomy and catches .NET SDK mismatches, ArgoCD RBAC gaps, and secrets in public repos
