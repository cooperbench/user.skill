import unittest

from reparse_dataclaw import normalized_session


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
            [turn["role"] for turn in session["turns"]], ["user", "assistant"]
        )

        with_context = normalized_session(
            document, "donor-1", include_context=True
        )
        self.assertIn(tool_output, with_context["turns"][-1]["text"])


if __name__ == "__main__":
    unittest.main()
