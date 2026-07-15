> DEVELOPER

lets fix this issue https://github.com/entireio/skills/issues/6

> AGENT

I’m going to inspect the repo and pull in the GitHub issue details so we can fix the right thing end to end. After that I’ll trace the affected files, make the change, and verify it locally.

> AGENT

I’ve confirmed the repo shape and there’s an untracked [TUTORIAL.md](/Users/rizel/Documents/work/skills/TUTORIAL.md) that I’ll leave alone. Next I’m pulling the issue details and reading the relevant skill files so we can patch the exact behavior the issue describes.

> AGENT

The issue is clear now: clone-based installers only see one discoverable skill from this repo, and the likely culprit is the repository layout and how skill metadata is exposed. I’m checking the install surface the repo presents today against what flat auto-discovery tools usually expect, then I’ll patch the structure with the smallest compatible change.

> AGENT

I’ve narrowed the likely failure mode: `what-happened` is the only skill that currently declares an explicit frontmatter `name`, while the others only have `description`. I’m reproducing that against the actual `skills` installer now so we can confirm before editing anything.

> AGENT

The reproduction matches the issue exactly on `skills@1.5.2`: the installer reports “Found 1 skill” and only surfaces `What Happened`. I’m inspecting the installer’s discovery logic now to confirm whether the missing `name` metadata is the actual discriminator before I patch the repo.

> AGENT

The installer source confirms it: it ignores any `SKILL.md` whose frontmatter does not include both `name` and `description`. That means the fix is structural rather than behavioral, so I’m adding explicit skill names to the missing files and then I’ll rerun the exact installer repro.

> AGENT

I’m making a very small patch: just the missing frontmatter fields that the installer requires for discovery. After that I’ll rerun the installer against the local checkout to prove it now sees all four skills.

> AGENT

The patch is behaving the way we wanted: the same installer version now reports `Found 4 skills` against this checkout. I’m doing one last quick sanity pass for diff cleanliness, then I’ll hand you the exact change and verification.

> AGENT

The issue is fixed in this checkout by adding the missing `name` frontmatter to the three undiscoverable skills: [skills/explain/SKILL.md](/Users/rizel/Documents/work/skills/skills/explain/SKILL.md), [skills/search/SKILL.md](/Users/rizel/Documents/work/skills/skills/search/SKILL.md), and [skills/session-handoff/SKILL.md](/Users/rizel/Documents/work/skills/skills/session-handoff/SKILL.md). `skills@1.5.2` requires both `name` and `description` in `SKILL.md`, which is why only `what-happened` had been detected before. I verified the repro locally with `npx -y skills@1.5.2 add /Users/rizel/Documents/work/skills --list --yes`, and it now reports `Found 4 skills` instead of `Found 1 skill`. `git diff --check` is clean. I left the untracked [TUTORIAL.md](/Users/rizel/Documents/work/skills/TUTORIAL.md) alone.