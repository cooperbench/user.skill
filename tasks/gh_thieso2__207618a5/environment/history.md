> DEVELOPER

i created a new sandcastle in a project and my persisted dirs/files are owned by nobody. explore the reason and propose a fix: ~/Projects/GitHub/Sandcastle % sc ls [main] Server: demo (https://demo.sandcastle.rocks) NAME PROJECT STATUS CREATED DNS TAILSCALE IP IMAGE AGE tubu sc running 2026-05-07 20:08 admin.tubu.sc.sandman 10.206.10.3 13h ago dev sc running 2026-05-08 08:49 dev.sc.sandman 10.206.10.5 - ~/Projects/GitHub/Sandcastle % ssh dev.sc.sandman ls -la /persisted [main] total 0 drwxrwxrwx 1 thies thies 48 May 7 11:16 . drwxr-xr-x 1 root root 70 May 8 06:51 .. drwxrwxr-x 1 nobody nogroup 372 May 7 11:16 dockyard drwxrwxr-x 1 nobody nogroup 1152 May 7 11:19 sandcastle drwxrwxr-x 1 nobody nogroup 558 May 7 11:16 sysbox

> DEVELOPER

i created a new sandcastle in a project and my persisted dirs/files are owned by nobody. explore the reason and propose a fix: ~/Projects/GitHub/Sandcastle % sc ls [main] Server: demo (https://demo.sandcastle.rocks) NAME PROJECT STATUS CREATED DNS TAILSCALE IP IMAGE AGE tubu sc running 2026-05-07 20:08 admin.tubu.sc.sandman 10.206.10.3 13h ago dev sc running 2026-05-08 08:49 dev.sc.sandman 10.206.10.5 - ~/Projects/GitHub/Sandcastle % ssh dev.sc.sandman ls -la /persisted [main] total 0 drwxrwxrwx 1 thies thies 48 May 7 11:16 . drwxr-xr-x 1 root root 70 May 8 06:51 .. drwxrwxr-x 1 nobody nogroup 372 May 7 11:16 dockyard drwxrwxr-x 1 nobody nogroup 1152 May 7 11:19 sandcastle drwxrwxr-x 1 nobody nogroup 558 May 7 11:16 sysbox every user of sandcastle shoudl maybe have his own fixed UIS/GID - explain your strategy

> AGENT

I'll dig into how Sandcastle creates the persisted volume and how Sysbox maps UIDs, then explain a fix.

> AGENT

I've got enough to explain it. Here's the diagnosis and a strategy. ## Why this happens The `nobody:nogroup` files were not created by `dev` — they were created by your earlier sandbox (`tubu`, created `May 7 11:16` — same timestamp as the subdirs). Both sandboxes share the same `/persisted` source on the host (`/data/users/thies/data/sc`). Sysbox's user-namespace model is what trips you up: 1. Each Sysbox container gets its **own private sub-UID range** allocated from the dockyard user's `/etc/subuid` (e.g. `tubu` → host `296608‥362143`, `dev` → host `362144‥427679`). Inside the container, that range maps to `0‥65535`. 2. The first time a bind-mount source is used, `sysbox-mgr` recursively `chown`s its contents into the calling container's range so files appear correctly owned (UID 1001 = `thies` in `tubu`). 3. When a *second* container (`dev`) starts against the same source while `tubu` is still alive, sysbox detects the mount is in use, **refuses to re-chown** (it would break `tubu`), and leaves the on-disk UIDs as-is. Those UIDs sit outside `dev`'s range, so the kernel renders them as the overflow UID `65534` → `nobody:nogroup`. The top-level `/persisted` dir itself looks correct only because the entrypoint's `chown` in `images/sandbox/entrypoint.sh:41-43` fixed the mountpoint inode (which is a […]

> DEVELOPER

create an issue for dockyard

> AGENT

Filed as [thieso2/dockyard#20](https://github.com/thieso2/dockyard/issues/20). It asks for two things: (1) a passthrough for extra `sysbox-mgr` args in `dockyard.env` so Sandcastle can disable per-container userns allocation, and (2) a deterministic `/etc/subuid` allocation wide enough to hand per-user UID offsets out of. Either #1 alone unblocks the per-user fixed-UID strategy on the Sandcastle side.