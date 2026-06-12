---
name: error-paste-redirect
description: How kurtn718 reports failures — pastes raw error output verbatim (build log, crash message, runtime error) with minimal or no commentary, sometimes preceded by a short context line.
---

When something breaks, kurtn718 drops the raw error into the chat. The format is:

**Bare paste with no preamble:**
> `"codeql fails"`
> `"build error"`

**Short context + paste:**
> `"more progress i guess - Failed to load patients: Pablo.PabloError.JsonParse(message: \"error decoding response body\")"`
> `"ok let's commit these.   when i click quick start - choose patent i get an auth error"`
> `"ok let's commit if we haven't.   i noticed buffer overflow - after 35 seconds apture state: capturing(duration: 35.465677976608276)\nBuffer overflow: dropping 256 oldest samples\nBuffer overflow: dropping 512 oldest samples"`

**Full raw log when it's complex (no trimming):**
Pastes full cmake output, Xcode linker errors, Rust build failures — hundreds of lines — with no summarization. Example:
> `"Showing Recent Issues\n  --- stderr\n\n  running: cd \"/Users/kurtn/Developer/pablo-companion/core/target/debug/build/whisper-rs-sys-ebadd62fcd262bde/out/build\" && CMAKE_PREFIX_PATH=\"\"..."`

**Key tells:**
- No "I'm getting the following error:" header — goes straight to the content.
- May include "- i'm thinking" or "- i want" appended after the paste to suggest a fix direction.
- Typos appear in the surrounding text ("apture state" for "capture state", "patent" for "patient") — the pasted error itself is verbatim.
