---
name: release-command
description: >
  Triggered when features are merged and the user is ready to cut a release. User issues a
  short directive with the exact version number and expects all three release steps executed:
  code/version bump + npm publish + gh release. Sometimes asks for confirmation before publish.
---

melagiri cuts releases frequently (multiple per week during active development). His release commands are short and exact.

**Example 1:**
> "i think this should make the release 3.4.0 \n\nprepare the release with relevant updates to code, npm publish and gh release"

**Example 2:**
> "yes, do all necessary changes required to bump to 3.0.3 including npm publish and gh release"

**Example 3 (stop before publish):**
> "ok great. i think we are ready for another release.. One last task is add screenshot images to the @cli/README.md... Plan and set them up and finally bump the version to v3.5.0 and just come back to me before npm publish and git release"

**Example 4 (version + all steps):**
> "yes, bump to 3.6.0 and commit, push to master and then gh release along with npm publish"

**Example 5 (patch bump):**
> "also, bump the version to 3.1.2 and publish to gh and npm"

**Pattern**:
- Always specifies the exact semver string
- Expects all three steps: bump package.json(s) + `npm publish` + `gh release create`
- Occasionally adds a stop gate ("come back to me before npm publish") for big releases
- Uses "gh release" not "GitHub release"
- Expects version bump to follow patterns in existing commit history ("Look at old version bump commits for reference")
