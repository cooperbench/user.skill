---
session_id: "nathanbooth-konecta/claude-code-backup|cf4554a8-d99c-43c1-980c-7bdaea76d66b"
developer: "gh:nathanbooth-konecta"
split: train
source: crawl
repo: nathanbooth-konecta/claude-code-backup
start_time: "2026-02-17T07:54:00.639Z"
n_turns: 50
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

review the backlog here, https://github.com/orgs/konecta-ix-applications/projects/7 and link any items bidirectionally between that board and this board https://github.com/orgs/konecta-ix-workloads/projects/1/views/1 that are relevant

> AGENT

I'll start by fetching the details from both GitHub project boards to understand what items are on each.

> AGENT

Let me read the full output from both boards.

> AGENT

The workloads board is very large. Let me extract just the titles and key info from both boards.

> AGENT

Now let me analyze both boards to identify the cross-references. Let me also extract the apps board items more clearly.

> AGENT

Good, now I have a clear picture of both boards. Let me verify I can comment on issues in both repos.

> AGENT

I have a clear picture of both boards. Let me now analyze the cross-board relationships and create the bidirectional links.

**Summary of boards:**
- **Apps board** (konecta-ix-applications #7): KonectaIQ product launch - gurus, content, LiteLLM, CrewAI, RAG, MCP requirements and staging readiness
- **Workloads board** (konecta-ix-workloads #1): IQ Portal infrastructure migration (Cloud Run -> GKE) - Terraform, Helm, ArgoCD, CI/CD, testing

The key overlaps are:
1. **Infrastructure readiness items** on the apps board (#95, #79, #75, #77) depend on GKE/GCP infrastructure patterns from the workloads board
2. **Requirements items** (#68, #74, #78, #84) inform what the workloads infrastructure needs to support
3. **Repo/CI patterns** (apps #90) follow patterns established in workloads (#16, #17)
4. **UAT testing** (apps #44, #96-100) correlates with workloads e2e testing (#81)

Let me create the bidirectional cross-references now. I'll add comments on both sides so GitHub creates automatic cross-links.

> AGENT

Apps-side comments done. Now the remaining apps-side requirements items, then the workloads-side comments.

> AGENT

Now the workloads-side comments to complete the bidirectional links.

> AGENT

All bidirectional links are created. Here's a summary of what was linked:

## Links created (16 cross-references total)

### Apps Board → Workloads Board (9 comments)

| Apps Issue | Linked To (Workloads) | Relationship |
|---|---|---|
| **#95** GCP ready for MCP deployment | #1, #4, #5, #8, #9 | Depends on GKE/GCP infra patterns |
| **#79** CrewAI available in Staging | #1, #4, #5 | Depends on GKE deployment patterns |
| **#75** RAG Engine available in Staging | #1, #4, #5 | Depends on GKE deployment patterns |
| **#77** GCS per Guru | #4, #10 | Depends on GCP IAM/secrets patterns |
| **#84** MCP requirements | #1, #4, #5, #8 | Infra requirements for MCP services |
| **#90** MCP repos on GitHub | #16, #17, #8, #43 | Repo/CI/CD pattern references |
| **#68** LiteLLM requirements | #1, #4, #5 | Infra deployment patterns |
| **#74** RAG requirements | #1, #4, #5 | Infra deployment patterns |
| **#78** CrewAI requirements | #1, #4, #5 | Infra deployment patterns |

### Workloads Board → Apps Board (7 comments)

| Workloads Issue | Linked To (Apps) | Relationship |
|---|---|---|
| **#1** GKE namespace dev-iqportal | #95, #79, #75, #68, #74, #78, #84 | Pattern used by launch services |
| **#4** GCP service accounts | #95, #79, #75, #77 | Pattern used by launch services |
| **#5** Workload Identity binding | #95, #79, #75 | Pattern used by launch services |
| **#8** OIDC for GitHub Actions | #95, #84, #90 | CI/CD pattern for MCP services |
| **#16** Create code repo | #90 | Repo creation pattern for MCP |
| **#26** Migrate IQ Portal source | General launch board reference | Migration prerequisite for launch |
| **#81** Run e2e UAT | #44, #96-#100 | Aligned UAT testing efforts |

GitHub will now show automatic cross-references on all linked issues, making the relationships visible from either board.

> AGENT

I need to start by checking if the PRP template exists, and then understand what feature you'd like me to create a PRP for.

> AGENT

Good, the template exists. Before I proceed, I need to know what feature you'd like me to generate a PRP for.

> AGENT

<thinking>
The user wants a PRP for shared/reusable GitHub Actions workflows that would be hosted in a `.github-private` repo (or similar) and reused by workload repos. Let me start Phase 1 with the preflight analysis.

Let me first read the PRP template to understand the expected structure, and the existing PRP for reference patterns.
</thinking>

Got it - a PRP for shared reusable GitHub Actions workflows hosted in a `.github-private` (or similar) repo, consumed by workload repos like this one. Let me start with Phase 1: Preflight Analysis.

> AGENT

<thinking>
Excellent analysis from the preflight agent. It found that shared workflows already exist in `konecta-ix-services/.github-private` and identified critical gaps. Let me ask the user the key clarification questions.
</thinking>

The preflight analysis found something important: **shared reusable workflows already exist** in `konecta-ix-services/.github-private` and are actively being called by this repo. Four workflows are already in production use:
1. `terraform-validate.yml`
2. `terraform-plan.yml`
3. `terraform-apply.yml`
4. `argocd-deploy.yml`

Before proceeding to deep research, I have critical gaps to clarify:

> AGENT

<thinking>
The user has clarified:
1. The `.github-private` repo is at `/home/nathan_booth/code/konecta-ix-services/.github-private` - I can access it
2. Only add new workflows (existing Terraform/ArgoCD workflows stay as-is)
3. Self-contained auth per workflow (each handles its own GCP auth)
4. Image promotion is both re-tag in AR + update Helm values

Now I need to proceed to Phase 2: Comprehensive Research. Let me:
1. Read the existing `.github-private` repo to understand interfaces and patterns
2. Do codebase research on the calling patterns in the workload repo
3. Determine if external research is needed

Let me start by exploring the `.github-private` repo and the workload repo's workflows.
</thinking>

Now I have the answers I need. Let me proceed to Phase 2: Comprehensive Research. I'll analyze the existing `.github-private` repo and the workload repo's calling patterns in parallel.

> AGENT

<thinking>
Excellent, very comprehensive codebase research. Now let me determine if external research is needed.

Based on the codebase findings:
- The existing shared workflow patterns are very clear and well-documented
- Docker build patterns exist in the crewai old workflows
- Image promotion patterns exist in the crewai old workflows
- Helm lint is a standard operation
- OIDC/WIF auth is already implemented

Do I need external research?
- GitHub reusable workflows - the patterns are already in the codebase
- Docker build+push actions - standard and well-known (docker/build-push-action@v6 already used)
- Trivy container scanning - already have IaC scanning, just different args
- Cosign signing - already used in crewai workflows
- Image re-tagging in AR - standard gcr.io/crane operations

I think this is mostly internal patterns + standard GitHub Actions knowledge. Let me check if there are any specific gaps:
1. `gcloud artifacts docker tags add` for image promotion/re-tagging - I should confirm the correct command
2. Whether cross-org workflow_call needs specific org settings

Actually, I think I have enough context from the codebase. The existing patterns provide complete templates. Let me skip external research and proceed to writing the PRP.

Let me now:
1. Read the existing PRP for format reference
2. Write the new PRP
3. Generate the task breakdown

Let me also quickly read the existing PRP and task file for this repo to understand the format conventions.
</thinking>

The codebase research is comprehensive. Based on the findings:
- **Skip external research**: All patterns exist in the codebase (Docker build, image promotion, Helm lint, OIDC auth)
- The existing `.github-private` repo has clear conventions to follow
- Reference implementations exist in crewai old workflows and platform-images

Let me read the existing PRP for format reference, then write the new PRP.

> AGENT

<thinking>
Now I have all the context I need. Let me now write the PRP document. I have:
1. The PRP template structure
2. The existing PRP as a format reference
3. Complete codebase research including all existing workflow interfaces
4. User's answers on scope, auth model, and promotion strategy

Let me now write the comprehensive PRP for shared GitHub Actions workflows.

The new workflows needed are:
1. `docker-build-push.yml` - Build, scan, sign, push Docker images to AR
2. `helm-lint.yml` - Helm lint + template validation
3. `image-promote.yml` - Re-tag image in AR + update Helm values in workload repo
4. `container-scan.yml` - Trivy vulnerability scanning for container images (or merge with docker-build-push)

Actually, let me think about whether container scanning should be separate or part of docker-build-push. Looking at the crewai reference, it's all in one workflow. I think for reusability, it makes sense to have:
1. `docker-build-push.yml` - Build + push + scan + sign (all-in-one)
2. `helm-lint.yml` - Helm lint + template validation
3. `image-promote.yml` - Re-tag + update values
4. Optionally: `helm-values-check.yml` - Validate generated Helm values match committed ones

Let me write the PRP now.
</thinking>

I now have all the context needed. Let me write the PRP document.

> AGENT

PRP written. Now let me generate the task breakdown.

> AGENT

The PRP and task breakdown are complete. Let me verify both files were saved correctly.

> AGENT

Both files are generated. Here's a summary of what was produced:

---

## PRP: Shared Reusable GitHub Actions Workflows

**Confidence Score: 8/10**

**Location**: `docs/prps/shared-github-actions-workflows.md`

### Scope: 4 New Workflows for `.github-private`

| Workflow | Purpose | GCP Auth |
|---|---|---|
| `docker-build-push.yml` | Build, Trivy scan, Cosign sign, push to AR | Yes (self-contained OIDC) |
| `helm-lint.yml` | Helm lint + template render validation | No |
| `helm-values-check.yml` | Validate generated values match committed | No |
| `image-promote.yml` | Re-tag in AR + PR to update config.json | Yes (self-contained OIDC) |

### Key Design Decisions

- **Auth model**: Each workflow handles GCP OIDC internally using `vars.GCP_PROJECT_NUMBER` + `vars.SERVICE_NAME` (mirrors `terraform-plan.yml` pattern)
- **Promotion**: Both re-tags in Artifact Registry AND creates a PR to update `config.json` in the workload repo
- **Conventions**: `z_` prefix, `workflow_call` trigger, `static-ip-runner`, structured outputs, `$GITHUB_STEP_SUMMARY`
- **No changes** to existing 4 workflows (Terraform validate/plan/apply + ArgoCD deploy)

### Task Breakdown

**Location**: `docs/tasks/shared-github-actions-workflows.md` (5 tasks)

```
T-001 (helm-lint) ────────────┐
                               ├──> T-003 (docker-build-push) ──> T-004 (image-promote) ──> T-005 (validation)
T-002 (helm-values-check) ────┘
```

T-001 and T-002 can be done in parallel (simplest, no GCP auth). T-003 is the most complex (OIDC + buildx + Trivy + Cosign). T-004 adds cross-repo PR creation. T-005 validates all workflows against conventions.

> TOOL

<bash-input> code .</bash-input>

> TOOL

<bash-stdout></bash-stdout><bash-stderr></bash-stderr>

> AGENT

I'll start by reading the PRP and task breakdown to understand the full scope, then execute.

> AGENT

Now let me read the reference workflow files I need to mirror exactly.

> AGENT

I have all reference files. Let me set up task tracking and start implementing. I'll create T-001 and T-002 in parallel first (simplest workflows), then T-003 and T-004.

> AGENT

Starting T-001 and T-002 in parallel — creating both simple workflows.

> AGENT

Now T-003 — the most complex workflow: `docker-build-push.yml`.

> AGENT

Now T-004 — the image promotion workflow.

> AGENT

Now T-005 — validate all 4 workflows against the PRP checklist.

> AGENT

All validation checks pass. Let me verify the final file listing.

> AGENT

The user has clarified the workflows should be in `konecta-ix-applications/.github-private`, not `konecta-ix-services/.github-private`. Let me check if that repo exists and move the files.

> AGENT

The directory exists but is empty — the repo needs to be cloned.

> AGENT

This repo has no `.github/workflows/` directory yet. Let me create the directory structure and copy the 4 new workflows there, then remove them from the services repo.

> AGENT

Now I need to update the workflow files to reference `konecta-ix-applications/.github-private` instead of `konecta-ix-services/.github-private` in any self-references or comments, and move them. Let me also check if the workflows reference the services org path internally.

> AGENT

Good — none of the new workflows reference `konecta-ix-services` internally (they're self-contained). I can copy them directly and remove from the services repo.

> AGENT

Now remove them from the services repo (they don't belong there).

> AGENT

Let me verify both repos are correct now.

> AGENT

Now let me re-run validation on the correct location.

> AGENT

Based on the conversation summary, the implementation of the 4 reusable GitHub Actions workflows is complete and validated in the correct location (`konecta-ix-applications/.github-private/.github/workflows/`). Let me verify the current state of the files.

> AGENT

All 4 reusable workflow files are in place at the correct location:

| Workflow | File | Size |
|----------|------|------|
| Docker Build Push | `docker-build-push.yml` | 11.6 KB |
| Helm Lint | `helm-lint.yml` | 5.8 KB |
| Helm Values Check | `helm-values-check.yml` | 3.7 KB |
| Image Promote | `image-promote.yml` | 10.5 KB |

The implementation from the PRP is complete. All 4 workflows are in `konecta-ix-applications/.github-private/.github/workflows/` with:

- **Self-contained GCP OIDC auth** (docker-build-push, image-promote) using the `vars.GCP_PROJECT_NUMBER` + `vars.SERVICE_NAME` pattern
- **`static-ip-runner`** as the runner for all workflows
- **`z_` naming prefix** for UI sorting
- **Step summaries** with markdown tables on every workflow
- **Trivy scanning + Cosign signing** on docker-build-push
- **Cross-repo PR creation** via GitHub App tokens on image-promote

The workflows have not been committed yet in the `konecta-ix-applications/.github-private` repo. Would you like me to commit and push these, or is there anything you'd like adjusted first?

> DEVELOPER

yes

> AGENT

4 new untracked files in `.github/workflows/`. I'll create a feature branch, commit, push, and open a PR.

> AGENT

The push failed because the current OAuth token doesn't have the `workflow` scope, which is required to push files under `.github/workflows/`. This is a GitHub restriction — pushing workflow files requires the `workflow` scope on the token.

To fix this, you'll need to either:

1. **Re-authenticate with the `workflow` scope**:
   ```
   gh auth login -s workflow
   ```

2. **Or use SSH instead of HTTPS** (if you have an SSH key configured with write access).

Want me to try `gh auth login -s workflow` to add the required scope?

> TOOL

<bash-input>gh auth login -s workflowg</bash-input>

> TOOL

<bash-stdout></bash-stdout><bash-stderr>
failed to authenticate via web browser: The scopes requested are invalid: workflowg. (invalid_scope)
</bash-stderr>

> TOOL

<bash-input>gh auth login -s workflow</bash-input>

> TOOL

<bash-stdout>! First copy your one-time code: 159C-9D0E
Open this URL to continue in your web browser: https://github.com/login/device
✓ Authentication complete.
! Authentication credentials saved in plain text
✓ Logged in as nathanbooth-konecta
! You were already logged in to this account</bash-stdout><bash-stderr></bash-stderr>

> DEVELOPER

ok, push now

> AGENT

Pushed. Let me create the PR.

> AGENT

PR created: https://github.com/konecta-ix-applications/.github-private/pull/1
