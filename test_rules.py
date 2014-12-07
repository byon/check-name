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

from clang.cindex import CursorKind
import rules
import pytest
from mock import MagicMock


def test_unidentified_node_will_have_no_rules(identify_rules_tester):
    assert not identify_rules_tester.test()


def test_namespace_should_have_camel_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.NAMESPACE).test()
    assert rules.CamelCaseRule in _rule_types(result)


def test_variable_should_have_headless_camel_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.VAR_DECL).test()
    assert rules.HeadlessCamelCaseRule in _rule_types(result)


def test_class_should_have_camel_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.CLASS_DECL).test()
    assert rules.CamelCaseRule in _rule_types(result)


def test_struct_should_have_camel_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.STRUCT_DECL).test()
    assert rules.CamelCaseRule in _rule_types(result)


def test_interface_class_should_have_if_postfix(identify_rules_tester):
    result = identify_rules_tester.with_interface_class().test()
    assert _rule_of_type(result, rules.PostFixRule).postfix == 'If'


def test_identifying_class():
    result = rules.identify_rules_for_class(_Node(CursorKind.CLASS_DECL))
    assert rules.CamelCaseRule in _rule_types(result)


def test_construction_of_camel_case_rule():
    rule = rules.CamelCaseRule('identifier')
    assert rule.type_name == 'identifier'
    assert rule.error_description == 'is not in CamelCase'
    assert rule.rule_test == rules.is_camel_case


def test_construction_of_headless_camel_case_rule():
    rule = rules.HeadlessCamelCaseRule('identifier')
    assert rule.type_name == 'identifier'
    assert rule.error_description == 'is not in headlessCamelCase'
    assert rule.rule_test == rules.is_headless_camel_case


def test_construction_of_post_fix_rule():
    rule = rules.PostFixRule('identifier', 'postfix')
    assert rule.type_name == 'identifier'
    assert rule.error_description == 'does not have postfix "postfix"'
    # assert rule.rule_test == rules.has_postfix


def test_missing_postfix_is_failure():
    assert False == rules.PostFixRule('', 'P').test(_Node(name='name'))


def test_postfix_in_middle_is_failure():
    assert False == rules.PostFixRule('', 'P').test(_Node(name='naPme'))


def test_existin_postfix_is_success():
    assert True == rules.PostFixRule('', 'P').test(_Node(name='nameP'))


def test_recognizing_camel_case_with_one_part():
    assert rules.is_camel_case('Foo')


def test_recognizing_camel_case_with_multiple_parts():
    assert rules.is_camel_case('FooBar')


def test_recognizing_camel_case_with_number_at_end():
    assert rules.is_camel_case('Foo1234Bar')


def test_recognizing_camel_case_with_number_at_end_of_part():
    assert rules.is_camel_case('Foo1234Bar')


def test_recognizing_camel_case_error_when_all_lowercase():
    assert not rules.is_camel_case('foo')


def test_recognizing_camel_case_error_when_starts_with_lowercase():
    assert not rules.is_camel_case('fooBar')


def test_recognizing_camel_case_error_when_snake_case():
    assert not rules.is_camel_case('foo_bar')


def test_recognizing_camel_case_error_when_capitalized_snake_case():
    assert not rules.is_camel_case('Foo_Bar')


def test_recognizing_camel_case_error_when_too_many_uppercase():
    assert not rules.is_camel_case('MMHeight')


def test_recognizing_camel_case_error_with_number_at_middle_of_part():
    assert not rules.is_camel_case('Fo1234oBar')


def test_recognizing_headless_camel_case_with_one_part():
    assert rules.is_headless_camel_case('foo')


def test_recognizing_headless_camel_case_with_multiple_parts():
    assert rules.is_headless_camel_case('fooBar')


def test_recognizing_headless_camel_case_with_number_at_end():
    assert rules.is_headless_camel_case('fooBar1234')


def test_recognizing_headless_camel_case_with_number_at_end_of_part():
    assert rules.is_headless_camel_case('foo1234Bar')


def test_recognizing_headless_camel_case_error_when_all_uppercase():
    assert not rules.is_headless_camel_case('FOO')


def test_recognizing_headless_camel_case_error_when_starts_with_Uppercase():
    assert not rules.is_headless_camel_case('FooBar')


def test_recognizing_headless_camel_case_error_when_snake_case():
    assert not rules.is_headless_camel_case('foo_bar')


def test_recognizing_headless_camel_case_error_when_capitalized_snake_case():
    assert not rules.is_headless_camel_case('Foo_Bar')


def test_recognizing_headless_camel_case_error_when_too_many_uppercase():
    assert not rules.is_headless_camel_case('isInWWF')


def test_recognizing_headless_camel_case_error_with_number_at_middle_of_part():
    assert not rules.is_headless_camel_case('fo1234oBar')


@pytest.fixture
def identify_rules_tester():
    return _IdentifyRulesTester()


class _Node:
    def __init__(self, kind=None, name=None):
        self.kind = MagicMock()
        self.kind.__eq__.side_effect = lambda k: k == kind
        self.spelling = name if name else ''
        self.pure_virtual_method = False
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children


class _Method(_Node):
    def __init__(self, virtual=False, pure_virtual=False, name=None):
        assert not pure_virtual or (pure_virtual and virtual)
        _Node.__init__(self, CursorKind.CXX_METHOD, name)
        self.virtual = virtual
        self.pure_virtual = pure_virtual

    def is_pure_virtual_method(self):
        return self.pure_virtual

    def is_virtual_method(self):
        return self.virtual


class _IdentifyRulesTester:
    def __init__(self):
        self.node = _Node()

    def test(self):
        return rules.identify_rules(self.node)

    def with_kind(self, kind):
        self.node = _Node(kind)
        return self

    def with_interface_class(self):
        self.node = _Node(CursorKind.CLASS_DECL)
        self.node.add_child(_Method(True, True))
        return self


def _rule_types(rules):
    return [r.__class__ for r in rules]


def _rule_of_type(rules, type):
    for rule in rules:
        if rule.__class__ == type:
            return rule
    assert False, 'Could not find type ' + type.__name__
