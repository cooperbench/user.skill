[DEVELOPER]: read @docs/plans/week-6-7-todo.md and lets start

[AGENT]: I've read the todo file. All 20 tasks across all 4 phases are checked off as complete. Nice work! However, git status shows you have an uncommitted change in `src/controllers/auth.js`. Let me check what's been modified.

[AGENT]: The pending change adds `id: user.id` to the JWT payload in the login controller — so the token now carries the user's database ID alongside the username. This is a useful change since protected routes (like favorites) likely need the user ID. Everything on the todo is done. What would you like to do next — commit this change, or is there something else you'd like to work on?