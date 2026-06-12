# PREFERENCES — robouden

## Pushback distribution

| Type | Rate |
|---|---|
| non_pushback (accepts) | 45.9% |
| correction | 29.8% |
| failure_report | 22.2% |
| takeover | 1.3% |
| rejection | 0.8% |

Roughly half of all prompts accept the prior agent turn; the other half are corrections or
failure reports. Rejection is rare but pointed.

## What triggers corrections

- **Wrong environment**: agent runs checks locally when production was requested.
  `"We need to check on the porduction sever not locally!!!"`
- **Agent fabricates state**: claiming it lacks AWS access when it used it an hour earlier.
  `"Not true. You have been modifing aws setup one hor before!!"`
- **Autonomous git commits**: robouden wants to control when code is committed.
  `"Next time you made changes to the code, let me commit."` / `"Seems you did commit by yourselve?"`
- **Visual/UX regressions**: spacing, color, icons, favicon drift after agent changes.
  `"I want not green blue for the CSS.."` / `"[Image]\nBetetr, but can we remove the space between the header of the table and the data?"`
- **Oversimplified solutions**: `"Prefable wihtout bridge."` — agent proposed a workaround he
  didn't want.
- **Missing link or table format**: `"If sensors are shown in the answers, they shoul have a
  clickable link to the sensors on the simplemap.safecast.org."` / `"For this kind data we
  need to have it in a table format the be more readable."`
- **Scope creep after fix**: agent summarizes a long list of things done; robouden has already
  moved to the next issue without acknowledging the summary.

## What triggers failure reports

- Persistent visual bugs after a claimed fix (screenshot shows same problem).
- Services not deployed despite `✅ Deployed` message from agent.
- Streaming/UI hangs not resolved: `"[Image]\nSeems to get stuck in thinking?"`
- Large file uploads failing with auth errors after small file uploads worked.
- MCP server returning no data after agent said it was fixed.

## What satisfies him

- One-word or short confirmations work: `"yes"`, `"yes,,"`, `"Good idea to keep both running."`.
- When the fix is verifiable visually, he confirms briefly and moves on.
- Agent asking him to check and confirm works well — he runs the test himself and reports back.
- README and documentation updates after completing features (he often asks `"can you update the README.md?"`).

## Workflow habits

- **Batches visual fixes**: sends 2–3 UI issues in one numbered message.
- **Screenshots for bugs**: almost always attaches a screenshot rather than describing the bug in text.
- **Tests himself**: does hard-refresh, incognito windows, curl commands; reports results back.
- **Manual deploys sometimes**: `"I did reset the changes we made today and send tthe new build code to the production server."` — he sometimes deploys manually outside of CI.
- **Delegates commit+push when done**: `"Please build, commit and push the code."` — but only at session end or after explicit decision.
- **Interrupts long runs**: frequently cancels mid-flight with `[Request interrupted by user]`; resumes with a new directive.
- **No test-driven development**: test intent is only 0.9% — he relies on live testing and screenshots.
- **Documentation after features**: consistently asks to update README, commit docs, and push after completing a feature cluster.
- **Asks about architecture**: occasionally checks understanding: `"Would moving the MCP server to the map server speed up the queries?"` — wants a yes/no, not a lecture.

## Stack preferences visible in prompts

- Go (MCP server and map server are both Go binaries)
- PostgreSQL + PostGIS for spatial data
- DuckDB for analytics/logging inside MCP
- Nginx as reverse proxy
- AWS CloudFront + Route53 + ACM for CDN/SSL
- GitHub Actions for CI/CD (cross-compile + deploy)
- Ollama + Mistral for local AI testing
- Hetzner VPS as production host
- Mermaid diagrams for architecture documentation
