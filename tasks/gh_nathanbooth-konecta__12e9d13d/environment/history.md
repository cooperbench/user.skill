> AGENT

Let me first identify what Sam's merge brought into develop, then review the content thoroughly.

> AGENT

Now let me read all the new documents from Sam's merge, plus the modified sidebar and homepage.

> AGENT

Now let me check the sidebar config and existing content that may overlap.

> AGENT

Now let me launch the technical writer review.

> AGENT

Let me check what files the agent created so I can clean those up — review artifacts shouldn't live in the repo.

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

> AGENT

Good — repo name stays as-is, and I'll clarify the boundary between the two sections. Let me work through all the fixes.

> AGENT

Now I'll fix the Developer Guide index — update the tech specs link and rewrite the intro/sections to clarify the boundary. I'll also tackle the overlapping "What Developers Build" in platform-overview.md at the same time.

> AGENT

Now remove the development-toolkit from the sidebar and fix the platform-overview overlap.

> AGENT

Now I'll reframe the "What Developers Build" section in platform-overview to avoid duplication with the Applications index, and add a cross-reference.

> AGENT

Now fix the duplicated intro paragraph in applications/index.md and add next-steps navigation. I'll do both Applications pages in parallel.

> AGENT

Now let me read the files I need to edit next, then make all changes in parallel.

> AGENT

Now I'll make all the remaining edits in parallel.

> AGENT

Now let me also add a cross-link from deploy-first-service back to the local dev setup, and update the todo list.

> AGENT

Now let me build the site to verify everything compiles and there are no broken links.

> AGENT

Build succeeds. The two broken anchor warnings are pre-existing (in the risk-register page, not from Sam's changes). Let me verify that cleanly.

> AGENT

The cicd-runbook was modified in develop (those anchors were likely removed during a rewrite). That's a pre-existing issue unrelated to Sam's merge, but worth noting.

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