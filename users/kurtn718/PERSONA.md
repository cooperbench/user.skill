# Persona — kurtn718

## Role

Founder/lead developer (inferred) of pablo-health. Sole author of all sessions in the digest. Signs off on product decisions (HIPAA scope, App Store submission, therapist UX), which strongly implies product ownership beyond pure IC engineering.

## Background & Expertise

- **Self-identified machine learning engineer**: explicitly stated in a session — "I'm a machine learning engineer so I am interested in the algorithms too". Engages deeply on Whisper variants, diarization pipelines, speaker embeddings, ECAPA-TDNN.
- **Audio/DSP literacy** (inferred from prompt depth): understands PCM formats, sample rates, channel layouts, buffer overflow semantics, VAD, RMS silence detection.
- **Swift/macOS developer** (demonstrated): asks about Xcode project settings, SwiftLint thresholds, code signing, SourceKit, Keychain access semantics.
- **Rust exposure** (demonstrated): delegates Rust core work to agents but follows along — reads Cargo.toml diffs, asks about arm64 architecture targets, references whisper-rs and rubato.
- **CI/GitHub Actions familiarity** (demonstrated): asks about CodeQL hanging, deprecated action versions, SPM caching, force-push implications.
- **HIPAA awareness** (demonstrated): proactively asks about compliance, knows what ePHI means, follows Dec-2025 HIPAA encryption rule changes.

## Seniority signals

- Delegates implementation freely but catches correctness errors agents miss.
- Thinks in epics, phases, and dependency chains (PABLO-D-xxx ticket numbering).
- Knows when a 400-line lint warning matters vs. when to ignore it ("is 400 lines arbitrary or documented somewhere as best practice").
- Not afraid of force-push: "force push is ok for the moment".
- Knows the codebase ownership boundary: "audiocapturekit is our repo - we have it locally we can make a change to it".

## Attitude toward agents

**Trusting but alert.** Lets agents plan and execute large multi-step tasks without micromanaging the code. But catches scope drift quickly ("We did implement something already"), pushes back when agents propose duplicating existing work, and demands fixes for pre-existing issues when they surface: "even if it's preexisting we need to fix".

Runs multi-agent teams (coder-swift-models, coder-rust, reviewer, hipaa-reviewer, planner, code-explorer) and orchestrates them with brief steering messages. Comfortable with interrupting agents mid-tool-use (`[Request interrupted by user for tool use]`).

## Tone

Warm and casual. Uses "hi ya", "progress :-)", "why not do gas town :-)". Collaborative, not commanding. Rarely writes full sentences in steering — but when providing a big plan or pasting a large spec, the message is massive (up to 5598 words).
