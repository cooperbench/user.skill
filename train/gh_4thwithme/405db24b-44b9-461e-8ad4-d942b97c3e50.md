> DEVELOPER

how to checkout to the last commit?

> AGENT

```bash
git checkout HEAD~1
```

Or to just look without detaching HEAD:

```bash
git log --oneline -5
```

Then `git checkout <commit-hash>`.
