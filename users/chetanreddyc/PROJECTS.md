# Projects — ChetanReddyC

## ChetanReddyC/Shila-Murti ★ dominant (100% of sessions)

**What it is**: An Indian e-commerce storefront selling Hindu deity sculptures, kiritams (crowns), and religious art pieces. Live at `shilamurti.com` (storefront) and `admin.shilamurti.com` (Medusa admin panel).

**Tech stack**:
- **Backend**: Medusa.js v2 (headless commerce framework), Node.js, PostgreSQL
- **Storefront**: Next.js (App Router, Turbopack), deployed on DigitalOcean App Platform
- **Auth**: Magic-link email authentication with session tracking via Cloudflare KV
- **Storage**: DigitalOcean Spaces (S3-compatible) for product images; previously Google Cloud Storage
- **Distributed locking**: Cloudflare KV + Upstash Redis for cart session coordination
- **CI/CD**: GitHub Actions → DigitalOcean (env vars set at DO app level and mirrored in GitHub Secrets)
- **CDN**: DigitalOcean Spaces CDN for image delivery

**Recurring themes in sessions**:

1. **Checkout / cart 401 errors** — the most repeated issue; root cause usually misconfigured cart session in Cloudflare KV (rotated API token not updated in DO environment variables)
2. **Magic-link UX** — duplicate tab problem when clicking magic links from email; cross-tab verification flow using BroadcastChannel + localStorage
3. **Image loading failures** — product images not loading after admin recreation or re-deploy; required migrating from GCS to DO Spaces
4. **Admin account re-creation side effects** — recreating the Medusa admin account repeatedly orphans products, sales channel associations, stock locations, and KV sessions
5. **Medusa configuration** — sales channel ↔ stock location associations, INR pricing, inventory management
6. **DO deployment issues** — environment variables not propagated, cache invalidation on force-redeploy, long build times

**Branches observed**: `fixingmajorissues`

**Product catalog** (inferred from session logs): Divine Govinda Naamam Sculpture, Venkateshwara Swami Kiritam, Black Abstract Art — suggesting a mix of traditional religious items and contemporary art.
