import unittest

from build_clean_cohort import (
    SWECHAT_ROLES,
    apply_command_expansion_policy,
    candidate,
    choose_candidate,
    collapse_reconstructed_sessions,
    lookup_candidates,
    session_aliases,
)


def record(sid, split, source, turns):
    return {
        "sid": sid,
        "canonical": sid,
        "source": source,
        "source_aliases": [source],
        "owner": "gh:test",
        "repo": "owner/repo",
        "ts": "2026-03-20T07:08:57Z" if split == "train" else "2026-04-10T00:00:00Z",
        "turns": turns,
        "trace_hash": sid,
        "sequence": tuple(),
        "human_turns": sum(turn["role"] == "user" for turn in turns),
        "substantial_human_turns": sum(
            turn["role"] == "user" and len(turn["text"]) >= 24 for turn in turns
        ),
        "content_chars": sum(len(turn["text"]) for turn in turns),
        "original_ids": [sid],
        "dedup_rules": [],
        "split": split,
        "text_fidelity": "full",
        "parser_version": "test-parser",
    }


class CleanCohortDedupTest(unittest.TestCase):
    def test_swechat_context_roles_are_retained(self):
        self.assertEqual(SWECHAT_ROLES["tool_result"], "tool")
        self.assertEqual(SWECHAT_ROLES["tool_use"], "tool")
        self.assertEqual(SWECHAT_ROLES["system_injected"], "system")
        self.assertEqual(SWECHAT_ROLES["assistant_thinking"], "metadata")
        self.assertNotIn("progress", SWECHAT_ROLES)
        self.assertNotIn("queue_operation", SWECHAT_ROLES)

    def test_legacy_crawl_requires_full_reparse(self):
        record = candidate(
            {
                "session_id": "session-1",
                "turns": [{"role": "user", "text": "question"}],
            },
            "crawl",
        )
        self.assertEqual(record["text_fidelity"], "legacy_unknown")

    def test_crawl_wrapper_ids_expose_uuid_aliases(self):
        uuid = "00690083-466a-4e7f-b883-e5e53c04ab72"
        aliases = session_aliases(f"owner/repo|{uuid}")
        self.assertIn(uuid, aliases)
        self.assertIn(f"owner/repo|{uuid}", aliases)

    def test_lookup_candidates_matches_reparse_manifest_to_repo_corpus_id(self):
        uuid = "00690083-466a-4e7f-b883-e5e53c04ab72"
        corpus = record(f"owner/repo|{uuid}", "train", "crawl", [{"role": "user", "text": "hi"}])
        by_alias = {}
        for alias in session_aliases(corpus["sid"]):
            by_alias.setdefault(alias, []).append(corpus)
        found = lookup_candidates(f"reparse|owner|{uuid}", by_alias)
        self.assertEqual(found, [corpus])
        self.assertEqual(lookup_candidates(uuid, by_alias), [corpus])
    def test_candidate_selection_rejects_legacy_truncated_sources(self):
        legacy = record(
            "same",
            "held",
            "entire",
            [{"role": "user", "text": "legacy copy with more apparent rows"}] * 3,
        )
        legacy["text_fidelity"] = "legacy_unknown"
        full = record(
            "same",
            "held",
            "swechat",
            [{"role": "user", "text": "full copy"}],
        )
        self.assertIs(choose_candidate([legacy, full]), full)
        with self.assertRaisesRegex(RuntimeError, "no full-fidelity candidate"):
            choose_candidate([legacy])

    def test_command_payload_is_reclassified_across_source_copies(self):
        payload = "# Comprehensive PR Review\nRun all configured review agents."
        marked = record(
            "marked",
            "held",
            "entire",
            [
                {"role": "user", "text": "<command-message>review-pr</command-message>"},
                {"role": "user", "text": payload},
            ],
        )
        unmarked = record(
            "unmarked",
            "train",
            "swechat",
            [{"role": "user", "text": payload}],
        )
        payloads, turn_count = apply_command_expansion_policy([marked, unmarked])
        self.assertEqual(len(payloads), 1)
        self.assertEqual(turn_count, 2)
        self.assertEqual(marked["turns"][1]["role"], "system")
        self.assertEqual(unmarked["turns"][0]["role"], "system")
        self.assertEqual(unmarked["human_turns"], 0)

    def test_reconstruction_crossing_split_is_kept_in_train(self):
        shared = [
            ("2026-03-20T07:08:57Z", "Evaluate the released model on TB-Lite and report the score."),
            ("2026-03-20T08:00:00Z", "Can you investigate why the failed cases timed out?"),
            ("2026-03-20T08:10:00Z", "Can you retry the TB-Lite evaluation now?"),
            ("2026-03-20T08:20:00Z", "Show me the exact evaluation command that was used."),
            ("2026-03-20T08:30:00Z", "Compare the timeout counts against the previous model."),
        ]
        train_turns = []
        held_turns = []
        for timestamp, text in shared:
            train_turns.extend(
                [
                    {"role": "user", "ts": timestamp, "text": text},
                    {"role": "assistant", "text": "Train-source response."},
                ]
            )
            held_turns.extend(
                [
                    {"role": "user", "ts": timestamp, "text": text},
                    {"role": "assistant", "text": "Additional analysis."},
                    {"role": "assistant", "text": "Held-source response."},
                ]
            )
        records = [
            record("train-copy", "train", "swechat", train_turns),
            record("held-copy", "held", "entire", held_turns),
        ]
        kept, provenance, _ = collapse_reconstructed_sessions(records, "gh:test")
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0]["sid"], "held-copy")
        self.assertEqual(kept[0]["split"], "train")
        self.assertEqual(kept[0]["ts"], "2026-03-20T07:08:57Z")
        self.assertEqual(kept[0]["source_aliases"], ["entire", "swechat"])
        self.assertIn("reconstructed_session", kept[0]["dedup_rules"])
        self.assertTrue(provenance[0]["crossed_split"])


if __name__ == "__main__":
    unittest.main()
