> DEVELOPER

I think writing on the problem setup is not good. Is the problem our contribution as well because look like it is not seen in the literature ?

> AGENT

You're right on both counts. The failure mode (normalization-induced routing collapse) **is** one of your contributions; the intro lists it as contribution 1 (line 76) and related work explicitly claims it as "not characterized in prior literature" (line 238). But the current "Problem setup." paragraph (line 245) reads as a generic formalization of per-window mixture-of-adapters, with the failure relegated to a forward-pointing parenthetical ("prior work routes on hidden states, which fails on instance-normalized TSFMs"). That framing hides the contribution: the reader sees a textbook MoA setup, not a novel problem statement. Two ways to fix it, with the main tradeoff: 1. **Split into "Task setup" (standard formalism) + "Problem statement" (novel failure mode you identify).** Owns the contribution where the method begins, and matches the contribution-1 claim in the intro. Costs ~6-10 lines. 2. **Rewrite the existing paragraph to lead with the unsolved problem, with the formalism in service of it.** Same length, but the reader hits "what's broken and unaddressed" before "here is notation." I'd recommend (1): the failure mode deserves its own labelled paragraph since you build a whole diagnosis around it (Observation 1, $R(\mathcal{D})$, eight causal controls). Want me to draft it?

> DEVELOPER

I want problem formulation to read very explicitly. Mention of any specific ram number is not good

> AGENT

Now compile to verify the build is clean.

> AGENT

Build is clean (exit 0, no undefined refs, 52 pages). Changes to the Problem Setup at `main.tex:243-248`: - **Renamed** `Problem setup` → split into `Task setup` (formal task formalism) and `Problem statement (this paper)` (the failure mode you identify). - **Removed** the specific RAM/storage number (`{\sim}2$\,MB`); replaced with "small parameter budget" and "many task-specific adapters can be hot-swapped onto a single shared backbone." - **Promoted the failure mode to the central problem.** New paragraph names *normalization-induced routing collapse* explicitly, asserts it is "not previously characterized," and states the formal problem as: *given a frozen instance-normalized TSFM, find the routing input $u(\mathbf{x})$ such that the per-window mixture trains without entropy collapse and improves over a single static head.* - **Forward-points** to §diagnosis and §main_results as the answer ($u(\mathbf{x}){=}\mathbf{x}$, raw window) and to §related_work for the prior-art gap. - Added `\label{sec:related_work}` so the cross-reference resolves. The contribution-1 claim in the intro now lands in the method section's own framing, not just as a forward-reference.

> DEVELOPER

is the flow smooth now, problem is very clearly defined and cited ?

> AGENT

Now verify all citations exist in the bibliography and the build is clean.

> AGENT

All 24 citations resolve. Recompile and verify.

> AGENT

Build clean (exit 0, no undefined refs, 52 pages). **What changed and why:** 1. **Added inline citations at every claim** in the Problem statement — Shazeer/Switch for the standard MoE recipe, AdaMix as the closest TSFM-adapter precedent, RevIN + MOMENT/PatchTST/TimesFM at "instance-normalized TSFMs," Switch+ST-MoE+ReMoE+Expert-Choice at the optimization rescues, and dedicated citation clusters for the three prior-art threads we claim do not address the problem (MoE-adapter, MoE routing-collapse, time-series-normalization). Reviewers can now check the novelty claim without flipping to Related Work. 2. **Pulled out the formal problem into a `quote` block** so the central question is visually unmissable and reads as the section's anchor. 3. **Added forward-ref to Observation 1** at the point where the routing-information-loss claim is first made, so the formalization is signposted at the moment of the claim. 4. **Tightened the closing bridge:** the previous version pointed only to other sections; now it says "the remainder of this section answers the problem with $u(\mathbf{x}){=}\mathbf{x}$" and then lists the verification (§diagnosis, §main_results, 720-run rescue sweep, $2.7\times$ margin). Reader knows exactly what's coming next in this same section vs. what's in later sections. **Flow now reads:** task setup (notation) → standard MoE recipe and what it does (cited) → claim […]