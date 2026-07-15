> DEVELOPER

Show the ".pdf" file ending in the FileList

> AGENT

Now let's typecheck and check the existing FileList tests for any that assert on file names.

> AGENT

No test file for FileList. Let me typecheck the frontend.

> AGENT

Typecheck passes. `FileList.tsx` now shows `file.name + '.pdf'` for the row text, its truncation tooltip, and the Drive-assignment field's accessible label — scoped to this component only, since the backend still strips the extension for other consumers.

> DEVELOPER

Why does the backend strip the ending?

> AGENT

The comment on `filetree.go:12` still says it plainly: `Name string \`json:"name"\` // filename without extension; display-only for now`. That's the original design decision from the commit that introduced local file scanning — since every file here is already known to be a `.pdf` (non-PDF files are filtered out before this point), the extension was treated as redundant noise for a *display* label, so it got stripped at the source. `Path` retains the real filename with extension for anything that actually needs it (upload, comparisons, etc.) — `Name` was only ever meant for showing the user something readable. The `"for now"` in the comment suggests it wasn't a deeply considered call, just a reasonable default at the time — which is exactly the gap your request today closed: it turns out users do want to see the `.pdf` ending in the list, so the display concatenates it back on rather than the backend needing to change (since nothing else consumes the extension-stripped form).

> DEVELOPER

But doesn't it then make sense to leave the extension in in the backend?

> AGENT

Good catch on my own approach — there's actually a real bug lurking in what I just did. The match at `filetree.go:77` is case-insensitive (`strings.ToLower(entryName)`), but the strip on line 88 uses `filepath.Ext(entryName)` on the *original-case* name. So a file like `Invoice.PDF` gets `Name = "Invoice"`, and my frontend fix now displays `Invoice.pdf` — silently wrong casing versus the real file on disk.

> AGENT

Yes — I'd actually now recommend reverting the frontend concatenation and fixing it in the backend instead. Reasoning: - The backend match is case-insensitive (`strings.ToLower(entryName)`) but the strip preserves original casing, so a real file named `Invoice.PDF` would get `Name = "Invoice"`, and my frontend fix would display `Invoice.pdf` — wrong casing versus the file on disk. Keeping the extension in the backend's `Name` avoids reconstructing it with an assumed lowercase suffix. - `Name` is already documented as "display-only for now" and its only consumer is `FileList.tsx`, so there's no other code relying on the stripped form — the change is contained to `filetree.go` (drop the `TrimSuffix`, update the comment) and `filetree_test.go` (its many assertions expect stripped names like `"misc"`, `"doc"`, etc., so they'd need `.pdf` appended). The tradeoff: it's a slightly bigger diff (touches Go + tests instead of just the one TS file) but it's a correctness fix, not just a preference — want me to make that swap?

> DEVELOPER

yes

> AGENT

Good, both imports still used. Now update the test assertions.

> AGENT

Now updating each file-name assertion to expect the extension:

> AGENT

All file-name assertions updated (the folder-name assertions for `sub.Name`, `a.Name`, `tree.Subgroups[i].Name` etc. stay untouched, since those are directory names, not files). Now revert the frontend concatenation.

> AGENT

Now let's run the Go tests and frontend typecheck.

> AGENT

Both pass. Let's confirm the final diff is clean.

> AGENT

`filetree.go` and `filetree_test.go` now carry the full change; `FileList.tsx` is back to its original state (no diff), since it no longer needs to reconstruct the extension itself. Go tests and the frontend typecheck both pass.

> DEVELOPER

commit

> AGENT

Diff confirmed clean — just the two Go files. Committing now.

> AGENT

That was the culprit — an apostrophe in the draft message tripped up the shell. Committed as `e86a4e8`.

> AGENT

Clean working tree.

> DEVELOPER

Now I'm wondering: What if the user has non-pdf files in the folder that's being processed for Drive upload? Scans could be stored as image files, or something else entirely. And he might want to upload those as well. Therefore, isn't it risky to only show PDF files?

> AGENT

That's the intended scope, not an oversight — the spec (`spec.md:168`) explicitly frames Drive Upload as "the step after Split mode: once PDFs are exported to a local folder, the user switches to Drive Upload to route each file." Every prior stage of this app (Merge, Split) only produces PDFs, so filtering to `.pdf` matches the rest of the pipeline rather than being an arbitrary restriction. If you do have stray scans sitting around as images (e.g. straight off a scanner before this app ever touches them), that'd be a real scope expansion, not a small tweak — there's no thumbnail/preview infrastructure for images (the PDF preview step you built uses `pdftoppm`/MuPDF-specific tooling), so it'd need its own design pass rather than just loosening the filename filter. Is that actually a workflow you have, or was this more of a "what if" check?