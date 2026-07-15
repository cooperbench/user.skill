> AGENT

Let me first identify what Sam's merge brought into develop, then review the content thoroughly.

> TOOL

tool_use Bash
id: toolu_015VRFLuTgfE12jyYyGCjLqh
```json
{
  "command": "git log --oneline --since=\"2025-02-01\" --all | head -30",
  "description": "View recent commits to find Sam's merge"
}
```

> TOOL

tool_use Bash
id: toolu_01BznPJwPt4znhR7jaxnrS2f
```json
{
  "command": "git log --oneline develop..HEAD 2>/dev/null; git log --oneline main..develop 2>/dev/null | head -20",
  "description": "Check what's in develop but not main"
}
```

> TOOL

tool_result
id: toolu_015VRFLuTgfE12jyYyGCjLqh
```
8c03269 Merge pull request #193 from konecta-ix-platform/feature/application-docs
731cf2f application docs
437d7f0 Merge pull request #181 from konecta-ix-platform/feature/cloud-sql-techdocs
c8b1112 Merge pull request #192 from konecta-ix-platform/feature/workload-secrets-pipeline
0404dd8 docs: add workload secrets pipeline guide
ce0284c Merge pull request #191 from konecta-ix-platform/develop
694214a Merge pull request #190 from konecta-ix-platform/feature/gcp-project-env-docs
8095d59 docs: add GOOGLE_CLOUD_PROJECT requirement for workloads
fc61c3a fix: switch TechDocs workflow to manual dispatch
a5e9203 Merge pull request #180 from konecta-ix-platform/develop
d937b61 Merge pull request #179 from konecta-ix-platform/feature/cloud-sql-techdocs
3263b2d feat: add Cloud SQL and data services TechDocs for Backstage
f037b19 Merge pull request #178 from konecta-ix-platform/develop
2dee558 Merge pull request #177 from konecta-ix-platform/feature/deployment-docs-pipelines-argowf
9701b8d docs: rewrite deployment guide and CI/CD runbook for pipelines and Argo Workflows
104a31b Merge pull request #176 from konecta-ix-platform/develop
f7fcd9a Merge pull request #175 from konecta-ix-platform/feature/app-migration-docs-update
ce39813 feat: update brand palette to Konecta guidelines and add GitHub Orgs navbar dropdown
f587acd Merge pull request #174 from konecta-ix-platform/develop
fbbd52d Merge pull request #173 from konecta-ix-platform/feature/app-migration-docs-update
1b2708a docs: add branching-strategy to sidebar and update logos to PNG
845406f Merge pull request #172 from konecta-ix-platform/develop
2c85ec9 Merge pull request #171 from konecta-ix-platform/feature/app-migration-docs-update
964eea6 Merge remote-tracking branch 'origin/develop' into feature/app-migration-docs-update
dff755b Merge pull request #170 from konecta-ix-platform/feature/app-migration-docs-update
3ce8948 docs: org […]

> TOOL

tool_result
id: toolu_01BznPJwPt4znhR7jaxnrS2f
```
8c03269 Merge pull request #193 from konecta-ix-platform/feature/application-docs
731cf2f application docs
437d7f0 Merge pull request #181 from konecta-ix-platform/feature/cloud-sql-techdocs
c8b1112 Merge pull request #192 from konecta-ix-platform/feature/workload-secrets-pipeline
0404dd8 docs: add workload secrets pipeline guide
ce0284c Merge pull request #191 from konecta-ix-platform/develop
694214a Merge pull request #190 from konecta-ix-platform/feature/gcp-project-env-docs
8095d59 docs: add GOOGLE_CLOUD_PROJECT requirement for workloads
fc61c3a fix: switch TechDocs workflow to manual dispatch
a5e9203 Merge pull request #180 from konecta-ix-platform/develop
d937b61 Merge pull request #179 from konecta-ix-platform/feature/cloud-sql-techdocs
3263b2d feat: add Cloud SQL and data services TechDocs for Backstage
f037b19 Merge pull request #178 from konecta-ix-platform/develop
2dee558 Merge pull request #177 from konecta-ix-platform/feature/deployment-docs-pipelines-argowf
9701b8d docs: rewrite deployment guide and CI/CD runbook for pipelines and Argo Workflows
104a31b Merge pull request #176 from konecta-ix-platform/develop
f7fcd9a Merge pull request #175 from konecta-ix-platform/feature/app-migration-docs-update
ce39813 feat: update brand palette to Konecta guidelines and add GitHub Orgs navbar dropdown
f587acd Merge pull request #174 from konecta-ix-platform/develop
fbbd52d Merge pull request #173 from konecta-ix-platform/feature/app-migration-docs-update
```

> TOOL

tool_use Bash
id: toolu_01Me1Wa44ZemM62F472ohfPg
```json
{
  "command": "git diff --name-status main..develop",
  "description": "List all files changed between main and develop"
}
```

> TOOL

tool_result
id: toolu_01Me1Wa44ZemM62F472ohfPg
```
A	.github/workflows/techdocs-publish.yml
M	CLAUDE.md
M	CLAUDE_NAVIGATION.md
M	MISTAKES_ARCHIVE.md
M	VALIDATION_METRICS.md
A	backstage/all.yaml
A	backstage/cloud-sql/docs/iam-auth.md
A	backstage/cloud-sql/docs/index.md
A	backstage/cloud-sql/docs/jobs.md
A	backstage/cloud-sql/docs/other-services.md
A	backstage/cloud-sql/docs/proxy.md
A	backstage/cloud-sql/mkdocs.yml
A	backstage/domains.yaml
A	backstage/groups.yaml
A	backstage/resources.yaml
A	backstage/systems.yaml
M	docs/adr/adr-003-backstage.md
M	docs/app-migration/appendix-reference.md
M	docs/app-migration/backstage-onboarding.md
M	docs/app-migration/cicd-pipeline.md
M	docs/app-migration/current-state.md
M	docs/app-migration/gitops-promotion.md
M	docs/app-migration/index.md
M	docs/app-migration/ingress-networking.md
M	docs/app-migration/kubernetes-helm.md
M	docs/app-migration/migration-phases.md
M	docs/app-migration/observability.md
M	docs/app-migration/operations-risks.md
M	docs/app-migration/security.md
M	docs/app-migration/service-guides/iq-portal.md
M	docs/app-migration/target-architecture.md
A	docs/applications/application-architecture.md
A	docs/applications/developer-guidelines.md
A	docs/applications/index.md
A	docs/applications/local-development-setup.md
R099	docs/developer-guide/technology-specs.md	docs/applications/technology-specs.md
M	docs/architecture/infrastructure.md
A	docs/developer-guide/branching-strategy.md
M	docs/developer-guide/building-use-cases.md
M	docs/developer-guide/claude-code.md
M	docs/developer-guide/deploy-first-service.md
A	docs/developer-guide/development-toolkit.md
M	docs/developer-guide/index.md
M	docs/developer-guide/platform-overview.md
M	docs/developer-guide/secrets-management.md
M	docs/developer-guide/testing.md
M	docs/developer-guide/use-case-examples.md
A	docs/developer-guide/workload-secrets-pipeline.md
M	docs/getting-started/onboarding.md
M	docs/infrastructure-ops/cicd-runbook.md
M	docs/infrastructure-ops/deployment-guide.md
M	docs/infrastructure-ops/dns-architecture.md
A	docs/infrastructure-ops/ip-allocation-schema.md
M	docs/reference/creating-new-repository.md
M	docs/reference/quick-reference.md
M	docs/strategy/services-catalog.md
M	docusaurus.config.js
M	package-lock.json
M	package.json
M	sidebars.js
M	src/css/custom.css
M	src/pages/index.js
A	static/img/kix-platform-ai-architecture.jpg
A	static/img/kix-platform-local-architecture.jpg
A	static/img/logo-dark.png
D	static/img/logo-dark.svg
A	static/img/logo.png
D	static/img/logo.svg
```

> TOOL

tool_use Bash
id: toolu_01Gy2SdFoXWPBjz5orxgAxMe
```json
{
  "command": "git log --oneline --author-name-map=/dev/null 731cf2f -1 --format=\"%an - %s\"",
  "description": "Check author of the application docs commit"
}
```

> TOOL

tool_use Bash
id: toolu_01QrnK6b8sRh51kcTgYxCnB6
```json
{
  "command": "git diff --name-status 731cf2f^..731cf2f",
  "description": "Files changed in Sam's application docs commit"
}
```

> TOOL

tool_result ERROR
id: toolu_01Gy2SdFoXWPBjz5orxgAxMe
```
Exit code 128
fatal: unrecognized argument: --author-name-map=/dev/null

fatal: unrecognized argument: --author-name-map=/dev/null
```

> TOOL

tool_result
id: toolu_01QrnK6b8sRh51kcTgYxCnB6
```
A	docs/applications/application-architecture.md
A	docs/applications/developer-guidelines.md
A	docs/applications/index.md
A	docs/applications/local-development-setup.md
R100	docs/developer-guide/technology-specs.md	docs/applications/technology-specs.md
A	docs/developer-guide/development-toolkit.md
M	package-lock.json
M	package.json
M	sidebars.js
M	src/pages/index.js
A	static/img/kix-platform-ai-architecture.jpg
A	static/img/kix-platform-local-architecture.jpg
```

> AGENT

Now let me read all the new documents from Sam's merge, plus the modified sidebar and homepage.

> TOOL

tool_use Read
id: toolu_012yXhuzHCK1aCnBprQjjxpk
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/index.md"
}
```

> TOOL

tool_use Read
id: toolu_01K55iphbXErMKzZqqiLCT9c
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/application-architecture.md"
}
```

> TOOL

tool_use Read
id: toolu_01X4QX4SuCc5jB7TCndo6xUm
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/developer-guidelines.md"
}
```

> TOOL

tool_use Read
id: toolu_01GGvX7aXLzJhxyuQdy6vCpD
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/local-development-setup.md"
}
```

> TOOL

tool_use Read
id: toolu_017JsTd78uoyNodzBt1wZCre
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/technology-specs.md"
}
```

> TOOL

tool_use Read
id: toolu_015wdSKsSGfRC45qHxSWKicD
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/development-toolkit.md"
}
```

> TOOL

tool_result
id: toolu_012yXhuzHCK1aCnBprQjjxpk
```
     1→---
     2→title: "Applications"
     3→sidebar_label: "Overview"
     4→sidebar_position: 1
     5→description: "Application development standards, architecture, and tooling for the KIX Platform"
     6→---
     7→
     8→# Applications
     9→
    10→The KIX Platform for AI Solutions is a modular architecture designed to build, deploy and operate AI-powered applications at Konecta. It connects front-end applications, agentic workflows, language models, tool servers and observability through well-defined integration points — so AI developers can focus on creating the building blocks for their use case while the platform handles infrastructure, routing, authentication and governance.
    11→
    12→## What Developers Build
    13→
    14→Developers contribute one or more of the following components:
    15→
    16→- **Python tools** — Custom code logic consumed by AI agents
    17→- **Agentic flows** — CrewAI Crews and Flows that orchestrate multi-step AI tasks
    18→- **MCP Servers** — Expose APIs and data sources to LLMs as callable tools
    19→- **Custom UI** — A dedicated front-end, or use **Konecta IQ** as a ready-made interface to interact with agents
    20→
    21→Each component is developed and tested locally against an environment that mirrors production, then submitted for packaging and deployment through the standard CI/CD pipeline.
    22→
    23→## In This Section
    24→
    25→| Page | Description |
    26→|---|---|
    27→| [Application Architecture](./application-architecture) […]

> TOOL

tool_result
id: toolu_01X4QX4SuCc5jB7TCndo6xUm
```
     1→---
     2→title: "Developer Guidelines"
     3→sidebar_label: "Developer Guidelines"
     4→sidebar_position: 2
     5→description: "Development standards and best practices for KIX Platform applications"
     6→draft: true
     7→---
     8→
     9→# Developer Guidelines
    10→
    11→## Definition of Done
    12→
    13→The code produced must meet the specifications. If the specifications list several cases, all these cases must be covered by the code and have been tested.
    14→
    15→**Always think about the users and the product.**
    16→
    17→Even if the task does not explicitly mention every situation, take five minutes to consider use cases not specified: what if the user is not connected? What if the user doesn't have permissions? Empty state? etc.
    18→
    19→---
    20→
    21→## General Code Guidelines
    22→
    23→### Readability
    24→
    25→**We should be able to read the code and understand what it does with minimum comments.**
    26→
    27→- All variables are named in English and are singular noun if only one value, plural names if a list
    28→- All function names are in English and start with a verb describing what the function does
    29→- Settings should be in a config file or env file; if you introduce env variables, make sure to reflect that in the `.env.example`
    30→
    31→### Respect […]

> TOOL

tool_result
id: toolu_01K55iphbXErMKzZqqiLCT9c
```
     1→---
     2→title: "Application Architecture"
     3→sidebar_label: "Application Architecture"
     4→sidebar_position: 4
     5→description: "Architecture patterns and standards for KIX Platform applications"
     6→---
     7→
     8→# Application Architecture
     9→
    10→## Overview
    11→
    12→The KIX Platform for AI Solutions is a modular architecture designed to build, deploy and operate AI-powered applications at Konecta. It provides a unified foundation where front-end applications, agentic workflows, language models and observability all connect through well-defined integration points.
    13→
    14→![KIX Platform for AI Solutions](/img/kix-platform-ai-architecture.jpg)
    15→
    16→## Architecture Components
    17→
    18→### Application Layer
    19→
    20→At the top of the architecture sit the consumer-facing applications:
    21→
    22→- **Konecta IQ (Showcase Environment)** — A demonstration environment that showcases the platform's AI-state-of-the-art capabilities and serves as an in-consultation tool within the platform.
    23→- **Use Cases** — Production AI solutions built on the platform, including Portfolio analysis, Competitor Analysis, Market Intelligence and Email Responder.
    24→
    25→Both application types connect downward into the platform's core services.
    26→
    27→### LiteLLM (AI Gateway)
    28→
    29→LiteLLM acts as the central AI Gateway, providing a unified API layer that abstracts away the specifics of individual model providers. Applications and agents make requests through LiteLLM, which routes them to the appropriate model backend. This decouples application code from […]

> TOOL

tool_result
id: toolu_015wdSKsSGfRC45qHxSWKicD
```
     1→---
     2→title: "Development Toolkit"
     3→sidebar_label: "Development Toolkit"
     4→sidebar_position: 3
     5→description: "Tools and utilities for developing KIX Platform applications"
     6→---
     7→
     8→# Development Toolkit
     9→
    10→## AI
    11→
    12→### Claude Code Plugin
    13→
    14→*Coming soon.*
    15→
    16→### Claude Code Setup Script
    17→
    18→*Coming soon.*
    19→
    20→---
    21→
    22→## Boilerplates
    23→
    24→### MCP Server
    25→
    26→*Coming soon.*
    27→
    28→### CrewAI Flow
    29→
    30→*Coming soon.*
    31→
    32→### CrewAI Crew
    33→
    34→*Coming soon.*
    35→
    36→### NuxtJS / NuxtUI Frontend
    37→
    38→*Coming soon.*
    39→
    40→---
    41→
    42→## DevOps
    43→
    44→### Docker Recommendations
    45→
    46→*Coming soon.*
    47→
    48→### Secrets and Env Management Recommendations
    49→
    50→*Coming soon.*
    51→
    52→---
    53→
    54→## Security
    55→
    56→### Security Checklist
    57→
    58→*Coming soon.*
    59→
    60→---
    61→
    62→## Git
    63→
    64→### Branching Conventions
    65→
    66→*Coming soon.*
    67→
    68→### Branch Protection
    69→
    70→*Coming soon.*
    71→
    72→---
    73→
    74→## Observability
    75→
    76→### OpenTelemetry
    77→
    78→*Coming soon.*
    79→
```

> TOOL

tool_result
id: toolu_017JsTd78uoyNodzBt1wZCre
```
     1→---
     2→title: "Technology Specifications"
     3→sidebar_label: "Technology Specs"
     4→sidebar_position: 7
     5→description: "Detailed specifications for each platform component including CrewAI, LiteLLM, Kong, databases, and more"
     6→---
     7→
     8→# Technology Specifications
     9→
    10→## CrewAI
    11→
    12→**Purpose:** Multi-agent orchestration for autonomous task execution
    13→
    14→**What It Does:**
    15→- Defines agents with roles, goals, and tools
    16→- Orchestrates tasks across multiple agents
    17→- Manages agent collaboration and handoffs
    18→- Integrates with LLM gateway for model access
    19→
    20→**Constraints:**
    21→- All LLM calls must use platform gateway (no direct API calls)
    22→- Maximum execution time configurable per agent
    23→- Agent state must be externalized for fault tolerance
    24→
    25→**Example Crew Structure:**
    26→```
    27→End-User Self-Healing Crew
    28→├── Triage Agent
    29→│   └── Classifies issue type, urgency, complexity
    30→├── Diagnostic Agent
    31→│   └── Runs diagnostic checks via Nexthink MCP
    32→├── Resolution Agent
    33→│   └── Executes fixes via ServiceNow/AD MCP
    34→├── Communication Agent
    35→│   └── Updates user on progress
    36→└── Escalation Agent
    37→    └── Hands off to human with full context
    38→```
    39→
    40→## ElevenLabs
    41→
    42→**Purpose:** Voice synthesis and conversational AI (primary voice runtime)
    43→
    44→**What It Does:**
    45→- Text-to-speech synthesis
    46→- Real-time conversational AI
    47→- Speech-to-Text
    48→- Multi-language support
    49→
    50→**Constraints:**
    51→- Voice calls […]

> TOOL

tool_result
id: toolu_01GGvX7aXLzJhxyuQdy6vCpD
```
     1→---
     2→title: "Local Development Setup"
     3→sidebar_label: "Local Development Setup"
     4→sidebar_position: 5
     5→description: "Setting up your local environment for KIX Platform application development"
     6→---
     7→
     8→# Local Development Setup
     9→
    10→## What AI Developers Build
    11→
    12→AI developers are expected to use the platform and focus on creating the building blocks required for their use case. The platform handles infrastructure, routing, authentication and observability — developers provide the logic. Typical contributions include:
    13→
    14→- **Python tools** — Custom code logic consumed by agents
    15→- **Agentic flows** — CrewAI Crews and Flows that orchestrate multi-step AI tasks
    16→- **MCP Servers** — Make APIs and data sources accessible to LLMs as tools
    17→- **Custom UI** — A dedicated front-end for a specific use case, or simply use **Konecta IQ** as a readily available UI to interact with agents without building any interface
    18→
    19→## Production Architecture Recap
    20→
    21→The KIX Platform for AI Solutions runs a modular architecture in production where applications connect to an AI gateway (LiteLLM), an agentic orchestration layer (CrewAI), MCP Servers for tool capabilities and a full observability stack. For a detailed breakdown of each component and how they interact, see the [Application Architecture](./application-architecture) page. […]

> AGENT

Now let me check the sidebar config and existing content that may overlap.

> TOOL

tool_use Read
id: toolu_01GaFyLhA5qzXET7RbbATPJv
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/sidebars.js"
}
```

> TOOL

tool_use Read
id: toolu_017ny4QXy9kQCcEnGv3TbRuH
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/index.md"
}
```

> TOOL

tool_use Read
id: toolu_01EukGY9DkH1kFfPDCZGSyCA
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/platform-overview.md"
}
```

> TOOL

tool_use Read
id: toolu_01Tx9pkhuNVfqpuFGCaq33sJ
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/deploy-first-service.md"
}
```

> TOOL

tool_result
id: toolu_01GaFyLhA5qzXET7RbbATPJv
```
     1→/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
     2→const sidebars = {
     3→  docs: [
     4→    {
     5→      type: 'category',
     6→      label: 'Getting Started',
     7→      collapsed: false,
     8→      items: [
     9→        'getting-started/index',
    10→        'getting-started/prerequisites',
    11→        'getting-started/onboarding',
    12→      ],
    13→    },
    14→    {
    15→      type: 'category',
    16→      label: 'Application Migration',
    17→      items: [
    18→        'app-migration/index',
    19→        'app-migration/current-state',
    20→        'app-migration/target-architecture',
    21→        'app-migration/migration-phases',
    22→        'app-migration/kubernetes-helm',
    23→        'app-migration/ingress-networking',
    24→        'app-migration/docker-security',
    25→        'app-migration/cicd-pipeline',
    26→        'app-migration/gitops-promotion',
    27→        'app-migration/backstage-onboarding',
    28→        'app-migration/security',
    29→        'app-migration/observability',
    30→        'app-migration/operations-risks',
    31→        'app-migration/appendix-reference',
    32→        {
    33→          type: 'category',
    34→          label: 'Service Guides',
    35→          items: [
    36→            'app-migration/service-guides/index',
    37→            'app-migration/service-guides/iq-portal',
    38→          ],
    39→        },
    40→      ],
    41→    },
    42→    {
    43→      type: 'category',
    44→      label: 'Applications',
    45→      items: [
    46→        'applications/index',
    47→        // 'applications/developer-guidelines',
    48→        'applications/application-architecture',
    49→        'applications/technology-specs',
    50→        'applications/local-development-setup',
    51→      ],
    52→    },
    53→    {
    54→      type: 'category',
    55→      label: 'Developer Guide',
    56→      items: [
    57→        'developer-guide/index',
    58→        'developer-guide/platform-overview',
    59→        'developer-guide/deploy-first-service',
    60→        'developer-guide/branching-strategy',
    61→        'developer-guide/building-use-cases',
    62→        'developer-guide/use-case-examples',
    63→        'developer-guide/testing',
    64→        'developer-guide/secrets-management',
    65→        'developer-guide/development-toolkit',
    66→        'developer-guide/claude-code',
    67→      ],
    68→    },
    69→    {
    70→      type: 'category',
    71→      label: 'Platform Architecture',
    72→      items: [
    73→        'architecture/index',
    74→        'architecture/control-plane',
    75→        'architecture/platform-layers',
    76→        'architecture/infrastructure',
    77→        'architecture/gke-cluster',
    78→        'architecture/namespaces',
    79→        'architecture/network-flows',
    80→        'architecture/decision-records',
    81→      ],
    82→    },
    83→    { […]

> TOOL

tool_result
id: toolu_01EukGY9DkH1kFfPDCZGSyCA
```
     1→---
     2→title: "Platform Overview"
     3→sidebar_label: "Platform Overview"
     4→sidebar_position: 2
     5→description: "What the KIX Platform provides to use case developers and what developers are responsible for building"
     6→---
     7→
     8→# Platform Overview
     9→
    10→## What the Platform Provides
    11→
    12→When a use case is onboarded, the platform automatically provisions:
    13→
    14→| Resource | Description |
    15→|----------|-------------|
    16→| **Kubernetes Namespace** | Isolated environment for workloads |
    17→| **PostgreSQL Database** | Dedicated database with credentials |
    18→| **Redis Key Prefix** | Shared cache with isolated keyspace |
    19→| **GCS Bucket** | Object storage for documents and artifacts |
    20→| **Pub/Sub Topic** | Event bus for async messaging |
    21→| **Kong Routes** | API endpoints at `/api/v1/{use-case}/*` |
    22→| **Secrets Folder** | Secret Manager path for credentials |
    23→| **Service Account** | GCP identity with least-privilege permissions |
    24→| **Observability** | Pre-configured dashboard, logs, and traces |
    25→| **Identity** | Identity services abstracting credential handling |
    26→| **Security** | Security monitoring, WAF, and firewall services |
    27→| **Service Catalogue** | Backstage portal for discovering available services |
    28→
    29→### Service Discovery via Backstage
    30→
    31→Use case developers discover available platform services through **Backstage**, the internal service catalogue:
    32→
    33→| What […]

> TOOL

tool_result
id: toolu_017ny4QXy9kQCcEnGv3TbRuH
```
     1→---
     2→title: "Developer Guide"
     3→sidebar_label: "Overview"
     4→sidebar_position: 1
     5→description: "Guide for use case developers building AI agents and services on the KIX Platform"
     6→---
     7→
     8→# Developer Guide
     9→
    10→This guide explains how to build services on the KIX Platform. It covers what the platform provides, how to build use cases, service patterns, and technology specifications.
    11→
    12→**Audience:** Use case developers building on KIX
    13→
    14→## Architecture Layers
    15→
    16→| Layer | Purpose | Components |
    17→|-------|---------|------------|
    18→| **Northbound** | Service exposure to consumers | Kong API Gateway, LiteLLM MCP Gateway, Admin UI |
    19→| **Capability** | Business logic and orchestration | Control Plane, Agents, Voice, Messaging, Knowledge |
    20→| **Southbound** | Infrastructure (abstracted) | GCP services, databases, storage, events |
    21→
    22→## Service Consumption Model
    23→
    24→Consumers access platform capabilities through three methods:
    25→
    26→| Method | Consumer Type | Authentication |
    27→|--------|---------------|----------------|
    28→| REST API (Kong) | External systems, applications | API Key or JWT |
    29→| MCP Tools (LiteLLM) | AI agents | Service account |
    30→| Admin UI | Internal users | OIDC |
    31→
    32→All requests are authenticated, routed through the appropriate gateway, and executed by the capability layer. Infrastructure is […]

> TOOL

tool_result
id: toolu_01Tx9pkhuNVfqpuFGCaq33sJ
```
     1→---
     2→title: Deploy Your First Service
     3→sidebar_label: Deploy First Service
     4→sidebar_position: 3
     5→description: Step-by-step tutorial for deploying your first service on KIX Platform
     6→---
     7→
     8→# Deploy Your First Service
     9→
    10→## Overview
    11→
    12→This hands-on tutorial walks you through deploying a complete service on the KIX Platform, from code to production. You'll build a simple Python FastAPI service with health checks, secrets management, and proper observability.
    13→
    14→**What You'll Build:**
    15→- Python FastAPI REST API service
    16→- Terraform-managed GCP resources (secrets, IAM)
    17→- Helm chart for Kubernetes deployment
    18→- ArgoCD continuous deployment
    19→- Integration with Kong API Gateway
    20→
    21→**Time Required:** 2-3 hours
    22→
    23→**Prerequisites:**
    24→- Completed [Onboarding](/docs/getting-started/onboarding)
    25→- Access to `konecta-ix-workloads` GitHub organization
    26→- Local tools installed: `terraform`, `kubectl`, `helm`, `gh` CLI
    27→- GCP project access (provided during onboarding)
    28→
    29→---
    30→
    31→## Step 1: Create Repository
    32→
    33→### 1.1 Create from Template
    34→
    35→```bash
    36→# Clone the workload template
    37→gh repo create konecta-ix-workloads/kix-usecase-hello-world \
    38→  --template konecta-ix-workloads/kix-usecase-template \
    39→  --private \
    40→  --clone
    41→
    42→cd kix-usecase-hello-world
    43→```
    44→
    45→### 1.2 Initialize Git Flow
    46→
    47→```bash
    48→# Create develop branch
    49→git checkout -b develop
    50→git push -u origin develop
    51→
    52→# Set default branch […]

> TOOL

tool_use Read
id: toolu_015kJzvozuokw7UJZikeGJf3
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/building-use-cases.md"
}
```

> TOOL

tool_use Read
id: toolu_01NN8qfti97uE48kW8jccTPt
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/app-migration/service-guides/index.md"
}
```

> TOOL

tool_use Read
id: toolu_01GvCeJcQvZzGnApSHUZ1UuA
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/src/pages/index.js"
}
```

> TOOL

tool_result
id: toolu_015kJzvozuokw7UJZikeGJf3
```
     1→---
     2→title: "Building Use Cases"
     3→sidebar_label: "Building Use Cases"
     4→sidebar_position: 5
     5→description: "Development flow, service patterns, and deployment guide for building use cases on the KIX Platform"
     6→---
     7→
     8→# Building Use Cases
     9→
    10→## Development Flow
    11→
    12→1. Define capability schema (inputs, outputs, SLA)
    13→2. Register capability in Schema Registry
    14→3. Implement agent or service
    15→4. Configure API routes
    16→5. Deploy to development environment via ArgoCD GitOps
    17→6. Test via API and MCP
    18→7. Promote through QA to production (ArgoCD syncs from Git)
    19→
    20→### GitOps Deployment via ArgoCD
    21→
    22→All deployments follow a GitOps workflow managed by ArgoCD running on the shared platform cluster:
    23→
    24→| Step | Action | Tool |
    25→|------|--------|------|
    26→| 1 | Push code to repository | Git |
    27→| 2 | CI pipeline builds container image | GitHub Actions |
    28→| 3 | Image pushed to Artifact Registry (`kd-ix-eur-shr-artifacts`) | Docker/Buildkit |
    29→| 4 | ArgoCD Image Updater detects new image | Automatic |
    30→| 5 | ArgoCD syncs manifests to target cluster | Automatic |
    31→| 6 | Verify deployment status | ArgoCD UI or CLI |
    32→
    33→**ArgoCD UI:** `https://argocd.ix.konecta-digital.com` (Google OIDC login)
    34→
    35→**Key concepts:**
    36→- […]

> TOOL

tool_result
id: toolu_01GvCeJcQvZzGnApSHUZ1UuA
```
     1→import clsx from 'clsx';
     2→import Link from '@docusaurus/Link';
     3→import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
     4→import Layout from '@theme/Layout';
     5→import styles from './index.module.css';
     6→
     7→const features = [
     8→  {
     9→    title: 'Getting Started',
    10→    link: '/docs/getting-started',
    11→    description: 'Set up your environment, understand prerequisites, and deploy your first infrastructure.',
    12→  },
    13→  {
    14→    title: 'Application Development',
    15→    link: '/docs/applications',
    16→    description: 'Build AI agents on the platform using CrewAI, LiteLLM, and MCP tools.',
    17→  },
    18→  {
    19→    title: 'Architecture',
    20→    link: '/docs/architecture',
    21→    description: 'Control Plane, platform layers, GKE clusters, network flows, and decision records.',
    22→  },
    23→  {
    24→    title: 'Infrastructure Ops',
    25→    link: '/docs/infrastructure-ops',
    26→    description: 'Terraform structure, deployment guides, CI/CD runbooks, and DNS migration.',
    27→  },
    28→  {
    29→    title: 'Security & Compliance',
    30→    link: '/docs/security',
    31→    description: 'Security architecture, GDPR, EU AI Act, governance, and risk management.',
    32→  },
    33→  {
    34→    title: 'Strategy & Roadmap',
    35→    link: '/docs/strategy',
    36→    description: 'Platform vision, services catalog, operating model, metrics, and roadmap.',
    37→  },
    38→];
    39→
    40→const audiences = [
    41→  {
    42→    title: 'Platform Engineers',
    43→    links: [
    44→      { label: 'Onboarding Guide', to: '/docs/getting-started/onboarding' },
    45→      { label: 'Terraform Structure', to: '/docs/infrastructure-ops/terraform-structure' […]

> TOOL

tool_result
id: toolu_01NN8qfti97uE48kW8jccTPt
```
     1→---
     2→title: Service Migration Guides
     3→sidebar_label: Service Guides
     4→sidebar_position: 1
     5→description: Detailed migration guides for specific services
     6→---
     7→
     8→# Service Migration Guides
     9→
    10→This section contains detailed, step-by-step migration guides for specific services. Each guide covers the complete migration process from Cloud Run to kix-infrastructure.
    11→
    12→## Available Guides
    13→
    14→| Service | Type | Priority | Guide |
    15→|---------|------|----------|-------|
    16→| IQ Portal | Multi-tier (Nuxt + Express + Cloud SQL) | P0 (Pilot) | [IQ Portal Migration Guide](iq-portal) |
    17→
    18→## Upcoming Guides
    19→
    20→The following guides will be added as migrations progress:
    21→
    22→| Service | Type | Priority | Status |
    23→|---------|------|----------|--------|
    24→| MCP Gateway | Python FastMCP | P1 | Pending |
    25→| HR Fraud | Multi-tier (Nuxt + FastAPI + Cloud SQL) | P3 | Pending |
    26→| RAG Ingestion | Python Pipeline | P4 | Pending |
    27→
    28→## Guide Structure
    29→
    30→Each service guide follows a consistent structure:
    31→
    32→1. **Current State Assessment** — Existing architecture and dependencies
    33→2. **Target State** — Kubernetes architecture and configuration
    34→3. **Pre-requisites** — Required access and platform components
    35→4. **Step-by-Step Migration** — Detailed migration instructions:
    36→   - Repository creation
    37→   - Application […]

> AGENT

Now let me launch the technical writer review.

> TOOL

tool_use Task
id: toolu_018No1GeeEFawaJiKoZzA8qk
```json
{
  "subagent_type": "technical-writer",
  "description": "Review Sam's new application docs",
  "prompt": "You are reviewing new documentation that was merged into a Docusaurus-based platform docs site. The merge added a new \"Applications\" sidebar section and a \"Development Toolkit\" page. Your job is to do a thorough technical writing review and identify issues with content overlap, organization, clarity, completeness, and consistency.\n\n## New files added by Sam's merge:\n\n### 1. docs/applications/index.md (Overview page for new \"Applications\" section)\n- Introduces the KIX Platform for AI Solutions\n- Lists what developers build: Python tools, Agentic flows, MCP Servers, Custom UI\n- Links to Application Architecture and Local Development Setup\n- Cross-links to Development Toolkit in Developer Guide\n\n### 2. docs/applications/application-architecture.md\n- Overview of the AI platform architecture (LiteLLM, CrewAI, MCP, Models, Observability)\n- \"How It All Connects\" flow\n- Related docs links (some may be broken: /docs/architecture, /docs/services/litellm-gateway)\n\n### 3. docs/applications/developer-guidelines.md (marked draft: true, commented out of sidebar)\n- General coding guidelines: readability, respect existing code, right amount of code\n- Document and monitor, automate, commit and deploy sections\n- Generic software development advice, not KIX-specific\n\n### 4. docs/applications/local-development-setup.md\n- How to set up local dev: Konecta IQ, LiteLLM, CrewAI local runner, Models, MCP Servers, Observability\n- References a GitHub repo: konecta-ix-applications/kix-apps-konectaiq (note: org name may be […]

> TOOL

tool_result
id: toolu_018No1GeeEFawaJiKoZzA8qk
```
Perfect! Now let me create a final summary to share with you:

## Summary

I've completed a comprehensive technical writing review of the new Applications documentation merge. Here's what I found:

### **CRITICAL ISSUES (Must Fix Before Merge)**

**1. Homepage Broken Link** (`src/pages/index.js:53`)
- Link points to `/docs/developer-guide/technology-specs` but page moved to `/docs/applications/technology-specs`
- Fix: Change the URL in one line
- Impact: 404 error for users clicking "Technology Specs" from homepage

**2. Developer Guide Index Broken Link** (`docs/developer-guide/index.md:39`)
- References `./technology-specs` but file no longer in that directory
- Fix: Update relative link to `../applications/technology-specs`
- Impact: 404 error in sidebar navigation

**3. Verify GitHub Repository Name** (`docs/applications/local-development-setup.md:35`)
- Links to `konecta-ix-applications/kix-apps-konectaiq`
- Action: Confirm this repository name is correct (CLAUDE.md lists `kix-app-iqportal`)
- Impact: "Repository not found" if URL is wrong

### **HIGH PRIORITY ISSUES**

**4. Empty Placeholder Page in Sidebar** (`docs/developer-guide/development-toolkit.md`)
- Entire page is "Coming soon" placeholders
- Should be removed from sidebar until content is available
- Fix: Comment out line 65 in `sidebars.js`

### **MEDIUM PRIORITY ISSUES (Content Quality)**

**5. Duplicate "What Developers Build" Sections**
- Applications section describes components (Python tools, MCP servers, etc.)
- Developer Guide describes responsibilities […]

> AGENT

Let me check what files the agent created so I can clean those up — review artifacts shouldn't live in the repo.

> TOOL

tool_use Glob
id: toolu_0116TWdvftYhYC967nshSBeF
```json
{
  "pattern": "*REVIEW*"
}
```

> TOOL

tool_use Glob
id: toolu_01P1wzm9P9MN84o3R21kdtwC
```json
{
  "pattern": "*CRITICAL_FIXES*"
}
```

> TOOL

tool_use Glob
id: toolu_019WgBsHjxQVFp1Nvg6cAMER
```json
{
  "pattern": "*TECHNICAL_REVIEW*"
}
```

> TOOL

tool_use Glob
id: toolu_01YGfmT3tFKD7Gcyw8Yfk5ie
```json
{
  "pattern": "*ARCHITECTURE_AND_CLARITY*"
}
```

> TOOL

tool_result
id: toolu_0116TWdvftYhYC967nshSBeF
```
/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/REVIEW_NEW_APPLICATIONS_DOCS.md
/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/TECHNICAL_REVIEW_SUMMARY.md
/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/REVIEW_FINDINGS_AT_A_GLANCE.md
```

> TOOL

tool_result
id: toolu_01P1wzm9P9MN84o3R21kdtwC
```
/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/CRITICAL_FIXES_NEEDED.md
```

> TOOL

tool_result
id: toolu_01YGfmT3tFKD7Gcyw8Yfk5ie
```
/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/ARCHITECTURE_AND_CLARITY_ISSUES.md
```

> TOOL

tool_result
id: toolu_019WgBsHjxQVFp1Nvg6cAMER
```
/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/TECHNICAL_REVIEW_SUMMARY.md
```

> TOOL

tool_use Bash
id: toolu_01U7FyJFvR18B1Vy5HepHj1w
```json
{
  "command": "rm /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/REVIEW_NEW_APPLICATIONS_DOCS.md /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/TECHNICAL_REVIEW_SUMMARY.md /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/REVIEW_FINDINGS_AT_A_GLANCE.md /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/CRITICAL_FIXES_NEEDED.md /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/ARCHITECTURE_AND_CLARITY_ISSUES.md",
  "description": "Remove review artifacts from repo"
}
```

> TOOL

tool_result
id: toolu_01U7FyJFvR18B1Vy5HepHj1w
```

```

> AGENT

Here's the full review of Sam's merge into develop.

---

## Critical Issues (fix before merging to main)

### 1. Broken link on homepage
[index.js:53](src/pages/index.js#L53) — The AI Engineers audience section links to `/docs/developer-guide/technology-specs`, but that page was **moved** to `/docs/applications/technology-specs`. This will 404.

### 2. Broken link in Developer Guide index
[developer-guide/index.md:39](docs/developer-guide/index.md#L39) — Still lists `[Technology Specs](./technology-specs)` in its Sections list. The file no longer exists at that path. Needs updating to `../applications/technology-specs` or removing from the list entirely.

### 3. Suspect GitHub repo URL
[local-development-setup.md:35](docs/applications/local-development-setup.md#L35) — Links to `konecta-ix-applications/kix-apps-konectaiq`. The CLAUDE.md repo structure lists the app repo as `kix-app-iqportal` under the `konecta-ix-applications` org. Worth confirming which name is correct.

---

## High Priority

### 4. Development Toolkit is 100% placeholder
[development-toolkit.md](docs/developer-guide/development-toolkit.md) — Every single subsection is *"Coming soon."* This adds a sidebar entry that leads to zero useful content. Recommend commenting it out of [sidebars.js:65](sidebars.js#L65) until at least one section has real content.

### 5. Broken "Related Documentation" links in Application Architecture
[application-architecture.md:78-81](docs/applications/application-architecture.md#L78-L81) — Three links at the bottom:
- `/docs/architecture` — works (resolves to architecture index)
- `/docs/services/litellm-gateway` — works (exists in sidebar)
- `/docs/app-migration/observability` — works but is an odd cross-reference from an "Applications" page into […]

> AGENT

Two things I need your input on:

> TOOL

tool_use AskUserQuestion
id: toolu_01V7wDHgB6tD14947FmWHx7c
```json
{
  "questions": [
    {
      "question": "What is the correct GitHub repo name for Konecta IQ? The local-development-setup.md links to konecta-ix-applications/kix-apps-konectaiq, but CLAUDE.md lists kix-app-iqportal under that org.",
      "header": "IQ Repo Name",
      "options": [
        {
          "label": "kix-app-iqportal",
          "description": "Match the naming convention in CLAUDE.md (kix-app-iqportal)"
        },
        {
          "label": "kix-apps-konectaiq",
          "description": "Keep the current link as Sam wrote it (kix-apps-konectaiq)"
        }
      ],
      "multiSelect": false
    },
    {
      "question": "For the Applications vs Developer Guide split, which approach do you prefer?",
      "header": "Section Split",
      "options": [
        {
          "label": "Clarify the boundary",
          "description": "Keep both sections but add a sentence to each index explaining what belongs where (Applications = what you build, Developer Guide = platform tooling and workflows)"
        },
        {
          "label": "Merge into Applications",
          "description": "Fold Developer Guide content into Applications as the single developer-facing section"
        },
        {
          "label": "Keep as-is for now",
          "description": "Only fix the broken links and overlap issues, defer the restructure"
        }
      ],
      "multiSelect": false
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01V7wDHgB6tD14947FmWHx7c
```
User has answered your questions: "What is the correct GitHub repo name for Konecta IQ? The local-development-setup.md links to konecta-ix-applications/kix-apps-konectaiq, but CLAUDE.md lists kix-app-iqportal under that org."="kix-apps-konectaiq", "For the Applications vs Developer Guide split, which approach do you prefer?"="Clarify the boundary". You can now continue with the user's answers in mind.
```

> TOOL

tool_use TodoWrite
id: toolu_01GRpXieu1sntWcxroHCZcPi
```json
{
  "todos": [
    {
      "content": "Fix broken homepage link (technology-specs URL)",
      "status": "in_progress",
      "activeForm": "Fixing broken homepage link"
    },
    {
      "content": "Fix broken Developer Guide index link (technology-specs)",
      "status": "pending",
      "activeForm": "Fixing Developer Guide index link"
    },
    {
      "content": "Remove development-toolkit from sidebar until it has content",
      "status": "pending",
      "activeForm": "Removing empty placeholder from sidebar"
    },
    {
      "content": "Deduplicate 'What Developers Build' across Applications and Developer Guide",
      "status": "pending",
      "activeForm": "Deduplicating overlapping content"
    },
    {
      "content": "Remove duplicated intro paragraph between applications/index.md and application-architecture.md",
      "status": "pending",
      "activeForm": "Removing duplicated intro paragraph"
    },
    {
      "content": "Add cross-links between Local Dev Setup and Deploy First Service",
      "status": "pending",
      "activeForm": "Adding cross-links between pages"
    },
    {
      "content": "Clarify boundary between Applications and Developer Guide sections",
      "status": "pending",
      "activeForm": "Clarifying section boundaries"
    },
    {
      "content": "Add Next Steps links to Applications pages",
      "status": "pending",
      "activeForm": "Adding Next Steps navigation"
    },
    {
      "content": "Clean up misleading sidebar_position values in front matter",
      "status": "pending",
      "activeForm": "Cleaning up front matter positions"
    },
    {
      "content": "Build and verify no broken links",
      "status": "pending",
      "activeForm": "Building site and verifying links"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01GRpXieu1sntWcxroHCZcPi
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

> AGENT

Good — repo name stays as-is, and I'll clarify the boundary between the two sections. Let me work through all the fixes.

> TOOL

tool_use Edit
id: toolu_01P4taCQFhx41nxdc6crHpvD
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/src/pages/index.js",
  "old_string": "      { label: 'Technology Specs', to: '/docs/developer-guide/technology-specs' },",
  "new_string": "      { label: 'Technology Specs', to: '/docs/applications/technology-specs' },"
}
```

> TOOL

tool_use Read
id: toolu_01ARVABX5NShno5xGVfTaveF
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/index.md"
}
```

> TOOL

tool_result
id: toolu_01P4taCQFhx41nxdc6crHpvD
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/src/pages/index.js has been updated successfully.
```

> TOOL

tool_result
id: toolu_01ARVABX5NShno5xGVfTaveF
```
     1→---
     2→title: "Developer Guide"
     3→sidebar_label: "Overview"
     4→sidebar_position: 1
     5→description: "Guide for use case developers building AI agents and services on the KIX Platform"
     6→---
     7→
     8→# Developer Guide
     9→
    10→This guide explains how to build services on the KIX Platform. It covers what the platform provides, how to build use cases, service patterns, and technology specifications.
    11→
    12→**Audience:** Use case developers building on KIX
    13→
    14→## Architecture Layers
    15→
    16→| Layer | Purpose | Components |
    17→|-------|---------|------------|
    18→| **Northbound** | Service exposure to consumers | Kong API Gateway, LiteLLM MCP Gateway, Admin UI |
    19→| **Capability** | Business logic and orchestration | Control Plane, Agents, Voice, Messaging, Knowledge |
    20→| **Southbound** | Infrastructure (abstracted) | GCP services, databases, storage, events |
    21→
    22→## Service Consumption Model
    23→
    24→Consumers access platform capabilities through three methods:
    25→
    26→| Method | Consumer Type | Authentication |
    27→|--------|---------------|----------------|
    28→| REST API (Kong) | External systems, applications | API Key or JWT |
    29→| MCP Tools (LiteLLM) | AI agents | Service account |
    30→| Admin UI | Internal users | OIDC |
    31→
    32→All requests are authenticated, routed through the appropriate gateway, and executed by the capability layer. Infrastructure is […]

> TOOL

tool_use TodoWrite
id: toolu_01XdAL3tk6pvnnmAxhyJMCph
```json
{
  "todos": [
    {
      "content": "Fix broken homepage link (technology-specs URL)",
      "status": "completed",
      "activeForm": "Fixing broken homepage link"
    },
    {
      "content": "Fix broken Developer Guide index link (technology-specs)",
      "status": "in_progress",
      "activeForm": "Fixing Developer Guide index link"
    },
    {
      "content": "Remove development-toolkit from sidebar until it has content",
      "status": "pending",
      "activeForm": "Removing empty placeholder from sidebar"
    },
    {
      "content": "Deduplicate 'What Developers Build' across Applications and Developer Guide",
      "status": "pending",
      "activeForm": "Deduplicating overlapping content"
    },
    {
      "content": "Remove duplicated intro paragraph between applications/index.md and application-architecture.md",
      "status": "pending",
      "activeForm": "Removing duplicated intro paragraph"
    },
    {
      "content": "Add cross-links between Local Dev Setup and Deploy First Service",
      "status": "pending",
      "activeForm": "Adding cross-links between pages"
    },
    {
      "content": "Clarify boundary between Applications and Developer Guide sections",
      "status": "pending",
      "activeForm": "Clarifying section boundaries"
    },
    {
      "content": "Add Next Steps links to Applications pages",
      "status": "pending",
      "activeForm": "Adding Next Steps navigation"
    },
    {
      "content": "Clean up misleading sidebar_position values in front matter",
      "status": "pending",
      "activeForm": "Cleaning up front matter positions"
    },
    {
      "content": "Build and verify no broken links",
      "status": "pending",
      "activeForm": "Building site and verifying links"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01XdAL3tk6pvnnmAxhyJMCph
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

> AGENT

Now I'll fix the Developer Guide index — update the tech specs link and rewrite the intro/sections to clarify the boundary. I'll also tackle the overlapping "What Developers Build" in platform-overview.md at the same time.

> TOOL

tool_use Edit
id: toolu_01YGkPxCCcNt5y6cfFZ94ZRR
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/index.md",
  "old_string": "This guide explains how to build services on the KIX Platform. It covers what the platform provides, how to build use cases, service patterns, and technology specifications.\n\n**Audience:** Use case developers building on KIX\n\n## Architecture Layers\n\n| Layer | Purpose | Components |\n|-------|---------|------------|\n| **Northbound** | Service exposure to consumers | Kong API Gateway, LiteLLM MCP Gateway, Admin UI |\n| **Capability** | Business logic and orchestration | Control Plane, Agents, Voice, Messaging, Knowledge |\n| **Southbound** | Infrastructure (abstracted) | GCP services, databases, storage, events |\n\n## Service Consumption Model\n\nConsumers access platform capabilities through three methods:\n\n| Method | Consumer Type | Authentication |\n|--------|---------------|----------------|\n| REST API (Kong) | External systems, applications | API Key or JWT |\n| MCP Tools (LiteLLM) | AI agents | Service account |\n| Admin UI | Internal users | OIDC |\n\nAll requests are authenticated, routed through the appropriate gateway, and executed by the capability layer. Infrastructure is never exposed directly to consumers.\n\n## Sections\n\n- **[Platform Overview](./platform-overview)** — What the platform provides and what developers build\n- **[Building Use Cases](./building-use-cases)** — Service patterns, development flow, and deployment\n- **[Branching Strategy](./branching-strategy)** — Gitflow model and branch-to-environment mapping\n- **[Technology Specs](./technology-specs)** — Detailed specifications for each platform component\n- […]

> TOOL

tool_result
id: toolu_01YGkPxCCcNt5y6cfFZ94ZRR
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/index.md has been updated successfully.
```

> TOOL

tool_use TodoWrite
id: toolu_01CtE9Updr7qQx8c1nH4f5MV
```json
{
  "todos": [
    {
      "content": "Fix broken homepage link (technology-specs URL)",
      "status": "completed",
      "activeForm": "Fixing broken homepage link"
    },
    {
      "content": "Fix broken Developer Guide index link (technology-specs)",
      "status": "completed",
      "activeForm": "Fixing Developer Guide index link"
    },
    {
      "content": "Remove development-toolkit from sidebar until it has content",
      "status": "in_progress",
      "activeForm": "Removing empty placeholder from sidebar"
    },
    {
      "content": "Deduplicate 'What Developers Build' across Applications and Developer Guide",
      "status": "pending",
      "activeForm": "Deduplicating overlapping content"
    },
    {
      "content": "Remove duplicated intro paragraph between applications/index.md and application-architecture.md",
      "status": "pending",
      "activeForm": "Removing duplicated intro paragraph"
    },
    {
      "content": "Add cross-links between Local Dev Setup and Deploy First Service",
      "status": "pending",
      "activeForm": "Adding cross-links between pages"
    },
    {
      "content": "Clarify boundary between Applications and Developer Guide sections",
      "status": "pending",
      "activeForm": "Clarifying section boundaries"
    },
    {
      "content": "Add Next Steps links to Applications pages",
      "status": "pending",
      "activeForm": "Adding Next Steps navigation"
    },
    {
      "content": "Clean up misleading sidebar_position values in front matter",
      "status": "pending",
      "activeForm": "Cleaning up front matter positions"
    },
    {
      "content": "Build and verify no broken links",
      "status": "pending",
      "activeForm": "Building site and verifying links"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01CtE9Updr7qQx8c1nH4f5MV
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

> AGENT

Now remove the development-toolkit from the sidebar and fix the platform-overview overlap.

> TOOL

tool_use Edit
id: toolu_01FYy8hCuChCFC92EkKp8DFL
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/sidebars.js",
  "old_string": "        'developer-guide/secrets-management',\n        'developer-guide/development-toolkit',\n        'developer-guide/claude-code',",
  "new_string": "        'developer-guide/secrets-management',\n        // 'developer-guide/development-toolkit', // Placeholder — re-enable when content is added\n        'developer-guide/claude-code',"
}
```

> TOOL

tool_use Read
id: toolu_01A43dwRTdpyKgj7nTcSDNXu
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/platform-overview.md"
}
```

> TOOL

tool_result
id: toolu_01FYy8hCuChCFC92EkKp8DFL
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/sidebars.js has been updated successfully.
```

> TOOL

tool_result
id: toolu_01A43dwRTdpyKgj7nTcSDNXu
```
     1→---
     2→title: "Platform Overview"
     3→sidebar_label: "Platform Overview"
     4→sidebar_position: 2
     5→description: "What the KIX Platform provides to use case developers and what developers are responsible for building"
     6→---
     7→
     8→# Platform Overview
     9→
    10→## What the Platform Provides
    11→
    12→When a use case is onboarded, the platform automatically provisions:
    13→
    14→| Resource | Description |
    15→|----------|-------------|
    16→| **Kubernetes Namespace** | Isolated environment for workloads |
    17→| **PostgreSQL Database** | Dedicated database with credentials |
    18→| **Redis Key Prefix** | Shared cache with isolated keyspace |
    19→| **GCS Bucket** | Object storage for documents and artifacts |
    20→| **Pub/Sub Topic** | Event bus for async messaging |
    21→| **Kong Routes** | API endpoints at `/api/v1/{use-case}/*` |
    22→| **Secrets Folder** | Secret Manager path for credentials |
    23→| **Service Account** | GCP identity with least-privilege permissions |
    24→| **Observability** | Pre-configured dashboard, logs, and traces |
    25→| **Identity** | Identity services abstracting credential handling |
    26→| **Security** | Security monitoring, WAF, and firewall services |
    27→| **Service Catalogue** | Backstage portal for discovering available services |
    28→
    29→### Service Discovery via Backstage
    30→
    31→Use case developers discover available platform services through **Backstage**, the internal service catalogue:
    32→
    33→| What […]

> TOOL

tool_use TodoWrite
id: toolu_01Cdhzf2BJpndX8wk83jNDZG
```json
{
  "todos": [
    {
      "content": "Fix broken homepage link (technology-specs URL)",
      "status": "completed",
      "activeForm": "Fixing broken homepage link"
    },
    {
      "content": "Fix broken Developer Guide index link (technology-specs)",
      "status": "completed",
      "activeForm": "Fixing Developer Guide index link"
    },
    {
      "content": "Remove development-toolkit from sidebar until it has content",
      "status": "completed",
      "activeForm": "Removing empty placeholder from sidebar"
    },
    {
      "content": "Deduplicate 'What Developers Build' across Applications and Developer Guide",
      "status": "in_progress",
      "activeForm": "Deduplicating overlapping content"
    },
    {
      "content": "Remove duplicated intro paragraph between applications/index.md and application-architecture.md",
      "status": "pending",
      "activeForm": "Removing duplicated intro paragraph"
    },
    {
      "content": "Add cross-links between Local Dev Setup and Deploy First Service",
      "status": "pending",
      "activeForm": "Adding cross-links between pages"
    },
    {
      "content": "Clarify boundary between Applications and Developer Guide sections",
      "status": "pending",
      "activeForm": "Clarifying section boundaries"
    },
    {
      "content": "Add Next Steps links to Applications pages",
      "status": "pending",
      "activeForm": "Adding Next Steps navigation"
    },
    {
      "content": "Clean up misleading sidebar_position values in front matter",
      "status": "pending",
      "activeForm": "Cleaning up front matter positions"
    },
    {
      "content": "Build and verify no broken links",
      "status": "pending",
      "activeForm": "Building site and verifying links"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01Cdhzf2BJpndX8wk83jNDZG
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

> AGENT

Now I'll reframe the "What Developers Build" section in platform-overview to avoid duplication with the Applications index, and add a cross-reference.

> TOOL

tool_use Edit
id: toolu_01PqKN2TMtpDSAroY6auLhF8
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/platform-overview.md",
  "old_string": "## What Developers Build\n\n| Component | Responsibility |\n|-----------|----------------|\n| **Agent Logic** | Business logic using CrewAI framework |\n| **API Endpoints** | Request handlers behind Kong routes |\n| **Data Schema** | Database tables and vector collections |\n| **Prompts** | LLM prompts and configurations |\n| **Workflows** | Multi-step orchestration (if needed) |",
  "new_string": "## Developer Responsibilities\n\nFor an overview of the components you build (CrewAI flows, MCP Servers, Python tools, custom UI), see the [Applications overview](/docs/applications). The table below summarises what you are responsible for once your use case is onboarded:\n\n| Responsibility | What This Means |\n|----------------|-----------------|\n| **Agent Logic** | Business logic using the CrewAI framework |\n| **API Endpoints** | Request handlers behind Kong routes |\n| **Data Schema** | Database tables and vector collections |\n| **Prompts** | LLM prompts and configurations |\n| **Workflows** | Multi-step orchestration (if needed) |"
}
```

> TOOL

tool_result
id: toolu_01PqKN2TMtpDSAroY6auLhF8
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/platform-overview.md has been updated successfully.
```

> AGENT

Now fix the duplicated intro paragraph in applications/index.md and add next-steps navigation. I'll do both Applications pages in parallel.

> TOOL

tool_use Edit
id: toolu_011PmEL5ahL4xNGy6CfWTkA1
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/index.md",
  "old_string": "# Applications\n\nThe KIX Platform for AI Solutions is a modular architecture designed to build, deploy and operate AI-powered applications at Konecta. It connects front-end applications, agentic workflows, language models, tool servers and observability through well-defined integration points — so AI developers can focus on creating the building blocks for their use case while the platform handles infrastructure, routing, authentication and governance.\n\n## What Developers Build\n\nDevelopers contribute one or more of the following components:\n\n- **Python tools** — Custom code logic consumed by AI agents\n- **Agentic flows** — CrewAI Crews and Flows that orchestrate multi-step AI tasks\n- **MCP Servers** — Expose APIs and data sources to LLMs as callable tools\n- **Custom UI** — A dedicated front-end, or use **Konecta IQ** as a ready-made interface to interact with agents\n\nEach component is developed and tested locally against an environment that mirrors production, then submitted for packaging and deployment through the standard CI/CD pipeline.\n\n## In This Section\n\n| Page | Description |\n|---|---|\n| [Application Architecture](./application-architecture) | Production architecture overview — LiteLLM, CrewAI, MCP Servers, models and observability |\n| [Local Development Setup](./local-development-setup) | Set up the full platform locally with step-by-step instructions for each component |\n\nSee also the […]

> TOOL

tool_result ERROR
id: toolu_011PmEL5ahL4xNGy6CfWTkA1
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Read
id: toolu_01WPhpeUc2TjhkaSwsmXLKw8
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/index.md"
}
```

> TOOL

tool_result
id: toolu_01WPhpeUc2TjhkaSwsmXLKw8
```
     1→---
     2→title: "Applications"
     3→sidebar_label: "Overview"
     4→sidebar_position: 1
     5→description: "Application development standards, architecture, and tooling for the KIX Platform"
     6→---
     7→
     8→# Applications
     9→
    10→The KIX Platform for AI Solutions is a modular architecture designed to build, deploy and operate AI-powered applications at Konecta. It connects front-end applications, agentic workflows, language models, tool servers and observability through well-defined integration points — so AI developers can focus on creating the building blocks for their use case while the platform handles infrastructure, routing, authentication and governance.
    11→
    12→## What Developers Build
    13→
    14→Developers contribute one or more of the following components:
    15→
    16→- **Python tools** — Custom code logic consumed by AI agents
    17→- **Agentic flows** — CrewAI Crews and Flows that orchestrate multi-step AI tasks
    18→- **MCP Servers** — Expose APIs and data sources to LLMs as callable tools
    19→- **Custom UI** — A dedicated front-end, or use **Konecta IQ** as a ready-made interface to interact with agents
    20→
    21→Each component is developed and tested locally against an environment that mirrors production, then submitted for packaging and deployment through the standard CI/CD pipeline.
    22→
    23→## In This Section
    24→
    25→| Page | Description |
    26→|---|---|
    27→| [Application Architecture](./application-architecture) […]

> TOOL

tool_use Edit
id: toolu_014Db7CLxsZyZfFL2CWNPaEF
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/index.md",
  "old_string": "# Applications\n\nThe KIX Platform for AI Solutions is a modular architecture designed to build, deploy and operate AI-powered applications at Konecta. It connects front-end applications, agentic workflows, language models, tool servers and observability through well-defined integration points — so AI developers can focus on creating the building blocks for their use case while the platform handles infrastructure, routing, authentication and governance.\n\n## What Developers Build\n\nDevelopers contribute one or more of the following components:\n\n- **Python tools** — Custom code logic consumed by AI agents\n- **Agentic flows** — CrewAI Crews and Flows that orchestrate multi-step AI tasks\n- **MCP Servers** — Expose APIs and data sources to LLMs as callable tools\n- **Custom UI** — A dedicated front-end, or use **Konecta IQ** as a ready-made interface to interact with agents\n\nEach component is developed and tested locally against an environment that mirrors production, then submitted for packaging and deployment through the standard CI/CD pipeline.\n\n## In This Section\n\n| Page | Description |\n|---|---|\n| [Application Architecture](./application-architecture) | Production architecture overview — LiteLLM, CrewAI, MCP Servers, models and observability |\n| [Local Development Setup](./local-development-setup) | Set up the full platform locally with step-by-step instructions for each component |\n\nSee also the […]

> TOOL

tool_result
id: toolu_014Db7CLxsZyZfFL2CWNPaEF
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/index.md has been updated successfully.
```

> TOOL

tool_use TodoWrite
id: toolu_01Hg2PWH734tPNRBVUjeGemN
```json
{
  "todos": [
    {
      "content": "Fix broken homepage link (technology-specs URL)",
      "status": "completed",
      "activeForm": "Fixing broken homepage link"
    },
    {
      "content": "Fix broken Developer Guide index link (technology-specs)",
      "status": "completed",
      "activeForm": "Fixing Developer Guide index link"
    },
    {
      "content": "Remove development-toolkit from sidebar until it has content",
      "status": "completed",
      "activeForm": "Removing empty placeholder from sidebar"
    },
    {
      "content": "Deduplicate 'What Developers Build' across Applications and Developer Guide",
      "status": "completed",
      "activeForm": "Deduplicating overlapping content"
    },
    {
      "content": "Remove duplicated intro paragraph between applications/index.md and application-architecture.md",
      "status": "completed",
      "activeForm": "Removing duplicated intro paragraph"
    },
    {
      "content": "Add cross-links between Local Dev Setup and Deploy First Service",
      "status": "in_progress",
      "activeForm": "Adding cross-links between pages"
    },
    {
      "content": "Clarify boundary between Applications and Developer Guide sections",
      "status": "completed",
      "activeForm": "Clarifying section boundaries"
    },
    {
      "content": "Add Next Steps links to Applications pages",
      "status": "pending",
      "activeForm": "Adding Next Steps navigation"
    },
    {
      "content": "Clean up misleading sidebar_position values in front matter",
      "status": "pending",
      "activeForm": "Cleaning up front matter positions"
    },
    {
      "content": "Build and verify no broken links",
      "status": "pending",
      "activeForm": "Building site and verifying links"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01Hg2PWH734tPNRBVUjeGemN
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

> AGENT

Now let me read the files I need to edit next, then make all changes in parallel.

> TOOL

tool_use Read
id: toolu_01HHSAfsjagTCJZ1qbVq8zAQ
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/application-architecture.md"
}
```

> TOOL

tool_use Read
id: toolu_01Wg7C9ParQiQuaMfnvEc8vu
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/local-development-setup.md"
}
```

> TOOL

tool_use Read
id: toolu_01RSc4eT3xfRkbwJvfizCoAy
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/technology-specs.md"
}
```

> TOOL

tool_result
id: toolu_01HHSAfsjagTCJZ1qbVq8zAQ
```
     1→---
     2→title: "Application Architecture"
     3→sidebar_label: "Application Architecture"
     4→sidebar_position: 4
     5→description: "Architecture patterns and standards for KIX Platform applications"
     6→---
     7→
     8→# Application Architecture
     9→
    10→## Overview
    11→
    12→The KIX Platform for AI Solutions is a modular architecture designed to build, deploy and operate AI-powered applications at Konecta. It provides a unified foundation where front-end applications, agentic workflows, language models and observability all connect through well-defined integration points.
    13→
    14→![KIX Platform for AI Solutions](/img/kix-platform-ai-architecture.jpg)
    15→
    16→## Architecture Components
    17→
    18→### Application Layer
    19→
    20→At the top of the architecture sit the consumer-facing applications:
    21→
    22→- **Konecta IQ (Showcase Environment)** — A demonstration environment that showcases the platform's AI-state-of-the-art capabilities and serves as an in-consultation tool within the platform.
    23→- **Use Cases** — Production AI solutions built on the platform, including Portfolio analysis, Competitor Analysis, Market Intelligence and Email Responder.
    24→
    25→Both application types connect downward into the platform's core services.
    26→
    27→### LiteLLM (AI Gateway)
    28→
    29→LiteLLM acts as the central AI Gateway, providing a unified API layer that abstracts away the specifics of individual model providers. Applications and agents make requests through LiteLLM, which routes them to the appropriate model backend. This decouples application code from […]

> TOOL

tool_result
id: toolu_01Wg7C9ParQiQuaMfnvEc8vu
```
     1→---
     2→title: "Local Development Setup"
     3→sidebar_label: "Local Development Setup"
     4→sidebar_position: 5
     5→description: "Setting up your local environment for KIX Platform application development"
     6→---
     7→
     8→# Local Development Setup
     9→
    10→## What AI Developers Build
    11→
    12→AI developers are expected to use the platform and focus on creating the building blocks required for their use case. The platform handles infrastructure, routing, authentication and observability — developers provide the logic. Typical contributions include:
    13→
    14→- **Python tools** — Custom code logic consumed by agents
    15→- **Agentic flows** — CrewAI Crews and Flows that orchestrate multi-step AI tasks
    16→- **MCP Servers** — Make APIs and data sources accessible to LLMs as tools
    17→- **Custom UI** — A dedicated front-end for a specific use case, or simply use **Konecta IQ** as a readily available UI to interact with agents without building any interface
    18→
    19→## Production Architecture Recap
    20→
    21→The KIX Platform for AI Solutions runs a modular architecture in production where applications connect to an AI gateway (LiteLLM), an agentic orchestration layer (CrewAI), MCP Servers for tool capabilities and a full observability stack. For a detailed breakdown of each component and how they interact, see the [Application Architecture](./application-architecture) page. […]

> TOOL

tool_result
id: toolu_01RSc4eT3xfRkbwJvfizCoAy
```
     1→---
     2→title: "Technology Specifications"
     3→sidebar_label: "Technology Specs"
     4→sidebar_position: 7
     5→description: "Detailed specifications for each platform component including CrewAI, LiteLLM, Kong, databases, and more"
     6→---
     7→
     8→# Technology Specifications
     9→
    10→## CrewAI
    11→
    12→**Purpose:** Multi-agent orchestration for autonomous task execution
    13→
    14→**What It Does:**
    15→- Defines agents with roles, goals, and tools
    16→- Orchestrates tasks across multiple agents
    17→- Manages agent collaboration and handoffs
    18→- Integrates with LLM gateway for model access
    19→
    20→**Constraints:**
    21→- All LLM calls must use platform gateway (no direct API calls)
    22→- Maximum execution time configurable per agent
    23→- Agent state must be externalized for fault tolerance
    24→
    25→**Example Crew Structure:**
    26→```
    27→End-User Self-Healing Crew
    28→├── Triage Agent
    29→│   └── Classifies issue type, urgency, complexity
    30→├── Diagnostic Agent
    31→│   └── Runs diagnostic checks via Nexthink MCP
    32→├── Resolution Agent
    33→│   └── Executes fixes via ServiceNow/AD MCP
    34→├── Communication Agent
    35→│   └── Updates user on progress
    36→└── Escalation Agent
    37→    └── Hands off to human with full context
    38→```
    39→
    40→## ElevenLabs
    41→
    42→**Purpose:** Voice synthesis and conversational AI (primary voice runtime)
    43→
    44→**What It Does:**
    45→- Text-to-speech synthesis
    46→- Real-time conversational AI
    47→- Speech-to-Text
    48→- Multi-language support
    49→
    50→**Constraints:**
    51→- Voice calls […]

> AGENT

Now I'll make all the remaining edits in parallel.

> TOOL

tool_use Edit
id: toolu_0139BPaQrih248eke2rzRXuP
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/application-architecture.md",
  "old_string": "---\ntitle: \"Application Architecture\"\nsidebar_label: \"Application Architecture\"\nsidebar_position: 4\ndescription: \"Architecture patterns and standards for KIX Platform applications\"\n---",
  "new_string": "---\ntitle: \"Application Architecture\"\nsidebar_label: \"Application Architecture\"\nsidebar_position: 2\ndescription: \"Architecture patterns and standards for KIX Platform applications\"\n---"
}
```

> TOOL

tool_use Edit
id: toolu_01Lo1oTXubbQSa1T4ZaKPhYk
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/application-architecture.md",
  "old_string": "## Related Documentation\n\n- [Platform Architecture](/docs/architecture) — Infrastructure-level view of the KIX Platform (GCP, GKE, networking)\n- [LiteLLM Gateway](/docs/services/litellm-gateway) — Detailed configuration and operations guide for the AI gateway\n- [Observability](/docs/app-migration/observability) — Full monitoring, logging and tracing stack details",
  "new_string": "## Next Steps\n\n- [Technology Specs](./technology-specs) — Detailed specifications for each platform component\n- [Local Development Setup](./local-development-setup) — Replicate this architecture on your local machine\n\n## Related Documentation\n\n- [Platform Architecture](/docs/architecture) — Infrastructure-level view of the KIX Platform (GCP, GKE, networking)\n- [LiteLLM Gateway](/docs/services/litellm-gateway) — Detailed configuration and operations guide for the AI gateway\n- [Observability](/docs/app-migration/observability) — Monitoring, logging and tracing stack details"
}
```

> TOOL

tool_use Edit
id: toolu_01PZiWDy3ZELuVhQSkkCmKsC
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/local-development-setup.md",
  "old_string": "---\ntitle: \"Local Development Setup\"\nsidebar_label: \"Local Development Setup\"\nsidebar_position: 5\ndescription: \"Setting up your local environment for KIX Platform application development\"\n---",
  "new_string": "---\ntitle: \"Local Development Setup\"\nsidebar_label: \"Local Development Setup\"\nsidebar_position: 4\ndescription: \"Setting up your local environment for KIX Platform application development\"\n---"
}
```

> TOOL

tool_use Edit
id: toolu_01Djv6ffLeDnQj6kZzJ2nhar
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/local-development-setup.md",
  "old_string": "## What AI Developers Build\n\nAI developers are expected to use the platform and focus on creating the building blocks required for their use case. The platform handles infrastructure, routing, authentication and observability — developers provide the logic. Typical contributions include:\n\n- **Python tools** — Custom code logic consumed by agents\n- **Agentic flows** — CrewAI Crews and Flows that orchestrate multi-step AI tasks\n- **MCP Servers** — Make APIs and data sources accessible to LLMs as tools\n- **Custom UI** — A dedicated front-end for a specific use case, or simply use **Konecta IQ** as a readily available UI to interact with agents without building any interface\n\n## Production Architecture Recap\n\nThe KIX Platform for AI Solutions runs a modular architecture in production where applications connect to an AI gateway (LiteLLM), an agentic orchestration layer (CrewAI), MCP Servers for tool capabilities and a full observability stack. For a detailed breakdown of each component and how they interact, see the [Application Architecture](./application-architecture) page.",
  "new_string": "The production architecture (LiteLLM, CrewAI, MCP Servers, observability) can be replicated on your local machine so you can develop and test before deploying. For a breakdown of each component see the [Application […]

> TOOL

tool_use Edit
id: toolu_01LMkG9QHSzNHPkhmqsSRg25
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/local-development-setup.md",
  "old_string": "*Documentation on local observability setup coming soon.*",
  "new_string": "*Documentation on local observability setup coming soon.*\n\n## Next Steps\n\n- [Deploy First Service](/docs/developer-guide/deploy-first-service) — End-to-end tutorial taking code through to production via Terraform, Helm and ArgoCD\n- [Building Use Cases](/docs/developer-guide/building-use-cases) — Service patterns, development flow and governance requirements\n- [Secrets Management](/docs/developer-guide/secrets-management) — External Secrets Operator and GCP Secret Manager"
}
```

> TOOL

tool_use Edit
id: toolu_01SAvcb1jDiuz7S4uaF32W9J
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/technology-specs.md",
  "old_string": "---\ntitle: \"Technology Specifications\"\nsidebar_label: \"Technology Specs\"\nsidebar_position: 7\ndescription: \"Detailed specifications for each platform component including CrewAI, LiteLLM, Kong, databases, and more\"\n---",
  "new_string": "---\ntitle: \"Technology Specifications\"\nsidebar_label: \"Technology Specs\"\nsidebar_position: 3\ndescription: \"Detailed specifications for each platform component including CrewAI, LiteLLM, Kong, databases, and more\"\n---"
}
```

> TOOL

tool_result
id: toolu_0139BPaQrih248eke2rzRXuP
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/application-architecture.md has been updated successfully.
```

> TOOL

tool_result
id: toolu_01Lo1oTXubbQSa1T4ZaKPhYk
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/application-architecture.md has been updated successfully.
```

> TOOL

tool_result
id: toolu_01PZiWDy3ZELuVhQSkkCmKsC
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/local-development-setup.md has been updated successfully.
```

> TOOL

tool_result
id: toolu_01Djv6ffLeDnQj6kZzJ2nhar
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/local-development-setup.md has been updated successfully.
```

> TOOL

tool_result
id: toolu_01LMkG9QHSzNHPkhmqsSRg25
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/local-development-setup.md has been updated successfully.
```

> TOOL

tool_result
id: toolu_01SAvcb1jDiuz7S4uaF32W9J
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/applications/technology-specs.md has been updated successfully.
```

> AGENT

Now let me also add a cross-link from deploy-first-service back to the local dev setup, and update the todo list.

> TOOL

tool_use Read
id: toolu_01Rzeb6QLp8UHWSwNbXb4m7L
```json
{
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/deploy-first-service.md",
  "offset": 1005,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01Rzeb6QLp8UHWSwNbXb4m7L
```
  1005→
  1006→---
  1007→
  1008→## Next Steps
  1009→
  1010→**Congratulations!** You've deployed a complete service on the KIX Platform.
  1011→
  1012→**Learn More:**
  1013→- [Secrets Management](/docs/developer-guide/secrets-management) - Advanced ESO patterns
  1014→- [Kong Gateway Guide](/docs/services/kong-gateway) - Authentication, rate limiting, plugins
  1015→
  1016→**Platform Services:**
  1017→- [LiteLLM Gateway](/docs/services/litellm-gateway) - AI model routing
  1018→- [Cloud SQL](/docs/services/cloud-sql) - Managed PostgreSQL
  1019→- [Memorystore Redis](/docs/services/redis) - Managed Redis cache
  1020→
  1021→**Get Help:**
  1022→- Documentation: https://konecta-ix-platform.github.io/kix-platform-docs
  1023→
  1024→---
  1025→
  1026→**Document Version:** 1.0
  1027→**Last Updated:** 2026-02-09
  1028→**Maintained By:** Platform Engineering Team
  1029→
```

> TOOL

tool_use Edit
id: toolu_0195YqnbY8QSt3rZo4ZEA3CR
```json
{
  "replace_all": false,
  "file_path": "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/deploy-first-service.md",
  "old_string": "**Learn More:**\n- [Secrets Management](/docs/developer-guide/secrets-management) - Advanced ESO patterns\n- [Kong Gateway Guide](/docs/services/kong-gateway) - Authentication, rate limiting, plugins\n\n**Platform Services:**\n- [LiteLLM Gateway](/docs/services/litellm-gateway) - AI model routing\n- [Cloud SQL](/docs/services/cloud-sql) - Managed PostgreSQL\n- [Memorystore Redis](/docs/services/redis) - Managed Redis cache",
  "new_string": "**Learn More:**\n- [Local Development Setup](/docs/applications/local-development-setup) - Run the full platform locally (LiteLLM, CrewAI, MCP Servers)\n- [Secrets Management](/docs/developer-guide/secrets-management) - Advanced ESO patterns\n- [Kong Gateway Guide](/docs/services/kong-gateway) - Authentication, rate limiting, plugins\n\n**Platform Services:**\n- [LiteLLM Gateway](/docs/services/litellm-gateway) - AI model routing\n- [Cloud SQL](/docs/services/cloud-sql) - Managed PostgreSQL\n- [Memorystore Redis](/docs/services/redis) - Managed Redis cache"
}
```

> TOOL

tool_result
id: toolu_0195YqnbY8QSt3rZo4ZEA3CR
```
The file /home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/docs/developer-guide/deploy-first-service.md has been updated successfully.
```

> TOOL

tool_use TodoWrite
id: toolu_01N6319VgHkGK3Qpf5Now839
```json
{
  "todos": [
    {
      "content": "Fix broken homepage link (technology-specs URL)",
      "status": "completed",
      "activeForm": "Fixing broken homepage link"
    },
    {
      "content": "Fix broken Developer Guide index link (technology-specs)",
      "status": "completed",
      "activeForm": "Fixing Developer Guide index link"
    },
    {
      "content": "Remove development-toolkit from sidebar until it has content",
      "status": "completed",
      "activeForm": "Removing empty placeholder from sidebar"
    },
    {
      "content": "Deduplicate 'What Developers Build' across Applications and Developer Guide",
      "status": "completed",
      "activeForm": "Deduplicating overlapping content"
    },
    {
      "content": "Remove duplicated intro paragraph between applications/index.md and application-architecture.md",
      "status": "completed",
      "activeForm": "Removing duplicated intro paragraph"
    },
    {
      "content": "Add cross-links between Local Dev Setup and Deploy First Service",
      "status": "completed",
      "activeForm": "Adding cross-links between pages"
    },
    {
      "content": "Clarify boundary between Applications and Developer Guide sections",
      "status": "completed",
      "activeForm": "Clarifying section boundaries"
    },
    {
      "content": "Add Next Steps links to Applications pages",
      "status": "completed",
      "activeForm": "Adding Next Steps navigation"
    },
    {
      "content": "Clean up misleading sidebar_position values in front matter",
      "status": "completed",
      "activeForm": "Cleaning up front matter positions"
    },
    {
      "content": "Build and verify no broken links",
      "status": "in_progress",
      "activeForm": "Building site and verifying links"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01N6319VgHkGK3Qpf5Now839
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

> AGENT

Now let me build the site to verify everything compiles and there are no broken links.

> TOOL

tool_use Bash
id: toolu_01Wim4PYCcFbyLuqCRjbJXrK
```json
{
  "command": "npm run build 2>&1",
  "description": "Build Docusaurus site to check for broken links",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01Wim4PYCcFbyLuqCRjbJXrK
```
> kix-platform-docs@2.0.0 build
> docusaurus build

[INFO] [en] Creating an optimized production build...
Warn: `blogDir` doesn't exist: "/home/nathan_booth/code/konecta-ix-platform/kix-platform-docs/blog".
[webpackbar] ℹ Compiling Client
[webpackbar] ℹ Compiling Server
[webpackbar] ✔ Server: Compiled successfully in 57.48s
[webpackbar] ✔ Client: Compiled successfully in 1.31m
[WARNING] Docusaurus found broken anchors!

Please check the pages of your site in the list below, and make sure you don't reference any anchor that does not exist.
Note: it's possible to ignore broken anchors with the 'onBrokenAnchors' Docusaurus configuration, and let the build pass.

Exhaustive list of all broken anchors found:
- Broken anchor on source page path = /docs/security/risk-register:
   -> linking to /docs/infrastructure-ops/cicd-runbook#nightly-qualityyml
   -> linking to /docs/infrastructure-ops/cicd-runbook#rollback-procedure

[SUCCESS] Generated static files in "build".
[INFO] Use `npm run serve` command to test your build locally.
```

> AGENT

Build succeeds. The two broken anchor warnings are pre-existing (in the risk-register page, not from Sam's changes). Let me verify that cleanly.

> TOOL

tool_use Bash
id: toolu_01NabNgGN6uwUNFtoEXwmb5r
```json
{
  "command": "git diff --name-only main..develop -- docs/security/risk-register.md docs/infrastructure-ops/cicd-runbook.md 2>/dev/null",
  "description": "Check if the broken anchor files were changed in this branch"
}
```

> TOOL

tool_result
id: toolu_01NabNgGN6uwUNFtoEXwmb5r
```
docs/infrastructure-ops/cicd-runbook.md
```

> AGENT

The cicd-runbook was modified in develop (those anchors were likely removed during a rewrite). That's a pre-existing issue unrelated to Sam's merge, but worth noting.

> TOOL

tool_use TodoWrite
id: toolu_01NMVDydkstpbh6d1mkW8W4Q
```json
{
  "todos": [
    {
      "content": "Fix broken homepage link (technology-specs URL)",
      "status": "completed",
      "activeForm": "Fixing broken homepage link"
    },
    {
      "content": "Fix broken Developer Guide index link (technology-specs)",
      "status": "completed",
      "activeForm": "Fixing Developer Guide index link"
    },
    {
      "content": "Remove development-toolkit from sidebar until it has content",
      "status": "completed",
      "activeForm": "Removing empty placeholder from sidebar"
    },
    {
      "content": "Deduplicate 'What Developers Build' across Applications and Developer Guide",
      "status": "completed",
      "activeForm": "Deduplicating overlapping content"
    },
    {
      "content": "Remove duplicated intro paragraph between applications/index.md and application-architecture.md",
      "status": "completed",
      "activeForm": "Removing duplicated intro paragraph"
    },
    {
      "content": "Add cross-links between Local Dev Setup and Deploy First Service",
      "status": "completed",
      "activeForm": "Adding cross-links between pages"
    },
    {
      "content": "Clarify boundary between Applications and Developer Guide sections",
      "status": "completed",
      "activeForm": "Clarifying section boundaries"
    },
    {
      "content": "Add Next Steps links to Applications pages",
      "status": "completed",
      "activeForm": "Adding Next Steps navigation"
    },
    {
      "content": "Clean up misleading sidebar_position values in front matter",
      "status": "completed",
      "activeForm": "Cleaning up front matter positions"
    },
    {
      "content": "Build and verify no broken links",
      "status": "completed",
      "activeForm": "Building site and verifying links"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01NMVDydkstpbh6d1mkW8W4Q
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

> AGENT

All 10 fixes are done. Build passes with no new warnings. Here's a summary of everything changed:

## Changes Made

### Critical fixes
| File | Change |
|---|---|
| [index.js:53](src/pages/index.js#L53) | Fixed broken link: technology-specs URL now points to `/docs/applications/technology-specs` |
| [developer-guide/index.md](docs/developer-guide/index.md) | Removed broken technology-specs link, rewrote intro and sections list |

### Sidebar cleanup
| File | Change |
|---|---|
| [sidebars.js:65](sidebars.js#L65) | Commented out `development-toolkit` (all placeholder content) |

### Content deduplication
| File | Change |
|---|---|
| [applications/index.md](docs/applications/index.md) | Replaced duplicated architecture intro with concise signpost; added Technology Specs to the "In This Section" table; added cross-link to Developer Guide explaining the boundary |
| [developer-guide/platform-overview.md](docs/developer-guide/platform-overview.md) | Renamed "What Developers Build" to "Developer Responsibilities" with cross-reference to Applications section |
| [applications/local-development-setup.md](docs/applications/local-development-setup.md) | Removed third copy of "What Developers Build" list; condensed the architecture recap to a single sentence with link |

### Navigation improvements
| File | Change |
|---|---|
| [applications/application-architecture.md](docs/applications/application-architecture.md) | Added "Next Steps" section linking to Technology Specs and Local Dev Setup |
| [applications/local-development-setup.md](docs/applications/local-development-setup.md) | Added "Next Steps" section linking to Deploy First Service, Building Use Cases, Secrets Management |
| [developer-guide/deploy-first-service.md](docs/developer-guide/deploy-first-service.md) | Added cross-link to Local Development […]