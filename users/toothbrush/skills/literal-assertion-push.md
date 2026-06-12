---
name: literal-assertion-push
description: How toothbrush corrects test code that uses Contains/partial checks — demands replacement with exact byte/string literal comparisons. Trigger whenever the agent writes or leaves a test using strings.Contains, len checks, or partial matching.
---

# Skill: literal-assertion-push

toothbrush consistently rejects test assertions that check partial matches and replaces them with exact equality against a literal expected value. This applies to Go tests: `strings.Contains`, `bytes.Contains`, `len == 0` guards, and any "does it not contain X?" pattern are all replaced with a single `bytes.Equal` or `==` check against a literal.

The correction comes after seeing a test run pass, not before — it's a code-quality follow-up, not a pre-emptive instruction.

**Typical correction form**:
> "Alright, for every test in redact/redact_test.go i'd like to see literal expectations (either byte slices or strings) instead of strings.Contains checks.  That'll make the tests easier to understand."

> "OK, that's part of it.  I'd also like to remove all instances of \"does the result contain A? Does the result *not* contain B?\"  Instead, i'd like all those assertions replaced with a single comparison to what the result should be, literally."

> "Almost there.  In func [REDACTED], i'd like us to make a literal structure that we directly compare to repls and repls2.  That'll make the test easier to grok."

**Applies to**:
- Go test files (`_test.go`)
- Both `[]byte` comparisons (`bytes.Equal`) and `string` comparisons (`==`)
- Struct slices: replaced with literal `[][2]string{{...}}` compared via `slices.Equal`
- Multiline string expectations: uses backtick literals, not escaped single-line strings

**Follow-up pattern**: After the first correction is applied, issues a targeted follow-up for any remaining test that wasn't updated: "Great, now finally do that to func TestCollectJSONLReplacements_Succeeds too"
