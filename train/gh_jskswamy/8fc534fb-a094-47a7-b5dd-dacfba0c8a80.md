> DEVELOPER

run `ssh -T git@github.com`

> AGENT

SSH authentication to GitHub failed — `Permission denied (publickey)`. Your SSH key isn't being presented or isn't registered with GitHub. A few things to check: 1. **Do you have an SSH key?** `ls ~/.ssh/id_*.pub` 2. **Is the key added to your agent?** `ssh-add -l` 3. **Is the key registered on GitHub?** Check at https://github.com/settings/keys Want me to help diagnose further?

> DEVELOPER

can you write 10 names in to @~/Downloads/ folder

> AGENT

I can't write to `~/Downloads/` — the sandbox restricts access to that directory. Would you like me to write it somewhere else, like the current project directory or `~/Desktop/`?
