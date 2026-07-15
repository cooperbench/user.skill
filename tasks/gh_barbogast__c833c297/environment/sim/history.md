> DEVELOPER

Is it possible for you to: - warn me if the requested feature / change results in much churned code and should rather be split into separate implementation steps? - the context window is getting too full?

> AGENT

Two different answers here: **Large/churned changes** — yes, straightforward. This is already in your CLAUDE.md ("break checklist work into small, independently reviewable steps"), so I'm supposed to do this anyway. I can be more proactive about it: before starting an implementation, if it looks like it'll touch many files or produce a large diff, I'll flag that up front and propose splitting it into 1a/1b/1c-style steps rather than just doing it and letting you notice after the fact. **Context window filling up** — no, not reliably. I don't have a live "% of context used" signal I can introspect mid-conversation. Compression happens automatically at the harness level, and it's largely invisible to me too — I don't get a clean threshold to warn against. The best I could do is a rough heuristic ("this session has a lot of large file reads/long tool outputs, it's probably getting long"), but that's not a precise or trustworthy warning, so I'd rather not promise it as a feature. Want me to save the first one (proactively flag large diffs before implementing) as a standing preference in memory?

> DEVELOPER

Yes, with one addition: This doesn't only apply to checklist items in spec.md but also messages in the chat.

> AGENT

This is a distinct scenario (proactive warning before implementing an ad-hoc chat request, not spec checklist authoring), so I'll add a new memory rather than overload this one.

> AGENT

Saved. From now on, before implementing any non-trivial request — whether it's a spec.md checklist item or something you ask for directly in chat — I'll flag if it looks like it'll produce a large/churned diff and propose splitting it into smaller reviewable steps before writing code.

> DEVELOPER

Could you add this to claude.md?

> AGENT

Added to CLAUDE.md under Conventions, right after the checklist-splitting rule.