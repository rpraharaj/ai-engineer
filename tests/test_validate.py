"""Validate authoring errors at the public file and CLI boundaries."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SkillValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / 'sample'
        self.folder.mkdir()
        self.path = self.folder / 'SKILL.md'

    def validate(self, fields='name: sample\ndescription: Sample task; use for samples.\n', body='# Sample\n'):
        self.path.write_text('---\n' + fields + '---\n' + body)
        return validator.validate_skill(self.path)

    def test_valid_strings_and_metadata(self):
        self.assertEqual([], self.validate('name: sample\ndescription: "Task: use for samples."\nmetadata:\n  pack: example\n  version: "1.0"\n'))

    def test_duplicate_top_level_key_is_rejected(self):
        errors = self.validate('name: wrong\nname: sample\ndescription: Sample task.\n')
        self.assertTrue(any('duplicate' in e for e in errors), errors)

    def test_metadata_requires_mapping(self):
        errors = self.validate('name: sample\ndescription: Sample task.\nmetadata: invalid-scalar\n')
        self.assertTrue(any('metadata' in e for e in errors), errors)

    def test_duplicate_metadata_key_is_rejected(self):
        errors = self.validate('name: sample\ndescription: Sample task.\nmetadata:\n  pack: one\n  pack: two\n')
        self.assertTrue(any('duplicate' in e for e in errors), errors)

    def test_scalar_types_are_checked(self):
        for field in ('description', 'license', 'compatibility'):
            with self.subTest(field=field):
                fields = {'name': 'sample', 'description': 'Sample task.'}
                fields[field] = 'true'
                errors = self.validate(''.join(f'{k}: {v}\n' for k, v in fields.items()))
                self.assertTrue(errors)

    def test_metadata_values_are_strings(self):
        self.assertTrue(self.validate('name: sample\ndescription: Sample task.\nmetadata:\n  version: 1.2\n'))

    def test_bad_indentation_and_unclosed_quotes_are_rejected(self):
        for source in ('name: sample\n description: Sample task.\n', 'name: sample\ndescription: "unfinished\n'):
            with self.subTest(source=source):
                self.assertTrue(self.validate(source))

    def test_yaml_non_strings_and_empty_metadata_are_rejected(self):
        for value in ('0xFF', '0o17', '.inf', '2026-10-28', '# only a comment', '- a sequence'):
            with self.subTest(value=value):
                self.assertTrue(self.validate('name: sample\ndescription: ' + value + '\n'))
        self.assertTrue(self.validate('name: sample\ndescription: Task.\nmetadata:\n'))

    def test_missing_template_is_rejected(self):
        errors = self.validate(body='Read `references/missing.md`.\n')
        self.assertTrue(any('missing' in e for e in errors), errors)

    def test_existing_template_and_its_nested_reference(self):
        refs = self.folder / 'references'
        refs.mkdir()
        (refs / 'guide.md').write_text('Read [details](details.md).\n')
        (refs / 'details.md').write_text('# Details\n')
        self.assertEqual([], self.validate(body='Read `references/guide.md`.\n'))
        (refs / 'details.md').unlink()
        self.assertTrue(self.validate(body='Read `references/guide.md`.\n'))

    def test_host_only_fields_and_supporting_content_are_rejected(self):
        self.assertTrue(self.validate('name: sample\ndescription: Sample task.\nallowed-tools: shell\n'))
        refs = self.folder / 'references'
        refs.mkdir()
        (refs / 'guide.md').write_text('Use the spawn_subagent tool.\n')
        self.assertTrue(self.validate(body='Read `references/guide.md`.\n'))

    def test_name_and_description_limits(self):
        self.assertTrue(self.validate('name: another\ndescription: Sample task.\n'))
        self.assertTrue(self.validate('name: sample\ndescription: ' + 'a' * 1025 + '\n'))

    def test_skill_must_be_under_500_lines(self):
        self.assertEqual([], self.validate(body='line\n' * 494))  # 498 total
        self.assertTrue(self.validate(body='line\n' * 496))  # 500 total


class PackValidationTests(unittest.TestCase):
    def test_real_pack(self):
        self.assertEqual(0, subprocess.run([sys.executable, str(ROOT / 'scripts/validate.py')], capture_output=True).returncode)

    def test_cli_rejects_directory_without_skill_and_template_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            pack = Path(temp)
            (pack / 'skills/empty').mkdir(parents=True)
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate.py'), str(pack)], capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn('SKILL.md', result.stdout + result.stderr)

    def test_cli_detects_template_drift_and_missing_readme(self):
        with tempfile.TemporaryDirectory() as temp:
            pack = Path(temp)
            folder = pack / 'skills/explore-codebase'
            (folder / 'references').mkdir(parents=True)
            (folder / 'SKILL.md').write_text('---\nname: explore-codebase\ndescription: Explore a repo.\n---\n# Explore\n')
            (folder / 'references/agents-template.md').write_bytes(b'one\n')
            (pack / 'templates').mkdir()
            (pack / 'templates/AGENTS.md').write_bytes(b'two\n')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate.py'), str(pack)], capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn('identical', result.stdout)
            self.assertIn('README.md', result.stdout)


if __name__ == '__main__':
    unittest.main()
