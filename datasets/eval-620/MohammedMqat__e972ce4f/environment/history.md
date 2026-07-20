> DEVELOPER

read @docs/plans/week-6-7-todo.md and lets start

> AGENT

I've read the todo file. All 20 tasks across all 4 phases are checked off as complete. Nice work!

However, git status shows you have an uncommitted change in `src/controllers/auth.js`. Let me check what's been modified.

> TOOL

tool_use Bash
id: toolu_01GEKG1AuZgNt261yBHYGpzD
```json
{
  "command": "git diff src/controllers/auth.js",
  "description": "Show uncommitted changes in auth.js"
}
```

> TOOL

tool_result
id: toolu_01GEKG1AuZgNt261yBHYGpzD
```
diff --git i/src/controllers/auth.js w/src/controllers/auth.js
index 2aeb997..7cc9159 100644
--- i/src/controllers/auth.js
+++ w/src/controllers/auth.js
@@ -44,7 +44,7 @@ export function login(req, res, next) {
         if (!isMatch) {
           return res.status(401).json({ message: "invalid credentials" });
         }
-        const token = jwt.sign({ username: user.username }, process.env.JWT_SECRET);
+        const token = jwt.sign({ id: user.id, username: user.username }, process.env.JWT_SECRET);
         res.cookie("token", token, { httpOnly: true });
         return res.status(200).json({ username: user.username });
       });
```

> AGENT

The pending change adds `id: user.id` to the JWT payload in the login controller — so the token now carries the user's database ID alongside the username. This is a useful change since protected routes (like favorites) likely need the user ID.

Everything on the todo is done. What would you like to do next — commit this change, or is there something else you'd like to work on?