> DEVELOPER

Show the ".pdf" file ending in the FileList

> AGENT

Now let's typecheck and check the existing FileList tests for any that assert on file names.

> AGENT

No test file for FileList. Let me typecheck the frontend.

> AGENT

Typecheck passes. `FileList.tsx` now shows `file.name + '.pdf'` for the row text, its truncation tooltip, and the Drive-assignment field's accessible label — scoped to this component only, since the backend still strips the extension for other consumers.