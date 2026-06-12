---
name: json-only-output-demand
description: How musicofhel enforces structured output — a strict JSON-only contract with explicit schema, key names, nullable field rules, and a fallback for the empty-findings case. Present in 100% of prompts, verbatim.
---

Every prompt contains an `## Instructions` section that ends with an absolute output constraint and a precise JSON schema. The wording never varies.

The constraint line (always uppercase on `ONLY`):
> `Respond with ONLY valid JSON — no markdown fences, no explanation outside the JSON.`

The schema block (always this exact structure):
```json
{
  "findings": [
    {
      "severity": "critical|warning|suggestion",
      "message": "description of the issue",
      "file": "path/to/file or null",
      "line": line_number_or_null,
      "rule": "which criteria this violates"
    }
  ],
  "summary": "one-line overall assessment"
}
```

The null-findings fallback (always present, always this exact string):
> `If there are no findings, return: {"findings": [], "summary": "No issues found."}`

The full `## Instructions` block as it appears in every prompt:
```
## Instructions
1. Review the diff below carefully.
2. For each finding, classify it as: critical, warning, or suggestion.
3. Respond with ONLY valid JSON — no markdown fences, no explanation outside the JSON.
4. Use this exact schema:

{
  "findings": [
    {
      "severity": "critical|warning|suggestion",
      "message": "description of the issue",
      "file": "path/to/file or null",
      "line": line_number_or_null,
      "rule": "which criteria this violates"
    }
  ],
  "summary": "one-line overall assessment"
}

If there are no findings, return: {"findings": [], "summary": "No issues found."}
```

This pattern reflects that the pipeline's downstream consumer parses JSON directly — any prose in the response would cause a parse failure. The `"rule"` field ties each finding back to one of the five review criteria, enabling the pipeline to categorize findings by rule type.
