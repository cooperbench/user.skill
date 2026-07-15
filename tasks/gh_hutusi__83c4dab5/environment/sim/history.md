[DEVELOPER]: there seem not sign up or create account on welcome page, if it is a new user, he can not create an account

[AGENT]: The user reports that a brand-new user can't create an account from the welcome page. Let me explore the welcome/auth flow from the recent identity rework to understand what's there today.

[AGENT]: The fix is now clear and small. Let me check the docs that describe this flow so the plan covers the required doc updates.

[AGENT]: Plan approved. Starting with the fix in `AccountPanel.tsx`.