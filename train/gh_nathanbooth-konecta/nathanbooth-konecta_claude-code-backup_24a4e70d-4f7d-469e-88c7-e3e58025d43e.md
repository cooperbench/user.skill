---
session_id: "nathanbooth-konecta/claude-code-backup|24a4e70d-4f7d-469e-88c7-e3e58025d43e"
developer: "gh:nathanbooth-konecta"
split: train
source: crawl
repo: nathanbooth-konecta/claude-code-backup
start_time: "2026-02-06T17:24:23.391Z"
n_turns: 29
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Implement the following plan:

# Container Image Supply Chain - Implementation Plan

## Context

The `kix-platform-images` repository is empty and needs to become the container image supply chain for the KIX Platform. Currently, GKE workloads pull images directly from public registries (Docker Hub, Quay.io, etc.), which creates:

- **Rate limit risk** (Docker Hub anonymous: 100 pulls/6h)
- **No vulnerability scanning** before deployment
- **No audit trail** of which image versions are approved
- **Supply chain risk** from unvetted upstream changes

This pipeline mirrors approved upstream images into a shared GCP Artifact Registry (`kd-ix-eur-shr-artifacts`), providing a single controlled source for all GKE clusters to pull from.

## Current Image References (from infrastructure config)

| Image | Source | Used By |
|-------|--------|---------|
| `kong:3.5` | Docker Hub | Kong Gateway (dev/qa/prod) |
| `litellm/litellm-non_root:v1.81.0-stable` | Docker Hub | LiteLLM (dev/qa/prod) |
| `quay.io/argoproj/argocd:v2.13.3` | Quay.io | ArgoCD (shared) |
| `postgres` (various tags) | Docker Hub | Cloud SQL sidecar images |

## Architecture

```
Upstream Registries      GitHub Actions Runner        Artifact Registry
(Docker Hub, GHCR,  -->  (pull + retag + push)  -->  europe-west1-docker.pkg.dev/
 Quay.io, private)            |                        kd-ix-eur-shr-artifacts/
                              |                          approved-images/*
                         WIF (OIDC)                         |
                         No stored keys               GCP Container Scanning
                                                       (automatic on push)
                                                            |
                                                       GKE clusters pull
                                                       via cross-project IAM
```

**Target AR path:** `europe-west1-docker.pkg.dev/kd-ix-eur-shr-artifacts/approved-images`

## Files to Create

All files are new (repo is empty).

### 1. `images.yaml` - Image Manifest

Declarative YAML defining all images to sync. Grouped by source registry. Explicit version pins only (no `latest`/floating tags).

```
sources:
  - registry: dockerhub
    images:
      - name: kong              tags: ["3.5"]
      - name: litellm/litellm-non_root  target_name: litellm  tags: ["v1.81.0-stable"]
      - name: library/postgres  target_name: postgres  tags: ["16.2-alpine", "15.6-alpine"]
  - registry: ghcr
    images:
      - name: berriai/litellm   target_name: litellm-gateway  tags: ["main-v1.56.4"]
  - registry: quay
    images:
      - name: argoproj/argocd   target_name: argocd  tags: ["v2.13.3"]
```

Schema per source entry:
- `registry` - one of: `dockerhub`, `ghcr`, `quay`, `custom`
- `host` - required only for `custom` registries
- `auth` - boolean, whether to use credentials (default: false)
- `images[].name` - upstream image path
- `images[].target_name` - name in AR (defaults to last segment of name)
- `images[].tags` - explicit version list
- `images[].description` - human-readable note

### 2. `.github/workflows/sync-images.yml` - Primary Workflow

**Triggers:**
- `workflow_dispatch` - manual with optional `image_filter` and `dry_run` inputs
- `schedule` - weekly Sunday 04:00 UTC
- `push` to `main` when `images.yaml` changes

**Jobs:**
1. **`build-matrix`** - Parse `images.yaml` into a JSON matrix (one entry per image:tag pair)
2. **`sync`** - Matrix job (`max-parallel: 5`, `fail-fast: false`)
   - WIF auth to GCP (`google-github-actions/auth@v2`)
   - Configure Docker for AR (`gcloud auth configure-docker`)
   - Conditional source auth (per `matrix.registry` + `matrix.auth`)
   - `docker pull` source → `docker tag` for AR → `docker push` to AR
   - Job summary with source/target/status

### 3. `.github/workflows/validate-manifest.yml` - PR Validation

**Triggers:** Pull requests modifying `images.yaml`

**Jobs:**
1. **`validate`** - Run `scripts/validate-manifest.py`, check for duplicates, output manifest summary

### 4. `scripts/validate-manifest.py` - Schema Validator

Python script validating:
- Required fields present (`registry`, `images`, `tags`)
- Valid registry types
- `custom` registries have `host`
- No floating tags (`latest`, `stable`, `edge`)
- No empty tag lists

### 5. `.gitignore`

Standard Python/Docker ignores.

### 6. `CLAUDE.md`

Repository-specific guidance: manifest schema, how to add images, secrets reference, workflow triggers, WIF config pointer to infrastructure repo.

## GitHub Secrets Required

| Secret | Purpose | Required? |
|--------|---------|-----------|
| `WIF_PROVIDER` | WIF provider path for GCP auth | Yes |
| `WIF_SA` | Service account email | Yes |
| `DOCKERHUB_USERNAME` | Docker Hub auth (rate limits) | Optional |
| `DOCKERHUB_TOKEN` | Docker Hub PAT | Optional |
| `GHCR_TOKEN` | GHCR PAT (`read:packages`) | Only for private GHCR |
| `QUAY_USERNAME` / `QUAY_PASSWORD` | Quay.io auth | Only for private Quay |
| `CUSTOM_REGISTRY_USERNAME` / `CUSTOM_REGISTRY_PASSWORD` | Vendor registries | Per vendor |

## Infrastructure Prerequisites (kix-platform-infrastructure changes)

These are **not implemented in this repo** but documented as prerequisites. Include as `docs/infrastructure-prerequisites.md`:

### a) Create AR Repository
```hcl
resource "google_artifact_registry_repository" "approved_images" {
  project       = "kd-ix-eur-shr-artifacts"
  location      = "europe-west1"
  repository_id = "approved-images"
  format        = "DOCKER"
}
```

### b) WIF Pool for this Repo
Create in `kd-ix-eur-shr-artifacts` project:
- Service account: `github-images-shared@kd-ix-eur-shr-artifacts.iam.gserviceaccount.com`
- WIF Pool: `github-images-shared`
- Attribute condition: restrict to `konecta-ix-platform/kix-platform-images` repo, `refs/heads/main` branch
- Grant SA `roles/artifactregistry.writer` on the project
- Ensure `sts.googleapis.com` enabled on `kd-ix-eur-shr-artifacts`

### c) Cross-Project IAM for GKE
Each GKE node SA needs `roles/artifactregistry.reader` on `kd-ix-eur-shr-artifacts`:
- `kd-ix-eur-dev-gke` node SA
- `kd-ix-eur-qa-gke` node SA
- `kd-ix-eur-prod-gke` node SA
- `kd-ix-eur-shr-gke` node SA

## Vulnerability Scanning

Automatic - `containerscanning.googleapis.com` is already enabled on `kd-ix-eur-shr-artifacts`. Every image pushed to AR is scanned. Results viewable in GCP Console and via `gcloud artifacts docker images describe --show-all-metadata`.

## What This Does NOT Include (by design)

- **No Terraform** in this repo (infrastructure changes go to kix-platform-infrastructure)
- **No per-environment AR repos** (single shared repo, cross-project IAM)
- **No floating tags** (explicit pins only, updates via PRs)
- **No multi-arch handling** initially (uses `docker pull/tag/push`; can upgrade to `crane copy` later if needed)
- **No Binary Authorization attestation** (API enabled but attestation policy is future work)
- **No automatic version bumping** (future enhancement: scheduled workflow to check for updates and create PRs)

## Verification

1. Run `python scripts/validate-manifest.py images.yaml` locally
2. Trigger `sync-images.yml` manually with `dry_run: true` to validate auth and pulls
3. Trigger for real - verify images in AR: `gcloud artifacts docker images list europe-west1-docker.pkg.dev/kd-ix-eur-shr-artifacts/approved-images`
4. Verify vulnerability scan results in GCP Console
5. Test GKE pull: deploy test pod referencing AR image path

## Implementation Order

1. Create all files on a feature branch
2. Commit and push (triggers validate-manifest on PR)
3. Merge to main (triggers sync-images workflow)
4. Note: sync will fail until WIF is configured in infrastructure repo - this is expected


If you need specific details from before exiting plan mode (like exact code snippets, error messages, or content you generated), read the full transcript at: /home/nathan_booth/.claude/projects/-home-nathan-booth-code-konecta-ix-platform-kix-platform-images/24a4e70d-4f7d-469e-88c7-e3e58025d43e.jsonl

> AGENT

I'll implement all the files for the container image supply chain. Let me start by checking the current state of the repository.

> AGENT

Now let me create all the files. I'll start with the independent ones in parallel.

> AGENT

Now let me create the remaining supporting files in parallel.

> AGENT

Now let me verify the implementation by running the validator.

> AGENT

Let me also verify the workflow YAML is syntactically valid and the file structure looks right.

> AGENT

All files are created and validated. Here's a summary of what was implemented:

**Files created (6):**

| File | Purpose |
|------|---------|
| `images.yaml` | Declarative manifest — 6 image:tag pairs across 3 registries (dockerhub, ghcr, quay) |
| `.github/workflows/sync-images.yml` | Primary sync workflow — builds matrix from manifest, authenticates via WIF, pulls/retags/pushes to AR. Triggers on push to main, weekly schedule, and manual dispatch with `image_filter` and `dry_run` options |
| `.github/workflows/validate-manifest.yml` | PR validation — runs the schema validator and outputs a manifest summary |
| `scripts/validate-manifest.py` | Python validator — checks required fields, valid registries, no floating tags, no duplicates, custom registries have host |
| `.gitignore` | Standard Python/Docker/IDE ignores |
| `CLAUDE.md` | Repository guide — schema reference, how to add images, secrets list, workflow triggers |
| `docs/infrastructure-prerequisites.md` | Documents the AR repo, WIF, and cross-project IAM changes needed in kix-platform-infrastructure |

**Validation result:** `Validation passed. 6 image:tag pair(s) defined.`

**Next steps:**
1. Commit and push to a feature branch
2. Open a PR (triggers `validate-manifest.yml`)
3. Merge to main (triggers `sync-images.yml` — will fail until WIF is configured in infrastructure repo, as expected)

> DEVELOPER

ok commit that

> AGENT

All new files, no prior commits. Let me stage and commit.

> AGENT

Committed as `f59987b` — 7 files, 563 insertions. Working tree is clean.

> DEVELOPER

ok, push

> AGENT

Pushed to `origin/main`.

> TOOL

<bash-input>code .</bash-input>

> TOOL

<bash-stdout></bash-stdout><bash-stderr></bash-stderr>

> DEVELOPER

ok, that works, whats next in the plan

> AGENT

Everything in this repo is done. The remaining work is in `kix-platform-infrastructure` — the prerequisites documented in `docs/infrastructure-prerequisites.md`:

1. **Create the AR repository** — `approved-images` in `kd-ix-eur-shr-artifacts`
2. **Set up WIF** — service account (`github-images-shared@...`), WIF pool, and attribute condition restricting to this repo/branch
3. **Cross-project IAM** — grant `roles/artifactregistry.reader` to each GKE node SA (dev, qa, prod, shared)
4. **Set GitHub secrets** — `WIF_PROVIDER` and `WIF_SA` on this repo (plus optionally `DOCKERHUB_USERNAME`/`DOCKERHUB_TOKEN` to avoid rate limits)

Once WIF is configured, you can verify by triggering the sync workflow manually with `dry_run: true` to confirm auth works, then run it for real.

> DEVELOPER

it works! what next

> AGENT

The pipeline is running end-to-end. The high-impact next step is **updating workload image references** to actually pull from AR instead of public registries. In `kix-platform-infrastructure`, you'd change references like:

| Current | New (AR) |
|---------|----------|
| `kong:3.5` | `europe-west1-docker.pkg.dev/kd-ix-eur-shr-artifacts/approved-images/kong:3.5` |
| `litellm/litellm-non_root:v1.81.0-stable` | `.../approved-images/litellm:v1.81.0-stable` |
| `quay.io/argoproj/argocd:v2.13.3` | `.../approved-images/argocd:v2.13.3` |
| `postgres:16.2-alpine` | `.../approved-images/postgres:16.2-alpine` |

Beyond that, optional future enhancements from the plan:

- **Automatic version bumping** — a scheduled workflow that checks upstream for new versions and opens PRs
- **Multi-arch support** — switch from `docker pull/tag/push` to `crane copy` to preserve multi-platform manifests
- **Binary Authorization** — add attestation signing to the sync workflow so GKE enforces only AR images are deployed

Want to start updating the workload references, or tackle one of the other items?

> DEVELOPER

is it worth adding TRIVY scanning to the pipeline

> AGENT

Marginal value for this pipeline, honestly. GCP Container Analysis is already scanning every image on push to AR — you get CVE detection, continuous re-scanning when new CVEs are published, and it integrates with Binary Authorization if you go that route later.

**What Trivy would add:**
- **Pre-push gating** — block images with critical CVEs from entering AR at all
- **Visibility in GitHub** — scan results in the PR/workflow without needing GCP Console access
- **Language-level deps** — npm, pip, go module scanning (though less relevant for base images you're mirroring, not building)

**Why it's probably not worth it here:**
- You're mirroring upstream images, not building your own — if `kong:3.5` has a CVE, you likely still need to mirror it and handle policy at the deployment layer
- GCP Container Analysis already covers the CVE detection
- It adds runtime to every sync job and another thing to maintain
- Gating decisions are better enforced closer to deployment (admission controllers, Binary Authorization)

If you want GitHub-visible scan results, a lighter option would be a separate **reporting workflow** that queries GCP Container Analysis after sync and posts results to a PR or Slack — no duplicate scanning, just surfacing what GCP already found.

I'd prioritize Binary Authorization or updating the workload references over adding Trivy.

> DEVELOPER

and how can we cosign the images

> AGENT

Good fit for this pipeline. Since you already have WIF/OIDC set up, **keyless signing** is the cleanest approach — no key management, signatures are tied to the GitHub Actions identity via Sigstore's Fulcio CA.

You'd add two steps to the `sync` job in `sync-images.yml`, after the push:

```yaml
      - name: Install cosign
        if: env.DRY_RUN != 'true'
        uses: sigstore/cosign-installer@v3

      - name: Sign image
        if: env.DRY_RUN != 'true'
        env:
          COSIGN_EXPERIMENTAL: "1"
        run: |
          cosign sign --yes \
            "$AR_REGISTRY/$TARGET"
```

That's it. With `id-token: write` already in the workflow permissions, cosign uses the GitHub Actions OIDC token to get a short-lived certificate from Fulcio. The signature is stored in Rekor (public transparency log) and as an OCI artifact alongside the image in AR.

**Verification** would look like:

```bash
cosign verify \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp "github.com/konecta-ix-platform/kix-platform-images" \
  europe-west1-docker.pkg.dev/kd-ix-eur-shr-artifacts/approved-images/kong:3.5
```

**Enforcement at the cluster level** is where this pays off — Kyverno or GCP Binary Authorization can require valid cosign signatures before admitting a pod.

Want me to add this to the workflow?

> DEVELOPER

ok, lets do that

> AGENT

Now update CLAUDE.md to mention cosign signing and verification.

> AGENT

Done. Added two steps to the sync workflow (`sigstore/cosign-installer@v3` + `cosign sign --yes`) after push, and documented verification in CLAUDE.md.

The signing uses keyless mode — cosign picks up the GitHub Actions OIDC token (already available via `id-token: write` permission) to get a short-lived Fulcio certificate. Signatures are logged in Rekor and stored as OCI artifacts next to the image in AR. Skipped on dry runs.

> DEVELOPER

lets push

> AGENT

Branch protection requires a PR. Let me push to a feature branch and create one.

> AGENT

PR created: https://github.com/konecta-ix-platform/kix-platform-images/pull/1

Branch protection blocked the direct push to main, so it's on `feature/add-cosign-signing` ready for review and merge.

> DEVELOPER

can we create a workflow that allows end users to request images and adds them to a the images.yaml and raises a feature request?
