> DEVELOPER

i want that that sandcastle cli maintains /etc/hosts so that i can ping sandcastle.project and don't need to remember tailscale ip adresses. whats the best ways to do this on my mac. any btter way that /etc/hosts (needs sudo).

> AGENT

I’ll first check how the Sandcastle CLI is structured and how it currently discovers project/Tailscale addresses, then I’ll map the macOS options against that shape.

> AGENT

The CLI is a Go/Cobra app under `vendor/sandcastle-cli`; the Rails app already exposes project/sandbox API data and has a `TailscaleManager` that reads sandbox IPs from Docker network state. I’m narrowing down which API fields the CLI can already consume and whether names are unique enough for DNS aliases.

> AGENT

Two practical paths stand out. The best low-friction option is to lean on Tailscale MagicDNS by making the sandbox machine name stable; a Sandcastle-managed DNS layer is better only if you specifically want custom names like `sandbox.project` rather than Tailscale’s tailnet names.

> AGENT

A local resolver means macOS delegates only a chosen suffix, for example `.project`, to a small DNS service running on your Mac. Sandcastle would update that service’s data from the API, and macOS would ask it whenever you run `ping sandcastle.project`.

> AGENT

A local resolver would look like this on macOS: 1. One-time sudo setup: Create `/etc/resolver/project`, telling macOS that names ending in `.project` should go to a local DNS server. Example: ```text nameserver 127.0.0.1 port 53535 ``` 2. Sandcastle runs or manages a small local DNS service on `127.0.0.1:53535`. 3. That DNS service answers records like: ```text sandcastle.project -> 100.x.y.z mybox.project -> 100.x.y.z api.project -> 100.x.y.z ``` 4. The CLI keeps the records fresh by calling the existing Sandcastle API, which already returns sandbox names and `tailscale_ip`. The upside over `/etc/hosts`: no sudo for every IP change, no fragile file editing, TTLs can be short, and stale entries can disappear automatically. The downside: you now have a background service/launch agent to install and debug. My recommendation: Use Tailscale MagicDNS if you can accept Tailscale-style names. Tailscale’s docs say MagicDNS lets devices be reached by machine name, and macOS tools like `ping` use system DNS even though `host`/`nslookup` may not. Use a Sandcastle local resolver if you specifically want friendly Sandcastle-owned names like `sandbox.project`. I would avoid direct `/etc/hosts` syncing except as a fallback command like `sandcastle dns hosts sync`, because it needs sudo and gets stale easily. Sources: Tailscale MagicDNS docs: […]