---
name: commit-convention-correction
description: "Trigger: Agent proposes or creates a commit with a wrong conventional-commit prefix, wrong scope, or a commit that will cascade unwanted version bumps. FSM1 corrects with a specific replacement."
---

# Skill: Commit Convention Correction

FSM1 enforces conventional commits with component scopes. When the agent gets it wrong — even slightly — he corrects with the exact replacement in one sentence, no explanation.

Pattern: states what it should be, sometimes asking agent to rewrite/force-push.

## Examples

Wrong prefix triggers correction:
```
please use `feat(api):` in commit message to accurately attribute the commit to the right component
```

Cascade version bumps from `fix:` prefix:
```
the previous `fix` commit caused a cascade of version bumps. Can we force push that to a `chore(ci):` commit message and stop all the unnecessary bumps?
```

Unsure about the right type, asks instead of deciding:
```
ok now commit the api client (not sure if this should be a chore/feat commit though - a new property is being added.
```

Branch/PR direction correction:
```
yeah do this on a chore branch
```

Docs commit:
```
yeah a `docs:` commit, branch and pr please
```

## Key Rules FSM1 Enforces

- `feat(api):` for API-only additions
- `chore(ci):` for CI/config changes that should NOT bump versions
- `docs:` for documentation-only changes
- Wrong prefix on a `fix:` can trigger Release Please to bump versions for all packages — FSM1 knows this and corrects immediately
- Branch name must match the feature exactly (`feat/phase-12-multi-factor`, not `feat/phase-12-mfa`)
