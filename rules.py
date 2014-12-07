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

import clang
import re


def identify_rules(node):
    if is_namespace(node):
        return [CamelCaseRule('namespace')]
    if is_variable(node):
        return [HeadlessCamelCaseRule('variable')]
    return []


class Rule:
    def __init__(self, type_name, error_description, rule_test):
        self.type_name = type_name
        self.error_description = error_description
        self.rule_test = rule_test

    def test(self, node):
        return self.rule_test(node.spelling)


class CamelCaseRule(Rule):
    def __init__(self, identifier):
        Rule.__init__(self, identifier, 'is not in CamelCase', is_camel_case)


class HeadlessCamelCaseRule(Rule):
    def __init__(self, identifier):
        Rule.__init__(self, identifier, 'is not in headlessCamelCase',
                      is_headless_camel_case)


def is_camel_case(name):
    return True if re.match('^([A-Z][a-z]+\d*)+$', name) else False


def is_headless_camel_case(name):
    return True if re.match('^[a-z]+\d*([A-Z][a-z]+\d*)*$', name) else False


def is_namespace(node):
    return clang.cindex.CursorKind.NAMESPACE == node.kind


def is_variable(node):
    return clang.cindex.CursorKind.VAR_DECL == node.kind
