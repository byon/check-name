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

from clang.cindex import CursorKind, TypeKind
import affixed_name_rule
import case_rules
import identification
import rules
import pytest
from mock import MagicMock, patch


def test_unidentified_node_will_have_no_rules(identify_rules_tester):
    assert not identify_rules_tester.test()


def test_namespace_should_have_camel_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.NAMESPACE).test()
    assert rules.CamelCaseRule in _rule_types(result)


def test_method_should_have_headless_camel_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.CXX_METHOD).test()
    assert rules.HeadlessCamelCaseRule in _rule_types(result)


def test_function_should_have_headless_camel_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.FUNCTION_DECL).test()
    assert rules.HeadlessCamelCaseRule in _rule_types(result)


def test_class_should_have_camel_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.CLASS_DECL).test()
    assert rules.CamelCaseRule in _rule_types(result)


def test_struct_should_have_camel_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.STRUCT_DECL).test()
    assert rules.CamelCaseRule in _rule_types(result)


def test_interface_class_should_have_if_postfix(identify_rules_tester):
    result = identify_rules_tester.with_interface_class().test()
    rule = _rule_of_type(result, rules.PostFixRule)
    assert rule.postfix == 'If'
    assert rule.condition == identification.is_interface_class


def test_identifying_class():
    result = rules.identify_rules_for_class(_Node(CursorKind.CLASS_DECL))
    assert rules.CamelCaseRule in _rule_types(result)


def test_variable_should_have_affixed_name_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.VAR_DECL).test()
    assert affixed_name_rule.AffixedNameRule in _rule_types(result)


def test_variable_should_have_base_name(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.VAR_DECL).test()
    identified_rule = _rule_of_type(result, affixed_name_rule.AffixedNameRule)
    assert identified_rule.base_name == 'variable'


def test_member_variable_should_have_affixed_name_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.FIELD_DECL).test()
    assert affixed_name_rule.AffixedNameRule in _rule_types(result)


def test_member_variable_should_have_base_name(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.FIELD_DECL).test()
    identified_rule = _rule_of_type(result, affixed_name_rule.AffixedNameRule)
    assert identified_rule.base_name == 'member variable'


def test_parameter_should_have_affixed_name_rule(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.PARM_DECL).test()
    assert affixed_name_rule.AffixedNameRule in _rule_types(result)


def test_parameter_should_have_base_name(identify_rules_tester):
    result = identify_rules_tester.with_kind(CursorKind.PARM_DECL).test()
    identified_rule = _rule_of_type(result, affixed_name_rule.AffixedNameRule)
    assert identified_rule.base_name == 'parameter'


def test_m_postfix_rule_for_member_variables(identify_rules_tester,
                                             affixed_rule):
    identify_rules_tester.with_kind(CursorKind.VAR_DECL).test()
    affixed_rule.add_postfix_rule.assert_any_call(
        None, 'M', identification.is_member)


def test_r_prefix_rule_for_reference_variables(identify_rules_tester,
                                               affixed_rule):
    identify_rules_tester.with_kind(CursorKind.VAR_DECL).test()
    affixed_rule.add_prefix_rule.assert_any_call(
        'reference', 'r', identification.is_reference)


def test_p_prefix_rule_for_pointer_variables(identify_rules_tester,
                                             affixed_rule):
    identify_rules_tester.with_kind(CursorKind.VAR_DECL).test()
    affixed_rule.add_prefix_rule.assert_any_call(
        'pointer', 'p', identification.is_pointer)


def test_a_prefix_rule_for_array_variables(identify_rules_tester,
                                           affixed_rule):
    identify_rules_tester.with_kind(CursorKind.VAR_DECL).test()
    affixed_rule.add_prefix_rule.assert_any_call(
        'array', 'a', identification.is_array)


def test_p_postfix_rule_for_parameters(identify_rules_tester, affixed_rule):
    identify_rules_tester.with_kind(CursorKind.PARM_DECL).test()
    affixed_rule.add_postfix_rule.assert_any_call(
        None, 'P', identification.is_parameter)


def test_s_postfix_rule_for_static_variables(identify_rules_tester,
                                             affixed_rule):
    identify_rules_tester.with_kind(CursorKind.VAR_DECL).test()
    affixed_rule.add_postfix_rule.assert_any_call(
        'static', 'S', identification.is_static)


def test_g_postfix_rule_for_global_variables(identify_rules_tester,
                                             affixed_rule):
    identify_rules_tester.with_kind(CursorKind.VAR_DECL).test()
    affixed_rule.add_postfix_rule.assert_any_call(
        'global', 'G', identification.is_global)


def test_constant_should_have_screaming_snake_case_rule(identify_rules_tester):
    result = identify_rules_tester.with_constant_variable().test()
    assert rules.ScreamingSnakeCaseRule in _rule_types(result)


def test_construction_of_rule():
    test = MagicMock()
    rule = rules.Rule('identifier', 'description', test)
    assert rule.type_name == 'identifier'
    assert rule.rule_test == test


def test_noticing_rule_failure():
    test = MagicMock(return_value=False)
    expected = [rules.Error('id', 'name', 'error')]
    assert expected == rules.Rule('id', 'error', test).test(_Node(name='name'))


def test_noticing_rule_success():
    test = MagicMock(return_value=True)
    assert [] == rules.Rule('', '', test).test(_Node(name=''))


def test_construction_of_conditional_rule():
    test = MagicMock()
    condition = MagicMock()
    rule = rules.ConditionalRule('identifier', 'original', 'inverted', test,
                                 condition)
    assert rule.type_name == 'identifier'
    assert rule.rule_test == test
    assert rule.original_description == 'original'
    assert rule.inverted_description == 'inverted'
    assert rule.condition == condition


def test_conditional_rule_test_is_not_inverted_by_default():
    test = MagicMock(return_value=True)
    rule = rules.ConditionalRule('', '', '', test)
    assert [] == rule.test(_Node(name=''))


def test_conditional_rule_test_is_not_inverted_with_true_condition():
    test = MagicMock(return_value=True)
    rule = rules.ConditionalRule('', '', '', test, lambda _: True)
    assert [] == rule.test(_Node(name=''))


def test_conditional_rule_uses_original_description_with_true_condition():
    test = MagicMock(return_value=False)
    rule = rules.ConditionalRule('', 'original', '', test, lambda _: True)
    assert [rules.Error('', '', 'original')] == rule.test(_Node(name=''))


def test_conditional_rule_uses_inverted_description_for_false_condition():
    test = MagicMock(return_value=True)
    rule = rules.ConditionalRule('', '', 'inverted', test, lambda _: False)
    assert [rules.Error('', '', 'inverted')] == rule.test(_Node(name=''))


def test_construction_of_camel_case_rule():
    rule = rules.CamelCaseRule('identifier')
    assert rule.error_description == 'is not in CamelCase'
    assert rule.rule_test == case_rules.is_camel_case


def test_construction_of_headless_camel_case_rule():
    rule = rules.HeadlessCamelCaseRule('identifier')
    assert rule.error_description == 'is not in headlessCamelCase'
    assert rule.rule_test == case_rules.is_headless_camel_case


def test_construction_of_screaming_snake_case_rule():
    rule = rules.ScreamingSnakeCaseRule('identifier')
    assert rule.error_description == 'is not in SCREAMING_SNAKE_CASE'
    assert rule.rule_test == case_rules.is_screaming_snake_case


def test_construction_of_postfix_rule():
    rule = rules.PostFixRule('identifier', 'postfix', MagicMock())
    assert rule.postfix == 'postfix'
    assert rule.error_description == 'does not have postfix "postfix"'


def test_missing_postfix_is_failure():
    assert len(rules.PostFixRule('id', 'P').test(_Node(name='name'))) > 0


def test_postfix_in_middle_is_failure():
    assert len(rules.PostFixRule('id', 'P').test(_Node(name='naPme'))) > 0


def test_existing_postfix_is_success():
    assert [] == rules.PostFixRule('', 'P').test(_Node(name='nameP'))


@pytest.fixture
def identify_rules_tester():
    return _IdentifyRulesTester()


@pytest.fixture
def affixed_rule(request):
    patcher = patch('affixed_name_rule.AffixedNameRule', autospec=True)
    constructor = patcher.start()
    result = MagicMock()
    constructor.return_value = result
    request.addfinalizer(patch.stopall)
    return result


class _Node:
    def __init__(self, kind=None, name=None, is_constant=False):
        self.kind = MagicMock()
        self.kind.__eq__.side_effect = lambda k: k == kind
        self.spelling = name if name else ''
        self.pure_virtual_method = False
        self.children = []
        self.type = MagicMock()
        self.type.is_const_qualified.return_value = is_constant

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

    def with_reference_variable(self):
        self.node = _Node(CursorKind.VAR_DECL)
        self.node.type.kind = TypeKind.LVALUEREFERENCE
        return self

    def with_reference_member(self):
        self.node = _Node(CursorKind.FIELD_DECL)
        self.node.type.kind = TypeKind.LVALUEREFERENCE
        return self

    def with_constant_variable(self):
        self.node = _Node(CursorKind.VAR_DECL, is_constant=True)
        return self


def _rule_types(rules):
    return [r.__class__ for r in rules]


def _rule_of_type(rules, type):
    for rule in rules:
        if rule.__class__ == type:
            return rule
    assert False, 'Could not find type ' + type.__name__
