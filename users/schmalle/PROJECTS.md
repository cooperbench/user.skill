---
name: schmalle-projects
description: Repos, tech stack, and recurring work themes for schmalle.
---

## schmalle/secman ★ DOMINANT (100% of sessions)

A production **security-management platform** deployed at `secman.covestro.net`. Schmalle is the sole developer and owner.

### What it does
- Ingests vulnerability data from **CrowdStrike Falcon API** (800 000+ vulnerabilities per customer environment)
- Tracks **assets** (servers, EC2 instances) linked to AWS accounts, AD domains, workgroups
- Manages **vulnerability exceptions** (request → review → approval → expiration workflow)
- **Alignment/release gating**: requirement change reviews, reviewer feedback, NOGO/CHANGE/GO assessments, Excel exports
- **User access control**: RBAC (ADMIN, SECCHAMPION, VULN, RELEASE_MANAGER, REQADMIN roles), workgroup-based filtering, AWS account sharing, AD domain mapping
- **CLI**: Kotlin/PicoCLI tool for CrowdStrike data import, S3 bucket management
- **Security hardening**: JWT signing, JWKS validation, WebAuthn, OAuth OIDC, CSP, rate limiting, encrypted fields at rest

### Tech stack
| Layer | Technologies |
|-------|-------------|
| Backend | Kotlin, Micronaut, JPA/Hibernate, Flyway, MariaDB, HikariCP |
| Frontend | Astro, React (TSX), Bootstrap 5, Axios, ExcelJS, Playwright |
| CLI | Kotlin, PicoCLI, AWS S3 SDK v2 |
| Auth | JWT (HS256), HttpOnly cookies, OAuth OIDC, WebAuthn/FIDO2, TOTP |
| Cloud | AWS S3, AWS EC2 (via CrowdStrike metadata), CrowdStrike Falcon API |
| Build | Gradle multi-project (`:backendng`, `:cli`, `:shared`, `:frontend`) |
| Test | Playwright E2E (Edge + Chrome), JUnit, credentials via 1Password CLI |

### Recurring work themes (session-frequency order)

1. **Debugging UI discrepancies**: stale data vs. live-calculated values, NaN pagination, wrong error states swallowing pages, badge/count mismatches. Usually screenshot-reported.
2. **Security hardening**: OWASP Top 10 audit passes, JWT `alg:none` fix, JWKS fallback removal, rate limiting, CSP, cookie flags, hardcoded secrets removal. Full parallel sub-agent reviews.
3. **Access control extensions**: Adding new access-control criteria (owner field, AWS sharing, domain mapping, workgroup membership) to asset and vulnerability queries. Always follows the same chain: backend filter → service merge → frontend visibility guard.
4. **Exception workflow features**: Exception request lifecycle (create, approve, cancel, supersede, delete), scope types (SINGLE_VULNERABILITY, CVE_PATTERN, ASSET, IP, PRODUCT), access control on requests.
5. **Feature completions / table columns**: Adding AWS Account ID, Instance ID, Account column to various tables. Removing clutter columns. Renaming labels. Very frequent small UI iterations.
6. **Export functionality**: Excel downloads for vulnerability data, reviews, config bundles. Memory optimization for large exports (lazy ExcelJS import, streaming).
7. **CLI improvements**: CrowdStrike import memory optimization (streaming vs. batch), S3 local testing support (Adobe S3Mock, `--endpoint-url`), Micronaut `cli` environment isolation to suppress backend startup listeners.
8. **Config bundle import/export**: Serialization of users, workgroups, mappings, email configs, AWS sharing rules across environments.
9. **Sidebar/navigation visibility rules**: Showing/hiding menu items based on user role and data availability (no workgroups → hide WG vulns, no AWS accounts → hide Account vulns, ADMIN → hide filtered views).
10. **Performance**: Memory footprint reduction for 800k+ vulnerability imports, lazy bundle splitting to avoid reverse-proxy truncation, pagination for large datasets.
