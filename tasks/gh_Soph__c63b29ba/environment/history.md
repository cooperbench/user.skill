> DEVELOPER

can you review the branch / PR, i wonder if cobra hasn't better handling build in?

> AGENT

I'll look at the branch changes first to understand what was done.

> AGENT

Let me check for any other secret flags that might have been missed and read the full flags.go for context.

> AGENT

Let me verify the commands these helpers attach to are leaf commands (PreRunE only runs on the executed leaf command, not parents).

> AGENT

Reviewed the branch. The fix is correct and well-targeted. Here's my assessment, including the cobra question. ## Verdict: solid, ship it The root cause is real: `pflag` captures `DefValue` from `flag.Value.String()` at registration time, and `FlagUsages` prints `(default "…")` for any non-empty default — both in `--help` and in the usage block dumped on a parse error. Seeding the env value as the flag default therefore leaks it (into CI logs, etc.). The fix — register secret flags with an empty default and apply the env value post-parse in `PreRunE`, gated on `Changed()` so an explicit flag wins — is the right shape. Tests pass and cover both the leak and the fallback/precedence behavior. The `chainPreRunE` extraction is necessary, not incidental: previously `allRefsFlag` *replaced* `PreRunE`, so now that multiple helpers (`allRefsFlag` + several `addSecretFlag`) attach to the same command, clobbering would be a real bug. They all chain correctly, and their effects are independent (bools vs. distinct string targets), so ordering is safe. I also verified the **parent/child PreRunE trap doesn't apply here**: cobra only runs the executed leaf command's `PreRunE` (not parents'). All auth flags attach to leaf commands (`sync`, `replicate`, `plan`, `bootstrap`, `probe`, `fetch`, `convert`), each with its […]