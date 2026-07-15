> DEVELOPER

Do we have profile edit mutation? See ../hackerspub

> AGENT

Yes — there's an `updateAccount` mutation in hackerspub. **Location:** `../hackerspub/graphql/account.ts:496-602` (schema: `graphql/schema.graphql:1424-1443`) **Signature:** ```graphql mutation updateAccount(input: UpdateAccountInput!): UpdateAccountPayload! ``` **`UpdateAccountInput` editable fields:** - `id` (required), `username`, `name`, `bio` - `avatarUrl` — server fetches image from URL (JPEG/PNG/GIF/WebP); no separate upload mutation - `locales`, `links` (`[{name, url}]`) - Toggles: `hideFromInvitationTree`, `hideForeignLanguages`, `preferAiSummary` - Defaults: `defaultNoteVisibility`, `defaultShareVisibility` **Notes:** - No header/banner field. - No separate avatar upload mutation — you pass a URL that the server fetches.

> DEVELOPER

How we handle avatar upload then?

> AGENT

Here's the avatar upload flow: **No direct file upload endpoint** — `updateAccount.avatarUrl` accepts a `URL`, and on the web client that URL is just a **`data:` URL**. **Web flow** (`web-next/src/routes/[handle]/settings/index.tsx:200-324`): 1. User picks file via dropzone (5 MB limit) 2. Cropper.js crops in a dialog 3. `canvas.toDataURL()` → `data:image/...;base64,...` 4. Data URL passed directly as `avatarUrl` in `updateAccount` 5. Server fetches the data URL and stores it (validates MIME, transforms via `transformAvatar()`) **For Android**, you'd do the same: - Pick image → crop → encode as `data:image/jpeg;base64,<base64>` → pass as `avatarUrl` in `updateAccount`. Note: there's a separate `uploadMedia` mutation (`graphql/post.ts:1341-1398`) for post attachments which also takes a URL (data URL works) and returns a stored URL — but for avatars it's unused; the settings page just passes the data URL straight to `updateAccount`.