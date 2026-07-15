[DEVELOPER]: https://changelogue-app.azurewebsites.net/releases/5fc988f5-ad2a-4584-93f8-170cf9969b37 https://changelogue-app.azurewebsites.net/projects/1772f23b-1425-4fc3-9396-430401cc4008/semantic-releases/202fd308-c621-4999-be8e-22923df64994 我其实感觉这两个页面应该合并在第一个的页面里面， 一个初步的想法是弄成tab： 一个是basic： 就是Version Details+Release Notes 第二个semantic releases: 这个tab从上到下显是所有的report item，每个item可以展开或者折叠，最新的是默认展开，其他是折叠 Redesign based on this feedback

[AGENT]: Let me explore the two pages and related components to understand the current structure.

[AGENT]: Now I have a clear picture. Let me also check if there's a tab component available and how the semantic releases list API works.

[AGENT]: I need to check if there's an API to list semantic releases by release ID (since a release can have linked SRs).

[AGENT]: Now let me read the semantic release detail and the tabs component.

[AGENT]: Now I need to understand how to list all semantic releases for a given release. Currently the release page fetches a single SR via `release.semantic_release_id`. Let me check the API for listing SRs that reference a release.

[AGENT]: Now I have everything I need. Let me check the SemanticRelease type to see what fields are available.

[AGENT]: Good. Now let me write the plan.

[AGENT]: Starting implementation. First, I'll extract the SR report rendering into a shared component, then modify both files.

[AGENT]: Now I'll create all three files. Let me start with the shared report component, then update both pages.

[AGENT]: Now update `semantic-release-detail.tsx` to use the shared component.

[AGENT]: Now remove the helper functions that are now in the shared component.

[AGENT]: Now replace the report rendering section (items 7-13) with the shared component.

[AGENT]: Now I need to remove the remaining sections that were part of the report block (11-13 and their closing tags) and keep the source releases and context sources sections after the shared component. Let me see the current state.

[AGENT]: I need to fix the indentation — the source releases and context sources sections are still indented as if inside the old `{report && (` block. Let me fix that.

[AGENT]: Now I also need to remove the unused `SectionLabel` import since it's still used for source releases/context sources. Let me check.

[AGENT]: Good — `SectionLabel`, `ExternalLink`, `BookOpen` are still used. `Link` might not be used anymore. Let me check.

[AGENT]: Only in the import. Remove it.

[AGENT]: Now the big change — rewrite `release-detail.tsx` with tabs.

[AGENT]: Now I'll rewrite the entire file.

[AGENT]: Now I need to add the i18n keys for the new tabs. Let me find the translation files.

[AGENT]: I need to add `releases.tabBasic` and `releases.tabSemanticReleases` keys.

[AGENT]: Now do the same for zh.json.

[AGENT]: Now let me verify the build compiles.

[AGENT]: There's a duplicate variable issue in the SR detail. Let me check.

[AGENT]: Duplicate block. Let me see the context around lines 65-95.

[AGENT]: My edit left a duplicate block. Remove lines 87-90.

[AGENT]: Build succeeded. Let me start the dev server and verify.