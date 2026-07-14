# Entire checkpoint backfill

Scripts synced from Seoul `/data/entire-backfill`.

The corpus is private and remains in SSE-KMS S3. These scripts discover and
clone `entire/*` checkpoint refs, choose the richest checkpoint for each
session, and parse native transcripts with
`../claude-crawl/native_transcript.py`.

Message text is never length-truncated. Source records written by the current
harvester retain system, user, assistant, tool, and thinking context. Repeated
transport-only progress and queue snapshots remain in the raw checkpoint but
are not promoted to transcript messages. Source records include:

```json
{"text_fidelity": "full", "parser_version": "swesimbench-native-transcript-2026-07-14.4"}
```

Rebuild the corpus before rebuilding v2; old shards produced by the previous
harvester contain a 300-word cap and are intentionally not refresh-safe.
