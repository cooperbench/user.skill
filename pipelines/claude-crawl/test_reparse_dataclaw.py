import unittest

from reparse_dataclaw import normalized_session


class DataClawReparseTest(unittest.TestCase):
    def test_messages_and_tool_payloads_are_not_truncated(self):
        user_text = " ".join(f"user-{index}" for index in range(700))
        tool_output = " ".join(f"output-{index}" for index in range(900))
        session = normalized_session(
            {
                "session_id": "session-1",
                "project": "owner/repo",
                "model": "claude-opus-4-6",
                "start_time": "2026-04-06T00:00:00Z",
                "messages": [
                    {"role": "user", "content": user_text},
                    {
                        "role": "assistant",
                        "content": "I will inspect it.",
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
            },
            "donor-1",
        )
        self.assertIsNotNone(session)
        self.assertEqual(session["text_fidelity"], "full")
        self.assertEqual(session["turns"][0]["text"], user_text)
        self.assertEqual(len(session["turns"][0]["text"].split()), 700)
        self.assertIn(tool_output, session["turns"][-1]["text"])


if __name__ == "__main__":
    unittest.main()
