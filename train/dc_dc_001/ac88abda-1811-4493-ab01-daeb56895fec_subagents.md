---
session_id: "ac88abda-1811-4493-ab01-daeb56895fec:subagents"
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-03-29T18:20:47.582Z"
n_turns: 17
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Research the current state (as of early 2026) of Clash-compatible proxy clients for Linux x86_64 CLI (no GUI). Focus on: 1. **Mihomo (Clash Meta)** - https://github.com/MetaCubeX/mihomo - current status, latest release, features vs original Clash 2. **sing-box** - https://github.com/SagerNet/sing-box - comparison with Mihomo, subscription compatibility 3. **Original Clash** - is it still maintained? (it was removed/archived) Key use case requirements: - Linux x86_64, Ubuntu 24.04, CLI only (no GUI/desktop) - Must support `relay` proxy chains (chaining proxies) - Must accept Clash-format subscription URLs - Must support SOCKS5 outbound proxies (for chaining with existing SOCKS5) - Must support rule-based routing (domain-suffix rules) - Trojan protocol support For each option evaluate: - Active maintenance status (last commit, release date) - relay/proxy chain support - SOCKS5 outbound support - Clash subscription format compatibility - Memory/CPU footprint - Installation method on Ubuntu Do web searches to get current information. Return a clear comparison with a final recommendation.

> AGENT

I'll research the current state of Clash-compatible proxy clients for Linux as of early 2026. Let me search for information on each of these projects.

> AGENT

Let me get more specific information about each project's features and compatibility.

> AGENT

Let me search for more specific information about recent commits, memory footprint, and Ubuntu installation methods.

> AGENT

Now let me search for information about memory and CPU footprint comparisons.

> AGENT

Now let me search for more specific information about dialer-proxy and sing-box's equivalent chaining mechanism.

> AGENT

Perfect. Now I have comprehensive information to provide a detailed comparison. Let me compile the final report. ## Comprehensive Comparison: Clash-Compatible Proxy Clients for Linux x86_64 CLI (Early 2026) Based on my research, here's the current state of Clash-compatible proxy clients as of March 2026: --- ### 1. MIHOMO (Clash Meta) - https://github.com/MetaCubeX/mihomo **Status & Maintenance:** - **Actively maintained** as of March 29, 2026 - Latest Prerelease-Alpha released March 29, 2026 (synchronizing Alpha branch) - Continuous commits addressing gRPC issues, connection handling, rule disabling, and performance improvements - This is the community fork that superseded the original Clash **Key Features vs Original Clash:** - Added support for VLESS, Trojan Reality, Hysteria2, TUIC, WireGuard alongside original protocols - XTLS variants (VLESS XTLS, Trojan XTLS) support - Modern protocol support making it significantly more capable than original Clash **Relay/Proxy Chain Support:** - **Status:** Relay group type was deprecated in v1.18.6 and completely removed - **Current method:** Uses `dialer-proxy` configuration at individual proxy level - Supports UDP transmission if both head and tail nodes support UDP over TCP - More flexible and granular approach than the legacy relay system **SOCKS5 Outbound Support:** - Full support via mixed port (HTTP(S) + SOCKS5) - Can be used as `dialer-proxy` target for chaining - Fully functional for routing traffic through SOCKS5 **Clash Subscription Format:** - **Native support** for Clash-format subscription URLs - Compatible with proxy-providers - Supports vless://, vmess://, ss://, trojan://, ssr://, hysteria://, hy2://, tuic:// formats **Trojan Protocol:** - Full support including Trojan XTLS variant **Installation on Ubuntu 24.04:** - Download binary from GitHub releases (no apt/snap packages available) - Manual installation: Download to `/usr/local/bin/mihomo` and config to `/etc/mihomo/config.yaml` - No official package manager integration for apt or snap **Memory/CPU Footprint:** - Efficient performance (described as "very top-level operating efficiency") - Performance largely depends on TUN/redirect mode selection - Comparable to sing-box in non-TUN modes - TUN mode less optimized than sing-box's auto_redirect mode --- ### 2. SING-BOX - https://github.com/SagerNet/sing-box **Status & Maintenance:** - **Actively maintained** as of March 2026 - Latest stable: v1.13.4 (March 26, 2026) - Pre-release: v1.14.0-alpha.6 (March 25, 2026) - Regular commits and issues being addressed **Key Features:** - Universal proxy platform with "universal" as its core design philosophy - Advanced routing and protocol support - Transparent proxying capabilities **Relay/Proxy Chain Support:** - **Not directly comparable to Mihomo's relay** - Uses routing-based chaining via outbound configuration - Outbounds can be chained through […]

> DEVELOPER

Do thorough web research to find ALL domains used by these three AI companies that need to be proxied. I need complete domain lists for: 1. **Anthropic** (Claude) - ALL domains including: - Main website, API endpoints - CDN domains, asset domains - Auth domains - Any subdomains used by Claude.ai web app - statsig, sentry, analytics used by Claude 2. **OpenAI** (ChatGPT, API) - ALL domains including: - openai.com and all subdomains in use - ChatGPT specific domains - CDN/asset domains - Auth0 domains used by OpenAI - Azure OpenAI endpoints - openaiusercontent.com, oaiusercontent.com - Any other domains in their ecosystem 3. **Google AI** (Gemini, Vertex AI) - ALL domains including: - gemini.google.com - generativelanguage.googleapis.com - Any other Gemini/Vertex AI specific domains - Google AI Studio domains Search for existing Clash/Mihomo rule sets on GitHub that cover these domains comprehensively. Look for: - blackmatrix7/ios_rule_script - ACL4SSR - Loyalsoldier/clash-rules - Any other popular rule repositories The goal is to ensure complete coverage so that when using a residential IP proxy for AI traffic, ALL requests related to these services go through the proxy - especially important for account safety (avoiding IP mixing). Return a definitive, clean list organized by company with DOMAIN-SUFFIX and DOMAIN-KEYWORD entries suitable for Mihomo config.

> AGENT

I'll help you find comprehensive domain lists for these AI companies. Let me search for existing rule sets and domain information.

> AGENT

Let me search for more specific domain lists and GitHub repositories.

> AGENT

Now let me fetch the actual GitHub repositories to get the complete domain lists:

> AGENT

Let me search for more specific domain information and complete lists:

> AGENT

Let me search for more specific domain lists and documentation:

> AGENT

Perfect! Now let me get more information about the actual domain lists from these repositories:

> AGENT

Let me search for more specific networking and domain information:

> AGENT

Now let me search for some additional specific domains and complete the picture:

> AGENT

Based on my comprehensive research, here is the definitive compiled list of ALL domains used by these three AI companies that should be proxied: ## COMPREHENSIVE AI COMPANY DOMAIN LISTS FOR MIHOMO PROXY ### 1. ANTHROPIC (CLAUDE) **Main Domains:** - DOMAIN-SUFFIX,anthropic.com - DOMAIN-SUFFIX,claude.ai - DOMAIN-SUFFIX,claude.com - DOMAIN-SUFFIX,claudeusercontent.com **API & Platform:** - DOMAIN-KEYWORD,api.anthropic.com - DOMAIN-KEYWORD,platform.claude.com - DOMAIN-KEYWORD,docs.anthropic.com **Authentication & Support:** - DOMAIN-KEYWORD,console.anthropic.com (now redirects to platform.claude.com) - DOMAIN-KEYWORD,status.anthropic.com - DOMAIN-KEYWORD,support.claude.com **Analytics & Monitoring:** - DOMAIN-SUFFIX,statsig.com - DOMAIN-KEYWORD,api.statsig.com - DOMAIN-KEYWORD,events.statsig.com - DOMAIN-SUFFIX,sentry.io - DOMAIN-KEYWORD,sentry.io **CDN & Assets:** - DOMAIN-KEYWORD,downloads.claude.ai **Voice Services (New - March 2026):** - DOMAIN-SUFFIX,livekit.cloud - DOMAIN-SUFFIX,deepgram.com --- ### 2. OPENAI (CHATGPT) **Main Domains:** - DOMAIN-SUFFIX,openai.com - DOMAIN-SUFFIX,chatgpt.com - DOMAIN-SUFFIX,chat.com - DOMAIN-SUFFIX,oaiusercontent.com - DOMAIN-SUFFIX,oaistatic.com - DOMAIN-SUFFIX,sora.com **Chat & API:** - DOMAIN-KEYWORD,api.openai.com - DOMAIN-KEYWORD,chat.openai.com - DOMAIN-KEYWORD,gpt.openai.com - DOMAIN-KEYWORD,platform.openai.com - DOMAIN-KEYWORD,platform-api.openai.com **Authentication:** - DOMAIN-KEYWORD,auth.openai.com - DOMAIN-KEYWORD,auth0.openai.com **File Upload & User Content:** - DOMAIN-SUFFIX,oaiusercontent.com - DOMAIN-KEYWORD,files.oaiusercontent.com - DOMAIN-KEYWORD,files07.oaiusercontent.com - DOMAIN-KEYWORD,files08.oaiusercontent.com - DOMAIN-KEYWORD,files09.oaiusercontent.com **CDN & Infrastructure:** - DOMAIN-KEYWORD,openai.com.cdn.cloudflare.net - DOMAIN-KEYWORD,openaiapi-site.azureedge.net - DOMAIN-KEYWORD,openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net - DOMAIN-KEYWORD,openaicom.imgix.net - DOMAIN-KEYWORD,openaicomproductionae4b.blob.core.windows.net - DOMAIN-KEYWORD,production-openaicom-storage.azureedge.net - DOMAIN-SUFFIX,akamaized.net **Analytics & Feature Management:** - DOMAIN-SUFFIX,statsig.com - DOMAIN-KEYWORD,events.statsig.com - DOMAIN-KEYWORD,events.statsigapi.net - DOMAIN-SUFFIX,segment.com - DOMAIN-KEYWORD,cdn.segment.com - DOMAIN-SUFFIX,launchdarkly.com **Customer Service & Communication:** - DOMAIN-SUFFIX,intercom.io - DOMAIN-KEYWORD,intercomcdn.com **Support & Community:** - DOMAIN-KEYWORD,help.openai.com - DOMAIN-KEYWORD,community.openai.com - DOMAIN-KEYWORD,status.openai.com - DOMAIN-KEYWORD,developers.openai.com **Voice Services (LiveKit - Advanced Voice Mode):** - DOMAIN-SUFFIX,livekit.cloud - DOMAIN-KEYWORD,chatgpt.livekit.cloud - DOMAIN-KEYWORD,host.livekit.cloud **Regional Storage (Livekit webpub):** - DOMAIN-KEYWORD,chatgpt-async-webps-prod-*.webpubsub.azure.com --- ### 3. GOOGLE AI (GEMINI / VERTEX AI) **Consumer Gemini:** - DOMAIN-SUFFIX,gemini.google.com - DOMAIN-KEYWORD,gemini.google.com **Developer Platforms:** - DOMAIN-SUFFIX,ai.google.dev - DOMAIN-SUFFIX,aistudio.google.com - DOMAIN-KEYWORD,ai.google.dev - DOMAIN-KEYWORD,aistudio.google.com **Workspace Studio:** - DOMAIN-KEYWORD,workspace.google.com/studio **Google Cloud - Vertex AI:** - DOMAIN-SUFFIX,cloud.google.com - DOMAIN-KEYWORD,cloud.google.com - DOMAIN-KEYWORD,vertex-ai.cloud.google.com - DOMAIN-KEYWORD,docs.cloud.google.com **Gemini API Endpoints:** - DOMAIN-SUFFIX,generativelanguage.googleapis.com - DOMAIN-KEYWORD,generativelanguage.googleapis.com - DOMAIN-KEYWORD,generativelanguage.googleapis.com/v1beta **Google APIs (General):** - DOMAIN-SUFFIX,googleapis.com - DOMAIN-SUFFIX,google.com **Google Cloud AI/Generative AI:** - DOMAIN-KEYWORD,cloud.google.com/generative-ai-studio **Documentation:** - DOMAIN-KEYWORD,ai.google.dev/api - DOMAIN-KEYWORD,docs.cloud.google.com --- ## ADDITIONAL THIRD-PARTY SERVICES (Used by multiple AI companies) These should be included to ensure comprehensive coverage: **Error Tracking & Monitoring:** - DOMAIN-SUFFIX,sentry.io - DOMAIN-SUFFIX,datadoghq.com - DOMAIN-SUFFIX,datadoghq.eu **Feature Management:** - DOMAIN-SUFFIX,statsig.com - DOMAIN-SUFFIX,launchdarkly.com **Analytics & Events:** - DOMAIN-SUFFIX,segment.com **Customer Communication:** - DOMAIN-SUFFIX,intercom.io - DOMAIN-SUFFIX,intercomcdn.com **Authentication:** - DOMAIN-SUFFIX,auth0.com **Infrastructure:** - DOMAIN-SUFFIX,livekit.cloud - DOMAIN-SUFFIX,deepgram.com --- ## NOTES FOR IMPLEMENTATION 1. **Wildcard Priority**: When using DOMAIN-SUFFIX (which matches subdomains), it's more efficient than listing individual subdomains. Example: `DOMAIN-SUFFIX,anthropic.com` covers api.anthropic.com, console.anthropic.com, etc. 2. **Account Safety**: To prevent IP mixing issues and maintain account security when using residential proxies, ensure ALL these domains are routed through your proxy to avoid detection/mixing of IPs across […]
