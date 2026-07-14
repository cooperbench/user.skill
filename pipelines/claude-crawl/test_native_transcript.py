import json
import unittest

from native_transcript import PARSER_VERSION, parse_full_jsonl


def jsonl(*records):
    return "\n".join(json.dumps(record) for record in records)


class NativeTranscriptTest(unittest.TestCase):
    def test_claude_messages_are_never_truncated(self):
        user_text = " ".join(f"user-{index}" for index in range(700))
        assistant_text = " ".join(f"assistant-{index}" for index in range(650))
        count, turns = parse_full_jsonl(
            jsonl(
                {
                    "type": "user",
                    "uuid": "u1",
                    "timestamp": "2026-04-06T00:00:00Z",
                    "message": {"content": [{"type": "text", "text": user_text}]},
                },
                {
                    "type": "assistant",
                    "uuid": "a1",
                    "timestamp": "2026-04-06T00:00:01Z",
                    "message": {
                        "id": "m1",
                        "content": [{"type": "text", "text": assistant_text}],
                    },
                },
            )
        )
        self.assertEqual(PARSER_VERSION, "swesimbench-native-transcript-2026-07-14.1")
        self.assertEqual(count, 1)
        self.assertEqual(turns[0]["text"], user_text)
        self.assertEqual(turns[1]["text"], assistant_text)
        self.assertEqual(len(turns[0]["text"].split()), 700)
        self.assertEqual(len(turns[1]["text"].split()), 650)

    def test_claude_streaming_snapshots_replace_instead_of_duplicate(self):
        count, turns = parse_full_jsonl(
            jsonl(
                {
                    "type": "user",
                    "uuid": "u1",
                    "message": {"content": "first draft"},
                },
                {
                    "type": "user",
                    "uuid": "u1",
                    "message": {"content": "final exact prompt"},
                },
                {
                    "type": "assistant",
                    "message": {
                        "id": "m1",
                        "content": [{"type": "text", "text": "partial"}],
                    },
                },
                {
                    "type": "assistant",
                    "message": {
                        "id": "m1",
                        "content": [
                            {"type": "text", "text": "complete response"},
                            {
                                "type": "tool_use",
                                "name": "Read",
                                "id": "tool-1",
                                "input": {"file_path": "/workspace/large.py"},
                            },
                        ],
                    },
                },
            )
        )
        self.assertEqual(count, 1)
        self.assertEqual(
            [turn["role"] for turn in turns], ["user", "assistant", "tool"]
        )
        self.assertEqual(turns[0]["text"], "final exact prompt")
        self.assertEqual(turns[1]["text"], "complete response")
        self.assertIn("/workspace/large.py", turns[2]["text"])

    def test_metadata_sidechains_and_tool_results_are_retained_as_context(self):
        count, turns = parse_full_jsonl(
            jsonl(
                {
                    "type": "user",
                    "uuid": "meta",
                    "isMeta": True,
                    "message": {"content": "system-injected context"},
                },
                {
                    "type": "user",
                    "uuid": "tool-result",
                    "message": {
                        "content": [
                            {
                                "type": "tool_result",
                                "content": "full tool output",
                            }
                        ]
                    },
                },
                {
                    "type": "user",
                    "uuid": "human",
                    "message": {"content": "please fix the parser"},
                },
            )
        )
        self.assertEqual(count, 1)
        self.assertEqual(
            [turn["role"] for turn in turns], ["system", "tool", "user"]
        )
        self.assertEqual(turns[1]["text"], "full tool output")

    def test_codex_prefers_exact_event_user_messages_without_duplication(self):
        long_text = " ".join(f"codex-{index}" for index in range(550))
        count, turns = parse_full_jsonl(
            jsonl(
                {
                    "type": "event_msg",
                    "timestamp": "2026-04-06T00:00:00Z",
                    "payload": {"type": "user_message", "message": long_text},
                },
                {
                    "type": "response_item",
                    "timestamp": "2026-04-06T00:00:00Z",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": long_text}],
                    },
                },
                {
                    "type": "response_item",
                    "timestamp": "2026-04-06T00:00:01Z",
                    "payload": {
                        "type": "message",
                        "role": "assistant",
                        "content": [
                            {"type": "output_text", "text": "full assistant reply"}
                        ],
                    },
                },
            )
        )
        self.assertEqual(count, 1)
        self.assertEqual([turn["role"] for turn in turns], ["user", "assistant"])
        self.assertEqual(turns[0]["text"], long_text)
        self.assertEqual(len(turns[0]["text"].split()), 550)

    def test_bare_role_and_whole_document_formats_are_supported(self):
        bare_count, bare_turns = parse_full_jsonl(
            jsonl(
                {"role": "user", "message": {"content": "bare user"}},
                {"role": "assistant", "message": {"content": "bare assistant"}},
            )
        )
        self.assertEqual(bare_count, 1)
        self.assertEqual(
            [turn["text"] for turn in bare_turns], ["bare user", "bare assistant"]
        )

        document_count, document_turns = parse_full_jsonl(
            json.dumps(
                {
                    "messages": [
                        {
                            "info": {
                                "role": "user",
                                "time": {"created": 123},
                            },
                            "parts": [{"type": "text", "text": "OpenCode user"}],
                        },
                        {
                            "type": "gemini",
                            "content": "Gemini response",
                        },
                    ]
                }
            )
        )
        self.assertEqual(document_count, 1)
        self.assertEqual(
            [turn["role"] for turn in document_turns], ["user", "assistant"]
        )


if __name__ == "__main__":
    unittest.main()
