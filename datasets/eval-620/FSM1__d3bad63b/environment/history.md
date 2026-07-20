> TOOL

tool_use Bash
id: toolu_01AjyCqixaRs4GfmYL4uKVgw
```json
{
  "command": "_GSD_SHIM_NAME=\"gsd-tools.cjs\"; _GSD_RUNTIME_ROOT=\"$(git rev-parse --show-toplevel 2>/dev/null || pwd)\"; GSD_TOOLS=\"${_GSD_RUNTIME_ROOT}/.claude/gsd-core/bin/${_GSD_SHIM_NAME}\"; gsd_run() { node \"$GSD_TOOLS\" \"$@\"; }; INIT=$(gsd_run query init.todos); if [[ \"$INIT\" == @file:* ]]; then INIT=$(cat \"${INIT#@file:}\"); fi; echo \"$INIT\"",
  "description": "Load todo context via GSD tools"
}
```

> TOOL

tool_result
id: toolu_01AjyCqixaRs4GfmYL4uKVgw
```
gsd-tools: warning: unknown config key(s) in .planning/config.json: created, notes — these will be ignored
{
  "commit_docs": true,
  "date": "2026-07-07",
  "timestamp": "2026-07-07T16:54:56.899Z",
  "todo_count": 77,
  "todos": [
    {
      "file": "2026-02-14-erc-1271-contract-wallet-authentication.md",
      "created": "2026-02-14",
      "title": "Add ERC-1271 contract wallet authentication support",
      "area": "auth",
      "path": ".planning/todos/pending/2026-02-14-erc-1271-contract-wallet-authentication.md"
    },
    {
      "file": "2026-02-22-crdt-ipns-inbox-sharing.md",
      "created": "2026-02-22T00:00",
      "title": "Research CRDT-based IPNS inbox for serverless share discovery",
      "area": "architecture",
      "path": ".planning/todos/pending/2026-02-22-crdt-ipns-inbox-sharing.md"
    },
    {
      "file": "2026-02-24-async-incremental-search-index.md",
      "created": "2026-02-24T23:30",
      "title": "Make search index build async/incremental for large vaults",
      "area": "ui",
      "path": ".planning/todos/pending/2026-02-24-async-incremental-search-index.md"
    },
    {
      "file": "2026-02-26-alternative-mfa-factor-types.md",
      "created": "2026-02-26T20:45",
      "title": "Add alternative MFA factor types",
      "area": "auth",
      "path": ".planning/todos/pending/2026-02-26-alternative-mfa-factor-types.md"
    },
    {
      "file": "2026-06-18-web-logger-redaction-and-faro-transport-unwired.md",
      "created": "2026-06-18T00:00:00.000Z",
      "title": "Web logger redaction interceptor missing and Faro transport never wired",
      "area": "observability",
      "path": ".planning/todos/pending/2026-06-18-web-logger-redaction-and-faro-transport-unwired.md"
    },
    {
      "file": "2026-06-20-e2e-helper-scripts-zeroize-userprivatekey.md",
      "created": "2026-06-20",
      "title": "Zeroize userPrivateKey and subFolderKey in E2E helper scripts",
      "area": "test-infra",
      "path": ".planning/todos/pending/2026-06-20-e2e-helper-scripts-zeroize-userprivatekey.md"
    },
    {
      "file": "2026-06-21-large-file-refactor-tier3-residue.md",
      "created": "2026-06-21",
      "title": "Large source-file refactor — remaining Tier-3 candidates (add tests first)",
      "area": "refactor",
      "path": ".planning/todos/pending/2026-06-21-large-file-refactor-tier3-residue.md"
    },
    {
      "file": "2026-06-22-desktop-e2e-recycle-bin-test-parity-sh-vs-ps1.md",
      "created": "2026-06-22T00:00:00.000Z",
      "title": "\"Desktop E2E recycle-bin: stronger bin-published assertion (API round-trip)\"",
      "area": "test-infra",
      "path": ".planning/todos/pending/2026-06-22-desktop-e2e-recycle-bin-test-parity-sh-vs-ps1.md"
    },
    {
      "file": "2026-06-22-periodic-kubo-ipfs-gc-on-staging.md",
      "created": "2026-06-22T22:01:24.000Z",
      "title": "Enable periodic Kubo IPFS garbage collection on staging",
      "area": "infra",
      "path": ".planning/todos/pending/2026-06-22-periodic-kubo-ipfs-gc-on-staging.md"
    },
    { […]

> AGENT

You have **77 pending todos**. Here they are, newest first:

**2026-07-07 (today)**
1. FUSE shared-scope-exit read-key rotation is fail-closed, not live-wired *(desktop-fuse-rotation)*
2. Deferred FUSE publish/concurrency hardening from Phase 69 ship review *(desktop-fuse)*
3. Cross-language node-codec KAT does not pin the file_iv string encoding (hex vs base64) *(crypto-kat-parity)*
4. SDK anti-rollback floor store is non-atomic under concurrency and blocks the async executor *(sdk-rotation-durability)*

**2026-07-06**
5. Phase 68.2 CodeRabbit hardening backlog (cache/freshness/a11y/tests) *(sdk)*
6. Promote the D-07 web/SDK boundary from a grep gate to an ESLint/CI rule *(web)*
7. Gate non-listing read facades (resolveNodeIdentity, resolveFileMetadata) with the ROT-07 floor *(sdk)*
8. Route SharedFolderRow drag-payload kind through the resolved listing *(web)*

**2026-07-04**
9. SealedChildRef size/modifiedAt display mirror lags after in-place replace/version *(sdk)*
10. Delete paths retain the removed child's WriteChildRef (write-chain growth) *(sdk)*
11. ipns.service.test.ts crashes at module-load (stale api-client mock) *(testing)*
12. Transient IPNS resolve miss in getWriteBodyParams can seal an empty write-body *(sdk)*
13. Nested write-share loses write capability on navigate-up / breadcrumb restore *(web)*
14. Owner sees stale/empty shared-out folder until they write to it *(web)*
15. Remove dead getShareKeys/resolveFolderIpnsPrivateKey folder-ipns path *(web)*
16. Rename in-memory ipnsPrivateKeyEncrypted → encryptedIpnsPrivateKey *(sdk)*
17. Shared-folder breadcrumb restore shows stale children (snapshot by […]