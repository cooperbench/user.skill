"""Refinement round on the winning 4-way taxonomy: sharpen the residual critical~inquiry,
critical~directive, approve~directive seams; re-evaluate κ with the 3 Claude-family CLI judges."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tax_eval_cli as TC

prev = {c["name"]: c for c in json.loads((HERE / "candidates.json").read_text())}

R1 = {
    "name": "axes4-sharp",
    "categories": ["approve", "critical", "directive", "inquiry"],
    "body": (
        "Classify the developer's MOVE — what the message DOES about the agent's previous turn. "
        "Judge function, not tone or topic. Choose exactly one:\n"
        "- critical: asserts or implies the agent's work is WRONG, broken, failing, or unwanted — a bug/error/"
        "failure report, 'that's wrong', 'no', 'you broke X', rejecting the approach, OR demanding a fix for a "
        "defect the agent caused. Negative judgment about work already produced (even if phrased as a question).\n"
        "- inquiry: seeks information, explanation, or options and expects an ANSWER, with NO claim the work is "
        "wrong ('why a mutex?', 'is this thread-safe?', 'what are the options?').\n"
        "- directive: tells the agent to do or change work with NO claim the existing work is wrong — a new task/"
        "feature, or a forward adjustment/constraint ('add a reset page', 'also handle empty input', 'use PUT'). "
        "Includes approval bundled with an instruction.\n"
        "- approve: pure acceptance / go-ahead with NO new instruction and NO complaint ('looks good', 'lgtm', "
        "'yes', 'continue', 'ship it', 'commit').\n\n"
        "DECISION RULE (top-down, first match wins):\n"
        "1. Says/implies the current work is wrong, broken, or rejected (incl. a fix-request for a defect the "
        "agent introduced) -> critical.\n"
        "2. Else seeks an answer with no problem claim -> inquiry.\n"
        "3. Else tells the agent to do or change work -> directive.\n"
        "4. Else only accepts/continues -> approve.\n\n"
        "EXAMPLES:\n"
        "agent 'I made the form submit via POST.' -> dev 'it 500s on submit' -> critical\n"
        "agent 'I made the form submit via POST.' -> dev 'should be PUT not POST' -> critical\n"
        "agent 'I made the form submit via POST.' -> dev 'also add client-side validation' -> directive\n"
        "agent 'Here is the sort fn.' -> dev 'looks good, also handle empty arrays' -> directive\n"
        "agent 'Here is the sort fn.' -> dev 'perfect, continue' -> approve\n"
        "agent 'I used recursion in the parser.' -> dev 'why recursion and not a loop?' -> inquiry\n"
        "agent 'Tests pass.' -> dev 'are the edge cases covered?' -> inquiry"),
}
# R2: same 4 axes, but resolve critical~directive toward DIRECTIVE unless a defect is explicitly asserted
R2 = {
    "name": "axes4-defect-test",
    "categories": ["approve", "critical", "directive", "inquiry"],
    "body": (
        "Classify the developer's MOVE about the agent's previous turn by one OBSERVABLE test each. "
        "Choose exactly one (check in order):\n"
        "1. critical — the message explicitly states the work is defective: names a bug/error/failure, says it's "
        "wrong/broken, rejects it, or says 'no/revert/undo'. The mere act of changing direction is NOT critical "
        "unless a defect is asserted.\n"
        "2. inquiry — the message's main act is asking for information/explanation/options and waiting for an "
        "answer (a '?' seeking knowledge), with no defect asserted.\n"
        "3. directive — the message tells the agent to build, add, change, or proceed-with-changes (forward work), "
        "with no defect asserted. Approval plus an instruction is directive.\n"
        "4. approve — the message only accepts or says go ahead, with no instruction and no defect.\n\n"
        "Key tie-breaks: 'fix the failing test' / 'this crashes' -> critical (defect asserted). "
        "'change it to use PUT' / 'also add caching' -> directive (no defect asserted). "
        "'why did you do X?' -> inquiry. 'lgtm' -> approve. 'looks good, now add tests' -> directive.\n\n"
        "EXAMPLES:\n"
        "agent 'Added the endpoint.' -> dev 'it returns 500' -> critical\n"
        "agent 'Added the endpoint.' -> dev 'now add auth to it' -> directive\n"
        "agent 'Refactored to async.' -> dev 'revert that, it deadlocks' -> critical\n"
        "agent 'Refactored to async.' -> dev 'is async safe here?' -> inquiry\n"
        "agent 'Done.' -> dev 'ship it' -> approve"),
}

cands = [R1, R2, prev["behavior-axes-4way"], prev["merge-4way-no-other"]]
results = [TC.evaluate(c) for c in cands]
print(f"\n===== REFINEMENT (3 Claude judges, {len(TC.SAMPLE)} items) =====")
print(f"{'taxonomy':22s} {'meanκ':>7} {'h-s':>6} {'h-o':>6} {'s-o':>6}  confusions")
for r in sorted(results, key=lambda r: -(r['mean_kappa'] or 0)):
    pw = r['pairwise']
    cf = ", ".join(f"{c['pair'][0]}~{c['pair'][1]}({c['n']})" for c in r['top_confusions'][:3])
    print(f"{r['name']:22s} {str(r['mean_kappa']):>7} {str(pw['haiku-sonnet']['kappa']):>6} "
          f"{str(pw['haiku-opus']['kappa']):>6} {str(pw['sonnet-opus']['kappa']):>6}  {cf}")
(HERE / "tax_refine_cli.jsonl").write_text("\n".join(json.dumps(r) for r in results) + "\n")
