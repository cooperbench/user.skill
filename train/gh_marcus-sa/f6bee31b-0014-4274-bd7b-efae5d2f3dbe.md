> DEVELOPER

write a README.md in each of the modules in server dirs following this format: # Address Labeling Looks up and classifies blockchain addresses via external providers (Arkham, Etherscan, on-chain registries) with forensic provenance tracking. ## The Problem A tax authority examines a blockchain transaction and sees funds moving to address `0x123...`. They need to answer: *"Who controls this address?"* Is it a centralized exchange (reportable), a DeFi protocol (different treatment), or an unknown wallet (requires investigation)? Getting this wrong affects tax treatment. Sending funds to Binance might indicate a disposal. Sending to a bridge is a cross-chain transfer (non-taxable). Sending to an unknown address could be either—or a gift, or a payment. ## What It Does - **Multi-provider address lookup**: Queries Arkham, Etherscan, and other providers for address classification - **Coalescing cache**: Deduplicates concurrent requests for the same address - **Tiered verification**: Maps provider confidence to forensic evidence tiers - **Negative caching**: Remembers when providers don't know an address to avoid repeated lookups - **Provenance tracking**: Stores raw provider responses for audit reconstruction ## Key Concepts | Term | Definition | |------|------------| | **Provider** | External API that classifies addresses (Arkham, Etherscan, ENS) | | **ProviderResult** | Standardized response format with label, category, and verification status | | **AddressCategory** | Classification type: Exchange, DeFi Protocol, Bridge, Contract, Unknown | | **Verification Tier** | Evidence quality: Tier1 (authoritative), Tier2 (verified), Tier3 (investigative) | | **Negative Lookup** | Cached result indicating no provider has classification for an address | | **CoalescingCache** | Mechanism that merges concurrent requests for the same lookup into one | ## Verification Tiers | Provider Result | Maps To | Usage | |-----------------|---------|-------| | `verified=true` | Tier2HighConfidence | External verification, auto-apply with audit flag | | `verified=false` | Tier3Investigative | Requires corroboration before reliance | | (Tier1 reserved) …

> AGENT

Let me explore the server directory structure first.

> AGENT

That's 28 server modules. Let me research them all in parallel, then write the READMEs. I'll launch multiple explore agents to cover all modules.

> AGENT

Launched 4 research agents in parallel to explore all 28 server modules. I'll write the READMEs once they report back.

> AGENT

All 4 research agents completed. Let me check the surreal module and a few files I need more detail on.

> AGENT

All research complete. Now I'll write all 27 READMEs in parallel batches. Let me start with the first batch.

> AGENT

All 27 READMEs written. Let me verify the count and check for any remaining modules.

> AGENT

27 READMEs created across all server modules (the `surreal/` directory had no TypeScript files so was skipped). Each README follows the format with: - **Title** — module name and one-line description - **The Problem** — why this module exists - **What It Does** — bullet points of capabilities - **Key Concepts** — terminology table - **How It Works** — concrete example flow - **Edge Cases** — table of scenarios and behaviors (where applicable) - **Where It Fits** — ASCII architecture diagram showing connections - **File Structure** — annotated file listing

> DEVELOPER

commit

> AGENT

Committed `b6d22b87` — 27 READMEs, 2,252 lines added across all server modules.
