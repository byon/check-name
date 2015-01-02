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
    if identification.is_member(node) or identification.is_variable(node):
        return identify_rules_for_variables(node)
    if identification.is_method(node):
        return [HeadlessCamelCaseRule('method')]
    if identification.is_function(node):
        return [HeadlessCamelCaseRule('function')]
    if identification.is_class(node):
        return identify_rules_for_class(node)
    if identification.is_struct(node):
        return [CamelCaseRule('struct')]
    return []


def identify_rules_for_class(node):
    result = [CamelCaseRule('class')]
    if identification.is_interface_class(node):
        result.append(PostFixRule('interface class', 'If'))
    return result


def identify_rules_for_variables(node):
    result = affixed_name_rule.AffixedNameRule()
    result.add_prefix_rule('reference variable', 'r',
                           identification.is_reference)
    result.add_postfix_rule('member variable', 'M', identification.is_member)
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


class CamelCaseRule(Rule):
    def __init__(self, identifier, prefix_size=0, postfix_size=0):
        Rule.__init__(self, identifier, 'is not in CamelCase',
                      case_rules.is_camel_case)


class HeadlessCamelCaseRule(Rule):
    def __init__(self, identifier):
        description = 'is not in headlessCamelCase'
        Rule.__init__(self, identifier, description,
                      case_rules.is_headless_camel_case)


class PostFixRule(Rule):
    def __init__(self, identifier, postfix):
        self.postfix = postfix
        Rule.__init__(self, identifier,
                      'does not have postfix "' + postfix + '"',
                      lambda n: n.endswith(self.postfix))
