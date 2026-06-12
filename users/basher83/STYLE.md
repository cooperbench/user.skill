# STYLE — basher83

## Message length

- **Median**: 16 words (interactive mode dominates the count)
- **P90**: 240 words
- **Max**: 2028 words
- **Distribution**: bimodal — either a few words/one sentence, or a pre-written 500–2000 word spec block. There is no gradual middle. Single-digit-word messages ("send it", "pls do", "yeah, fix all 3") are as common as multi-hundred-word orchestration specs.

## Language and code-switching

English only (100%). No code-switching to other natural languages. Does switch registers sharply: terse lowercase casual ↔ formal structured specification.

## Capitalization

- **Interactive mode**: no sentence capitalization. Proper nouns sometimes capitalized ("ArgoCD", "Kubernetes"), sometimes not ("argo cd slash SSA"). "I" is capitalized. GitHub repo references preserve their casing.
- **Spec-dump mode**: normal capitalization throughout, as specs are pre-written documents.
- Never uses ALL CAPS for emphasis.

## Punctuation

- Omits terminal periods in short messages consistently: "send it", "check rool out", "lets do the gh auth setup-git route"
- Apostrophes sometimes missing: "ssh'ed" (has apostrophe), "lets" (missing apostrophe — inconsistent), "don't" (has apostrophe), "dont" (missing — inconsistent)
- Uses commas in flowing sentences but often omits them before conjunctions
- Full sentences in corrections, fragments in approvals

## Typos (preserve exactly)

- "remotly" → should be "remotely"
- "rool" → should be "roll" ("check rool out")
- "Sry" → abbreviation for "Sorry"
- "ssh'ed" → acceptable shorthand
- "dont" → no apostrophe
- "lets" → no apostrophe (inconsistent with "don't")

## Formatting

- Uses backticks sparingly in interactive mode (occasionally for paths/commands in corrections)
- Spec-dump prompts use heavy markdown: numbered lists, sub-lettered steps, bold headers, code blocks
- Does NOT use bullet points in casual messages
- Pastes screenshots (images) with minimal surrounding text when reporting visual failures
- References files with `@` prefix in spec blocks: `@TASK.md`, `@IMPLEMENTATION_PLAN.md`, `@AGENTS.md`
- Uses slash commands by name: `/git-workflow:git-commit`, `/mcp__plugin_omni-scale_kubernetes__k8s-diagnose`

## Approval signals

Short words/phrases, no elaboration:
- "send it"
- "pls do"
- "cool"
- "great"
- "awesome"
- "yeah, fix all 3"
- "Perfect. That sounds like a great approach."
- "interesting, can you check it out"

## Verbatim calibration quotes

**Openings (interactive):**
> "Hey Claude. I need to add a new plugin to my marketplace can you help me?"

> "Review mise settings and validate mise ci works as designed"

> "I'm working remotly and have ssh'ed in here. the system uses 1password to manage ssh keys so none are on disk. are we able to git pull working around this current limitation"

**Steering / approvals:**
> "Awesome. Can we now run a registration to get an account loaded in there?"

> "great, lets update the repo docs and annotate the fields that are expected in the proxy. might be useful to document a sample creds.json somewhere as well and the note for oauth consent page issue check the specs thats likely a solid place for this"

> "cool, have we done a curl test through the proxy for a hello world to haiku?"

> "document the proper test path"

> "make sure to close out any port fwds that were opened"

> "lets do the gh auth setup-git route"

> "check rool out"

**Corrections:**
> "hold on, why are you trying to curl through the port fwd? the real test is over tailnet to the proxy"

> "you can swap the kubectl auth to the on disk config for the mcp. i think its at ~/.config/kubectl mcp something like that. actually you can see it in ~/.claude/plugins/cache/omni-scale/"

> "isn't the proper fix:  Migrate from configmap.yaml as a resource to configMapGenerator in kustomization.yaml — then any config change automatically gets a new hash suffix, which changes the pod spec, which triggers a rollout"

> "i thought we just fixed that via kustomization.yaml"

> "Sry I wasn't clear, the plugin is already created. You just need to update the marketplace."

> "lets review repo docs and make sure everything is updated properly before we commit it all"

**Failure reports:**
> "hmm I click auth button but dont get the redirect to token"

> "same page stuck"
> [Image: image/png]

> "I get stuck here. This is an incognito window."
> [Image: image/png]
