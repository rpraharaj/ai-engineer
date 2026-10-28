"""Check evaluation fixtures and snapshot boundaries, without invoking an agent."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('agent_evaluations', ROOT / 'tests/agent_evaluations.py')
evaluations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluations)


class EvaluationFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.parent = Path(cls.temp.name) / 'fixtures'
        evaluations.prepare(cls.parent)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_prepare_refuses_to_overwrite_existing_evidence(self):
        marker = self.parent / 'evidence.txt'
        marker.write_text('keep this evidence\n')
        with self.assertRaises(SystemExit):
            evaluations.prepare(self.parent)
        self.assertEqual('keep this evidence\n', marker.read_text())

    def test_clean_and_untracked_scenarios_have_distinct_states(self):
        clean = evaluations.snapshot(self.parent / '01')
        untracked = evaluations.snapshot(self.parent / '02')
        self.assertEqual('', clean['status'])
        self.assertIn('?? "new handler.py"', untracked['status'])
        self.assertIn('new handler.py', untracked['files'])

    def test_snapshots_preserve_index_and_worktree_as_separate_evidence(self):
        repo = self.parent / '03'
        snap = evaluations.snapshot(repo)
        self.assertIn('MM other.txt', snap['status'])
        self.assertEqual('staged other text\n', evaluations.git(repo, 'show', ':other.txt'))
        self.assertEqual('staged other text\nunstaged other text\n', (repo / 'other.txt').read_text())
        saved = json.loads((self.parent / '03-before.json').read_text())
        self.assertEqual(saved, snap)

    def test_contract_variants_differ_in_backfill_evidence(self):
        self.assertTrue((self.parent / '06/evidence/backfill.json').is_file())
        self.assertFalse((self.parent / '06b/evidence/backfill.json').exists())
        self.assertEqual((self.parent / '06/migrations/003_contract.sql').read_bytes(),
                         (self.parent / '06b/migrations/003_contract.sql').read_bytes())

    def test_ui_fixture_connects_the_changed_stylesheet(self):
        html = (self.parent / '08/index.html').read_text()
        self.assertIn('rel="stylesheet"', html)
        self.assertIn('href="style.css"', html)

    def test_missing_backfill_fixture_has_no_recoverable_record(self):
        result = subprocess.run(['git', 'log', '--all', '--oneline', '--', 'evidence/backfill.json'],
                                cwd=self.parent / '06b', env=evaluations.ENV,
                                capture_output=True, text=True, check=True, timeout=15)
        self.assertEqual('', result.stdout)

    def test_old_client_fixture_reproduces_compatibility_failure(self):
        result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                                cwd=self.parent / '11', capture_output=True, text=True, timeout=15)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('test_existing_request_remains_valid', result.stderr)
        self.assertIn('AssertionError: False is not true', result.stderr)


if __name__ == '__main__':
    unittest.main()
