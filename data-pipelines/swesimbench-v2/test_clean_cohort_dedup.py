import unittest

from build_clean_cohort import (
    apply_command_expansion_policy,
    collapse_reconstructed_sessions,
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
    }


class CleanCohortDedupTest(unittest.TestCase):
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
