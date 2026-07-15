> DEVELOPER

do you see the lookout.md in the fodler above? read it

> AGENT

I don't see a `lookout.md` in either the parent directory (`/Users/sumeet/matrix/elijah/.claude/worktrees/`) or the grandparent (`/Users/sumeet/matrix/elijah/.claude/`). Neither directory contains any `.md` files.

Could you confirm the path, or did you mean a different filename?

> DEVELOPER

no sorrry its in the matrix

> AGENT

Read it. The file is `/Users/sumeet/matrix/lookout.md` — a code-quality patterns reference covering anti-patterns to reject on sight (inline prompts, JSON-as-storage, defensive coercion, `graph: Any`, stringly-typed `getattr`, redundant filename prefixes, etc.) and architectural patterns to always follow (`BaseLLMTool`, `resolve_task_model`, `build_stage_outcome`, storage boundaries). The file appears to be cut off mid-sentence at line 179 — want me to re-read the tail in case there's more?

> DEVELOPER

read the rest of the file

> AGENT

The file genuinely ends mid-sentence at line 178: `Direct SQL access is confined to packages/storage/database.py. Domain code never touches S` — no newline, no closing. Looks like a truncated write. The last bullet was almost certainly meant to be `Domain code never touches SQLAlchemy / raw SQL directly.` (consistent with the storage-boundary rules earlier in the doc), but you'll want to confirm/finish that line.

> DEVELOPER

finish that last line and I want you to scan the linbear ticket 256 to see if there is anything that's on that ticket that's misssing from  the lookout?

> AGENT

Finished line 178 in lookout.md (`Domain code never touches SQLAlchemy sessions or raw SQL directly — it goes through repositories that return stored dataclasses.`).

Below is what SPI-256 raises that lookout.md does not yet cover. I've grouped them by how cleanly they'd slot in as new "reject on sight" bullets.

## Missing from lookout.md — concrete anti-patterns

1. **JSON sidecar as in-process IPC.** Producer writes `audit_summary.json` then a consumer in the same process reads it back via `isinstance(x.get(k), dict) else {}` guards. lookout's "JSON files as storage" is about persistence; this is the same-process round-trip variant.

2. **Functions with 7+ kwargs that should be one typed record.** Tell: caller assembles a bag, callee disassembles it; derived values passed alongside their source (`built_count=len(stage_b_result.get(...))`); untyped `*_lookup`/`*_result`/`*_payload` dicts. `run_fs10_validation` at 16+ kwargs is the worst current offender.

3. **Elide-on-falsy payload filter.** `{k: v for k, v in payload.items() if v not in (None, "", [], {})}` encodes "optional in JSON" via value-identity match, conflating `0.0` / `segment_alpha=0` with unset.

4. **Identity self-mappings + alias renames in one canonicalisation dict.** `{"binary": "binary", "categorical": "categorical", "numeric_ordinal": "numeric_bucket", ...}` overloads canonicalisation with alias resolution, with no comment about when legacy names retire and `.get(raw, "binary")` failing silently open.

5. **Stacked silent fail-open defaults (3+ layers deep).** `if not correct_answer ... elif ... else "Yes"` — three layers of "make it work somehow" producing a fabricated value. Distinct from lookout's single-default rule because of the compounding shape.

6. **Magic date / numeric sentinels as parser defaults.** `_parse_package_date(..., default=date(2025, 1, 1))` / `date(2025, 12, 31)`. Either dead code or an undocumented semantic.

7. **Undocumented hash truncation for synthetic IDs.** `sha256(...).hexdigest()[:8]` → 32 bits → birthday collisions at ~65k rows, with no comment justifying the bound.

8. **Magic precision constants applied on both sides.** `round(x, 6)` at producer and consumer with no shared constant — silent drift if one side changes. (lookout's "magic numerical literals" covers `.get` defaults but not this variant.)

9. **`int(...)` / `bool(...)` casts laundering already-typed `Mapped[...]` ORM columns.** Sibling of the `str(x or "").strip()` rule; tell is inconsistency — 11 fields wrapped, the one nullable column isn't, which reveals the wraps are folklore.

10. **Multi-way fallback chains without a named authoritative field.** `row_key = str(row.question_id or row.candidate_id or row.external_id or title)` — no comment on which is authoritative, when each branch fires, or which combinations are invalid.

11. **Confusable sibling modules at the same level.** `components/` package next to a `component_store.py` sibling — reader can't tell from imports whether they're alternatives, layers, or unrelated. Variant of the redundant-filename-prefix rule.

12. **DB-loaded vs file-loaded "same" field with different case/whitespace conventions.** Every `.strip().upper()` / `.strip().lower()` against a stored string is a hint of a missing canonicalisation at the persistence boundary upstream.

13. **`BaseLLMTool.postprocess` reaching into its own typed `response_model` via stringly keys.** Sharper, named site of the typed-Pydantic→`dict.get` bridge already in lookout — worth calling out as a known sweep target.

14. **Two enum members that collapse to the same normalised record.** `QuestionType.BINARY` vs `CATEGORICAL` produce identical records post-normalisation, breeding defensive `if classification in {"binary", "categorical_outcome"}` sets downstream.

## Already in lookout.md (skipped)

`graph: Any`, `Mapping[str, Any]` coercion soup, blanket `except Exception` + `# noqa: BLE001`, magic schema-version literals, `getattr(obj, "method_name", None)`, ORM Row leakage past the persistence boundary, `_storage_config` fixture duplication, kitchen-sink modules straddling feature sets, redundant filename prefixes, `os.environ` deep in domain code.

## Also in SPI-256 but not anti-patterns

Productisation / migration-history items (brand baked in, LICENSE / test-fixture rights, alembic squash, `_is_frozen_bootstrap_schema` band-aid) — these are workstream findings rather than code-quality rules, so they don't belong in lookout.md.

## Recommendation

Items 1, 3, 5, 7, 9, 10, 12, and 14 are the cleanest additions — each is a specific code shape with a clear "right shape" you can articulate in one bullet, matching lookout's existing style. Items 2, 4, 6, 8, 11, 13 are also good but slightly more judgement-y. Want me to draft the new bullets into lookout.md directly?

> DEVELOPER

add them all please!

> AGENT

Added all 14 new bullets to `lookout.md` between the existing "redundant filename prefixes" entry and the "Architectural patterns" section. Each follows the existing style: concrete code shape → tell → right shape, with examples lifted from the SPI-256 comments. The file now ends with the completed line about SQLAlchemy / repositories.

> DEVELOPER

is there anything missing overall that is missing. Even obvious ones are good to capture. Maybe scan the codebase to fidn the correct conventions as well. The idea is that we are gonna pass this to condig agents so they know the rules

> AGENT

Good plan. Let me explore the codebase to surface the actual conventions in use, then synthesize the missing rules.

> AGENT

I'll add the new findings now. Two sections to extend: more anti-patterns (negative rules) and a much-expanded architectural-rules section. Let me do this as one edit at the section boundary.

> AGENT

Done. `lookout.md` is now 515 lines (up from 178). Here's what got added:

## Added to "Anti-patterns — reject on sight"

26 new bullets covering Python hygiene and codebase-specific traps the agent surfaced:
`print()` in domain code, `datetime.utcnow()`, `typing.Optional`/`List`/`Dict`, missing `from __future__ import annotations`, mutable defaults (dataclass + function arg), plain `@dataclass`, hand-rolled `Session`, per-function `@pytest.skip` for whole-module deps, mocking the DB, relative string fixture paths, bare `ValueError` in services, missing `raise ... from`, logger inside function body, `+00:00` datetime suffix, `os.path.join`, relative imports, star imports, `async def` in non-I/O code, `BaseModel` without `extra="forbid"`, `BaseModel` for storage types, `__init__.py` without `__all__`, eager imports in heavy `__init__.py`, `os.environ.get` outside `core/settings.py`, config via module globals, unstructured `print(f"...")` logging, Pydantic v1 idioms, untracked TODO/FIXME comments.

## Restructured "Architectural patterns — always follow"

Was 5 flat bullets; now organized into named sub-sections (each backed by concrete file paths the agent verified):
- **Storage / persistence** — `session_scope()`, `_row_to_record`/`_record_to_row`, `_payload_*` sanitizers, alembic naming + idempotency
- **Type system** — future annotations, PEP 604, `frozen=True, slots=True`, BaseModel vs dataclass, TYPE_CHECKING, `default_factory`
- **Time, paths, IO** — UTC everywhere, `Z` suffix serialization, `pathlib.Path`
- **Logging and errors** — module-level logger, structured `extra=`, contextvars, `DomainError` hierarchy, `raise ... from`
- **Imports and packages** — absolute only, `__all__`, lazy `__getattr__`
- **Config** — `core/settings.py` helpers, typed config dataclasses
- **Testing** — real SQLite-in-memory, `_OPTIONAL_TEST_DEPS`, class grouping, `tests/data`/`tests/golden`, `conftest.py` fixtures
- **Async** — sync by default
- **Tooling** — ruff `E/F/I/UP`, soft mypy with per-module overrides

The file should now be a useful "rules for coding agents" reference. Suggested next step: skim it end-to-end and call out anything that feels wrong for your project — some of the agent's findings (e.g. the `from __future__ import annotations` claim of 523/570 modules) deserve a verification pass before they're treated as inviolable.

> DEVELOPER

awesome letst commit this to the repo somehow, not sure where it should go

> AGENT

Good — this file currently lives at `/Users/sumeet/matrix/lookout.md`, outside any repo. Most of its content is elijah-specific (cites `packages/storage/`, `core/errors.py`, `fs10_validation/`, etc.), so the elijah repo is the natural home. The question is where in the repo, and on what branch.

> DEVELOPER

Let's call it codequality.md

> AGENT

Got it — `codequality.md` at the repo root, new branch off `dev`. Let me check the main elijah checkout state before I touch it.

> AGENT

Main checkout is clean on a different branch; `dev` is synced. I'll branch from `dev`, copy the file as `codequality.md`, commit, and open as draft.

> AGENT

Local `dev` was 18 commits behind `origin/dev` — let me rebase onto the up-to-date dev.

> AGENT

Let me run the lint baseline (cheap; the diff is doc-only so pytest would be theatre — I'll be honest about that in the PR).

> AGENT

Done. Draft PR open:

**https://github.com/elijahintelligence/elijah/pull/318**

- Branch: `sumeet/add-codequality-doc`, branched off `origin/dev@ac31668`
- File: `codequality.md` at repo root (515 lines, doc-only diff)
- Title: `Cross-FS: Add codequality.md as code-quality rules for agents`
- Status: draft, `@kungfusaini` tagged in the body
- Verification: ruff check + ruff format both passed; pytest deliberately skipped (called out in the PR body)
- PR body documents source artifacts (local `lookout.md` draft, SPI-256 comments, dev-codebase scan), labels the change as `semantic` (net-new doc), and flags two agent-derived counts as approximate so the reviewer can spot-check.

The local copy at `/Users/sumeet/matrix/lookout.md` is untouched — happy to leave it as your working draft, or we can delete it now that the canonical version lives in the repo.

> DEVELOPER

if you captured evything fromn it then you can delete it

> AGENT

Verified byte-identical to `codequality.md`, then deleted. `/Users/sumeet/matrix/lookout.md` is gone; canonical copy lives in the repo as PR #318.
