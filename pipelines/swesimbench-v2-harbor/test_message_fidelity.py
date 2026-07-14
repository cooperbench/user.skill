import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PIPELINES = ROOT.parent


class MessageFidelityTest(unittest.TestCase):
    def test_private_v2_artifacts_do_not_cap_message_text(self):
        prepare = (ROOT / "prepare.py").read_text()
        atif = (ROOT / "build_atif_sample.py").read_text()
        tasks = (ROOT / "make_tasks_v2.py").read_text()
        entire = (PIPELINES / "entire-backfill" / "harvest.py").read_text()

        self.assertNotIn("CTX_WORDS", prepare)
        self.assertNotIn("STEP_CHARS", atif)
        self.assertNotIn("render_transcript(traj, cap=", tasks)
        self.assertNotIn("[:800]", tasks)
        self.assertNotIn("def truncate_words(s, n=300)", entire)

    def test_entire_refresh_streams_large_shards_to_disk(self):
        entire = (PIPELINES / "entire-backfill" / "harvest.py").read_text()
        self.assertIn("for session in iter_ref(repo_path, ref):", entire)
        self.assertNotIn("sessions = parse_ref(repo_path, ref)", entire)

    def test_refresh_requires_explicit_full_fidelity_candidates(self):
        builder = (ROOT / "build_clean_cohort.py").read_text()
        self.assertIn('"text_fidelity": fidelity', builder)
        self.assertIn("no full-fidelity candidate", builder)
        self.assertIn("corpus.full.jsonl", builder)
        self.assertIn("ENTIRE_CORPUS_GLOB", builder)
        self.assertIn("corpus-full-v4/*.jsonl", builder)


if __name__ == "__main__":
    unittest.main()
