# PROJECTS — mheers

## mheers/opencode-sandbox ★ (dominant — 100% of sessions)

**What it is:** A personal Dockerized sandbox for running OpenCode (an AI coding CLI) with a customized environment: skills installed from external registries, host audio/notification passthrough, USB device access, and a tuned shell prompt.

**Tech stack:**
- Dockerfile (multi-layer, copies skills from `skills/` directory)
- Shell wrapper scripts: `oc` (docker run wrapper), `os` (alternate wrapper), invoked as `./os -t`
- `make` as build entry point
- OpenCode CLI with plugin config at `~/.config/opencode/opencode.json` (mounted from host, not baked in)
- libnotify / DBUS for desktop notifications from inside the container
- USB device passthrough via `--device` and `CAP_MKNOD`
- Skills installed from npm registries (`npx skills add`) and GitHub repos (`pbakaus/impeccable`, `antfu/skills`)

**Recurring themes:**
1. **Host ↔ container parity bugs**: behavior that works on the host breaks inside Docker (sound, notifications, device paths, skills availability).
2. **Container capability flags**: getting the right `--cap-add`, `--device`, path mappings so hardware works inside the sandbox.
3. **Plugin/skill management**: baking new OpenCode skills into the Dockerfile, aligning installed skills between host and container.
4. **Shell prompt integrity**: changes to notification or environment setup scripts break the prompt appearance.
5. **Docker Compose upgrade**: migrating from `docker-compose` (v1) to `docker compose` (v2 plugin).

**Session date range:** 2026-02-27 to 2026-03-13
