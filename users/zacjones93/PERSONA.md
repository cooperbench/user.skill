# Persona — zacjones93

## Background (inferred)

Zac is the founder or lead engineer of Wodsmith, a competition management SaaS for CrossFit events
(inferred from sole ownership of the repo, domain handles like `mountainwestfitnesschampionship.com`,
and deep personal familiarity with CrossFit rulebooks and penalty frameworks). He is an experienced
full-stack engineer comfortable with TypeScript, React, Drizzle ORM, PlanetScale MySQL, Cloudflare
Workers, and Stripe Connect. He treats the agent as a capable junior — hands it specs and expects
correct output, but will catch domain mistakes quickly.

## Domain expertise

CrossFit competition scoring is Zac's business domain. He can cite penalty percentages, score
scheme distinctions (time, time-with-cap, AMRAP reps), and the difference between minor/major
penalties without looking anything up. When the agent gets scoring logic wrong, he corrects it
with precise technical language ("for time scored events we need to ADD time. for reps we need to
subtract reps").

## Seniority signals

- References file paths from memory without searching
- Uses `@path` shorthand as if the agent should already have the file open
- Understands schema migration risk ("yes, will this result in data loss?")
- Maintains an ADR discipline — numbered, cross-linked, agent-executable specs
- Has team-memory and test skills already wired into the repo's `.claude/skills/`
- Routinely interrupts agent mid-run when it takes a wrong turn

## Role

Founder/IC (inferred). Makes product decisions in-session: "lets just not handle re-registration
right now... that's fine as a constraint". Shifts scope based on what the agent surfaces.

## Attitude toward the agent

- **Trusting** for implementation details — delegates fully once direction is set
- **Fast to correct** — 36.8% correction rate; won't re-explain, just redirects
- **Impatient with wrong assumptions** — interrupts rather than letting the agent finish
- **Uses skills consciously** — invokes `/test`, `/team-memory`, `/adr-skill` explicitly
- **Blunt when frustrated** — doesn't soften criticism when the agent misses something obvious

## Tone

Casual, imperative, lowercase by default. "Please" is habitual, not deferential. Goes ALL-CAPS
only when the agent has made a significant domain error. Swears occasionally under pressure.
