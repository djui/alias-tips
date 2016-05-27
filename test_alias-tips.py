from subprocess import PIPE
from unittest import TestCase, expectedFailure
import imp
import os
import subprocess

alias_tips = imp.load_source('alias-tips', 'alias-tips')


def run_blackboxed(args, aliases):
    p = subprocess.Popen(['./alias-tips', args], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout, _ = p.communicate(input=aliases.encode())
    return stdout


class TestAliasTipFormatting(TestCase):
    def test_no_prefix(self):
        self.assertEqual(alias_tips.format_tip('foo', ''), '\x1b[94m\x1b[1;94mfoo\x1b[0m')

    def test_prefix(self):
        self.assertEqual(alias_tips.format_tip('foo', 'Bar'), '\x1b[94mBar\x1b[1;94mfoo\x1b[0m')


class TestAliasParsing(TestCase):
    def test_no_aliases(self):
        self.assertEqual(alias_tips.parse_aliases([]), [])
        self.assertEqual(alias_tips.parse_aliases(['']), [])

    def test_simpliest(self):
        self.assertEqual(alias_tips.parse_aliases(['foo=bar']), [('foo', 'bar')])

    def test_quoted_expand(self):
        self.assertEqual(alias_tips.parse_aliases(['foo=\'bar\'']), [('foo', 'bar')])

    def test_quoted_alias(self):
        self.assertEqual(alias_tips.parse_aliases(['\'foo\'=bar']), [('foo', 'bar')])

    def test_mulitword_expand(self):
        self.assertEqual(alias_tips.parse_aliases(['foo=\'bar -1\'']), [('foo', 'bar -1')])

    def test_singlesplit(self):
        self.assertEqual(alias_tips.parse_aliases(['foo=\'bar=baz\'']), [('foo', 'bar=baz')])

    @expectedFailure  # Multiple quotes are not yet detected correctly
    def test_multiple_quotes(self):
        self.assertEqual(alias_tips.parse_aliases(['foo=\'bar \'baz\'\'']), [('foo', 'bar \'baz\'')])

    @expectedFailure  # Multiline aliases not yet supported
    def test_skipmultiline(self):
        self.assertEqual(alias_tips.parse_aliases(['foo=\'bar', 'baz']), [])

    def test_git_alias(self):
        self.assertEqual(alias_tips.parse_aliases(['git st = git status -sb']), [('git st', 'git status -sb')])


class TestAliasExcludes(TestCase):
    def test_no_excludes(self):
        self.assertEqual(alias_tips.exclude_aliases([('foo', 'bar')], []), [('foo', 'bar')])

    def test_single_exclude(self):
        self.assertEqual(alias_tips.exclude_aliases([('foo', 'bar')], ['foo']), [])

    def test_single_exclude_missed(self):
        self.assertEqual(alias_tips.exclude_aliases([('foo', 'bar')], ['foo2']), [('foo', 'bar')])


class TestAliasExpand(TestCase):
    def test_no_aliases(self):
        self.assertEqual(alias_tips.expand_input([], ''), '')
        self.assertEqual(alias_tips.expand_input([], 'gR -v'), 'gR -v')

    def test_no_input(self):
        self.assertEqual(alias_tips.expand_input([('gRv', 'git remote -v'), ('gR', 'git remote')], ''), '')

    def test_no_expand(self):
        self.assertEqual(alias_tips.expand_input([('gRv', 'git remote -v')], 'gR -v'), 'gR -v')
        self.assertEqual(alias_tips.expand_input([('gR', 'git remote')], 'gR -v'), 'git remote -v')

    def test_expand(self):
        self.assertEqual(alias_tips.expand_input([('gRv', 'git remote -v'), ('gR', 'git remote')], 'gR -v'), 'git remote -v')


class TestFindAlias(TestCase):
    def test_no_aliases(self):
        self.assertEqual(alias_tips.find_alias([], ''), '')
        self.assertEqual(alias_tips.find_alias([], 'foo'), 'foo')

    def test_equal_length(self):
        self.assertEqual(alias_tips.find_alias([('foo', 'bar')], 'bar'), 'foo')

    def test_single(self):
        self.assertEqual(alias_tips.find_alias([('f', 'bar')], 'bar'), 'f')

    def test_suffix(self):
        self.assertEqual(alias_tips.find_alias([('f', 'bar')], 'bar -v'), 'f -v')

    def test_pick_first_of_multiple(self):
        self.assertEqual(alias_tips.find_alias([('f', 'bar'), ('g', 'bar')], 'bar -v'), 'f -v')

    def test_multiple(self):
        self.assertEqual(alias_tips.find_alias([('g', 'git'), ('git st', 'git status -sb')], 'git status -sb'), 'g st')

class TestWhitebox(TestCase):
    def test_no_aliases(self):
        self.assertEqual(alias_tips.run([], 'bar -v', False, []), 'bar -v')

    def test_simple(self):
        self.assertEqual(alias_tips.run([('f', 'bar'), ('g', 'baz')], 'bar -v', False, []), 'f -v')

    def test_multiple_exchanges(self):
        self.assertEqual(alias_tips.run([('ff', 'bar'), ('f', 'ff')], 'bar -v', False, []), 'f -v')
        self.assertEqual(alias_tips.run([('ff', 'bar'), ('f', 'ff')], 'bar -v', True, []), 'f -v')
        self.assertEqual(alias_tips.run([('ff', 'bar'), ('f', 'ff')], 'bar', False, []), 'f')
        self.assertEqual(alias_tips.run([('ff', 'bar'), ('f', 'ff')], 'bar', True, []), 'f')
        self.assertEqual(alias_tips.run([('g', 'git'),  ('git st', 'git status -sb')], 'git status -sb', True,  []), 'g st')
        self.assertEqual(alias_tips.run([('g', 'git'),  ('git st', 'git status -sb')], 'git status -sb', False, []), 'g st')


class TestBlackbox(TestCase):
    def test_no_envs(self):
        self.assertEqual(run_blackboxed('foo', ''), b'')

    def test_text_env(self):
        os.putenv('ZSH_PLUGINS_ALIAS_TIPS_TEXT', 'Foo')
        self.assertEqual(run_blackboxed('bar', 'f=bar'), b'\x1b[94mFoo\x1b[1;94mf\x1b[0m\n')

    def test_exclude_env(self):
        os.putenv('ZSH_PLUGINS_ALIAS_TIPS_TEXT', 'Foo')
        os.putenv('ZSH_PLUGINS_ALIAS_TIPS_EXCLUDES', '"f b"')
        self.assertEqual(run_blackboxed('bar', 'f=bar'), b'\x1b[94mFoo\x1b[1;94mf\x1b[0m\n')
        self.assertEqual(run_blackboxed('f', 'f=bar'), b'')
        self.assertEqual(run_blackboxed('b', 'f=bar'), b'')
        self.assertEqual(run_blackboxed('f', 'f=bar\nb=baz'), b'')
        self.assertEqual(run_blackboxed('b', 'f=bar\nb=baz'), b'')

    def test_multiple(self):
        os.putenv('ZSH_PLUGINS_ALIAS_TIPS_TEXT', '')
        self.assertEqual(run_blackboxed('git status -sb', 'g=\'git\'\ngit st = git status -sb'), b'\x1b[94m\x1b[1;94mg st\x1b[0m\n')

    def test_expand_env(self):
        os.putenv('ZSH_PLUGINS_ALIAS_TIPS_TEXT', '')

        os.putenv('ZSH_PLUGINS_ALIAS_TIPS_EXPAND', '0')
        self.assertEqual(run_blackboxed('gR -v', 'gRv=\'git remote -v\'\ngR=\'git remote\''), b'')
        self.assertEqual(run_blackboxed('gR -v -foo', 'gRv=\'git remote -v\'\ngR=\'git remote\''), b'')
        self.assertEqual(run_blackboxed('g status -sb',   'g=\'git\'\ngit st = git status -sb'),       b'')

        os.putenv('ZSH_PLUGINS_ALIAS_TIPS_EXPAND', '1')
        self.assertEqual(run_blackboxed('gR -v', 'gRv=\'git remote -v\'\ngR=\'git remote\''), b'\x1b[94m\x1b[1;94mgRv\x1b[0m\n')
        self.assertEqual(run_blackboxed('gR -v -foo', 'gRv=\'git remote -v\'\ngR=\'git remote\''), b'\x1b[94m\x1b[1;94mgRv -foo\x1b[0m\n')
        self.assertEqual(run_blackboxed('g status -sb',   'g=\'git\'\ngit st = git status -sb'),       b'\x1b[94m\x1b[1;94mg st\x1b[0m\n')
