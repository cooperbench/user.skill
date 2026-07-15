> DEVELOPER

perform a deep review of this project against https://github.com/github/spec-kit/tree/main which one is better?

> AGENT

I'll dig into both projects in parallel — explore this repo's structure and content, and research spec-kit.

> AGENT

Let me read this project's README and research spec-kit in parallel.

> AGENT

Let me ground the comparison by reading a representative Shaper skill and spec-kit's actual templates.

> AGENT

I've reviewed both in depth. Here's the comparison, grounded in what each actually ships. ## What each one is **spec-kit** (GitHub, official) — a packaged, agent-agnostic toolkit for **Spec-Driven Development**. A real CLI (`specify`, installed via `uv`), versioned releases, support for 30+ coding agents, and a tight 7-step pipeline centered on one idea: the *spec* is the executable source of truth, code is generated output. Its arc: `constitution → specify → clarify → plan → tasks → implement → analyze → converge`. It scaffolds `.specify/` (templates, bash scripts, constitution) and produces `specs/<feature>/{spec,plan,tasks,data-model,research,contracts}`. **Shaper** (this repo, personal project) — a Markdown-only skill pack encoding **engineering discipline as enforced gates**, biased toward Claude Code. Much wider arc: `idea triage → project → design/spikes → delivery → build/debug/simplify → verify/review → pr-prepare/finishing`. It ships skills, a SessionStart navigator hook, mechanical hooks (stop-the-line, ta[REDACTED_SK]), persistent rule files (PRODUCT_RULES, eng-principles), and is structured so an orchestrator (drain-cycle) can drive a delivery plan unattended. ## Where they actually differ | Dimension | spec-kit | Shaper | |---|---|---| | **Lifecycle covered** | "We've decided to build feature X" → working code | "Is this worth building?" → shipped, reviewed PRs | | **Front of funnel** | None […]

> DEVELOPER

are there any ideas from spec-kit that shaper should adopt? consider your answer carefully

> AGENT

Good question — let me check what Shaper already has before claiming any gaps, so I don't recommend things it already does.

> AGENT

Yes — a few, and they're worth taking for a specific reason: Shaper's artifact chain is *longer* than spec-kit's (idea → project → design → delivery → AC → diff), so it has more places to drift and more loop to close. The best spec-kit ideas are exactly the ones that exploit that. I grounded each against what Shaper already has. ## Worth adopting **1. `analyze` — a cross-artifact consistency check. (Strongest fit.)** Shaper reviews each artifact well but never checks the *chain's mutual coherence*. `plan-review` is adversarial but single-artifact; `verify-implementation` checks diff-vs-AC only. Nothing asks: do the delivery plan's acceptance criteria still trace to the project's KRs, which trace to the idea's stated outcome and the design's decisions? spec-kit can afford to skip this because it has three artifacts; Shaper has six, so the drift surface is larger and currently unguarded. This is the cleanest gap, and it leans directly on Shaper's existing "traceability spine" — `analyze` would just verify that spine end-to-end instead of assuming it holds. **2. `converge` — an initiative-level outcome closeout. (Strong, genuine hole.)** My grep found nothing matching this. Shaper verifies per-ticket but has no step that closes the loop at the initiative level: […]

> DEVELOPER

compare shaper against this PDF ~/Downloads/Day_1_v3.pdf perform a gap analysis

> AGENT

I'll read the PDF first to understand what it covers.

> AGENT

51 pages — I'll read it in chunks.

> AGENT

This is Addy Osmani et al.'s "The New SDLC With Vibe Coding" (Google, May 2026). Let me read the core SDLC, harness, and orchestration sections.

> AGENT

Now the final section — economics and "where to start" recommendations, which is where the gap analysis will land hardest.

> AGENT

This is the Addy Osmani / Google "New SDLC with Vibe Coding" paper (Day 1 of a series) — a strategy/manifesto, not a tool. So this is a different kind of comparison from spec-kit: the paper defines the *ideal* of "agentic engineering," and Shaper is essentially a concrete *implementation* of that ideal. Let me ground a few gap claims before writing.

> AGENT

Read the full paper and grounded the gaps against Shaper's actual files. Here's the analysis. ## What this comparison actually is The spec-kit comparison was tool-vs-tool. This is different: **the paper is the manifesto, and Shaper is a concrete implementation of its "agentic engineering" end of the spectrum.** They're not competitors — the paper describes the ideal, Shaper is one instantiation of it. Shaper's own README even opens with the same "vibe coding drifts, encode the discipline" framing the paper is built on. So the gap analysis asks one question: **where does the paper name a practice that Shaper doesn't yet embody?** ## Strong alignment (Shaper already satisfies these) The paper's closing recommendations read almost like a Shaper feature list: | Paper recommendation | Shaper | |---|---| | "Set up AGENTS.md, treat it as code, versioned, owned" | `AGENTS.md` + `CLAUDE.md` + versioned `rules/` ✓ | | "Install a set of skills (progressive disclosure)" | Shaper *is* a lazy-loaded skill pack ✓ | | "Write tests before generating code" | `build` = RED before GREEN; AC before code ✓ | | "Review every line; re-shape review for AI code" | `execution-review` (spec/security/quality personas), `stop-the-line` ✓ | | "Static vs dynamic […]

> DEVELOPER

yes

> AGENT

I'll run the intake gate on the eval-layer skill idea.

> AGENT

Running `shape:idea`. **Step 1 — Raw intake captured verbatim:** > A new Verify-stage skill for Shaper that adds an eval layer: rubric-scored output evaluation plus trajectory verification (did the agent run its gates, in order, without skipping). Gap found vs the Google/Osmani "New SDLC with Vibe Coding" paper — Shaper verifies deterministic correctness (build/tests) and applies human judgment (execution-review, verify-implementation) but has no eval layer and no trajectory check, the two things the paper names as separating agentic engineering from sophisticated vibe coding. **Step 2 — Elicit and refine.** Let me sharpen this before it gets scored or routed. ``` HYPOTHESIS: You want Shaper to verify the non-deterministic parts of agentic work — both the *quality* of an artefact against a rubric, and the *process* the agent took to produce it — so "the gates passed" stops being something an agent can fake. CONFIDENCE: ~45% — unresolved: this is really TWO capabilities (rubric eval vs trajectory check) that may not belong in one skill; and it's unclear how either works in a Markdown-only, stack-agnostic pack with no runtime/transcript access. ``` I'll ask one at a time, each with my guess attached. **Q1: Is this one skill or two?** Rubric-scored output […]

> DEVELOPER

it really should just be one skill: Review, which then fans out and reviews: - The artefacts themselves (hence the code review, simplification steps, security, etc, i.e. did the agent build it in the best way?) - The acceptance criteria (i.e. did the agent build the right thing?)

> AGENT

Got it — that reframes it meaningfully, and I want to flag a tension before I bank it, because it changes what this idea *is*. ``` UPDATED HYPOTHESIS: You want one "Review" door at the Verify stage that fans out into two questions — "did the agent build the right thing?" (acceptance criteria) and "did it build it the best way?" (code review / simplify / security) — consolidating the verify-stage skills under a single entry point. CONFIDENCE: ~55% — but this reframe has quietly dropped the original gap. What you're describing maps almost exactly onto skills Shaper ALREADY has. ``` Here's the tension I don't want to paper over. Your two axes are already built: - **"Did it build the right thing?"** → `verify-implementation` (diff vs AC checklist). - **"Did it build it the best way?"** → `execution-review` already fans out **spec-compliance + security-auditor + code-quality** personas into one GO/NO-GO verdict, and `simplify` handles the cleanup pass. So as stated, "Review" is a **consolidation/navigation** idea — one door over existing skills — *not* the capability gap I found in the paper. The two things the paper names that Shaper genuinely lacks were: 1. **Trajectory check** — did the agent […]

> DEVELOPER

consolidation first

> AGENT

Good — that's a clean decision. Banking it: **trajectory + rubric-eval are deferred to a separate idea; this one is the consolidation door.** ``` UPDATED HYPOTHESIS: You want a single "Review" entry point at the Verify stage that fans out to the existing skills — verify-implementation (right thing) and execution-review's personas + simplify (best way) — so there's one door instead of three-or-four to choose between. CONFIDENCE: ~70% — missing: the actual pain (navigation vs completeness), and whether Review replaces or wraps the sub-skills. ``` **Q3: What's the pain that consolidation actually fixes?** I can see two, and they design differently: ``` GUESS: It's completeness, not just navigation. The real itch is that today the verify steps fire piecemeal — an agent runs verify-implementation but skips the security pass, or marks Done after a code-review without checking AC. A single Review door makes the *full* fan-out the default, so steps stop getting silently dropped. (This also connects to the known drain-cycle issue where the prompt hardcodes one code-review gate and misses the others.) ``` Is the win mainly **"one obvious door so nobody picks the wrong verify skill"** (navigation), or **"one door that guarantees all the verify passes actually run"** […]

> DEVELOPER

i already have an exec:review skill planned (see ABA-405)

> AGENT

Let me pull ABA-405 so I'm not re-triaging something already captured.

> AGENT

That changes the picture — and it's worth stopping on, because it means the idea I've been sharpening **already exists in your design.** ABA-405 isn't a consolidation idea. It's a *rename*: `exec:review` is just `execution-review` (the existing spec/security/quality fan-out) moved under the `exec:*` prefix. Reading it against the rest of ADR-0004, your "one Review door that fans out to right-thing + best-way" is **already the shipped architecture**: - **`exec:pickup`** is the single front door (the supervisor pointer). - **`exec:verify`** (= `verify-implementation`) → "did it build the *right thing*?" (AC). - **`exec:review`** (= `execution-review` personas) → "did it build it the *best way*?" (spec/security/quality). - **`exec:simplify`** → the cleanup pass. So the consolidation isn't a new idea — it's the exec:* workflow you've already designed and are mid-rename on. Per shape:idea's own rules, I shouldn't file a triage record for something already on the roadmap being executed. There's nothing fresh to bank there. Which means the **only un-captured idea in this whole thread is the one you deferred two turns ago**: the third axis the paper names — *did the agent build it the way it claimed to* (trajectory: gates run in order, none skipped) + rubric-scored eval of non-deterministic output […]