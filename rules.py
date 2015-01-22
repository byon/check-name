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

import case_rules
import identification
import affixed_name_rule


def identify_rules(node):
    if identification.is_namespace(node):
        return [CamelCaseRule('namespace')]
    if identification.is_any_kind_of_variable(node):
        return identify_rules_for_variables(node)
    if identification.is_method(node):
        return [HeadlessCamelCaseRule('method')]
    if identification.is_function(node):
        return [HeadlessCamelCaseRule('function')]
    if identification.is_template_type_parameter(node):
        return [CamelCaseRule('template type parameter')]
    if identification.is_class(node):
        return identify_rules_for_class(node)
    if identification.is_struct(node):
        return [CamelCaseRule('struct')]
    if identification.is_typedef_declaration(node):
        return [CamelCaseRule('typedef')]
    return []


def identify_rules_for_class(node):
    result = [CamelCaseRule('class')]
    result.append(PostFixRule('interface class', 'If',
                              identification.is_interface_class))
    result.append(PostFixRule('abstract class', 'Abs',
                              identification.is_abstract_class))
    return result


def identify_rules_for_variables(node):
    if node.type.is_const_qualified():
        return [ScreamingSnakeCaseRule('constant variable')]
    result = affixed_name_rule.AffixedNameRule(_variable_base_name(node))
    result.add_prefix_rule('array', 'a', identification.is_array)
    result.add_prefix_rule('pointer', 'p', identification.is_pointer)
    result.add_prefix_rule('reference', 'r', identification.is_reference)
    result.add_postfix_rule(None, 'M', identification.is_member)
    result.add_postfix_rule(None, 'P', identification.is_parameter)
    result.add_postfix_rule('static', 'S', identification.is_static)
    result.add_postfix_rule('global', 'G', identification.is_global)
    return [result]


def identify_case_rule(node, prefix_size, postfix_size):
    if prefix_size > 0:
        return CamelCaseRule('variable', prefix_size, postfix_size)
    return HeadlessCamelCaseRule('variable', postfix_size)


class Error:
    def __init__(self, type_name, failed_name, error_description):
        self.type_name = type_name
        self.failed_name = failed_name
        self.error_description = error_description

    def __eq__(self, other):
        return (self.type_name == other.type_name and
                self.failed_name == other.failed_name and
                self.error_description == other.error_description)

    def __repr__(self):
        return str([self.type_name, self.failed_name, self.error_description])


class Rule:
    def __init__(self, type_name, error_description, rule_test=None):
        self.type_name = type_name
        self.error_description = error_description
        self.rule_test = rule_test

    def test(self, node):
        if self.rule_test(node.spelling):
            return []
        return [Error(self.type_name, node.spelling, self.error_description)]


class ConditionalRule(Rule):
    def __init__(self, type_name, original_description, inverted_description,
                 rule_test, condition=None):
        Rule.__init__(self, type_name, original_description, rule_test)
        self.original_description = original_description
        self.inverted_description = inverted_description
        self.condition = condition

    def test(self, node):
        result = self.rule_test(node.spelling)
        if result:
            if self._should_invert_result(node):
                return [Error(self.type_name, node.spelling,
                              self.inverted_description)]
        else:
            if not self._should_invert_result(node):
                return [Error(self.type_name, node.spelling,
                              self.original_description)]
        return []

    def _should_invert_result(self, node):
        return self.condition and not self.condition(node)


class CamelCaseRule(Rule):
    def __init__(self, identifier, prefix_size=0, postfix_size=0):
        Rule.__init__(self, identifier, 'is not in CamelCase',
                      case_rules.is_camel_case)


class HeadlessCamelCaseRule(Rule):
    def __init__(self, identifier):
        description = 'is not in headlessCamelCase'
        Rule.__init__(self, identifier, description,
                      case_rules.is_headless_camel_case)


class ScreamingSnakeCaseRule(Rule):
    def __init__(self, identifier):
        description = 'is not in SCREAMING_SNAKE_CASE'
        Rule.__init__(self, identifier, description,
                      case_rules.is_screaming_snake_case)


class PostFixRule(ConditionalRule):
    def __init__(self, identifier, postfix, condition=None):
        self.postfix = postfix
        ConditionalRule.__init__(self, identifier,
                                 'does not have postfix "' + postfix + '"',
                                 'has redundant postfix "' + postfix + '"',
                                 lambda n: n.endswith(self.postfix),
                                 condition)


def _variable_base_name(node):
    if identification.is_variable(node):
        return 'variable'
    if identification.is_member(node):
        return 'member variable'
    if identification.is_parameter(node):
        return 'parameter'
    assert False, 'unidentified variable type'
