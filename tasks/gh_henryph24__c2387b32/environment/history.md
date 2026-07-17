> DEVELOPER

[Image #1] [Image #2]

here is the preview when we paste @abstract_portal.txt 

look like the percent is not being rendered (10.9 MSE) ?

> AGENT

You're right — `$10.9\%$` is in LaTeX math mode and OpenReview's renderer is stripping the `\%`. Other percentages in the abstract (`26--79\%`, `12--79\%`, `13--42\%`) work because they're outside math mode. Easy fix: take it out of math mode to match the rest.

> TOOL

tool_use Edit
id: toolu_01TfMUuiT1v5pekrF5QZJobw
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/abstract_portal.txt",
  "old_string": "A 720-run sweep across standard MoE rescue mechanisms recovers at most $10.9\\%$ MSE, $2.7\\times$ worse than our causal intervention.",
  "new_string": "A 720-run sweep across standard MoE rescue mechanisms recovers at most 10.9\\% MSE, $2.7\\times$ worse than our causal intervention."
}
```

> TOOL

tool_result
id: toolu_01TfMUuiT1v5pekrF5QZJobw
```
The file /home/<USER>/neuralips26/abstract_portal.txt has been updated successfully.
```

> AGENT

Done. `$10.9\%$` → `10.9\%` (now consistent with the other percentages in the abstract — all outside math mode). The `$2.7\times$` stays in math mode because `\times` needs it. Re-paste and the percent should render.

> DEVELOPER

is it actually 10.9% based on main text

> TOOL

tool_use Bash
id: toolu_01WTYnim8bigS6EWVDNPUbf4
```json
{
  "command": "grep -n \"10.9\" /home/<USER>/neuralips26/main.tex | head -20",
  "description": "Check 10.9 occurrences in main.tex"
}
```

> TOOL

tool_result
id: toolu_01WTYnim8bigS6EWVDNPUbf4
```
58:Many time series foundation models (TSFMs) adapt to a target dataset by attaching a single trainable head to a frozen backbone. A single head is one-size-fits-all, yet target series mix heterogeneous regimes that a single head may underfit. The natural upgrade is to replace the single head with a mixture-of-experts (MoE) head whose router dispatches each window to a specialist. This upgrade fails on instance-normalized backbones, a dominant TSFM design class that strips each window's mean and variance before encoding. We call this failure \emph{normalization-induced routing collapse}. Once joint training makes even one backbone transformer block trainable, routing entropy falls to $0.000$. Every input is sent to a single expert; the rest are never activated. A $720$-run sweep across standard MoE rescue mechanisms recovers at most $10.9\%$ MSE, $2.7\times$ worse than our causal intervention. The failure is in the router's input, not its optimization. We formalize this via a mutual-information decomposition. The resulting signal-ratio statistic is computable before training and predicts dataset vulnerability (Spearman $\rho{=}{-}0.88$, $p{<}0.002$). The diagnosis prescribes a minimal causal intervention: \emph{Raw-Routed Mixture of Adapters} (RR-MoA) routes on the raw, pre-normalization input. RR-MoA sets a new state of the art for adapter-based TSFM transfer […]

> AGENT

Yes, 10.9% is correct — main.tex line 501 says "reduces MSE by only $10.9\%$" and `tab:rescue` line 1743 confirms `-10.9%` for the best rescue (Z-loss). The fix to `abstract_portal.txt` is consistent with the paper.