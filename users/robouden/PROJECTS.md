# PROJECTS — robouden

## Safecast/safecast-map-MCP ★ dominant (52.4% of sessions)

**What it is**: A Go-based MCP (Model Context Protocol) server that exposes Safecast
radiation data via 15–16 MCP tools (radiation queries, sensor lookup, track listing,
gamma spectra). Runs on port 3333 of the production VPS. Fronted by AWS CloudFront at
`simplemap.safecast.org/mcp-http`.

**What robouden does here**:
- Debugs MCP tool data quality: wrong tables queried, future-dated sensor readings,
  missing realtime data, sensors not found in geographic searches.
- Adds AI hints in Go code to guide Claude and other AI models toward correct tools and
  tables (`"can you make an AI hintin the Go file that will direct Cluade or other AI
  to get the right data?"`).
- Maintains a web-chat frontend (`assistant.safecast.org`) that wraps the MCP server,
  adding markdown rendering, streaming responses, Safecast branding.
- Manages CloudFront routing for `/mcp-http`, `/api/*`, `/docs/*` — recurring source of
  streaming and caching bugs.
- Keeps docs and Mermaid architecture diagrams current after changes.
- Tests with local Ollama/Mistral as well as Claude.

**Tech stack**: Go, DuckDB (tool analytics), PostgreSQL/PostGIS, AWS CloudFront, GitHub Actions
(cross-compile + deploy to Hetzner VPS).

**Recurring themes**: MCP tool selection errors (realtime vs. historical table), CloudFront
buffering breaking streaming responses, AI-hint engineering in Go, unit conversion (CPM →
µSv/h), geographic search radius tuning, branding (Safecast logo/favicon).

---

## Safecast/safecast-new-map (47.6% of sessions)

**What it is**: A Go-based interactive map application serving the Safecast radiation dataset.
Runs on port 8765, served via Nginx reverse proxy → CloudFront at `simplemap.safecast.org`.
Includes user authentication (API key or password), admin panel, track uploads, and a
spatial tile layer backed by PostgreSQL/PostGIS.

**What robouden does here**:
- Manages user authentication and API key flows: login, registration, admin key generation.
- Handles bulk log-file imports and upload pipeline (bGeigie `.log` files).
- Debugs map performance issues: spatial index rebuilds, slow tile queries at various zoom
  levels, CloudFront caching behavior.
- Sets up and iterates on CloudFront distribution including SSL (ACM), Route53 DNS, and
  nginx configuration.
- Monitors CI/CD pipeline (GitHub Actions) for deployment failures.
- Fixes UI issues: responsive width, table spacing, favicon, admin buttons, login state.
- Responds to security abuse reports from Hetzner/BSI.

**Tech stack**: Go, PostgreSQL + PostGIS (markers, realtime_measurements, spectra tables),
Nginx, AWS CloudFront + Route53, GitHub Actions, Let's Encrypt SSL.

**Recurring themes**: Upload auth failures for large files (>10 KB), CloudFront MIME type
errors, spatial index performance, responsive CSS fixes, admin-only UI controls, CI/CD
deployment verification.

---

## Integration between repos

The two repos share the same production VPS (`simplemap.safecast.org`, IP 65.108.24.131).
The MCP server feeds AI clients; the map server feeds the browser UI and the REST API.
A Mermaid architecture diagram in `docs/architecture-diagram.mmd` documents their
interconnection. robouden periodically merges or syncs documentation across both repos.
