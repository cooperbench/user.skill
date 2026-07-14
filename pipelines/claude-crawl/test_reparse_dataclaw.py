import json
import tempfile
import unittest
from pathlib import Path

from reparse_dataclaw import build, normalized_session


class DataClawReparseTest(unittest.TestCase):
    def test_conversation_messages_are_not_truncated(self):
        user_text = " ".join(f"user-{index}" for index in range(700))
        assistant_text = " ".join(f"assistant-{index}" for index in range(650))
        tool_output = " ".join(f"output-{index}" for index in range(900))
        document = {
            "session_id": "session-1",
            "project": "owner/repo",
            "model": "claude-opus-4-6",
            "start_time": "2026-04-06T00:00:00Z",
            "messages": [
                {"role": "user", "content": user_text},
                {
                    "role": "assistant",
                    "content": assistant_text,
                    "thinking": "full internal reasoning",
                    "tool_uses": [
                        {
                            "tool": "bash",
                            "input": {"command": "run checks"},
                            "output": {"text": tool_output},
                        }
                    ],
                },
            ],
        }
        session = normalized_session(document, "donor-1")
        self.assertIsNotNone(session)
        self.assertEqual(session["text_fidelity"], "full")
        self.assertEqual(session["turns"][0]["text"], user_text)
        self.assertEqual(len(session["turns"][0]["text"].split()), 700)
        self.assertEqual(session["turns"][1]["text"], assistant_text)
        self.assertEqual(
            [turn["role"] for turn in session["turns"]],
            ["user", "assistant", "metadata", "tool"],
        )
        self.assertIn(tool_output, session["turns"][-1]["text"])

        conversation_only = normalized_session(
            document, "donor-1", include_context=False
        )
        self.assertEqual(
            [turn["role"] for turn in conversation_only["turns"]],
            ["user", "assistant"],
        )

    def test_flat_forks_are_deduplicated_and_keep_known_donor(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / "raw"
            raw.mkdir()
            document = {
                "session_id": "session-1",
                "messages": [
                    {"role": "user", "content": "question"},
                    {"role": "assistant", "content": "answer"},
                ],
            }
            line = json.dumps(document) + "\n"
            (raw / "fork-a__copy.conversations.jsonl").write_text(line)
            (raw / "fork-b__copy.conversations.jsonl").write_text(line)
            richer = {
                **document,
                "messages": [
                    *document["messages"],
                    {"role": "assistant", "content": "more detail"},
                ],
            }
            (raw / "fork-c__richer.conversations.jsonl").write_text(
                json.dumps(richer) + "\n"
            )
            legacy = root / "legacy.jsonl"
            legacy.write_text(
                json.dumps(
                    {"session_id": "session-1", "donor": "canonical-donor"}
                )
                + "\n"
            )
            output = root / "corpus.full.jsonl"

            sessions, human_turns = build(raw, output, legacy)

            self.assertEqual((sessions, human_turns), (1, 1))
            rebuilt = json.loads(output.read_text())
            self.assertEqual(rebuilt["donor"], "canonical-donor")
            self.assertEqual(len(rebuilt["turns"]), 3)
            self.assertEqual(rebuilt["text_fidelity"], "full")


if __name__ == "__main__":
    unittest.main()
