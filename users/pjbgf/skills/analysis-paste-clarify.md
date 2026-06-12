---
name: analysis-paste-clarify
description: When the agent asks for clarification or misses context, pjbgf pastes the full static-analysis or code-review output verbatim instead of summarizing it. Triggers when the agent says "could you clarify" or similar.
---

pjbgf does not re-explain issues in their own words. When the agent requests clarification or
when an issue was identified by an external tool (static analyzer, code reviewer), the user
pastes the tool's raw output as their reply — severity labels, file paths with line ranges,
technical prose and all. No framing, no "here is the output", just the text block.

This means messages can suddenly jump from 2 words to 150 words when a clarification is needed.
The 152-word maximum in the stats is this pattern.

**Example:**

Agent said:
> "Could you clarify which two issues you'd like me to resolve?"

User replied (truncated):
> "Unused resolver field allocated in every FetchingTree Low Severity The resolver field (*BlobResolver) is allocated via NewBlobResolver(s) in every NewFetchingTree call and propagated in Tree(), but no FetchingTree method ever reads it. File() uses t.inner.File() as the existence check and t.fetch for fetching—t.resolver.HasBlob() and t.resolver.ReadBlob() are never called. This is dead code that wastes a heap allocation per FetchingTree instance. Additional Locations (2) cmd/entire/cli/checkpoint/fetching_tree.go#L44-L45 cmd/entire/cli/checkpoint/fetching_tree.go#L160-L161..."

The paste continues for the full issue list without additional commentary from the user.
