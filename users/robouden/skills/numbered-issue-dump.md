---
name: numbered-issue-dump
description: >
  Trigger: robouden has 2–4 related fixes or improvements he wants done together.
  He batches them as a numbered list using "N-" (hyphen not period) format.
---

When robouden has multiple related items he fires them in one message, numbered with
a hyphen. He does not wait for one to be done before listing the next. Items are
terse imperatives, often with typos, and may mix bug fixes with UI changes:

Example 1 (opening prompt):
```
1- Now it seems we have a fied pixel width of the page,.Can you make the width of the withd just a procentage of the width and the text dynamyically adjusting?
2- Still in a table to much  space between the header and the data, Can you make the space smaller?
3- Text in tables, should be hythenaten not cut off
```

Example 2 (opening prompt):
```
1- Can you change the login for the users to be able to login with their API key or thier password?
2- if a new register, send the api key to them.
3- add  option for (admin only) to generate new api key for users.
```

Example 3 (mid-session correction):
```
Two more things to imrove.
1- make the downlaod button the same blue color as the rest of the buttons.
2- the log and text of the header on the right should , if clicked clear the page.
```

Note: the intro line ("Two more things to imrove.") is optional and short. Items are
always hyphen-separated. No trailing punctuation after list items is common.
