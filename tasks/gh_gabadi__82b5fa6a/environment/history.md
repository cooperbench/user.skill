> DEVELOPER

drywall can be in some where installed and used from pypi/uv? like any python lib?

> TOOL

tool_use Bash
id: toolu_01CJBZ7MQCjwcjYT5m36anm5
```json
{
  "command": "rtk ls /home/<USER>/workspace/addi/drywall",
  "description": "List repo root contents"
}
```

> TOOL

tool_result
id: toolu_01CJBZ7MQCjwcjYT5m36anm5
```
.agents/
.cargo/
.claude/
.codex/
.config/
.entire/
.github/
.swarmforge/
.worktrees/
acceptance/
docs/
features/
scripts/
src/
start/
swarmforge/
tests/
tmp/
.gitignore  160B
.mise.toml  153B
AGENTS.md  3.9K
CONTEXT.md  6.8K
Cargo.lock  24.9K
Cargo.toml  593B
README.md  1.7K
lcov.info  1015B
rust-toolchain.toml  88B
swarm  7.3K
```

> TOOL

tool_use Bash
id: toolu_01N98wxCcWgm5oZGDhnJ8bpk
```json
{
  "command": "rtk ls /home/<USER>/workspace/addi/drywall/docs; echo ---; find /home/<USER>/workspace/addi/drywall -iname \"*pypi*\" -o -iname \"*pyproject*\" -o -iname \"*maturin*\" 2>/dev/null; echo ---; cat /home/<USER>/workspace/addi/drywall/Cargo.toml",
  "description": "Check docs dir and search for python packaging files"
}
```

> TOOL

tool_result
id: toolu_01N98wxCcWgm5oZGDhnJ8bpk
```
adr/
qa-findings-jsts-detection.md  5.6K
---
---
[package]
name = "drywall"
version = "0.1.0"
edition = "2024"

[[bin]]
name = "drywall"
path = "src/main.rs"

[lib]
name = "drywall"
path = "src/lib.rs"

[dependencies]
rayon = "=1.12.0"
tree-sitter = "=0.26.9"
tree-sitter-rust = "=0.24.2"
regex = "=1.12.4"
clap = { version = "=4.6.1", features = ["derive"] }
serde = { version = "=1.0.228", features = ["derive"] }
serde_json = "=1.0.150"
ignore = "=0.4.26"
globset = "=0.4.18"
tree-sitter-javascript = "=0.25.0"
tree-sitter-typescript = "=0.23.2"
tree-sitter-python = "=0.25.0"

[dev-dependencies]
proptest = "=1.11.0"
tempfile = "=3.27.0"
```

> TOOL

tool_use Bash
id: toolu_01FKyzVD7DWpyxiafApGYkFw
```json
{
  "command": "rtk cat /home/<USER>/workspace/addi/drywall/README.md; echo ===GITHUB===; rtk ls /home/<USER>/workspace/addi/drywall/.github/workflows 2>/dev/null; echo ===; find /home/<USER>/workspace/addi/drywall/.github /home/<USER>/workspace/addi/drywall -iname \"*distribut*\" -o -iname \"*install*\" 2>/dev/null | grep -v .git/",
  "description": "Check README and search for distribution/install docs"
}
```

> TOOL

tool_result
id: toolu_01FKyzVD7DWpyxiafApGYkFw
```
# drywall

Polyglot AST subtree DRY analyzer. Detects duplicate code across files using Jaccard similarity over normalized AST fingerprints.

## Install

Download the binary for your platform from the [latest release](https://github.com/gabadi/drywall/releases/latest):

| Platform | Binary |
|----------|--------|
| Linux x86_64 | `drywall-linux-x86_64` |
| macOS Apple Silicon | `drywall-macos-aarch64` |
| macOS Intel | `drywall-macos-x86_64` |

```bash
# Linux
curl -sL https://github.com/gabadi/drywall/releases/latest/download/drywall-linux-x86_64 -o drywall
chmod +x ./drywall

# macOS Apple Silicon
curl -sL https://github.com/gabadi/drywall/releases/latest/download/drywall-macos-aarch64 -o drywall
chmod +x ./drywall

# macOS Intel
curl -sL https://github.com/gabadi/drywall/releases/latest/download/drywall-macos-x86_64 -o drywall
chmod +x ./drywall
```

The Linux binary is statically linked (musl) — no runtime dependencies.

## Usage

```bash
drywall [--threshold 0.82] ./src
```

`--threshold` is the Jaccard similarity cutoff (default `0.82`, same as dry4go). Pairs at or above the threshold are reported. Exit codes: `0` = no duplicates, `1` = duplicates found, `2` = bad arguments.

## Use as a CI gate

Add to any project's CI pipeline:

```yaml
- name: Install drywall
  run: |
    curl -sL https://github.com/gabadi/drywall/releases/latest/download/drywall-linux-x86_64 -o drywall
    chmod +x ./drywall

- name: DRY check
  run: ./drywall --threshold 0.82 ./src
```

`--threshold` sets the Jaccard similarity cutoff (default `0.82`). Pairs at or above the threshold are flagged. […]

> AGENT

Currently drywall is distributed only as raw prebuilt binaries via GitHub releases (no PyPI/uv, no crates.io, no Homebrew). It's a pure Rust CLI with no Python bindings at all — there's no `pyproject.toml`, no `maturin`/`pyo3` setup, nothing.

That said, it's absolutely feasible to make it `pip install`/`uvx`-able. The standard pattern for shipping a Rust binary through PyPI is a thin wheel that just bundles the compiled executable (no PyO3 bindings needed since drywall is a CLI, not a library API). Common approaches:

1. **`maturin` with `bin` target** — maturin supports packaging a Rust binary crate directly as a Python wheel entry point (no Python/PyO3 code needed). Simplest for a pure-CLI tool.
2. **Manual wheels per-platform** — build a wheel per platform tag that just drops the binary into `scripts/`, similar to how `ruff`, `uv` itself, or `ripgrep`-python wrappers do it. Usually paired with a tiny Python shim that does the multi-platform binary dispatch (like `ruff`'s `pyproject.toml` + `ruff/__main__.py` download-or-bundle trick).
3. **`pip install drywall`** then would just place the right platform binary on PATH; `uvx drywall` would work too since uv reads normal PyPI wheels.

Given you already have cross-compiled release artifacts per platform (Linux x86_64 musl, macOS arm64/x86_64) from […]