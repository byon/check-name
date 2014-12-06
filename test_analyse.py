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

import analyse

import clang

import pytest
from mock import MagicMock, patch


def test_analysing_empty_translation_unit(translation_unit, analyser):
    analyse.analyse_translation_unit(MagicMock(), translation_unit, ([],))
    assert analyser.call_count == 0


def test_analysing_one_namespace(translation_unit, analyser):
    namespace = translation_unit.cursor.new_namespace('Foo')
    output = MagicMock()
    analyse.analyse_translation_unit(output, translation_unit, ([], []))
    analyser.assert_called_once_with(output, namespace)


def test_only_declarations_are_analysed(analyse_nodes_tester):
    analyse_nodes_tester.with_non_declaration().test()
    assert analyse_nodes_tester.analyser.call_count == 0


def test_children_are_analysed_for_non_declarations(analyse_nodes_tester):
    analyse_nodes_tester.root.new_non_declaration().new_namespace('a')
    analyse_nodes_tester.test()
    assert analyse_nodes_tester.analyser.call_count == 1


def test_analysing_sequential_namespaces(analyse_nodes_tester):
    analyse_nodes_tester.with_namespace('Foo').with_namespace('Bar').test()
    assert analyse_nodes_tester.analyser.call_count == 2


def test_analysing_nested_namespaces(analyse_nodes_tester):
    analyse_nodes_tester.root.new_namespace('Foo').new_namespace('Bar')
    analyse_nodes_tester.test()
    assert analyse_nodes_tester.analyser.call_count == 2


def test_filtering_is_done(analyse_nodes_tester):
    node = analyse_nodes_tester.root.new_namespace('Foo')
    analyse_nodes_tester.test()
    analyse_nodes_tester.filter.assert_called_once_with(
        analyse_nodes_tester.filtering_options, node.location.file.name)


def test_filtered_nodes_are_not_analysed(analyse_nodes_tester):
    analyse_nodes_tester.filter.return_value = True
    analyse_nodes_tester.with_namespace('Foo').test()
    assert analyse_nodes_tester.analyser.call_count == 0


def test_root_is_not_checked_for_filtering(analyse_nodes_tester):
    analyse_nodes_tester.test()
    assert analyse_nodes_tester.filter.call_count == 0


def test_camel_case_analysis_succeeds(output, node):
    with patch('analyse.is_camel_case') as analyser:
        analyser.return_value = True
        analyse.analyse_camel_case(output, node)
    assert 0 == output.rule_violation.call_count


def test_camel_case_analysis_fails(output, node):
    with patch('analyse.is_camel_case') as analyser:
        analyser.return_value = False
        analyse.analyse_camel_case(output, node)
    output.rule_violation.assert_called_once_with(
        node.location, 'namespace', node.spelling, 'is not in CamelCase')


@pytest.fixture
def analyser(request):
    result = patch('analyse.analyse_camel_case', autospec=True)
    request.addfinalizer(patch.stopall)
    return result.start()


@pytest.fixture
def translation_unit():
    result = MagicMock
    result.cursor = _Node('name')
    return result


@pytest.fixture
def node():
    return _Node('name')


@pytest.fixture
def analyse_nodes_tester(request):
    result = _NodeAnalyseTester()
    request.addfinalizer(patch.stopall)
    return result


@pytest.fixture
def output():
    return MagicMock()


class _NodeAnalyseTester:
    def __init__(self):
        self.root = _Node('root')
        self.analyser = self._add_patch('analyse.analyse_camel_case')
        self.filter = self._add_patch('filter.should_filter')
        self.filter.return_value = False
        self.output = MagicMock()
        self.filtering_options = MagicMock()

    def test(self):
        analyse.analyse_nodes(self.output, self.root, self.filtering_options)

    def with_namespace(self, name):
        self.root.new_namespace(name)
        return self

    def with_non_declaration(self):
        self.root.new_non_declaration()
        return self

    def _add_patch(self, name):
        patcher = patch(name, autospec=True)
        return patcher.start()


class _Node:
    def __init__(self, name, kind=None):
        self.children = []
        self.cursor = MagicMock()
        self.cursor.get_children.return_value = iter(self.children)
        self.spelling = name
        self.location = MagicMock(file=MagicMock(name='File.cpp'))
        self.kind = MagicMock()
        self.kind.__eq__.side_effect = lambda k: k == kind
        self.kind.is_declaration.return_value = False

    @staticmethod
    def create_namespace(name):
        return _Node.create_declaration(
            clang.cindex.CursorKind.NAMESPACE, name)

    @staticmethod
    def create_declaration(kind, name):
        declaration = _Node(name, kind)
        declaration.kind.is_declaration.return_value = True
        return declaration

    def get_children(self):
        return iter(self.children)

    def new_namespace(self, name):
        return self._add_child(_Node.create_namespace, name)

    def new_non_declaration(self):
        non_declaration = _Node('irrelevant',
                                clang.cindex.CursorKind.TRANSLATION_UNIT)
        return self._add_child(lambda _: non_declaration)

    def _add_child(self, creator, *args):
        child = creator(args)
        self.children.append(child)
        return child
