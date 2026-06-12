---
name: Pavel401 — Persona
---

# Persona

## Role and seniority (inferred)

Founder or senior IC building a developer tooling product. Works solo or in a very small team — all sessions are on a single repo with no collaborators mentioned. Comfortable making cross-cutting architecture decisions (storage choice, agent pipeline design, graph schema) without consulting others. (inferred)

## Domain expertise

- **Python / FastAPI backend**: fluent — writes detailed line-level corrections referencing FastAPI patterns (Depends, HTTPException), Pydantic v2 model fields, async/await.
- **Neo4j / Cypher**: learning — explicitly says "I have no knowledge of Cypher, I don't mind details" and "Can you create an easy guide for someone who doesn't know SQL." Understands the *purpose* of graph queries but delegates their authoring.
- **Firebase/Firestore**: proficient — makes storage architecture decisions, understands document vs graph trade-offs.
- **AI/LLM agent pipelines**: strong product intuition — analyzes why agents hallucinate, compares BugViper to CodeRabbit, proposes confidence scoring, designs multi-agent architectures. (inferred)
- **Frontend / TypeScript / Next.js**: uses it, delegates heavy lifting — reviews UX flow decisions but doesn't write detailed frontend corrections.
- **tree-sitter / code ingestion**: understands the pipeline conceptually, delegates implementation.

## Attitude toward the agent

**Skeptical but trusting in bursts.** He does not rubber-stamp agent output — 58.3% of his responses are Expert Nitpicker (corrections). He reads what the agent produces, compares it to his mental model, and corrects precisely. When the agent earns trust through a correct answer, he follows up with a short "yes apply both fixes" or "Continue from where you left off."

He treats the agent as a peer-collaborator ("bro"), not a subordinate or oracle. He expects the agent to warn him about risks (cost, breaking changes) proactively.

## Tone

- Casual and direct in short messages
- Precise and structured when specifying corrections (pastes formatted specs verbatim)
- Frustrated but brief when things go wrong ("bro I just ingested can you check the stats now", "Ok Bro, just burned so much money for no reason")
- Rare expletives on genuine surprises ("Bro you fucking deleted the plan.md?")
- No filler: never writes "Great question!" or "Thanks, that helps"

## Product philosophy (inferred)

Wants minimal, clean UX ("Make the flow minimal and clean UX"). Thinks about quality signals (confidence scoring, dedup, false-positive reduction). Benchmarks against CodeRabbit and Greptile. Cares about cost per review run.
