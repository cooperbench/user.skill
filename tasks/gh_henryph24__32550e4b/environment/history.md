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
  "file_path": "/Users/hungpq2412/neuralips26/abstract_portal.txt",
  "old_string": "A 720-run sweep across standard MoE rescue mechanisms recovers at most $10.9\\%$ MSE, $2.7\\times$ worse than our causal intervention.",
  "new_string": "A 720-run sweep across standard MoE rescue mechanisms recovers at most 10.9\\% MSE, $2.7\\times$ worse than our causal intervention."
}
```

> TOOL

tool_result
id: toolu_01TfMUuiT1v5pekrF5QZJobw
```
The file /Users/hungpq2412/neuralips26/abstract_portal.txt has been updated successfully.
```

> AGENT

Done. `$10.9\%$` → `10.9\%` (now consistent with the other percentages in the abstract — all outside math mode). The `$2.7\times$` stays in math mode because `\times` needs it. Re-paste and the percent should render.