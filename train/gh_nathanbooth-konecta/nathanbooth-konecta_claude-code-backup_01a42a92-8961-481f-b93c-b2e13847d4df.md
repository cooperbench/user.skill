> AGENT

I can't add `bitnami/kubectl:latest` because this repository requires explicit version pins — no floating tags like `latest`, `main`, or `stable` are allowed.

Let me check the current available versions for bitnami/kubectl so I can suggest a specific tag.

> AGENT

The manifest requires explicit version pins — `latest` is not allowed. Looking at the current structure, I see images like `kong:3.5`, `postgres:16.2-alpine`, and `argocd:v2.13.3`.

There's also a complication: as of September 2025, [Bitnami's Docker Hub images](https://hub.docker.com/r/bitnami/kubectl) moved to a model where specific version tags require a commercial subscription — the free community tier primarily offers only the `latest` tag.

> AGENT

Let me find the specific tag format for bitnami/kubectl 1.32.x.

> AGENT

The search confirms that Bitnami's free community images now primarily only offer the `latest` tag — specific version tags require their commercial subscription. Since this repository doesn't allow floating tags, we have a few options:

> AGENT

This is proving difficult — Bitnami's free tier no longer offers versioned tags, and other popular kubectl images are outdated. Let me check the official Kubernetes distribution.

> AGENT

Here's the situation:

**Bitnami's kubectl no longer has versioned tags** in the free community tier — they only offer `latest`. This happened in September 2025 when they moved versioned images to their commercial subscription.

**Alternative options:**

| Image | Source | Status |
|-------|--------|--------|
| `registry.k8s.io/kubectl` | Official Kubernetes | Has versioned tags (1.32.x, etc.) but requires custom registry config |
| `d3fk/kubectl` | [Docker Hub](https://hub.docker.com/r/d3fk/kubectl) | Latest versioned tag is `v1.30` |
| `lachlanevenson/k8s-kubectl` | [Docker Hub](https://hub.docker.com/r/lachlanevenson/k8s-kubectl) | Outdated (stopped at v1.25) |

> AGENT

I'll add `d3fk/kubectl:v1.30` to the manifest.

> AGENT

Added `d3fk/kubectl:v1.30` to the manifest. Validation passed (7 image:tag pairs total).

> AGENT

Done. The image will be mirrored to `europe-west1-docker.pkg.dev/kd-ix-eur-shr-artifacts/approved-images/kubectl:v1.30` once merged.

Would you like me to commit this change?

> DEVELOPER

yes and raise a PR

> AGENT

I'll create a new branch from main for this change.

> AGENT

Done. PR created: https://github.com/konecta-ix-platform/kix-platform-images/pull/30
