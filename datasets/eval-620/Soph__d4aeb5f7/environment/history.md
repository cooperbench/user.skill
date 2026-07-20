> DEVELOPER

can you review the branch /  PR, i wonder if cobra hasn't better handling build in?

> AGENT

I'll look at the branch changes first to understand what was done.

> TOOL

tool_use Bash
id: toolu_014ZUYrWCYEEP9reTbS5zj9b
```json
{
  "command": "git log --oneline main..HEAD && echo \"---DIFF---\" && git diff main...HEAD",
  "description": "Show branch commits and diff vs main"
}
```

> TOOL

tool_result
id: toolu_014ZUYrWCYEEP9reTbS5zj9b
```
7c042428 Pair secret-flag registration with its env fallback
493b6412 Stop credential tokens leaking into usage output
---DIFF---
diff --git a/cmd/git-sync/convert_sha256.go b/cmd/git-sync/convert_sha256.go
index b6fb589d..6568fd4b 100644
--- a/cmd/git-sync/convert_sha256.go
+++ b/cmd/git-sync/convert_sha256.go
@@ -74,12 +74,10 @@ submodule repository first and re-point .gitmodules.`,
 	cmd.Flags().BoolVar(&req.SourceFollowInfoRefsRedirect, "source-follow-info-refs-redirect",
 		envBool("GITSYNC_SOURCE_FOLLOW_INFO_REFS_REDIRECT"),
 		"send follow-up source RPCs to the final /info/refs redirect host")
-	cmd.Flags().StringVar(&req.SourceAuth.Token, "source-token",
-		envOr("GITSYNC_SOURCE_TOKEN", ""), "source token/password")
+	addSecretFlag(cmd, &req.SourceAuth.Token, "source-token", "GITSYNC_SOURCE_TOKEN", "source token/password")
 	cmd.Flags().StringVar(&req.SourceAuth.Username, "source-username",
 		envOr("GITSYNC_SOURCE_USERNAME", "git"), "source basic auth username")
-	cmd.Flags().StringVar(&req.SourceAuth.BearerToken, "source-bearer-token",
-		envOr("GITSYNC_SOURCE_BEARER_TOKEN", ""), "source bearer token")
+	addSecretFlag(cmd, &req.SourceAuth.BearerToken, "source-bearer-token", "GITSYNC_SOURCE_BEARER_TOKEN", "source bearer token")
 	cmd.Flags().BoolVar(&req.SourceAuth.SkipTLSVerify, "source-insecure-skip-tls-verify",
 		envBool("GITSYNC_SOURCE_INSECURE_SKIP_TLS_VERIFY"),
 		"skip TLS certificate verification for the source")
diff --git a/cmd/git-sync/flags.go b/cmd/git-sync/flags.go
index 3d81fbca..3366cee0 100644
--- a/cmd/git-sync/flags.go
+++ b/cmd/git-sync/flags.go
@@ -25,18 +25,18 @@ func addTargetEndpoint(cmd *cobra.Command, ep *gitsync.Endpoint) {
 }
 
 func addSourceAuth(cmd *cobra.Command, auth *gitsync.EndpointAuth) {
-	cmd.Flags().StringVar(&auth.Token, "source-token", envOr("GITSYNC_SOURCE_TOKEN", ""), "source token/password")
+	addSecretFlag(cmd, &auth.Token, "source-token", "GITSYNC_SOURCE_TOKEN", "source token/password")
 	cmd.Flags().StringVar(&auth.Username, "source-username", envOr("GITSYNC_SOURCE_USERNAME", "git"), "source basic auth username")
-	cmd.Flags().StringVar(&auth.BearerToken, "source-bearer-token", envOr("GITSYNC_SOURCE_BEARER_TOKEN", ""), "source bearer token")
+	addSecretFlag(cmd, &auth.BearerToken, "source-bearer-token", "GITSYNC_SOURCE_BEARER_TOKEN", "source bearer token")
 	cmd.Flags().BoolVar(&auth.SkipTLSVerify, "source-insecure-skip-tls-verify",
 		envBool("GITSYNC_SOURCE_INSECURE_SKIP_TLS_VERIFY"),
 		"skip TLS certificate verification for the source")
 }
 
 func addTargetAuth(cmd *cobra.Command, auth *gitsync.EndpointAuth) {
-	cmd.Flags().StringVar(&auth.Token, "target-token", envOr("GITSYNC_TARGET_TOKEN", ""), "target token/password")
+	addSecretFlag(cmd, &auth.Token, "target-token", "GITSYNC_TARGET_TOKEN", […]

> AGENT

Let me check for any other secret flags that might have been missed and read the full flags.go for context.

> TOOL

tool_use Bash
id: toolu_01F7ddNWG1HS9yRwtvpEZb3y
```json
{
  "command": "grep -rn \"TOKEN\\|Token\\|password\\|Password\\|secret\\|Secret\\|envOr\\|envBool\" cmd/git-sync/*.go | grep -vi \"_test.go\" | grep -i \"flag\\|token\\|env\\|secret\\|pass\"",
  "description": "Find all flag/secret/env registrations"
}
```

> TOOL

tool_result
id: toolu_01F7ddNWG1HS9yRwtvpEZb3y
```
cmd/git-sync/convert_sha256.go:75:		envBool("GITSYNC_SOURCE_FOLLOW_INFO_REFS_REDIRECT"),
cmd/git-sync/convert_sha256.go:77:	addSecretFlag(cmd, &req.SourceAuth.Token, "source-token", "GITSYNC_SOURCE_TOKEN", "source token/password")
cmd/git-sync/convert_sha256.go:79:		envOr("GITSYNC_SOURCE_USERNAME", "git"), "source basic auth username")
cmd/git-sync/convert_sha256.go:80:	addSecretFlag(cmd, &req.SourceAuth.BearerToken, "source-bearer-token", "GITSYNC_SOURCE_BEARER_TOKEN", "source bearer token")
cmd/git-sync/convert_sha256.go:82:		envBool("GITSYNC_SOURCE_INSECURE_SKIP_TLS_VERIFY"),
cmd/git-sync/flags.go:16:		envBool("GITSYNC_SOURCE_FOLLOW_INFO_REFS_REDIRECT"),
cmd/git-sync/flags.go:23:		envBool("GITSYNC_TARGET_FOLLOW_INFO_REFS_REDIRECT"),
cmd/git-sync/flags.go:28:	addSecretFlag(cmd, &auth.Token, "source-token", "GITSYNC_SOURCE_TOKEN", "source token/password")
cmd/git-sync/flags.go:29:	cmd.Flags().StringVar(&auth.Username, "source-username", envOr("GITSYNC_SOURCE_USERNAME", "git"), "source basic auth username")
cmd/git-sync/flags.go:30:	addSecretFlag(cmd, &auth.BearerToken, "source-bearer-token", "GITSYNC_SOURCE_BEARER_TOKEN", "source bearer token")
cmd/git-sync/flags.go:32:		envBool("GITSYNC_SOURCE_INSECURE_SKIP_TLS_VERIFY"),
cmd/git-sync/flags.go:37:	addSecretFlag(cmd, &auth.Token, "target-token", "GITSYNC_TARGET_TOKEN", "target token/password")
cmd/git-sync/flags.go:38:	cmd.Flags().StringVar(&auth.Username, "target-username", envOr("GITSYNC_TARGET_USERNAME", "git"), "target basic auth username")
cmd/git-sync/flags.go:39:	addSecretFlag(cmd, &auth.BearerToken, "target-bearer-token", "GITSYNC_TARGET_BEARER_TOKEN", "target bearer token")
cmd/git-sync/flags.go:41:		envBool("GITSYNC_TARGET_INSECURE_SKIP_TLS_VERIFY"),
cmd/git-sync/flags.go:102:// addSecretFlag registers a string flag whose value may also come from an
cmd/git-sync/flags.go:103:// environment variable. Unlike non-secret flags, it must NOT register the env
cmd/git-sync/flags.go:105:// the usage block dumped on a flag error, which would leak the secret (e.g.
cmd/git-sync/flags.go:107:// one call so a new secret flag cannot accidentally re-introduce the leak by
cmd/git-sync/flags.go:108:// reaching for envOr.
cmd/git-sync/flags.go:109:func addSecretFlag(cmd *cobra.Command, dst *string, name, env, usage string) {
cmd/git-sync/flags.go:111:	addSecretEnvFallback(cmd, name, dst, env)
cmd/git-sync/flags.go:114:// addSecretEnvFallback fills *dst from the named environment variable after
cmd/git-sync/flags.go:116:func addSecretEnvFallback(cmd *cobra.Command, flag string, dst *string, env string) {
cmd/git-sync/flags.go:129:	return protocolModeFlag(protocolMode(envOr("GITSYNC_PROTOCOL", validation.ProtocolAuto)))
cmd/git-sync/flags.go:132:func envOr(key, fallback string) string {
cmd/git-sync/flags.go:140:func envBool(key string) bool {
cmd/git-sync/probe.go:62:		envBool("GITSYNC_TARGET_FOLLOW_INFO_REFS_REDIRECT"),
```

> TOOL

tool_use Bash
id: toolu_015hjUH3XEHVuSL7u5XAvk3D
```json
{
  "command": "go test ./cmd/git-sync/ 2>&1 | tail -20",
  "description": "Run flag tests"
}
```

> TOOL

tool_result
id: toolu_015hjUH3XEHVuSL7u5XAvk3D
```
ok  	entire.io/entire/git-sync/cmd/git-sync	0.388s
```

> AGENT

Let me verify the commands these helpers attach to are leaf commands (PreRunE only runs on the executed leaf command, not parents).

> TOOL

tool_use Bash
id: toolu_01P2Wr2nEaYVV2QxMUpQpLRQ
```json
{
  "command": "grep -rn \"addSourceAuth\\|addTargetAuth\\|PreRunE\\|PersistentPreRun\\|AddCommand\\|RunE:\" cmd/git-sync/*.go | grep -v \"_test.go\" | grep -v \"flags.go\"",
  "description": "Map where auth helpers attach and command tree"
}
```

> TOOL

tool_result
id: toolu_01P2Wr2nEaYVV2QxMUpQpLRQ
```
cmd/git-sync/fetch.go:31:		RunE: func(cmd *cobra.Command, args []string) error {
cmd/git-sync/fetch.go:68:	addSourceAuth(cmd, &sourceAuth)
cmd/git-sync/convert_sha256.go:50:		RunE: func(cmd *cobra.Command, args []string) error {
cmd/git-sync/bootstrap.go:30:		RunE: func(cmd *cobra.Command, args []string) error {
cmd/git-sync/bootstrap.go:71:	addSourceAuth(cmd, &sourceAuth)
cmd/git-sync/bootstrap.go:72:	addTargetAuth(cmd, &targetAuth)
cmd/git-sync/root.go:26:		RunE: func(cmd *cobra.Command, _ []string) error {
cmd/git-sync/root.go:33:	cmd.AddCommand(newSyncCmd())
cmd/git-sync/root.go:34:	cmd.AddCommand(newReplicateCmd())
cmd/git-sync/root.go:35:	cmd.AddCommand(newPlanCmd())
cmd/git-sync/root.go:36:	cmd.AddCommand(newBootstrapCmd())
cmd/git-sync/root.go:37:	cmd.AddCommand(newProbeCmd())
cmd/git-sync/root.go:38:	cmd.AddCommand(newFetchCmd())
cmd/git-sync/root.go:39:	cmd.AddCommand(newConvertSHA256Cmd())
cmd/git-sync/root.go:40:	cmd.AddCommand(newVersionCmd())
cmd/git-sync/probe.go:29:		RunE: func(cmd *cobra.Command, args []string) error {
cmd/git-sync/probe.go:64:	addSourceAuth(cmd, &sourceAuth)
cmd/git-sync/probe.go:65:	addTargetAuth(cmd, &targetAuth)
cmd/git-sync/syncplan.go:44:		RunE: func(cmd *cobra.Command, args []string) error {
cmd/git-sync/syncplan.go:107:	addSourceAuth(cmd, &sourceAuth)
cmd/git-sync/syncplan.go:108:	addTargetAuth(cmd, &targetAuth)
```

> AGENT

Reviewed the branch. The fix is correct and well-targeted. Here's my assessment, including the cobra question.

## Verdict: solid, ship it

The root cause is real: `pflag` captures `DefValue` from `flag.Value.String()` at registration time, and `FlagUsages` prints `(default "…")` for any non-empty default — both in `--help` and in the usage block dumped on a parse error. Seeding the env value as the flag default therefore leaks it (into CI logs, etc.). The fix — register secret flags with an empty default and apply the env value post-parse in `PreRunE`, gated on `Changed()` so an explicit flag wins — is the right shape. Tests pass and cover both the leak and the fallback/precedence behavior.

The `chainPreRunE` extraction is necessary, not incidental: previously `allRefsFlag` *replaced* `PreRunE`, so now that multiple helpers (`allRefsFlag` + several `addSecretFlag`) attach to the same command, clobbering would be a real bug. They all chain correctly, and their effects are independent (bools vs. distinct string targets), so ordering is safe.

I also verified the **parent/child PreRunE trap doesn't apply here**: cobra only runs the executed leaf command's `PreRunE` (not parents'). All auth flags attach to leaf commands (`sync`, `replicate`, `plan`, `bootstrap`, `probe`, `fetch`, `convert`), each with its […]