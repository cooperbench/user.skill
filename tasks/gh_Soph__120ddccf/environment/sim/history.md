> DEVELOPER

We have a repo with 50k refs and we go this error: 2026/06/18 13:17:39 WARN Permanent sync error, terminating error="sync: replicate relay failed: replicate execute: push target refs: target receive-pack: post RPC stream body: http 400: https://marvin.aws-us-east-2.entire.internal:8281/git/repo/01KVCD01JNGDNFSACE4TA54ZGF/git-receive-pack [Content-Type=text/plain; charset=utf-8] too many ref-update commands: 55006 (limit 25000)"

> AGENT

I'll look into this. Let me explore the git-sync codebase to understand where this limit comes from and how the push is structured.

> AGENT

My initial exploration shows this is the git-sync Go library. Let me find both the limit definition and the push logic that triggers it.

> AGENT

I've launched a search agent. Let me wait for its findings before proposing a fix.

> AGENT

The error string isn't in git-sync — it's enforced server-side. The server is the `entire` backend. Let me search there while the agent examines the push path.