# Boost Software License - Version 1.0 - August 17th, 2003
#
# Permission is hereby granted, free of charge, to any person or organization
# obtaining a copy of the software and accompanying documentation covered by
# this license (the "Software") to use, reproduce, display, distribute,
# execute, and transmit the Software, and to prepare derivative works of the
# Software, and to permit third-parties to whom the Software is furnished to
# do so, all subject to the following:
#
# The copyright notices in the Software and this entire statement, including
# the above license grant, this restriction and the following disclaimer,
# must be included in all copies of the Software, in whole or in part, and
# all derivative works of the Software, unless such copies or derivative
# works are solely in the form of machine-executable object code generated by
# a source language processor.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
# SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
# FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from affixed_name_rule import AffixedNameRule
from rules import Error
import pytest
from mock import MagicMock


def test_empty_name_is_not_an_error(tester):
    assert [] == tester.test('')


def test_name_without_prefixes_is_not_a_violation(tester):
    assert [] == tester.test('aName')


def test_name_without_expected_prefix_is_a_violation(tester):
    tester.with_expected_prefix('p').test('name')
    tester.assert_missing_failure('missing prefix "p"')


def test_name_with_expected_prefix_is_not_a_violation(tester):
    assert [] == tester.with_expected_prefix('p').test('pName')


def test_name_with_unexpected_prefix_is_a_violation(tester):
    tester.with_unexpected_prefix('p').test('pName')
    tester.assert_redundant_failure('has redundant prefix "p"')


def test_name_without_all_expected_prefixes_is_a_violation(tester):
    tester.with_expected_prefix('a').with_expected_prefix('p').test('pName')
    tester.assert_missing_failure('missing prefix "a"')


def test_name_with_all_expected_prefixes_is_not_a_violation(tester):
    tester.with_expected_prefix('a').with_expected_prefix('p')
    assert [] == tester.test('paName')


def test_all_violations_with_redundant_prefixes_are_reported(tester):
    tester.with_unexpected_prefix('a').with_unexpected_prefix('p')
    tester.test('apName')
    tester.assert_redundant_failure('has redundant prefix "a"')
    tester.assert_redundant_failure('has redundant prefix "p"')


def test_name_that_happens_to_match_expected_prefix_is_a_violation(tester):
    tester.with_expected_prefix('p').test('pointer')
    tester.assert_missing_failure('missing prefix "p"')


def test_only_specified_prefixes_are_allowed(tester):
    tester.with_expected_prefix('p').test('purePointer')
    tester.assert_missing_failure('missing prefix "p"')


def test_name_without_prefixes_needs_to_be_headless_camel_case(tester):
    tester.test('Name')
    tester.assert_generic_failures_include('is not in headlessCamelCase')


def test_name_with_prefixes_needs_to_be_camel_case(tester):
    tester.with_expected_prefix('p').test('pNAME')
    tester.assert_generic_failures_include('is not in CamelCase')


def test_name_with_only_prefix_is_a_violation(tester):
    tester.with_expected_prefix('p').test('p')
    tester.assert_generic_failures_include('missing name after prefix')


def test_name_without_expected_postfix_is_a_violation(tester):
    tester.with_expected_postfix('M').test('name')
    tester.assert_missing_failure('missing postfix "M"')


def test_name_with_expected_postfix_is_not_a_violation(tester):
    assert [] == tester.with_expected_postfix('M').test('nameM')


def test_name_with_unexpected_postfix_is_a_violation(tester):
    tester.with_unexpected_postfix('M').test('nameM')
    tester.assert_redundant_failure('has redundant postfix "M"')


def test_name_with_expected_pre_and_postfixes_is_not_a_violation(tester):
    tester.with_expected_prefix('a').with_expected_postfix('M')
    assert [] == tester.test('aNameM')


def test_prefix_error_also_without_specified_name(tester):
    rule = AffixedNameRule('base')
    rule.add_prefix_rule(None, 'p', lambda n: True)
    result = rule.test(MagicMock(spelling='name'))
    assert Error('base', 'name', 'missing prefix "p"') in result


def test_postfix_error_also_without_specified_name(tester):
    rule = AffixedNameRule('base')
    rule.add_postfix_rule(None, 'p', lambda n: True)
    result = rule.test(MagicMock(spelling='name'))
    assert Error('base', 'name', 'missing postfix "p"') in result


@pytest.fixture
def tester():
    return Tester()


class Tester:
    def __init__(self):
        self.rule = AffixedNameRule('base')

    def with_expected_prefix(self, prefix):
        self.rule.add_prefix_rule('type', prefix, lambda n: True)
        return self

    def with_expected_postfix(self, prefix):
        self.rule.add_postfix_rule('type', prefix, lambda n: True)
        return self

    def with_unexpected_prefix(self, prefix):
        self.rule.add_prefix_rule('type', prefix, lambda n: False)
        return self

    def with_unexpected_postfix(self, prefix):
        self.rule.add_postfix_rule('type', prefix, lambda n: False)
        return self

    def test(self, name_to_test):
        self.tested_name = name_to_test
        self.result = self.rule.test(MagicMock(spelling=name_to_test))
        return self.result

    def assert_missing_failure(self, expected):
        assert Error('type base', self.tested_name, expected) in self.result

    def assert_redundant_failure(self, expected):
        error = Error('non-type base', self.tested_name, expected)
        assert error in self.result

    def assert_generic_failures_include(self, expected):
        assert Error('base', self.tested_name, expected) in self.result
