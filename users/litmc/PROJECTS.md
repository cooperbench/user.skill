---
# LitMc — Projects
---

## LitMc/gc-playground ★ (dominant — 100% of sessions)

**Purpose:** Raspberry Pi Pico firmware that bridges a GameCube controller to a Nintendo Switch 2
via the Joybus protocol, compensating for the Switch 2 GameCube Classics' nonlinear stick
remapping so that F-ZERO GX receives correct inputs.

**Tech stack:**

| Layer | Technology |
|-------|-----------|
| Firmware language | C++ (pico-sdk, cmake, ARM cross-compile) |
| Firmware target | Raspberry Pi Pico (RP2040) |
| Flash format | UF2 |
| Measurement tools | Python (`uv run`, `measurement_lib`, `tools/*.py`) |
| Data | CSV readings in `resources/switch2/` |
| Visualization | HTML/JS (transform_viewer.html in resources/) |
| CI | GitHub Actions (`build-all-examples`) |
| Code review | GitHub Copilot automated review + Teams |
| Multi-agent system | Claude Code Teams (`.claude/agents/`) |
| Docs | `docs/` markdown (hardware.md, measurements.md, transforms.md, remote-dev.md) |

**Recurring themes:**

1. **Coordinate transform pipeline.** The core technical problem: raw stick values (0–255)
   pass through Switch 2's nonlinear octagon-clamping transform S. The Pico must apply
   P = S⁻¹+ ∘ φ ∘ C to pre-distort inputs so S(P(s)) ≈ the intended game input.
   - C: octagon clamp to Oct(125) (physical gate boundary)
   - φ: linear scale Oct(125) → Oct(100)
   - S⁻¹+: BFS-interpolated inverse of the measured Switch 2 transform

2. **LUT construction and validation.** Building the inverse lookup table from `readings.csv`,
   filling gaps via BFS nearest-neighbor interpolation, and verifying via the visualization tool.

3. **Mode switching.** Firmware has a FIX mode (raw passthrough) and COR mode (with transform).
   Toggle trigger: L+R+十字上+Start+Y (replaces earlier Z-button shortcut). Rumble feedback:
   FIX→COR = 1 vibration, COR→FIX = 2 vibrations.

4. **Status polling fix.** Switch 2 uses initial Status packet to set origin. Fix: send (128,128)
   in FIX mode during connection; switch to COR mode after a trigger input so the console has
   already locked in (128,128) as origin.

5. **Multi-agent Teams system.** The user built (and iterates on) a full Claude Code Teams
   setup in `.claude/agents/`:
   - `implementer` — C++ build + Python tool runs (merged from cpp-builder + python-tool)
   - `critic` — read-only ISR/timing safety reviewer
   - `guardian` — PR workflow + doc sync enforcer (merged from pr-workflow + doc-sync)
   - `navigator` — experiment design + transform pipeline verification
   - `facilitator` — retrospective lead + blocker bridge
   
   The user actively redesigns this system across sessions, enforcing that agents actually
   collaborate (parallel spawns, not serial baton-passing) and that PRs require a 4-point
   merge checklist.

6. **Remote dev environment.** Tailscale + macOS SSH + tmux from Android (Termux) so they
   can develop away from their desk. Set up and documented in `docs/remote-dev.md`.

7. **CI optimization.** GitHub Actions pre-built Docker image to speed up `Install build
   dependencies` step.

**Key files the user references by path:**
- `CLAUDE.md` — master rules file, synced to guardian.md and copilot-instructions.md
- `.claude/agents/guardian.md`
- `.github/copilot-instructions.md`
- `resources/switch2/20260205/readings.csv` — measured stick mapping data
- `resources/switch2/20260205/transform_viewer.html` — interactive visualization
- `tools/visualize_transforms.py`
- `docs/measurements.md`, `docs/transforms.md`, `docs/hardware.md`
