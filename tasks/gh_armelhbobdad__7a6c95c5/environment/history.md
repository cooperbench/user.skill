> DEVELOPER

I want to ship the next major release release @docs/_internal/RELEASING.md

> AGENT

I'll ship the next major release following the RELEASING.md playbook. First, let me scout the current state — versions, workflow health, and the pre-flight invariants the doc requires.

> TOOL

tool_use Bash
id: toolu_01HrbWFFLGGmcHcpRmYux9dv
```json
{
  "command": "git status --short && git log --oneline -5 && echo \"---LOCAL VERSION---\" && jq -r .version package.json && jq -r '.plugins[0].version' .claude-plugin/marketplace.json",
  "description": "Check git state and local versions"
}
```

> TOOL

tool_result
id: toolu_01HrbWFFLGGmcHcpRmYux9dv
```
d4a1df66 Merge pull request #443 from armelhbobdad/retire-export-count-threshold
01c33861 refactor(analyze-source): retire the unreachable export_count decomposition threshold
baf40c7f Merge pull request #442 from armelhbobdad/docs-compile-confidence-distribution
36e8d4e7 docs(create-skill): state the confidence_distribution binning rule at the compile step
44ba2c44 Merge pull request #441 from armelhbobdad/fix-confidence-distribution-invariant
---LOCAL VERSION---
1.9.0
1.9.0
```

> TOOL

tool_use Bash
id: toolu_01By7ksVWokHc1bwt5vxaHvw
```json
{
  "command": "npm view bmad-module-skill-forge dist-tags --json && echo \"---TIME---\" && npm view bmad-module-skill-forge time --json | jq '. | to_entries | last'",
  "description": "Check npm dist-tags and last publish time"
}
```

> TOOL

tool_use Bash
id: toolu_01DbsmS6F8dHpfbe9YXci9dR
```json
{
  "command": "gh api repos/armelhbobdad/bmad-module-skill-forge/actions/workflows --jq '.workflows[] | select(.name==\"Release\") | {name, state, path}' && echo \"---REMOTE VERSION---\" && gh api repos/armelhbobdad/bmad-module-skill-forge/contents/package.json --jq '.content' | base64 -d | jq -r .version && echo \"---RECENT RELEASES---\" && gh release list --limit 5",
  "description": "Check release workflow state, remote version, recent releases"
}
```

> TOOL

tool_result
id: toolu_01By7ksVWokHc1bwt5vxaHvw
```
{
  "alpha": "0.10.1-alpha.0",
  "rc": "1.0.0-rc.3",
  "latest": "1.9.0"
}
---TIME---
{
  "key": "1.9.0",
  "value": "2026-05-26T20:45:49.054Z"
}
```

> TOOL

tool_result
id: toolu_01DbsmS6F8dHpfbe9YXci9dR
```
{"name":"Release","path":".github/workflows/release.yaml","state":"active"}
---REMOTE VERSION---
1.9.0
---RECENT RELEASES---
Skill Forge (SKF) v1.9.0	Latest	v1.9.0	2026-05-26T20:45:52Z
Skill Forge (SKF) v1.8.0		v1.8.0	2026-05-25T16:56:42Z
Skill Forge (SKF) v1.7.0		v1.7.0	2026-05-25T04:38:24Z
Skill Forge (SKF) v1.6.0		v1.6.0	2026-05-21T17:18:04Z
Skill Forge (SKF) v1.5.1		v1.5.1	2026-05-20T16:15:22Z
```

> TOOL

tool_use Workflow
id: toolu_013F5Y4HNyy6ujrkaFJPkUGB
```json
{
  "script": "export const meta = {\n  name: 'v2-release-preflight',\n  description: 'Pre-flight verification before dispatching the v2.0.0 major release',\n  phases: [\n    { title: 'Verify', detail: 'parallel read-only checks per RELEASING.md' },\n  ],\n}\n\nconst CHECK_SCHEMA = {\n  type: 'object',\n  properties: {\n    pass: { type: 'boolean' },\n    findings: { type: 'array', items: { type: 'string' } },\n    blockers: { type: 'array', items: { type: 'string' }, description: 'Issues that must be resolved before dispatch' },\n  },\n  required: ['pass', 'findings', 'blockers'],\n}\n\nconst SCOPE_SCHEMA = {\n  type: 'object',\n  properties: {\n    commitCount: { type: 'number' },\n    breakingChanges: { type: 'array', items: { type: 'string' } },\n    features: { type: 'array', items: { type: 'string' } },\n    fixes: { type: 'array', items: { type: 'string' } },\n    majorWarranted: { type: 'boolean' },\n    assessment: { type: 'string' },\n  },\n  required: ['commitCount', 'breakingChanges', 'features', 'fixes', 'majorWarranted', 'assessment'],\n}\n\nphase('Verify')\n\nconst [invariants, ciHealth, repoState, scope] = await parallel([\n  () => agent(`You are verifying release-pipeline invariants for the repo at /home/armel/Projects/OSS/bmad-module-skill-forge (GitHub: armelhbobdad/bmad-module-skill-forge) per its docs/_internal/RELEASING.md. Run these READ-ONLY checks and report pass/fail per check:\n\n1. Single-root invariant: \\`grep -l 'id-token: write' .github/workflows/*.yaml .github/workflows/*.yml 2>/dev/null\\` — expected set is exactly docs.yaml and release.yaml.\n2. No v* push trigger in any workflow: \\`grep -A3 […]

> TOOL

tool_result
id: toolu_013F5Y4HNyy6ujrkaFJPkUGB
```
Workflow launched in background. Task ID: w892qa4sy
Summary: Pre-flight verification before dispatching the v2.0.0 major release
Transcript dir: /home/armel/.claude/projects/-home-armel-Projects-OSS-bmad-module-skill-forge/3ca42849-d777-42b0-b534-83867ba7ff74/subagents/workflows/wf_dedb5249-3af
Script file: /home/armel/.claude/projects/-home-armel-Projects-OSS-bmad-module-skill-forge/3ca42849-d777-42b0-b534-83867ba7ff74/workflows/scripts/v2-release-preflight-wf_dedb5249-3af.js
(Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/armel/.claude/projects/-home-armel-Projects-OSS-bmad-module-skill-forge/3ca42849-d777-42b0-b534-83867ba7ff74/workflows/scripts/v2-release-preflight-wf_dedb5249-3af.js"} to iterate without resending the script.)
Run ID: wf_dedb5249-3af
To resume after editing the script: Workflow({scriptPath: "/home/armel/.claude/projects/-home-armel-Projects-OSS-bmad-module-skill-forge/3ca42849-d777-42b0-b534-83867ba7ff74/workflows/scripts/v2-release-preflight-wf_dedb5249-3af.js", resumeFromRunId: "wf_dedb5249-3af"}) — completed agents return cached results.

You will be notified when it completes. Use /workflows to watch live progress.
```

> AGENT

Pre-flight verification is running — four parallel read-only checks per RELEASING.md:

1. **Invariants** — single-root workflow, `NPM_TOKEN: ""` defense-in-depth, zero-secret invariant, branch policy, `version_bump=major` input validity
2. **CI health** — main tip green, local == origin
3. **Repo state** — open PRs/issues, clean tree, CHANGELOG sanity
4. **Scope since v1.9.0** — breaking-change audit to confirm a major bump is warranted

Once it comes back clean, I'll confirm the **v2.0.0** dispatch with you before running `gh workflow run release.yaml -f version_bump=major --ref main` — the publish itself stays gated behind your two browser approvals (the `release` environment gate and the bot PR merge).

> AGENT

Pre-flight is back — three of four checks pass clean, but the scope audit flags something important. Let me read the full assessment and check the leftover state from a cancelled release run it spotted.

> TOOL

tool_use Bash
id: toolu_01NqD2n1rHbFFNx8tvdDvGVR
```json
{
  "command": "tail -c 1800 \"/tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/35600871-ad6f-4c41-8071-82c59eec462f/tasks/w892qa4sy.output\"",
  "description": "Read truncated tail of preflight scope assessment"
}
```

> TOOL

tool_result
id: toolu_01NqD2n1rHbFFNx8tvdDvGVR
```
tional-commit breaking markers: `git log v1.9.0..HEAD | grep -iE 'BREAKING|!:'` returns empty — no feat!:/fix!: subjects and no BREAKING CHANGE footers. I checked every plausible consumer-visible contract change and all are backward-compatible: (1) The deepwiki->forge-auto rename keeps `deepwiki` as a working deprecated alias (resolves to forge-auto + one-time notice); the sole deletion is docs/deepwiki.md, a docs page renamed to forge-auto.md, not a consumer command/API. (2) The scope.type enum is byte-identical between v1.9.0 and HEAD in both skill-brief.v1.json and skf-brief-result-envelope.v1.json (full-library, specific-modules, public-api, component-library, reference-app, docs-only) — the new whole-language reference shape rides on the existing reference-app value, exactly the 'light path' the team uses to avoid the ~25-file enum lockstep. (3) The only modified schema (skill-brief.v1.json) adds a single OPTIONAL `source` field whose own description states it is 'Absent on legacy/hand-authored entries' — additive, not required. (4) The validator-path change (SCHEMA_PATH sibling resolution) and `uv run <script>` idiom are internal-only. The headline change is an entirely NEW skf-campaign workflow (additive). The project's own CHANGELOG confirms the established convention: 1.7->1.8->1.9 were all MINOR feature releases with no breaking changes, mirroring this delta exactly. Note: package.json still reads 1.9.0 (not yet bumped), confirming the release has not been […]

> TOOL

tool_use Bash
id: toolu_019B1sVgKoKRZVjjCRUK2YeB
```json
{
  "command": "gh run list --workflow=release.yaml --limit 3 --json databaseId,status,conclusion,createdAt,headSha,displayTitle && echo \"---STRAY TAGS---\" && git fetch origin --tags --prune 2>&1 && git tag -l 'v*' --sort=-v:refname | head -3 && echo \"---STRAY BOT BRANCHES---\" && gh api 'repos/armelhbobdad/bmad-module-skill-forge/branches?per_page=100' --jq '.[].name' | grep -i 'release' || echo \"none\"",
  "description": "Inspect cancelled release run and check for stray tags or bot branches"
}
```

> TOOL

tool_result
id: toolu_019B1sVgKoKRZVjjCRUK2YeB
```
[{"conclusion":"cancelled","createdAt":"2026-06-04T15:51:20Z","databaseId":26963067033,"displayTitle":"Release","headSha":"d4a1df6640e18e0142573848df63109283e817f6","status":"completed"},{"conclusion":"success","createdAt":"2026-05-26T20:37:37Z","databaseId":26473737956,"displayTitle":"Release","headSha":"0fe17787a73af6c7413667e1483bef83e90eb68d","status":"completed"},{"conclusion":"success","createdAt":"2026-05-25T16:52:07Z","databaseId":26411083568,"displayTitle":"Release","headSha":"d64c9a2c19592a0efb8fdcca62fb71eeec354c94","status":"completed"}]
---STRAY TAGS---
v1.9.0
v1.8.0
v1.7.0
---STRAY BOT BRANCHES---
none
```

> TOOL

tool_use AskUserQuestion
id: toolu_01Bso4Z57k38wzUPoFj9eesC
```json
{
  "questions": [
    {
      "question": "The audit found zero breaking changes since v1.9.0 — strict semver says minor (v1.10.0), but you asked for a major (v2.0.0). Which cut should I dispatch?",
      "header": "Version bump",
      "multiSelect": false,
      "options": [
        {
          "label": "Major → v2.0.0",
          "description": "Milestone release headlined by skf-campaign. Semver-unorthodox (no breaking changes), and ^1.x range consumers won't auto-update past it."
        },
        {
          "label": "Minor → v1.10.0",
          "description": "Strict-semver correct for this delta; matches the 1.7/1.8/1.9 release pattern. Saves the 2.0 number for a real breaking change."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01Bso4Z57k38wzUPoFj9eesC
```
Your questions have been answered: "The audit found zero breaking changes since v1.9.0 — strict semver says minor (v1.10.0), but you asked for a major (v2.0.0). Which cut should I dispatch?"="But we replace onboard workflow with deepwiki and then forge-auto. Is it a breaking change?". You can now continue with these answers in mind.
```

> TOOL

tool_use Bash
id: toolu_01FkRoMT5emt57x9t1je3Egn
```json
{
  "command": "git log --oneline --all -i --grep='onboard' | head -20 && echo \"---FILE HISTORY---\" && git log --oneline --follow --diff-filter=ADR -- 'src/*onboard*' 'src/**/onboard*' 2>/dev/null | head -10",
  "description": "Find commits mentioning onboard workflow"
}
```

> TOOL

tool_result
id: toolu_01FkRoMT5emt57x9t1je3Egn
```
7db661e2 docs: round out campaign coverage and deepwiki/campaign troubleshooting
833a0269 docs: fix migration staleness and surface deepwiki + campaign entry points
68fda095 feat(campaign): onboard removal + v2.0 documentation
e562f4d1 feat: deepwiki pipeline alias + onboard deprecation
62cdd8b6 feat(skf-quick-skill): redirect free-form prose input to sibling skills before registry lookup
a967e84c fix(audit-skill): close three workflow gaps (#216, #217, #218) (#227) (#228)
7370b549 chore(docs): post-Epic-6 RELEASING.md polish (Story 6.3 deferreds) (#225)
45bed3aa chore(release): remove NPM_TOKEN repo secret + reconcile RELEASING.md (Story 6.3) (#224)
540fdda4 docs(release): pre-v1.0.0 readiness audit (Story 5.1)
67fc9f45 docs: audit and correct unverified assertions across docs/
06917a76 feat: contextual post-install notes for fresh install vs update
---FILE HISTORY---
```

> TOOL

tool_use Bash
id: toolu_01MULKgyoCjaZhbs9UmtEZqp
```json
{
  "command": "grep -rn -i 'onboard' src/ --include='*.md' --include='*.json' --include='*.py' --include='*.yaml' -l | head -10; echo \"---CURRENT ALIASES---\"; grep -rn -i 'onboard\\|deprecated' src/skf-help/ 2>/dev/null | grep -i 'onboard\\|alias' | head -10",
  "description": "Check if onboard still exists or aliases in current tree"
}
```

> TOOL

tool_result
id: toolu_01MULKgyoCjaZhbs9UmtEZqp
```
src/knowledge/skill-lifecycle.md
src/skf-forger/SKILL.md
src/skf-forger/.analysis/20260603-204315/report-data.json
src/skf-forger/.analysis/20260603-204315/quality-report.md
src/skf-quick-skill/references/resolve-target.md
src/skf-analyze-source/SKILL.md
---CURRENT ALIASES---
```

> TOOL

tool_use Bash
id: toolu_01RiULNhLvYDMoCDdpmPbL9k
```json
{
  "command": "for c in e562f4d1 68fda095; do echo \"=== $c ===\"; git log -1 --format='%ci %d' $c; git tag --contains $c | head -3; git branch -a --contains $c 2>/dev/null | head -5; done",
  "description": "Locate onboard commits relative to v1.9.0 tag and branches"
}
```

> TOOL

tool_result
id: toolu_01RiULNhLvYDMoCDdpmPbL9k
```
=== e562f4d1 ===
2026-05-26 20:10:28 +0400 
v1.9.0
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
=== 68fda095 ===
2026-05-27 06:08:10 +0400 
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```

> TOOL

tool_use Bash
id: toolu_015HN1JnG4hzj8iBRm8dEivo
```json
{
  "command": "git show --stat e562f4d1 | head -30; echo \"===========\"; git show --stat 68fda095 | head -40",
  "description": "Show what the onboard deprecation and removal commits changed"
}
```

> TOOL

tool_result
id: toolu_015HN1JnG4hzj8iBRm8dEivo
```
commit e562f4d1f61507830a5b1847bad09e91c609289a
Author: armel <armelhbobdad@gmail.com>
Date:   Tue May 26 19:06:41 2026 +0400

    feat: deepwiki pipeline alias + onboard deprecation
    
    Entire-Checkpoint: 534d94227689

 src/shared/references/pipeline-contracts.md | 9 ++++++++-
 src/skf-forger/SKILL.md                     | 8 +++++++-
 2 files changed, 15 insertions(+), 2 deletions(-)
===========
commit 68fda095e08f7c5d3c9e851f98877ed5472bb5a6
Author: armel <armelhbobdad@gmail.com>
Date:   Wed May 27 06:08:10 2026 +0400

    feat(campaign): onboard removal + v2.0 documentation
    
    Entire-Checkpoint: 1cdac80ff2d1

 docs/bmad-synergy.md                        |  13 ++++
 docs/campaign.md                            | 112 ++++++++++++++++++++++++++++
 docs/deepwiki.md                            |   4 +-
 docs/workflows.md                           |  57 ++++++++++----
 src/shared/references/pipeline-contracts.md |   3 +-
 src/skf-forger/SKILL.md                     |  13 ++--
 6 files changed, 179 insertions(+), 23 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_013amJGnKrcwCgDJpiqZYvZN
```json
{
  "command": "git show 68fda095 -- src/skf-forger/SKILL.md src/shared/references/pipeline-contracts.md | head -80",
  "description": "Show the onboard removal diff in forger and pipeline contracts"
}
```

> TOOL

tool_result
id: toolu_013amJGnKrcwCgDJpiqZYvZN
```
commit 68fda095e08f7c5d3c9e851f98877ed5472bb5a6
Author: armel <armelhbobdad@gmail.com>
Date:   Wed May 27 06:08:10 2026 +0400

    feat(campaign): onboard removal + v2.0 documentation
    
    Entire-Checkpoint: 1cdac80ff2d1

diff --git a/src/shared/references/pipeline-contracts.md b/src/shared/references/pipeline-contracts.md
index ac574504..7a14c0da 100644
--- a/src/shared/references/pipeline-contracts.md
+++ b/src/shared/references/pipeline-contracts.md
@@ -22,9 +22,10 @@ The forger also accepts common pipeline aliases:
 | `deepwiki` | `AN[auto] BS[auto] CS TS[min:90] EX` | Full zero-ceremony wiki-skill pipeline |
 | `forge` | `BS CS TS EX` | Full skill creation pipeline (brief through export) |
 | `forge-quick` | `QS TS EX` | Quick skill pipeline |
-| `onboard` | `AN CS TS EX` | Full brownfield onboarding (deprecated — use deepwiki) |
 | `maintain` | `AS US TS EX` | Maintenance cycle (audit → update → test → export) |
 
+**Note:** `campaign` is a standalone workflow invoked via `@Ferris campaign`, not a pipeline alias. It orchestrates its own multi-stage pipeline internally with dependency tracking and resume.
+
 ## Pipeline Rules
 
 1. **Left to right execution** — each workflow completes before the next begins
diff --git a/src/skf-forger/SKILL.md b/src/skf-forger/SKILL.md
index 19e0330d..05bf7118 100644
--- a/src/skf-forger/SKILL.md
+++ b/src/skf-forger/SKILL.md
@@ -43,8 +43,9 @@ Structured reports with inline AST citations during work — no metaphor, no com
 | 12 | EX | Package for distribution […]

> TOOL

tool_use Bash
id: toolu_01JzqJ3chwcUsBihDLH6UUko
```json
{
  "command": "grep -n -i -B2 -A4 'onboard' src/skf-forger/SKILL.md src/skf-quick-skill/references/resolve-target.md src/shared/references/pipeline-contracts.md 2>/dev/null | head -60",
  "description": "Check how onboard is handled in the current tree"
}
```

> TOOL

tool_result
id: toolu_01JzqJ3chwcUsBihDLH6UUko
```
src/skf-forger/SKILL.md-91-   > ⚠️ **`deepwiki` is now `forge-auto`.** The alias was renamed to avoid confusion with the DeepWiki MCP — this pipeline auto-forges a verified skill from source and does **not** call that MCP. `deepwiki` still works as a deprecated alias; prefer `forge-auto <repo-url>` going forward.
src/skf-forger/SKILL.md-92-
src/skf-forger/SKILL.md:93:   **Removed aliases:** If the parsed alias is `onboard`, do NOT expand it. Instead, HALT with:
src/skf-forger/SKILL.md-94-
src/skf-forger/SKILL.md:95:   > 🚫 **onboard has been removed.** Use `forge-auto <repo-url>` instead. forge-auto auto-scopes, auto-briefs, and tests at 90% quality. Run `forge-auto` with any GitHub URL, doc URL, or `--pin <version>`.
src/skf-forger/SKILL.md-96-
src/skf-forger/SKILL.md-97-2. **Validate the sequence** — check for anti-patterns (EX before TS, CS without BS, duplicates). If found, warn the user and ask to confirm or adjust. In `{headless_mode}`, warn but proceed.
src/skf-forger/SKILL.md-98-3. **Set `{headless_mode}` = true** — pipelines auto-activate headless mode for all workflows in the chain. The user committed to the sequence by providing it.
src/skf-forger/SKILL.md-99-4. **Execute left to right** — for each workflow in the sequence:
src/skf-quick-skill/references/resolve-target.md-69-**Otherwise — input looks like free-form prose, not a target:**
src/skf-quick-skill/references/resolve-target.md-70-
src/skf-quick-skill/references/resolve-target.md:71:The user typed something like "I want a skill that helps with onboarding" or "build me a brainstorming workflow" — quick-skill cannot resolve […]

> TOOL

tool_use Bash
id: toolu_01R1Mdq2q2JKMznVAiR8DSda
```json
{
  "command": "gh workflow run release.yaml -f version_bump=major --ref main && gh run list --workflow=release.yaml --limit 1 --json databaseId,status,createdAt,headSha",
  "description": "Dispatch the v2.0.0 major release workflow"
}
```

> TOOL

tool_result
id: toolu_01R1Mdq2q2JKMznVAiR8DSda
```
https://github.com/armelhbobdad/bmad-module-skill-forge/actions/runs/26963566693
[{"createdAt":"2026-06-04T16:00:09Z","databaseId":26963566693,"headSha":"d4a1df6640e18e0142573848df63109283e817f6","status":"queued"}]
```

> TOOL

tool_use Bash
id: toolu_015mEnXDLzXWNmaeFFL9eszL
```json
{
  "command": "gh run watch 26963566693 --exit-status; echo \"WATCH_EXIT=$?\"",
  "description": "Watch the v2.0.0 release run until completion",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_015mEnXDLzXWNmaeFFL9eszL
```
Command running in background with ID: byz0cksvd. Output is being written to: /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/35600871-ad6f-4c41-8071-82c59eec462f/tasks/byz0cksvd.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

🚀 **v2.0.0 release is in flight.** Two browser gates need you, in order:

1. **Now — `release` environment gate**: open the [run page](https://github.com/armelhbobdad/bmad-module-skill-forge/actions/runs/26963566693) → "Review deployments" → approve `release`
2. **In a few minutes — bot PR gate**: after the 7 required checks pass on the `release/bot/v2.0.0-26963566693` temp branch, either approve the bot PR or admin-bypass-merge it (your usual pattern per #209/#213)

Expected ~5–8 minutes end-to-end once both gates are cleared. I'm watching the run and will verify per RELEASING.md once it completes: `latest` → `2.0.0`, SLSA provenance non-null, GitHub Release not-prerelease, tag ancestry on main — then dispatch `install-smoke.yaml` for the NFR9 three-OS verification.

> AGENT

Run completed cleanly (exit 0). Running the full post-publish verification battery per RELEASING.md:

> TOOL

tool_use Bash
id: toolu_01WiC52MQpBAzrNTLKyuWqj2
```json
{
  "command": "tail -20 /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/35600871-ad6f-4c41-8071-82c59eec462f/tasks/byz0cksvd.output",
  "description": "Check final state of the release run watch"
}
```

> TOOL

tool_result
id: toolu_01WiC52MQpBAzrNTLKyuWqj2
```
  ✓ Commit version bump
  ✓ Generate release notes
  ✓ Push commit to temp branch
  ✓ Open bot PR
  ✓ Force-trigger required status checks on bot PR
  ✓ Cancel action_required pull_request runs on bot PR head
  ✓ Wait for required status checks
  ✓ Wait for PR approval or admin-bypass merge
  - Auto-merge bot PR
  - Wait for merge completion
  - Skip PR flow (non-main dispatch ref)
  ✓ Create and push tag
  ✓ Publish to npm via OIDC trusted publishing
  ✓ Create GitHub Release
  ✓ Summary
  ✓ Post Install uv
  ✓ Post Setup Node.js
  ✓ Post Checkout
  ✓ Complete job
WATCH_EXIT=0
```

> TOOL

tool_use Bash
id: toolu_01K64uXpGCiPoVSaniJ6qC34
```json
{
  "command": "npm view bmad-module-skill-forge dist-tags --json && echo \"---PROVENANCE---\" && npm view bmad-module-skill-forge@2.0.0 --json | jq '.dist.attestations'",
  "description": "Verify latest dist-tag flipped to 2.0.0 and SLSA provenance attached"
}
```

> TOOL

tool_use Bash
id: toolu_013HhHae2BUdnw6QiVgvgC2A
```json
{
  "command": "gh release view v2.0.0 --json tagName,isPrerelease && echo \"---TAG ANCESTRY---\" && git fetch origin --tags 2>&1 && git merge-base --is-ancestor \"$(git rev-parse 'v2.0.0^{}')\" origin/main && echo OK",
  "description": "Verify GitHub Release exists non-prerelease and tag is on main"
}
```

> TOOL

tool_result
id: toolu_01K64uXpGCiPoVSaniJ6qC34
```
{
  "alpha": "0.10.1-alpha.0",
  "rc": "1.0.0-rc.3",
  "latest": "2.0.0"
}
---PROVENANCE---
{
  "url": "https://registry.npmjs.org/-/npm/v1/attestations/bmad-module-skill-forge@2.0.0",
  "provenance": {
    "predicateType": "https://slsa.dev/provenance/v1"
  }
}
```

> TOOL

tool_result
id: toolu_013HhHae2BUdnw6QiVgvgC2A
```
{"isPrerelease":false,"tagName":"v2.0.0"}
---TAG ANCESTRY---
From https://github.com/armelhbobdad/bmad-module-skill-forge
   d4a1df66..88b0fd8a  main       -> origin/main
 * [new branch]        release/bot/v2.0.0-26963566693 -> origin/release/bot/v2.0.0-26963566693
 * [new tag]           v2.0.0     -> v2.0.0
OK
```

> TOOL

tool_use Bash
id: toolu_01HaksESgeaPEYkGQyDF5nLc
```json
{
  "command": "git pull --ff-only 2>&1 | tail -2 && jq -r .version package.json && jq -r '.plugins[0].version' .claude-plugin/marketplace.json && git log --oneline -3",
  "description": "Pull main and verify both version files at 2.0.0"
}
```

> TOOL

tool_use Bash
id: toolu_019sGdXnwnH88te3amehnqiv
```json
{
  "command": "gh pr list --state merged --head release/bot/v2.0.0-26963566693 --json number,title,mergedAt,state",
  "description": "Confirm the bot PR for v2.0.0 was merged"
}
```

> TOOL

tool_result
id: toolu_01HaksESgeaPEYkGQyDF5nLc
```
 package.json                    |  2 +-
 4 files changed, 53 insertions(+), 3 deletions(-)
2.0.0
2.0.0
88b0fd8a Merge pull request #444 from armelhbobdad/release/bot/v2.0.0-26963566693
2c243ea8 release: bump to v2.0.0
d4a1df66 Merge pull request #443 from armelhbobdad/retire-export-count-threshold
```

> TOOL

tool_use Bash
id: toolu_01BGFYV39qqwuyytDxuRkSHk
```json
{
  "command": "gh workflow run install-smoke.yaml -f version=latest --ref main && gh run list --workflow=install-smoke.yaml --limit 1 --json databaseId,status,createdAt",
  "description": "Dispatch NFR9 cross-platform install smoke test"
}
```

> TOOL

tool_result
id: toolu_019sGdXnwnH88te3amehnqiv
```
[{"mergedAt":"2026-06-04T16:06:35Z","number":444,"state":"MERGED","title":"release: bump to v2.0.0"}]
```

> TOOL

tool_result
id: toolu_01BGFYV39qqwuyytDxuRkSHk
```
https://github.com/armelhbobdad/bmad-module-skill-forge/actions/runs/26964044895
[{"createdAt":"2026-06-04T16:08:33Z","databaseId":26964044895,"status":"queued"}]
```

> AGENT

Everything checks out. Deleting the merged bot temp branch and watching the smoke test:

> TOOL

tool_use Bash
id: toolu_01TE2Axq8Jyxpnwh4d4fzB6c
```json
{
  "command": "git push --delete origin release/bot/v2.0.0-26963566693 && git fetch --prune origin 2>&1 | tail -2",
  "description": "Delete merged bot temp branch from origin"
}
```

> TOOL

tool_use Bash
id: toolu_01G9jPctZakexLxxhziaAMcL
```json
{
  "command": "gh run watch 26964044895 --exit-status; echo \"SMOKE_EXIT=$?\"",
  "description": "Watch the three-OS install smoke test",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_01TE2Axq8Jyxpnwh4d4fzB6c
```
To https://github.com/armelhbobdad/bmad-module-skill-forge.git
 - [deleted]           release/bot/v2.0.0-26963566693
```

> TOOL

tool_result
id: toolu_01G9jPctZakexLxxhziaAMcL
```
Command running in background with ID: b08fpxpd5. Output is being written to: /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/35600871-ad6f-4c41-8071-82c59eec462f/tasks/b08fpxpd5.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

## 🎉 v2.0.0 is live and verified

| RELEASING.md gate | Result |
|---|---|
| `latest` dist-tag | ✅ `2.0.0` (flipped from `1.9.0`; `rc`/`alpha` untouched) |
| SLSA L2 provenance (NFR4) | ✅ non-null, `https://slsa.dev/provenance/v1` |
| GitHub Release (NFR6) | ✅ `v2.0.0`, `isPrerelease: false` |
| Tag ancestry | ✅ `v2.0.0^{}` is ancestor of `origin/main` |
| Main advanced by 2 commits | ✅ `2c243ea8` (bump) + `88b0fd8a` (merge of bot PR #444) |
| `package.json` + `marketplace.json` | ✅ both `2.0.0`, pulled locally |
| Bot temp branch | ✅ `release/bot/v2.0.0-26963566693` deleted from origin |

**The breaking change justifying the major**: `onboard` pipeline alias removed (hard-halt with migration pointer to `forge-auto`), honoring the v1.9.0 deprecation notice that promised removal in v2.0.

**In flight**: [`install-smoke` run `26964044895`](https://github.com/armelhbobdad/bmad-module-skill-forge/actions/runs/26964044895) — the NFR9 three-OS verification (`npx bmad-module-skill-forge@latest --version` on ubuntu/windows/macos), dispatched well within the 1-hour window. I'll report the matrix when it completes; any failing leg routes through Rollback Playbook § Scenario B (deprecate + ship `2.0.1`).

> TOOL

tool_use Bash
id: toolu_011kWSsSikKVDq5uF22RQk1j
```json
{
  "command": "tail -15 /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/35600871-ad6f-4c41-8071-82c59eec462f/tasks/b08fpxpd5.output && echo \"---JOBS---\" && gh run view 26964044895 --json jobs --jq '.jobs[] | {name, conclusion}'",
  "description": "Confirm all three smoke-test matrix legs passed"
}
```

> TOOL

tool_result
id: toolu_011kWSsSikKVDq5uF22RQk1j
```
  ✓ Run npx bmad-module-skill-forge --version
  ✓ Post Setup Node
  ✓ Complete job
✓ smoke (ubuntu-latest) in 6s (ID 79561790340)
  ✓ Set up job
  ✓ Setup Node
  ✓ Run npx bmad-module-skill-forge --version
  ✓ Post Setup Node
  ✓ Complete job

ANNOTATIONS
! Node.js 20 actions are deprecated. The following actions are running on Node.js 20 and may not work as expected: actions/setup-node@v4. Actions will be forced to run with Node.js 24 by default starting June 16th, 2026. Node.js 20 will be removed from the runner on September 16th, 2026. Please check if updated versions of these actions are available that support Node.js 24. To opt into Node.js 24 now, set the FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true environment variable on the runner or in your workflow file. Once Node.js 24 becomes the default, you can temporarily opt out by setting ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
smoke (ubuntu-latest): .github#2

SMOKE_EXIT=0
---JOBS---
{"conclusion":"success","name":"smoke (macos-latest)"}
{"conclusion":"success","name":"smoke (windows-latest)"}
{"conclusion":"success","name":"smoke (ubuntu-latest)"}
```

> AGENT

## ✅ v2.0.0 shipped, verified, and smoke-tested — release complete

**NFR9 post-publish verification**: all three legs of [`install-smoke` run `26964044895`](https://github.com/armelhbobdad/bmad-module-skill-forge/actions/runs/26964044895) green —

| Leg | `npx bmad-module-skill-forge@latest --version` |
|---|---|
| ubuntu-latest | ✅ success |
| windows-latest | ✅ success |
| macos-latest | ✅ success |

**Full release record:**
- **npm**: `2.0.0` on `latest`, SLSA L2 provenance attached, published via OIDC trusted publishing
- **GitHub**: Release `v2.0.0` (not prerelease), tag anchored on bot PR #444's merge commit `88b0fd8a`
- **main**: advanced by exactly 2 commits, both version files at `2.0.0`, bot temp branch cleaned up
- **Why major**: `onboard` alias hard-removed (halts with `forge-auto` migration pointer) — fulfilling the v1.9.0 deprecation notice that promised removal in v2.0

One FYI from the smoke run's annotations, unrelated to the release: GitHub is deprecating Node 20 for actions — `actions/setup-node@v4` will be forced onto Node 24 starting **June 16, 2026** and Node 20 is removed from runners September 16, 2026. Your workflows using `setup-node@v4` may want a bump to `@v5`/Node 24 opt-in before then.