[DEVELOPER]: can you check why linting is failing in CI

[AGENT]: I'll check what's failing. Let me look at the CI config and check recent CI runs.

[AGENT]: The Lint job is failing. Let me get the logs.

[AGENT]: Let me find the actual lint error in the logs.

[AGENT]: It's a `gofmt` failure. Let me see the surrounding context.

[AGENT]: Found it. The `gofmt` lint check is failing because `internal/gitproto/smarthttp.go` isn't formatted. Let me verify locally and fix it.

[AGENT]: It's a trivial formatting issue — an extra blank line. Let me fix it.

[AGENT]: The CI lint failure was a `gofmt` issue, now fixed. **What was wrong:** The Lint job's `gofmt` check flagged `internal/gitproto/smarthttp.go` — it had a stray double blank line (two consecutive empty lines before `res, err := c.HTTP.Do(req)` around line 539). gofmt collapses consecutive blank lines to one. **Fix:** Ran `gofmt -w` on the file, which removed the extra blank line. The file is now clean. The change isn't committed yet. Want me to commit it (e.g. `gitproto: gofmt smarthttp.go`) and push so CI re-runs?