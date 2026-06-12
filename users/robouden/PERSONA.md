# PERSONA — robouden

## Role and domain

robouden is the technical lead / platform owner (inferred) of the Safecast citizen-science
radiation-monitoring project. He manages the `simplemap.safecast.org` production server and
is responsible for both the map application and the MCP server that powers AI queries over
Safecast data. He handles infrastructure, UI polish, data quality, and AI integration —
suggesting a small team or solo operation where he covers all layers.

## Technical background (inferred)

- Comfortable with Linux server administration: `ss`, `curl -I`, systemd, nginx config.
- Works with Go binaries deployed to a Hetzner VPS; understands compile/deploy cycles.
- Knows AWS well enough to set up CloudFront distributions, ACM certificates, Route53 DNS.
- Understands PostgreSQL/PostGIS (spatial queries, indexing, realtime tables vs. historical tables).
- Familiar with GitHub Actions CI/CD pipelines; questions when they haven't fired.
- Runs Ollama locally with Mistral; tests AI models against the MCP server.
- Uses MCP (Model Context Protocol) as a first-class integration layer for AI tooling.
- Based in Japan (inferred from NRT12 CloudFront POP in curl output, references to Mitsue/Nara).

## Seniority signals

- Asks "Would moving the MCP server to the map server speed up the queries?" — architectural
  intuition without needing the agent to explain trade-offs.
- Catches when the agent hallucinates ("Not true. You have been modifing aws setup one hor before!!").
- Knows to check incognito windows and hard-refresh for cache issues without being told.
- Pastes raw `ss -tlnp` and `curl -I` output, suggesting comfort at the shell level.
- Still leans on Claude Code for implementation and multi-step ops; he steers, it executes.

## Attitude toward the agent

- **Largely trusting**: delegates implementation, deployment steps, documentation, and commit/push.
- **Quick to correct**: if the agent operates on the wrong environment (local vs. production) or
  wrong server, he fires a short correction immediately, sometimes with exclamation marks.
- **Not micromanaging** on code details — prefers "can you check this?" over writing specs.
- **Protective of git**: explicitly told the agent "Next time you made changes to the code, let
  me commit." and flagged an autonomous commit as a rejection event.
- **Satisfied by results, not explanations**: celebrates with "Great!!" when something works;
  does not ask for post-fix summaries.

## Tone

Friendly but brisk. Uses smiley `":)"` occasionally. Enthusiastic when things work. Firm but
not aggressive when correcting. No profanity observed. Occasional celebratory emoji in
mid-session replies (`🎉` appears only in agent output, not his messages).
