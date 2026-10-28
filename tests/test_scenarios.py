"""Exercise documented Git procedures against disposable repositories, never the user's tree.

These tests prove command behavior; the companion scenarios.md supplies agent-level rubrics.
"""
import os
import re
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = (ROOT / 'skills/engineering-bar/references/change-scope.md').read_text()
COMMIT = (ROOT / 'skills/commit/SKILL.md').read_text()


class GitScenarios(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        # Avoid global hooks, signing, identities, and external configuration.
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME='Scenario', GIT_AUTHOR_EMAIL='scenario@example.invalid',
                        GIT_COMMITTER_NAME='Scenario', GIT_COMMITTER_EMAIL='scenario@example.invalid',
                        GIT_TERMINAL_PROMPT='0')
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'core.hooksPath', str(self.repo / 'no-hooks'))
        self.write('base.txt', 'base\n')
        self.git('add', '--', 'base.txt')
        self.git('commit', '-qm', 'base')
        self.base = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.repo, env=self.env, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15).stdout.decode()

    def write(self, path, content):
        (self.repo / path).write_text(content)

    def scope_command(self, prefix, **values):
        # Execute the commands shipped in the procedure, with fixture revisions substituted.
        lines = [line for block in re.findall(r'```sh\n(.*?)```', SCOPE, re.S)
                 for line in block.splitlines() if line == prefix or line.startswith(prefix + ' ')]
        self.assertEqual(1, len(lines), f'missing or ambiguous documented command: {prefix}')
        command = lines[0]
        for placeholder, value in values.items():
            command = command.replace('<' + placeholder + '>', value)
        args = shlex.split(command)
        self.assertEqual('git', args[0])
        return self.git(*args[1:])

    def feature_commit(self):
        self.git('checkout', '-qb', 'feature')
        self.write('feature.txt', 'feature\n')
        self.git('add', '--', 'feature.txt')
        self.git('commit', '-qm', 'feature')

    def test_clean_feature_branch_still_has_reviewable_change(self):
        self.feature_commit()
        self.assertEqual('', self.scope_command('git status'))
        merge_base = self.scope_command('git merge-base', base='main', tip='HEAD').strip()
        patch = self.scope_command('git diff <merge-base>', **{'merge-base': merge_base, 'tip': 'HEAD'})
        self.assertIn('+feature\n', patch)
        self.assertEqual(self.base, merge_base)

    def test_merge_base_excludes_new_base_branch_work(self):
        self.feature_commit()
        self.git('checkout', '-q', 'main')
        self.write('base-only.txt', 'other work\n')
        self.git('add', '--', 'base-only.txt')
        self.git('commit', '-qm', 'advance base')
        self.git('checkout', '-q', 'feature')
        merge_base = self.scope_command('git merge-base', base='main', tip='HEAD').strip()
        patch = self.scope_command('git diff <merge-base>', **{'merge-base': merge_base, 'tip': 'HEAD'})
        self.assertIn('feature.txt', patch)
        self.assertNotIn('base-only.txt', patch)

    def test_untracked_files_with_spaces_and_newlines_are_inventory_items(self):
        names = ['new file.txt', 'new\nline.txt']
        for name in names:
            self.write(name, 'untracked behavior\n')
        self.assertEqual('', self.scope_command('git diff HEAD'))
        inventory = self.scope_command('git ls-files').split('\0')
        self.assertEqual(set(names), set(inventory) - {''})

    def test_local_inventory_contains_both_staged_and_unstaged_content(self):
        self.write('base.txt', 'staged\n')
        self.git('add', '--', 'base.txt')
        self.write('base.txt', 'staged\nunstaged\n')
        patch = self.scope_command('git diff HEAD')
        self.assertIn('+staged\n', patch)
        self.assertIn('+unstaged\n', patch)

    def test_staged_change_is_visible_when_worktree_reverses_it(self):
        self.write('base.txt', 'staged behavior\n')
        self.git('add', '--', 'base.txt')
        self.write('base.txt', 'base\n')
        self.assertEqual('', self.scope_command('git diff HEAD'))
        self.assertIn('+staged behavior\n', self.scope_command('git diff --cached'))
        self.assertIn('-staged behavior\n', self.scope_command('git diff --'))

    def test_path_commit_preserves_unrelated_partial_staging(self):
        self.write('other.txt', 'initial\n')
        self.git('add', '--', 'other.txt')
        self.git('commit', '-qm', 'other baseline')
        self.write('other.txt', 'staged change\n')
        self.git('add', '--', 'other.txt')
        self.write('other.txt', 'staged change\nunstaged change\n')
        index_before = self.git('show', ':other.txt')
        self.write('base.txt', 'requested change\n')
        message = self.repo / 'message'
        message.write_text('requested change\n')
        match = re.search(r'`(git commit --only -F <message-file> -- <requested-paths>)`', COMMIT)
        self.assertIsNotNone(match, 'missing documented path-limited commit')
        args = shlex.split(match.group(1))
        args = [str(message) if arg == '<message-file>' else 'base.txt' if arg == '<requested-paths>' else arg for arg in args]
        self.git(*args[1:])
        self.assertEqual('base.txt\n', self.git('diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'))
        self.assertEqual(index_before, self.git('show', ':other.txt'))
        self.assertEqual('staged change\nunstaged change\n', (self.repo / 'other.txt').read_text())
        self.assertEqual('initial\n', self.git('show', 'HEAD:other.txt'))

    def test_remote_default_can_differ_from_existing_conventional_branch(self):
        self.git('branch', 'master')
        self.git('branch', 'release-line')
        self.git('update-ref', 'refs/remotes/origin/release-line', self.base)
        self.git('symbolic-ref', 'refs/remotes/origin/HEAD', 'refs/remotes/origin/release-line')
        selected = self.scope_command('git symbolic-ref', remote='origin').strip()
        self.assertEqual('refs/remotes/origin/release-line', selected)
        self.assertNotEqual('master', selected.rsplit('/', 1)[-1])


if __name__ == '__main__':
    unittest.main()
