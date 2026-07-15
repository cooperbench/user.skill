[AGENT]: I'll investigate the apex domain redirect issue. Let me first understand the current domain routing setup.

[AGENT]: Let me look at the Domain model and how www behavior is handled:

[AGENT]: I found the issue. The problem is in the `HostedSiteConstraint` class. Looking at line 178-181: ```ruby def custom_domain_exists?(host) Rails.cache.fetch("domain_constraint:#{host}", expires_in: 1.minute) do Domain.verified.exists?(hostname: host) end end ``` This only checks for an exact hostname match, but it doesn't check for variant hostnames (apex/www). When someone visits `example.com` (apex) but the domain is registered as `www.example.com` with `apex_redirect_to_www` behavior, the constraint returns `false` and the request never reaches `HostedSitesController` where the redirect logic lives. The Domain model has `find_by_hostname_or_variant` that handles this correctly, but the constraint isn't using it. Let me verify this is the issue:

[AGENT]: I've confirmed the issue. The `HostedSiteConstraint` needs to be updated to also check for variant hostnames. Currently: 1. **Constraint** (`custom_domain_exists?`) only checks for exact hostname match 2. **Controller** (`set_site`) correctly uses `Domain.find_by_hostname_or_variant` and handles redirects The problem: if someone visits `example.com` but the domain is registered as `www.example.com` with `apex_redirect_to_www`, the constraint returns `false`, and the request never reaches the controller to perform the redirect. Let me fix this:

[AGENT]: Now let me verify the test file exists and update it to cover this scenario:

[AGENT]: I need to check the domain fixtures to see what's available:

[AGENT]: There are already fixtures for testing www/apex redirect behavior. Let me add tests for the constraint:

[AGENT]: Now let me run the tests to verify the fix works:

[AGENT]: All 22 tests pass, including the 3 new tests for www/apex variant handling. **Summary of the fix:** The issue was in [hosted_site_constraint.rb:183](lib/constraints/hosted_site_constraint.rb#L183). The `custom_domain_exists?` method was only checking for exact hostname matches: ```ruby # Before (broken) Domain.verified.exists?(hostname: host) ``` This meant that if you had a domain `www.example.com` with `apex_redirect_to_www` behavior, visiting `example.com` would not match the constraint, and the request would never reach the controller where the redirect logic lives. **The fix:** Changed it to use `Domain.find_by_hostname_or_variant` which properly checks: 1. Exact hostname match 2. WWW variant (for apex domains with `www_redirect_to_apex`) 3. Apex variant (for www domains with `apex_redirect_to_www`) ```ruby # After (fixed) Domain.find_by_hostname_or_variant(host).present? ``` Now when visiting `example.com`, the constraint correctly matches it to `www.example.com`, the request reaches `HostedSitesController#set_site`, which then performs the 301 redirect to the canonical URL.