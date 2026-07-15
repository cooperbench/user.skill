> AGENT

Could you clarify what you mean by "match on multiple tags"? Are you asking about:

1. **Helm image tags** - Using multiple image tags in your deployment (e.g., deploying different containers with different tags)?
2. **Git tags** - Matching multiple git tags in a CI/CD workflow trigger?
3. **Something else** - Like container registry tag filtering or ArgoCD image updater patterns?

The context of your selection shows a single `image.tag` field in your Helm values, which only accepts one value. But the answer depends on what you're trying to accomplish.

> DEVELOPER

i want to match an image in the repo thats tagged both develop and latest

> AGENT

Container registries don't support multi-tag matching in a pull spec. You specify exactly one tag (or digest) when pulling an image.

If an image has both `develop` and `latest` tags, they point to the **same digest** — so pulling by either tag gives you the identical image:

```yaml
image:
  tag: "develop"   # same image as "latest" if both tags point to the same digest
```

If you need to **guarantee** you're getting a specific build rather than relying on mutable tags, use the **image digest** instead:

```yaml
image:
  tag: "sha256:abc123..."
```

You can find the shared digest with:

```bash
gcloud artifacts docker images list \
  europe-west1-docker.pkg.dev/kd-ix-eur-shr-artifacts/workload-images/kix-apps-konectaiq \
  --include-tags --format="table(digest,tags)"
```

This will show you which digest has both `develop` and `latest` tags attached.