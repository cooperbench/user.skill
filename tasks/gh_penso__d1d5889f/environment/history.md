> DEVELOPER

Read https://github.com/moltis-org/moltis/issues/813 and plan for a fix, add a test

> TOOL

tool_use ToolSearch
id: toolu_01AEuGw3V1BuUkCQfLgNcCsW
```json
{
  "query": "select:WebFetch",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_01AEuGw3V1BuUkCQfLgNcCsW
```
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
```

> TOOL

tool_use Bash
id: toolu_017vQTFF76EEEXLXVWAnjdFY
```json
{
  "command": "gh issue view 813 --json title,body,labels,state,comments",
  "description": "Fetch GitHub issue #813 details"
}
```

> TOOL

tool_result
id: toolu_017vQTFF76EEEXLXVWAnjdFY
```
{"body":"### Preflight Checklist\n\n- [x] I have searched existing issues and this hasn't been reported yet\n- [x] I am using the latest version of Moltis\n- [x] If this happened during a chat session, I included as much full session context as possible and redacted secrets\n\n### What happened?\n\nWhen a user sends a `.md` file as a Telegram document to a MOLTIS bot, the file is silently dropped. The agent sees only `[Document: filename.md (application/octet-stream)]` as the message body — never the file contents — and responds as if nothing was attached.\n\nRoot cause: Telegram's Bot API doesn't include `.md` in its MIME type database and sends either no `mime_type` field or `application/octet-stream` for markdown files. In `crates/telegram/src/handlers/media.rs`, `extract_document_file` reads `d.document.mime_type` directly and defaults to `application/octet-stream` when absent. Then `is_supported_document_type(\"application/octet-stream\")` returns `false`, and the document text is never extracted.\n\nThe codebase already has `moltis_media::mime::mime_from_extension` in `crates/media/src/mime.rs` which correctly handles `.md` via `mime_guess` — but it is never called on the inbound Telegram document path.\n\n### Expected behavior\n\nWhen Telegram sends a document with an unrecognized `mime_type` (missing or `application/octet-stream`), MOLTIS should derive the MIME type from the filename extension using the existing `mime_from_extension` helper before deciding whether the document is supported. `.md` files […]

> AGENT

Good, clear issue. Let me explore the relevant code.

> TOOL

tool_use Glob
id: toolu_01TT2nqAAA296zNqJM2fRLx7
```json
{
  "pattern": "crates/telegram/src/handlers/media.rs"
}
```

> TOOL

tool_result
id: toolu_01TT2nqAAA296zNqJM2fRLx7
```
/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/media.rs
```

> TOOL

tool_use Glob
id: toolu_01V8qFkM456kAHFQUcEDTLEx
```json
{
  "pattern": "crates/media/src/mime.rs"
}
```

> TOOL

tool_result
id: toolu_01V8qFkM456kAHFQUcEDTLEx
```
/Users/penso/.superset/worktrees/moltis/abalone-place/crates/media/src/mime.rs
```

> TOOL

tool_use Grep
id: toolu_01RUPi1szSCeNqpJiKie3eQd
```json
{
  "pattern": "is_supported_document_type",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01RUPi1szSCeNqpJiKie3eQd
```
Found 3 files
crates/telegram/src/handlers/tests/media.rs
crates/telegram/src/handlers/media.rs
crates/telegram/src/handlers/implementation.rs
```

> TOOL

tool_use Grep
id: toolu_01MzTXuxpW4By6fYvdECd6F1
```json
{
  "pattern": "extract_document_file",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01MzTXuxpW4By6fYvdECd6F1
```
Found 3 files
crates/telegram/src/handlers/tests/media.rs
crates/telegram/src/handlers/media.rs
crates/telegram/src/handlers/implementation.rs
```

> TOOL

tool_use Read
id: toolu_01Gu4c2AzBXrGuHvbR8be85i
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/media.rs"
}
```

> TOOL

tool_result
id: toolu_01Gu4c2AzBXrGuHvbR8be85i
```
     1→use std::sync::Arc;
     2→
     3→use {
     4→    teloxide::{
     5→        prelude::*,
     6→        types::{MediaKind, MessageKind},
     7→    },
     8→    tracing::{debug, warn},
     9→};
    10→
    11→use {
    12→    moltis_channels::{
    13→        ChannelAttachment, ChannelDocumentFile, ChannelEventSink, ChannelMessageKind,
    14→        ChannelReplyTarget, SavedChannelFile,
    15→    },
    16→    moltis_common::types::ChatType,
    17→};
    18→
    19→use super::outbound_to_for_msg;
    20→
    21→use crate::Result;
    22→
    23→pub(super) fn extract_text(msg: &Message) -> Option<String> {
    24→    match &msg.kind {
    25→        MessageKind::Common(common) => match &common.media_kind {
    26→            MediaKind::Text(t) => Some(t.text.clone()),
    27→            MediaKind::Photo(p) => p.caption.clone(),
    28→            MediaKind::Document(d) => d.caption.clone(),
    29→            MediaKind::Audio(a) => a.caption.clone(),
    30→            MediaKind::Voice(v) => v.caption.clone(),
    31→            MediaKind::Video(vid) => vid.caption.clone(),
    32→            MediaKind::Animation(a) => a.caption.clone(),
    33→            _ => None,
    34→        },
    35→        _ => None,
    36→    }
    37→}
    38→
    39→pub(super) fn has_media(msg: &Message) -> bool {
    40→    match &msg.kind {
    41→        MessageKind::Common(common) => !matches!(common.media_kind, MediaKind::Text(_)),
    42→        _ => false,
    43→    }
    44→}
    45→
    46→#[allow(dead_code)]
    47→pub(super) fn extract_media_url(msg: &Message) -> Option<String> {
    48→    match &msg.kind {
    49→        MessageKind::Common(common) => match &common.media_kind {
    50→            MediaKind::Photo(p) => p.photo.last().map(|ps| format!("tg://file/{}", ps.file.id)),
    51→            MediaKind::Document(d) => Some(format!("tg://file/{}", d.document.file.id)),
    52→            MediaKind::Audio(a) => Some(format!("tg://file/{}", a.audio.file.id)),
    53→            MediaKind::Voice(v) => Some(format!("tg://file/{}", v.voice.file.id)),
    54→            MediaKind::Sticker(s) => Some(format!("tg://file/{}", s.sticker.file.id)),
    55→            _ => None,
    56→        },
    57→        _ => None,
    58→    }
    59→}
    60→
    61→pub(super) struct VoiceFileInfo {
    62→    pub(super) file_id: String,
    63→    pub(super) format: String, […]

> TOOL

tool_use Read
id: toolu_01LtQHtGvMKH39LPzJQWZXBe
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/media/src/mime.rs"
}
```

> TOOL

tool_result
id: toolu_01LtQHtGvMKH39LPzJQWZXBe
```
     1→use image::ImageFormat;
     2→
     3→/// MIME detection via buffer sniffing with header fallback.
     4→pub fn detect_mime(buffer: &[u8], headers: Option<&str>) -> String {
     5→    if let Some(mime) = sniff_image_mime(buffer) {
     6→        return mime.to_string();
     7→    }
     8→
     9→    if buffer.starts_with(b"%PDF-") {
    10→        return "application/pdf".to_string();
    11→    }
    12→    if buffer.starts_with(&[0x50, 0x4B, 0x03, 0x04]) {
    13→        return "application/zip".to_string();
    14→    }
    15→    if buffer.starts_with(&[0x1F, 0x8B]) {
    16→        return "application/gzip".to_string();
    17→    }
    18→
    19→    let trimmed = trim_ascii_start(buffer);
    20→    if trimmed.starts_with(b"{") || trimmed.starts_with(b"[") {
    21→        return "application/json".to_string();
    22→    }
    23→    if trimmed.starts_with(b"<!DOCTYPE html") || trimmed.starts_with(b"<html") {
    24→        return "text/html".to_string();
    25→    }
    26→    if trimmed.starts_with(b"<?xml") {
    27→        return "application/xml".to_string();
    28→    }
    29→    if let Some(header) = headers.and_then(parse_content_type_header) {
    30→        return header;
    31→    }
    32→    if std::str::from_utf8(buffer).is_ok() {
    33→        return "text/plain".to_string();
    34→    }
    35→
    36→    "application/octet-stream".to_string()
    37→}
    38→
    39→fn sniff_image_mime(buffer: &[u8]) -> Option<&'static str> {
    40→    let format = image::guess_format(buffer).ok()?;
    41→    Some(match format {
    42→        ImageFormat::Jpeg => "image/jpeg",
    43→        ImageFormat::Png => "image/png",
    44→        ImageFormat::Gif => "image/gif",
    45→        ImageFormat::WebP => "image/webp",
    46→        ImageFormat::Bmp => "image/bmp",
    47→        ImageFormat::Pnm => "image/x-portable-pixmap",
    48→        ImageFormat::Tiff => "image/tiff",
    49→        ImageFormat::Ico => "image/x-icon",
    50→        ImageFormat::Avif => "image/avif",
    51→        _ => return None,
    52→    })
    53→}
    54→
    55→fn trim_ascii_start(buffer: &[u8]) -> &[u8] { […]

> TOOL

tool_use Read
id: toolu_012b3cQCc5wZLqffKFXpV4WJ
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/tests/media.rs"
}
```

> TOOL

tool_result
id: toolu_012b3cQCc5wZLqffKFXpV4WJ
```
     1→use super::*;
     2→
     3→#[test]
     4→fn voice_messages_are_marked_with_voice_message_kind() {
     5→    let msg: Message = serde_json::from_value(json!({
     6→        "message_id": 1,
     7→        "date": 1,
     8→        "chat": { "id": 42, "type": "private", "first_name": "Alice" },
     9→        "from": {
    10→            "id": 1001,
    11→            "is_bot": false,
    12→            "first_name": "Alice",
    13→            "username": "alice"
    14→        },
    15→        "voice": {
    16→            "file_id": "voice-file-id",
    17→            "file_unique_id": "voice-unique-id",
    18→            "duration": 1,
    19→            "mime_type": "audio/ogg",
    20→            "file_size": 123
    21→        }
    22→    }))
    23→    .expect("deserialize voice message");
    24→
    25→    assert!(matches!(
    26→        message_kind(&msg),
    27→        Some(ChannelMessageKind::Voice)
    28→    ));
    29→}
    30→
    31→#[test]
    32→fn extract_document_file_from_message() {
    33→    let msg: Message = serde_json::from_value(json!({
    34→        "message_id": 2,
    35→        "date": 1,
    36→        "chat": { "id": 42, "type": "private", "first_name": "Alice" },
    37→        "from": {
    38→            "id": 1001,
    39→            "is_bot": false,
    40→            "first_name": "Alice",
    41→            "username": "alice"
    42→        },
    43→        "caption": "please review",
    44→        "document": {
    45→            "file_id": "doc-file-id",
    46→            "file_unique_id": "doc-unique-id",
    47→            "file_name": "pinned.html",
    48→            "mime_type": "text/html",
    49→            "file_size": 512
    50→        }
    51→    }))
    52→    .expect("deserialize document message");
    53→
    54→    let document = extract_document_file(&msg).expect("document should be extracted");
    55→    assert_eq!(document.file_id, "doc-file-id");
    56→    assert_eq!(document.media_type, "text/html");
    57→    assert_eq!(document.file_name.as_deref(), Some("pinned.html"));
    58→}
    59→
    60→#[test]
    61→fn extract_document_file_defaults_media_type_when_missing() {
    62→    let msg: Message = serde_json::from_value(json!({
    63→        "message_id": 3,
    64→        "date": 1,
    65→        "chat": { "id": […]

> AGENT

Now let me check how `extract_document_file` is used in the implementation to see the full call path.

> TOOL

tool_use Grep
id: toolu_01MLEJZ41vR6TKHwk5ZWnWu1
```json
{
  "pattern": "extract_document_file|is_supported_document_type|unsupported document type",
  "path": "crates/telegram/src/handlers/implementation.rs",
  "output_mode": "content",
  "context": 5
}
```

> TOOL

tool_result
id: toolu_01MLEJZ41vR6TKHwk5ZWnWu1
```
321-                    None,
322-                    None,
323-                )
324-            },
325-        }
326:    } else if let Some(document_file) = extract_document_file(&msg) {
327-        // Handle documents/files - only download supported types to avoid
328-        // wasting bandwidth on files we cannot process.
329-        let caption = text.clone().unwrap_or_default();
330-        let doc_label = format_document_label(
331-            document_file.file_name.as_deref(),
332-            &document_file.media_type,
333-        );
334-
335:        if !is_supported_document_type(&document_file.media_type) {
336-            debug!(
337-                account_id,
338-                media_type = %document_file.media_type,
339-                file_name = ?document_file.file_name,
340:                "skipping unsupported document type"
341-            );
342-            let body = if caption.is_empty() {
343-                doc_label
344-            } else {
345-                format!("{caption}\n{doc_label}")
```

> AGENT

Now I have the full picture. Here's the plan:

## Issue #813: Plan

**Root cause**: In `extract_document_file()` (`media.rs:123-143`), when Telegram sends `mime_type: null` or `"application/octet-stream"`, the code uses that value as-is. The existing `mime_from_extension()` helper in `crates/media/src/mime.rs` is never consulted, so `.md`, `.toml`, `.yaml`, etc. all get `application/octet-stream` → `is_supported_document_type()` returns `false` → file silently dropped.

**Fix** (single-function change in `extract_document_file`):

When the resolved MIME is `application/octet-stream`, derive a better MIME from the filename extension via `moltis_media::mime::mime_from_extension`. This matches the issue's suggested fix exactly.

```rust
// In extract_document_file(), after computing `raw`:
let media_type = if raw == "application/octet-stream" {
    d.document.file_name.as_deref()
        .and_then(|name| name.rsplit('.').next())
        .and_then(moltis_media::mime::mime_from_extension)
        .unwrap_or(&raw)
} else {
    &raw
};
```

**Test**: Add a unit test `extract_document_file_infers_mime_from_extension_for_octet_stream` that sends a document with `mime_type: "application/octet-stream"` and `file_name: "notes.md"`, asserts `media_type == "text/markdown"`.

Let me check that `moltis_media` is already a dependency of the telegram crate.

> TOOL

tool_use Grep
id: toolu_01SKThGniovbhi2pfYqoWc9e
```json
{
  "pattern": "moltis.media|moltis_media",
  "path": "crates/telegram",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01SKThGniovbhi2pfYqoWc9e
```
Found 4 files
crates/telegram/src/outbound/media.rs
crates/telegram/src/handlers/media.rs
crates/telegram/src/handlers/implementation.rs
crates/telegram/Cargo.toml
```

> AGENT

Good, already a dependency. Let me implement the fix.

> TOOL

tool_use Edit
id: toolu_014ngQ8sSDnivm1yJ1MUiWUk
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/media.rs",
  "old_string": "pub(super) fn extract_document_file(msg: &Message) -> Option<DocumentFileInfo> {\n    match &msg.kind {\n        MessageKind::Common(common) => match &common.media_kind {\n            MediaKind::Document(d) => {\n                let raw = d\n                    .document\n                    .mime_type\n                    .as_ref()\n                    .map(ToString::to_string)\n                    .unwrap_or_else(|| \"application/octet-stream\".to_string());\n                Some(DocumentFileInfo {\n                    file_id: d.document.file.id.clone(),\n                    media_type: normalize_media_type(&raw),\n                    file_name: d.document.file_name.clone(),\n                })\n            },\n            _ => None,\n        },\n        _ => None,\n    }\n}",
  "new_string": "pub(super) fn extract_document_file(msg: &Message) -> Option<DocumentFileInfo> {\n    match &msg.kind {\n        MessageKind::Common(common) => match &common.media_kind {\n            MediaKind::Document(d) => {\n                let raw = d\n                    .document\n                    .mime_type\n                    .as_ref()\n                    .map(ToString::to_string)\n                    .unwrap_or_else(|| \"application/octet-stream\".to_string());\n                let normalized = normalize_media_type(&raw);\n                // Telegram often sends application/octet-stream for file types\n                // it doesn't recognise (e.g. .md, .toml, .yaml). Fall back to\n                // extension-based detection so these documents aren't silently\n                // dropped.\n                let media_type = if normalized == \"application/octet-stream\" {\n                    d.document\n                        .file_name\n                        .as_deref()\n                        .and_then(|name| name.rsplit('.').next())\n                        .and_then(moltis_media::mime::mime_from_extension)\n                        .map(str::to_string)\n                        .unwrap_or(normalized)\n                } else {\n                    normalized\n                };\n                Some(DocumentFileInfo {\n                    file_id: d.document.file.id.clone(),\n                    media_type,\n                    file_name: d.document.file_name.clone(),\n                })\n            },\n            _ => None,\n        },\n        _ => None,\n    }\n}"
}
```

> TOOL

tool_result
id: toolu_014ngQ8sSDnivm1yJ1MUiWUk
```
The file /Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/media.rs has been updated successfully.
```

> AGENT

Now let me check what's at the end of the test file to see the imports and add the new test.

> TOOL

tool_use Grep
id: toolu_01MgvoybHXfWpZ8czAb1vJT6
```json
{
  "pattern": "^use |^#\\[cfg|^mod ",
  "path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/tests/media.rs",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01MgvoybHXfWpZ8czAb1vJT6
```
1:use super::*;
```

> TOOL

tool_use Grep
id: toolu_01F13K9BM1GNp1XV4o4dP372
```json
{
  "pattern": "^use |^mod |^#\\[cfg\"",
  "path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/tests",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01F13K9BM1GNp1XV4o4dP372
```
crates/telegram/src/handlers/tests/voice.rs:1:use super::*;
crates/telegram/src/handlers/tests/media.rs:1:use super::*;
crates/telegram/src/handlers/tests/location.rs:1:use super::*;
crates/telegram/src/handlers/tests/mod.rs:3:use {
crates/telegram/src/handlers/tests/mod.rs:11:use {
crates/telegram/src/handlers/tests/mod.rs:26:use crate::{
crates/telegram/src/handlers/tests/mod.rs:308:mod location;
crates/telegram/src/handlers/tests/mod.rs:309:mod media;
crates/telegram/src/handlers/tests/mod.rs:310:mod session;
crates/telegram/src/handlers/tests/mod.rs:311:mod voice;
crates/telegram/src/handlers/tests/session.rs:1:use super::*;
```

> AGENT

Let me find the end of the media test file and add the new test after the existing `extract_document_file_defaults_media_type_when_missing` test (since that's the most related one).

> TOOL

tool_use Read
id: toolu_015DoUaVuwtURuTH9baNRWCz
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/tests/media.rs",
  "offset": 58,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_015DoUaVuwtURuTH9baNRWCz
```
    58→}
    59→
    60→#[test]
    61→fn extract_document_file_defaults_media_type_when_missing() {
    62→    let msg: Message = serde_json::from_value(json!({
    63→        "message_id": 3,
    64→        "date": 1,
    65→        "chat": { "id": 42, "type": "private", "first_name": "Alice" },
    66→        "from": {
    67→            "id": 1001,
    68→            "is_bot": false,
    69→            "first_name": "Alice",
    70→            "username": "alice"
    71→        },
    72→        "document": {
    73→            "file_id": "doc-file-id",
    74→            "file_unique_id": "doc-unique-id",
    75→            "file_name": "payload.bin",
    76→            "file_size": 128
    77→        }
    78→    }))
    79→    .expect("deserialize document message");
    80→
    81→    let document = extract_document_file(&msg).expect("document should be extracted");
    82→    assert_eq!(document.media_type, "application/octet-stream");
    83→}
    84→
    85→#[test]
    86→fn should_inline_markdown_document_types() {
    87→    assert!(should_inline_document_text("text/markdown"));
```

> AGENT

Now I need to update the existing test (`.bin` with no mime should still be `application/octet-stream`) and add new tests for the extension fallback. The existing test is still correct — `.bin` has no known MIME mapping, so it stays `application/octet-stream`.

> TOOL

tool_use Edit
id: toolu_01Cf9zMMqKmFjZE1iNN8m8QX
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/tests/media.rs",
  "old_string": "#[test]\nfn should_inline_markdown_document_types() {",
  "new_string": "#[test]\nfn extract_document_file_infers_mime_from_extension_for_octet_stream() {\n    // Telegram sends application/octet-stream for .md files — we should\n    // derive text/markdown from the filename extension.\n    let msg: Message = serde_json::from_value(json!({\n        \"message_id\": 4,\n        \"date\": 1,\n        \"chat\": { \"id\": 42, \"type\": \"private\", \"first_name\": \"Alice\" },\n        \"from\": {\n            \"id\": 1001,\n            \"is_bot\": false,\n            \"first_name\": \"Alice\",\n            \"username\": \"alice\"\n        },\n        \"document\": {\n            \"file_id\": \"doc-md-file-id\",\n            \"file_unique_id\": \"doc-md-unique-id\",\n            \"file_name\": \"notes.md\",\n            \"mime_type\": \"application/octet-stream\",\n            \"file_size\": 256\n        }\n    }))\n    .expect(\"deserialize document message\");\n\n    let document = extract_document_file(&msg).expect(\"document should be extracted\");\n    assert_eq!(document.media_type, \"text/markdown\");\n    assert!(is_supported_document_type(&document.media_type));\n}\n\n#[test]\nfn extract_document_file_infers_mime_for_other_text_extensions() {\n    for (file_name, expected_mime) in [\n        (\"config.toml\", \"application/toml\"),\n        (\"data.yaml\", \"application/x-yaml\"),\n        (\"data.yml\", \"application/x-yaml\"),\n        (\"readme.txt\", \"text/plain\"),\n        (\"schema.json\", \"application/json\"),\n    ] {\n        let msg: Message = serde_json::from_value(json!({\n            \"message_id\": 5,\n            \"date\": 1,\n            \"chat\": { \"id\": 42, \"type\": \"private\", \"first_name\": \"Alice\" },\n            \"from\": {\n                \"id\": 1001,\n                \"is_bot\": false,\n                \"first_name\": \"Alice\",\n                \"username\": \"alice\"\n            },\n            \"document\": {\n                \"file_id\": \"doc-file-id\",\n                \"file_unique_id\": \"doc-unique-id\",\n                \"file_name\": file_name,\n                \"mime_type\": \"application/octet-stream\",\n                \"file_size\": 128\n            }\n        }))\n        .expect(\"deserialize document message\");\n\n        let document = extract_document_file(&msg).expect(\"document should be extracted\");\n        assert_eq!(\n            document.media_type, expected_mime,\n            \"expected {expected_mime} for {file_name}, got {}\",\n            document.media_type\n        );\n    }\n}\n\n#[test]\nfn extract_document_file_keeps_explicit_mime_when_not_octet_stream() {\n    // When Telegram provides a real MIME type, don't override it.\n    let msg: Message = serde_json::from_value(json!({\n        \"message_id\": 6,\n        \"date\": 1,\n        \"chat\": { \"id\": […]

> TOOL

tool_result
id: toolu_01Cf9zMMqKmFjZE1iNN8m8QX
```
The file /Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/tests/media.rs has been updated successfully.
```

> AGENT

Now let me verify the MIME values that `mime_guess` returns for these extensions to make sure the test expectations are correct.

> TOOL

tool_use Bash
id: toolu_01AujATqkEnCp1wEWhmGJqmZ
```json
{
  "command": "cargo test -p moltis-media mime_from_extension -- --nocapture 2>&1 | tail -20",
  "description": "Run mime_from_extension tests to verify MIME values",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_01AujATqkEnCp1wEWhmGJqmZ
```
   Compiling idna v1.1.0
   Compiling url v2.5.8
   Compiling rustls-webpki v0.103.10
   Compiling tokio-rustls v0.26.4
   Compiling rustls-platform-verifier v0.6.2
   Compiling hyper-rustls v0.27.7
   Compiling reqwest v0.13.2
   Compiling moltis-common v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/common)
   Compiling moltis-media v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/media)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 15.65s
     Running unittests src/lib.rs (target/debug/deps/moltis_media-f8838c015bf955de)

running 4 tests
test mime::tests::mime_from_extension_unknown_returns_none ... ok
test mime::tests::mime_from_extension_covers_images ... ok
test mime::tests::mime_from_extension_extras_from_mime_guess ... ok
test mime::tests::mime_from_extension_covers_documents ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 13 filtered out; finished in 0.00s
```

> AGENT

Let me quickly check what `mime_guess` actually returns for `md`, `toml`, `yaml`, `yml` since the exact string matters.

> TOOL

tool_use Bash
id: toolu_01DahmyULjydhhtoidbE1EZv
```json
{
  "command": "cargo test -p moltis-media --lib -- --nocapture 2>&1 | grep -E \"^test |^running\" ; echo \"---\" ; cat <<'RUST' > /tmp/check_mime.rs\nfn main() {\n    for ext in &[\"md\", \"toml\", \"yaml\", \"yml\", \"txt\", \"json\"] {\n        let result = mime_guess::from_ext(ext).first_raw();\n        println!(\"{ext} => {result:?}\");\n    }\n}\nRUST\n# Can't easily run standalone, let me just write a quick test\n",
  "description": "Check mime_guess values for extensions",
  "timeout": 10000
}
```

> TOOL

tool_result
id: toolu_01DahmyULjydhhtoidbE1EZv
```
running 17 tests
test image_ops::tests::test_format_to_media_type ... ok
test mime::tests::extension_for_mime_covers_documents ... ok
test mime::tests::detect_mime_sniffs_png_bytes ... ok
test mime::tests::detect_mime_prefers_sniffed_bytes_over_header ... ok
test mime::tests::extension_for_mime_covers_images ... ok
test mime::tests::extension_for_mime_unknown_returns_bin ... ok
test mime::tests::mime_from_extension_covers_documents ... ok
test mime::tests::mime_from_extension_covers_images ... ok
test mime::tests::mime_from_extension_extras_from_mime_guess ... ok
test mime::tests::detect_mime_falls_back_to_header ... ok
test mime::tests::mime_from_extension_unknown_returns_none ... ok
test mime::tests::round_trip_document_types ... ok
test mime::tests::round_trip_image_types ... ok
test image_ops::tests::test_needs_optimization_small_image ... ok
test image_ops::tests::test_get_image_metadata ... ok
test image_ops::tests::test_resize_no_change_needed ... ok
test image_ops::tests::test_optimize_for_llm_small_image ... ok
test result: ok. 17 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
---
```

> TOOL

tool_use Bash
id: toolu_01UVfJ2t1VAiKHR5CbtYUhPE
```json
{
  "command": "cargo test -p moltis-telegram extract_document_file_infers 2>&1 | tail -20",
  "description": "Run the new tests to check MIME values",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01UVfJ2t1VAiKHR5CbtYUhPE
```
test handlers::implementation::tests::media::extract_document_file_infers_mime_from_extension_for_octet_stream ... ok
test handlers::implementation::tests::media::extract_document_file_infers_mime_for_other_text_extensions ... FAILED

failures:

---- handlers::implementation::tests::media::extract_document_file_infers_mime_for_other_text_extensions stdout ----

thread 'handlers::implementation::tests::media::extract_document_file_infers_mime_for_other_text_extensions' (391056988) panicked at crates/telegram/src/handlers/tests/media.rs:144:9:
assertion `left == right` failed: expected application/toml for config.toml, got text/x-toml
  left: "text/x-toml"
 right: "application/toml"
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    handlers::implementation::tests::media::extract_document_file_infers_mime_for_other_text_extensions

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 110 filtered out; finished in 0.00s

error: test failed, to rerun pass `-p moltis-telegram --lib`
```

> AGENT

Fix the MIME expectation for `.toml`:

> TOOL

tool_use Edit
id: toolu_01TLFZ8PYQeaH26PqHJA6248
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/tests/media.rs",
  "old_string": "        (\"config.toml\", \"application/toml\"),\n        (\"data.yaml\", \"application/x-yaml\"),\n        (\"data.yml\", \"application/x-yaml\"),",
  "new_string": "        (\"config.toml\", \"text/x-toml\"),\n        (\"data.yaml\", \"text/x-yaml\"),\n        (\"data.yml\", \"text/x-yaml\"),"
}
```

> TOOL

tool_result
id: toolu_01TLFZ8PYQeaH26PqHJA6248
```
The file /Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/tests/media.rs has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01UShiymdNQfZrkUJRzLS7Sy
```json
{
  "command": "cargo test -p moltis-telegram extract_document_file 2>&1 | tail -20",
  "description": "Run all extract_document_file tests",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01UShiymdNQfZrkUJRzLS7Sy
```
   Compiling moltis-telegram v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.25s
     Running unittests src/lib.rs (target/debug/deps/moltis_telegram-a45f1f0625af4ca3)

running 5 tests
test handlers::implementation::tests::media::extract_document_file_from_message ... ok
test handlers::implementation::tests::media::extract_document_file_keeps_explicit_mime_when_not_octet_stream ... ok
test handlers::implementation::tests::media::extract_document_file_infers_mime_from_extension_for_octet_stream ... ok
test handlers::implementation::tests::media::extract_document_file_defaults_media_type_when_missing ... ok
test handlers::implementation::tests::media::extract_document_file_infers_mime_for_other_text_extensions ... ok

test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 107 filtered out; finished in 0.01s
```

> AGENT

All 5 tests pass. Now I should also consider: `.toml` and `.yaml` resolve to `text/x-toml` and `text/x-yaml`, but `should_inline_document_text()` doesn't include those. Let me check if those should be inlinable too — the issue says these are "all likely affected."

> TOOL

tool_use Read
id: toolu_01PbzJpbzimi4qDnDeWFwtrX
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/media.rs",
  "offset": 239,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01PbzJpbzimi4qDnDeWFwtrX
```
   239→        .filter(|text| !text.is_empty())
   240→    {
   241→        sections.push(text.to_string());
   242→    }
   243→    sections.join("\n\n")
   244→}
   245→
   246→pub(super) fn normalize_media_type(media_type: &str) -> String {
   247→    media_type
   248→        .split(';')
   249→        .next()
   250→        .unwrap_or(media_type)
   251→        .trim()
   252→        .to_ascii_lowercase()
   253→}
```

> TOOL

tool_use Read
id: toolu_01RTbvMVoBMkspDa7tdYZSYy
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/media.rs",
  "offset": 255,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01RTbvMVoBMkspDa7tdYZSYy
```
   255→pub(super) fn should_inline_document_text(media_type: &str) -> bool {
   256→    matches!(
   257→        media_type,
   258→        "text/html"
   259→            | "text/plain"
   260→            | "text/markdown"
   261→            | "text/x-markdown"
   262→            | "text/xml"
   263→            | "application/json"
   264→            | "application/xml"
   265→    ) || media_type.ends_with("+json")
   266→        || media_type.ends_with("+xml")
   267→}
   268→
   269→pub(super) fn is_pdf_document_type(media_type: &str) -> bool {
```

> AGENT

The `should_inline_document_text` function doesn't cover `text/x-toml` or `text/x-yaml`. These are plain-text config formats that should absolutely be inlinable. The fix for the main issue (#813) is the MIME detection in `extract_document_file`, but to fully solve the ".toml/.yaml are also affected" part, I should add those to `should_inline_document_text` as well. Let me also add a broader `text/*` catch — actually, that would be too broad. Let me just add the specific types.

> TOOL

tool_use Edit
id: toolu_01U5JEk7wbC1LACDTfopm19q
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/media.rs",
  "old_string": "pub(super) fn should_inline_document_text(media_type: &str) -> bool {\n    matches!(\n        media_type,\n        \"text/html\"\n            | \"text/plain\"\n            | \"text/markdown\"\n            | \"text/x-markdown\"\n            | \"text/xml\"\n            | \"application/json\"\n            | \"application/xml\"\n    ) || media_type.ends_with(\"+json\")\n        || media_type.ends_with(\"+xml\")\n}",
  "new_string": "pub(super) fn should_inline_document_text(media_type: &str) -> bool {\n    matches!(\n        media_type,\n        \"text/html\"\n            | \"text/plain\"\n            | \"text/markdown\"\n            | \"text/x-markdown\"\n            | \"text/xml\"\n            | \"text/csv\"\n            | \"text/x-toml\"\n            | \"text/x-yaml\"\n            | \"application/json\"\n            | \"application/xml\"\n            | \"application/toml\"\n            | \"application/yaml\"\n            | \"application/x-yaml\"\n    ) || media_type.ends_with(\"+json\")\n        || media_type.ends_with(\"+xml\")\n}"
}
```

> TOOL

tool_result
id: toolu_01U5JEk7wbC1LACDTfopm19q
```
The file /Users/penso/.superset/worktrees/moltis/abalone-place/crates/telegram/src/handlers/media.rs has been updated successfully.
```

> AGENT

Now run the full telegram test suite to make sure nothing is broken.

> TOOL

tool_use Bash
id: toolu_01GtiqpB54kSadjduBthnmpM
```json
{
  "command": "cargo test -p moltis-telegram 2>&1 | tail -30",
  "description": "Run all telegram tests",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01GtiqpB54kSadjduBthnmpM
```
test handlers::implementation::tests::voice::voice_empty_transcription_sends_direct_reply_and_skips_dispatch ... ok
test outbound::tests::telegram_html_to_plain_text_decodes_numeric_entities ... ok
test outbound::tests::telegram_html_to_plain_text_decodes_uppercase_hex_entities ... ok
test outbound::tests::telegram_html_to_plain_text_preserves_non_tag_angle_bracket_text ... ok
test outbound::tests::telegram_html_to_plain_text_preserves_preformatted_indentation ... ok
test outbound::tests::telegram_html_to_plain_text_strips_tags_and_decodes_entities ... ok
test plugin::tests::descriptor_coherence ... ok
test plugin::tests::security_config_update_immediately_affects_access_control ... ok
test plugin::tests::update_account_config_nonexistent_account_errors ... ok
test plugin::tests::security_update_config_does_not_cancel_polling ... ok
test plugin::tests::update_account_config_preserves_bot_token ... ok
test plugin::tests::update_account_config_updates_allowlist ... ok
test topic::tests::parse_chat_with_thread ... ok
test plugin::tests::update_account_config_preserves_otp_state ... ok
test topic::tests::parse_invalid_chat_id_is_err ... ok
test topic::tests::parse_invalid_thread_id_is_err ... ok
test topic::tests::parse_negative_chat_id ... ok
test topic::tests::parse_plain_chat_id ... ok
test outbound::tests::send_html_fallback_sends_plain_text_without_raw_tags ... ok
test markdown::tests::chunk_markdown_html_respects_limit ... ok
test handlers::implementation::tests::media::document_pdf_is_inlined_into_chat_body ... ok

test result: ok. 112 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s

   Doc-tests moltis_telegram

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

> AGENT

All 112 tests pass. Let me also run a quick format and clippy check on the changed files.

> TOOL

tool_use Bash
id: toolu_01NsUnMYktQ3aZpLbsZAwquu
```json
{
  "command": "cargo +nightly-2025-11-30 fmt --all -- --check 2>&1 | head -20",
  "description": "Check Rust formatting",
  "timeout": 30000
}
```

> TOOL

tool_result
id: toolu_01NsUnMYktQ3aZpLbsZAwquu
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_016XFBNV7wp3SimKQKuXaba2
```json
{
  "command": "just lint 2>&1 | tail -10",
  "description": "Run clippy lint check",
  "timeout": 180000
}
```

> TOOL

tool_result
id: toolu_016XFBNV7wp3SimKQKuXaba2
```
Command running in background with ID: b601pi83r. Output is being written to: /private/tmp/claude-501/-Users-penso--superset-worktrees-moltis-abalone-place/36c89018-c8ec-4ad7-a7a7-2fe78ec0b3a3/tasks/b601pi83r.output
```

> TOOL

tool_use ToolSearch
id: toolu_01EwiZc5u2GiQJcsZQna2sCv
```json
{
  "query": "select:TaskOutput",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_01EwiZc5u2GiQJcsZQna2sCv
```
{
  "type": "tool_reference",
  "tool_name": "TaskOutput"
}
```

> TOOL

tool_use TaskOutput
id: toolu_01KUZVg8cyKegp6ezdYq8fJJ
```json
{
  "task_id": "b601pi83r",
  "block": true,
  "timeout": 180000
}
```

> TOOL

tool_result
id: toolu_01KUZVg8cyKegp6ezdYq8fJJ
```
<retrieval_status>success</retrieval_status>

<task_id>b601pi83r</task_id>

<task_type>local_bash</task_type>

<status>completed</status>

<exit_code>0</exit_code>

<output>
    Checking moltis-tools v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/tools)
    Checking moltis-provider-setup v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/provider-setup)
    Checking moltis-memory v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/memory)
    Checking moltis-auth v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/auth)
    Checking moltis-qmd v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/qmd)
    Checking moltis-chat v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/chat)
    Checking moltis-code-index v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/code-index)
    Checking moltis-gateway v0.1.0 (/Users/penso/.superset/worktrees/moltis/abalone-place/crates/gateway)
      Timing report saved to /Users/penso/.superset/worktrees/moltis/abalone-place/target/cargo-timings/cargo-timing-20260421T110826.842386Z.html
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1m 36s
</output>
```

> AGENT

Clippy passes clean. Here's a summary of the changes:

## Summary

**Issue**: Telegram sends `application/octet-stream` (or no MIME type) for files it doesn't recognise — `.md`, `.toml`, `.yaml`, etc. The handler saw an unsupported MIME and silently dropped the file.

**Two changes in `crates/telegram/src/handlers/media.rs`:**

1. **`extract_document_file()`** (line ~123): When the resolved MIME is `application/octet-stream`, derive a better MIME from the filename extension using the existing `moltis_media::mime::mime_from_extension` helper. If that returns `None` (truly unknown extension like `.bin`), keep `application/octet-stream`.

2. **`should_inline_document_text()`** (line ~255): Added `text/csv`, `text/x-toml`, `text/x-yaml`, `application/toml`, `application/yaml`, `application/x-yaml` — config/data formats that are plaintext and should be inlined, covering the additional extensions the issue mentions.

**Three new tests in `crates/telegram/src/handlers/tests/media.rs`:**

| Test | What it verifies |
|------|-----------------|
| `extract_document_file_infers_mime_from_extension_for_octet_stream` | `.md` with `application/octet-stream` → `text/markdown`, and `is_supported_document_type` returns `true` |
| `extract_document_file_infers_mime_for_other_text_extensions` | `.toml`, `.yaml`, `.yml`, `.txt`, `.json` all get correct MIME from extension |
| `extract_document_file_keeps_explicit_mime_when_not_octet_stream` | Explicit MIME (e.g. `image/jpeg`) is never overridden |

All 112 telegram tests pass, formatting and clippy are clean.

> AGENT

Already retrieved that output — clippy passed clean. The fix is ready for commit whenever you'd like.