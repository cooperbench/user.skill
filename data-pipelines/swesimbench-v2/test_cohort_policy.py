import sys
import unittest

sys.path.insert(0, "/data/claude-crawl")
from cohort_policy import (
    canonical_session_id,
    command_expansion_payloads,
    injected_role,
    is_extreme_session_fragmentation,
    is_human_target,
    is_incomplete_dialogue,
    reconstructed_session_evidence,
    scrub_text,
    trace_role,
    transcript_hash,
)


class CohortPolicyTest(unittest.TestCase):
    def test_short_human_replies_remain_targets(self):
        for text in ("yes", "ok", "lgtm", "commit it"):
            self.assertTrue(is_human_target(text), text)

    def test_injected_content_is_context_not_target(self):
        examples = {
            "Base directory for this skill: /tmp/skill": "system",
            "This session is being continued from a summary": "system",
            "<system_instruction>do something</system_instruction>": "system",
            "<subagent_notification>done</subagent_notification>": "tool",
            "<bash-stdout>ok</bash-stdout>": "tool",
            "## SKILL: SECURE CODING\nFollow these rules": "system",
            "<skill> <name>coordinator</name> body": "system",
            "# AGENTS.md instructions for /repo\n<INSTRUCTIONS>rules</INSTRUCTIONS>": "system",
            "<git_status>This is the git status at the start of the conversation.</git_status>": "system",
            "<cursor_commands> --- Cursor Command: commit --- do stuff": "system",
            "Implement the plan as specified, it is attached for your reference.": "system",
            "Verify each finding against the current code and report.": "system",
        }
        for text, role in examples.items():
            self.assertFalse(is_human_target(text), text)
            self.assertEqual(injected_role(text), role)
        self.assertEqual(trace_role({"role": "user", "text": "turn 12"}), "metadata")

    def test_cursor_user_query_unwrap(self):
        wrapped = (
            '<attached_files> <code_selection path="/tmp/a.py" lines="1-2"> '
            "1|print(1)\n </code_selection> </attached_files> "
            "<user_query> please fix the logger import </user_query>"
        )
        self.assertTrue(is_human_target(wrapped))
        self.assertEqual(trace_role({"role": "user", "text": wrapped}), "user")
        from cohort_policy import clean_turn, developer_text

        self.assertEqual(developer_text(wrapped), "please fix the logger import")
        cleaned = clean_turn({"role": "user", "text": wrapped})
        self.assertEqual(cleaned["role"], "user")
        self.assertEqual(cleaned["text"], "please fix the logger import")
        attached_only = (
            '<attached_files> <code_selection path="/tmp/a.py" lines="1-2"> '
            "1|print(1)\n </code_selection> </attached_files>"
        )
        self.assertFalse(is_human_target(attached_only))
        self.assertEqual(trace_role({"role": "user", "text": attached_only}), "system")
        self.assertFalse(is_human_target("<bash-input>ls</bash-input>"))
        self.assertEqual(
            injected_role("<system_notification>task finished</system_notification>"),
            "system",
        )

    def test_command_marker_identifies_following_payload(self):
        payload = "# Comprehensive PR Review\nRun the configured review workflow."
        turns = [
            {
                "role": "user",
                "text": "<command-message>review-pr</command-message>",
            },
            {"role": "user", "text": payload},
        ]
        self.assertEqual(
            command_expansion_payloads(turns),
            {"# Comprehensive PR Review Run the configured review workflow."},
        )

    def test_extreme_session_fragmentation_threshold(self):
        self.assertTrue(is_extreme_session_fragmentation(1206, 1481))
        self.assertFalse(is_extreme_session_fragmentation(52, 839))
        self.assertFalse(is_extreme_session_fragmentation(99, 100))

    def test_incomplete_dialogue_requires_assistant_and_human(self):
        user_only = [
            {"role": "user", "text": "Please summarize the recovery gap."},
            {"role": "user", "text": "And list the missing assistant turns."},
        ]
        assistant_only = [
            {"role": "assistant", "text": "I will inspect the logs."},
            {"role": "metadata", "text": "turn 1"},
        ]
        short_dialogue = [
            {"role": "user", "text": "Fix the flaky test."},
            {"role": "assistant", "text": "Done."},
        ]
        self.assertTrue(is_incomplete_dialogue(user_only))
        self.assertTrue(is_incomplete_dialogue(assistant_only))
        self.assertFalse(is_incomplete_dialogue(short_dialogue))

    def test_only_known_uuid_shapes_are_canonicalized(self):
        uuid = "511c8d2a-1234-4abc-8def-1234567890ab"
        self.assertEqual(canonical_session_id(uuid), uuid)
        self.assertEqual(canonical_session_id(f"reparse|owner__repo|{uuid}"), uuid)
        self.assertEqual(
            canonical_session_id(f"2026-01-21-{uuid}"),
            uuid,
        )
        self.assertEqual(
            canonical_session_id(f"unknown|owner__repo|{uuid}"),
            f"unknown|owner__repo|{uuid}",
        )

    def test_secrets_are_scrubbed(self):
        text = "token=abcdefghijklmnop and sk-abcdefghijklmnop"
        scrubbed = scrub_text(text)
        self.assertNotIn("abcdefghijklmnop", scrubbed)
        self.assertIn("[REDACTED", scrubbed)

    def test_transcript_hash_is_order_and_role_sensitive(self):
        first = [{"role": "user", "text": "yes"}, {"role": "assistant", "text": "done"}]
        reordered = list(reversed(first))
        role_changed = [{"role": "assistant", "text": "yes"}, {"role": "assistant", "text": "done"}]
        self.assertNotEqual(transcript_hash(first), transcript_hash(reordered))
        self.assertNotEqual(transcript_hash(first), transcript_hash(role_changed))

    def test_reconstructed_session_allows_inserted_and_omitted_turns(self):
        left = [
            {"role": "user", "ts": "2026-03-20T07:08:57.114Z", "text": "Evaluate the released model on TB-Lite and report the final score."},
            {"role": "tool", "text": "<task-notification>done</task-notification>"},
            {"role": "assistant", "text": "The evaluation scored 18 out of 100."},
            {"role": "user", "ts": "2026-03-20T08:00:00Z", "text": "Can you investigate why the failed cases timed out?"},
            {"role": "assistant", "text": "Most failures were timeouts."},
            {"role": "user", "ts": "2026-03-20T08:10:00Z", "text": "Can you retry the TB-Lite evaluation now?"},
            {"role": "user", "ts": "2026-03-20T08:20:00Z", "text": "Show me the exact evaluation command that was used."},
        ]
        right = [
            {"role": "user", "ts": "2026-03-20T07:08:57.114Z", "text": "Evaluate the released model on TB-Lite and report the final score."},
            {"role": "assistant", "text": "I will inspect the evaluation outputs."},
            {"role": "user", "ts": "2026-03-20T08:00:00Z", "text": "Can you investigate why the failed cases timed out?"},
            {"role": "assistant", "text": "The root cause is generation latency."},
            {"role": "assistant", "text": "Most failures were timeouts."},
            {"role": "user", "ts": "2026-03-20T08:10:00Z", "text": "Can you retry the TB-Lite evaluation now?"},
            {"role": "assistant", "text": "I will retry without changing generation settings."},
            {"role": "user", "ts": "2026-03-20T08:20:00Z", "text": "Show me the exact evaluation command that was used."},
        ]
        evidence = reconstructed_session_evidence(left, right)
        self.assertIsNotNone(evidence)
        self.assertEqual(evidence["anchor"], "exact_event_timestamp")
        self.assertEqual(evidence["ordered_shared_substantial_user_turns"], 4)

    def test_single_distinctive_turn_at_same_timestamp_is_reconstruction(self):
        left = [
            {
                "role": "user",
                "ts": "2026-03-20T07:08:57.114Z",
                "text": "Evaluate this exact released checkpoint on TB-Lite and report the score.",
            }
        ]
        right = [
            {"role": "assistant", "text": "Preparing the evaluation."},
            {
                "role": "user",
                "ts": "2026-03-20T07:08:57.114Z",
                "text": "Evaluate this exact released checkpoint on TB-Lite and report the score.",
            },
        ]
        evidence = reconstructed_session_evidence(left, right)
        self.assertIsNotNone(evidence)
        self.assertEqual(evidence["anchor"], "exact_event_timestamp")

    def test_repeated_workflow_without_session_anchor_is_not_reconstruction(self):
        left = [
            {"role": "user", "ts": "2026-03-20T07:00:00Z", "text": "Please investigate the deployment failures in production."},
            {"role": "assistant", "text": "I found a configuration issue."},
            {"role": "user", "ts": "2026-03-20T07:10:00Z", "text": "Can you retry the deployment after fixing the configuration?"},
            {"role": "user", "ts": "2026-03-20T07:20:00Z", "text": "Show me the exact deployment command that was used."},
        ]
        right = [
            {"role": "user", "ts": "2026-04-20T07:00:00Z", "text": "Please investigate the deployment failures in production."},
            {"role": "assistant", "text": "I found another configuration issue."},
            {"role": "user", "ts": "2026-04-20T07:10:00Z", "text": "Can you retry the deployment after fixing the configuration?"},
            {"role": "user", "ts": "2026-04-20T07:20:00Z", "text": "Show me the exact deployment command that was used."},
        ]
        self.assertIsNone(reconstructed_session_evidence(left, right))


if __name__ == "__main__":
    unittest.main()
