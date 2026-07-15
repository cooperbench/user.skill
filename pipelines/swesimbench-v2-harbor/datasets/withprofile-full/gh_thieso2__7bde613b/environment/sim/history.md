[DEVELOPER]: in the tmux.conf - when createing a new shell always do in in the currect working dir.

[AGENT]: Updated `images/sandbox/tmux.conf:17-20`. New windows (`prefix c`) and split panes (`prefix "` / `prefix %`) now open in the current pane's working directory via `-c "#{pane_current_path}"`. Note: `home-snap/` and `oidc/` have their own copies (untracked dirs in git status) — let me know if you want those updated too.

[DEVELOPER]: also alswy insert a new window rtight to the currect by default

[AGENT]: Added `-a` to the `new-window` bind so new windows are inserted immediately after the current one. Combined with `renumber-windows on`, the indices stay tidy.

[DEVELOPER]: commit

[AGENT]: Committed as `9e05374`, one commit ahead of origin.

[DEVELOPER]: commit and push

[AGENT]: Pushed `9e05374` to `origin/feat/projects-crud-and-filter`.

[AGENT]: # PR #91 Review — feat(projects): CRUD in user settings + dashboard project filter ## Overview Moves project management into Settings (new "Projects" tab with list/edit/delete actions), adds a project filter pills row to the dashboard, and DRYs the project form into a shared `_form` partial used by both `new` and `edit`. +200/-99, mostly view-layer + a small controller refactor. Also bundles an unrelated tmux.conf tweak. ## What's good - **Authorization is tight.** `set_project` does `policy_scope(Project).find` *and* `authorize @project` — defense in depth. Cross-user IDs return 404 rather than 403. `ProjectPolicy#owner_only?` covers update/destroy. - **DRY.** Extracting `_form.html.erb` removes ~90 lines of duplication between `new` and `edit`. - **No mass-assignment leaks.** `project_params` doesn't permit `user_id`; `Project.user` is set via `Current.user.projects.build`. - **`(none)` sentinel is safe.** Project name regex `/\A[a-z][a-z0-9_-]{0,62}\z/` rejects `(`, so the string can't collide with a real project name. - **CSRF/auth on destroy.** `button_to … method: :delete` issues a real form with token; `turbo_confirm` is the UX layer on top. ## Issues / suggestions ### Convention violation: guide.html.erb not updated Per `CLAUDE.md`: *"When features are changed or added, update the guide page at `app/views/pages/guide.html.erb`."* This PR ships a new Settings tab + dashboard filter and doesn't touch the guide. […]