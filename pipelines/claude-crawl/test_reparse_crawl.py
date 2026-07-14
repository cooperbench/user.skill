import json
import tempfile
import unittest
from pathlib import Path

from reparse_crawl import build


class CrawlReparseTest(unittest.TestCase):
    def test_reparse_keeps_full_context_for_known_session(self):
        session_id = "00690083-466a-4e7f-b883-e5e53c04ab72"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            clones = root / "clones" / "owner__repo" / ".claude" / "projects"
            clones.mkdir(parents=True)
            transcript = clones / f"{session_id}.jsonl"
            records = [
                {
                    "type": "system",
                    "content": "system context",
                },
                {
                    "type": "user",
                    "uuid": "user-1",
                    "message": {"content": "please inspect it"},
                },
                {
                    "type": "assistant",
                    "uuid": "assistant-1",
                    "message": {
                        "content": [
                            {"type": "text", "text": "complete response"},
                            {
                                "type": "tool_use",
                                "name": "Read",
                                "input": {"file_path": "/workspace/file.py"},
                            },
                        ]
                    },
                },
                {
                    "type": "user",
                    "uuid": "tool-1",
                    "message": {
                        "content": [
                            {
                                "type": "tool_result",
                                "content": "complete tool output",
                            }
                        ]
                    },
                },
            ]
            transcript.write_text(
                "\n".join(json.dumps(record) for record in records) + "\n"
            )
            corpus = root / "corpus"
            corpus.mkdir()
            (corpus / "owner.jsonl").write_text(
                json.dumps(
                    {
                        "user": "gh:owner",
                        "repo": "owner/repo",
                        "session_id": f"owner/repo|{session_id}",
                        "start_time": "2026-01-01T00:00:00Z",
                        "harness": "claude-code",
                        "turns": [
                            {"role": "user", "text": "please inspect it"}
                        ],
                    }
                )
                + "\n"
            )
            output = root / "corpus.full.jsonl"

            sessions, human_turns = build(
                root / "clones", str(corpus / "*.jsonl"), output
            )

            self.assertEqual((sessions, human_turns), (1, 1))
            rebuilt = json.loads(output.read_text())
            self.assertEqual(rebuilt["session_id"], session_id)
            self.assertEqual(
                [turn["role"] for turn in rebuilt["turns"]],
                ["system", "user", "assistant", "tool", "tool"],
            )
            self.assertEqual(rebuilt["text_fidelity"], "full")


if __name__ == "__main__":
    unittest.main()
