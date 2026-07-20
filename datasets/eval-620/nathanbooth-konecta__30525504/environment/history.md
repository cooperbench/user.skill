> AGENT

Could you clarify what you mean by "match on multiple tags"? Are you asking about:

1. **Helm image tags** - Using multiple image tags in your deployment (e.g., deploying different containers with different tags)?
2. **Git tags** - Matching multiple git tags in a CI/CD workflow trigger?
3. **Something else** - Like container registry tag filtering or ArgoCD image updater patterns?

The context of your selection shows a single `image.tag` field in your Helm values, which only accepts one value. But the answer depends on what you're trying to accomplish.