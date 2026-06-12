# Projects — kurtn718

## pablo-health/pablo-companion (dominant — 100% of sessions)

A HIPAA-compliant macOS app for therapists that records, transcribes, and diarizes therapy sessions. The codebase is a Swift/SwiftUI frontend over a Rust core library, with a cross-platform audio capture library maintained separately.

### Tech stack

| Layer | Technology |
|---|---|
| macOS UI | Swift / SwiftUI (`mac/PabloCompanion/`) |
| Core logic | Rust (`core/`) compiled to dylib via UniFFI |
| Audio capture | `pablo-health/AudioCaptureKit` — own Swift package |
| Transcription | `whisper-rs` (whisper.cpp bindings) via Rust core |
| Diarization | 2-channel approach: mic=therapist, system audio=client |
| Auth | Firebase (OAuth token refresh, Keychain storage) |
| CI | GitHub Actions — SwiftLint strict, xcodebuild, CodeQL, SPM caching |
| Issue tracking | Beads (`bd`) with PABLO-D-xxx IDs |
| Backend | `pablo-health/pablo` (separate Go/Python service, Google Cloud Run) |

### Recurring themes

- **Audio pipeline**: PCM sidecar files, 48→16 kHz resampling, stereo→mono downmix, RMS silence detection, buffer overflow prevention, Whisper word timestamps.
- **Speaker diarization**: 2-channel recording (mic=therapist, system=client). Couples counseling (3-speaker) is a future goal.
- **HIPAA compliance**: AES-256-GCM encryption, Keychain key storage, HTTPS enforcement, no cleartext PHI, audit controls. Actively tracks Dec-2025 HIPAA encryption rule changes.
- **CI health**: CodeQL failures (Swift/Rust linker, CMake, deprecated actions), SwiftLint 400-line limits, SPM caching.
- **Beads workflow**: PABLO-D-xxx epics and tasks; close tickets after PR merge; multi-agent team execution on epics.
- **Branding pass**: Pablo bear mascot, custom color palette, Fraunces/DM Sans fonts, app icon from pablo-avatar.png.

### pablo-health/AudioCaptureKit (companion repo)

Their own Swift Package for macOS audio capture. Used as SPM dependency in pablo-companion. Kurtn718 owns this too and upgrades it directly when features are needed:
- "audiocapturekit is our repo - we have it locally we can make a change to it"
- Upgraded to v1.0.1 to add `exportRawPCM` / PCM sidecar feature.
- `CompositeCaptureSession`, `CaptureConfiguration`, `RecordingResult` are key types.
