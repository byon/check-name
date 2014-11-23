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

import analyze

import clang

import pytest
from mock import MagicMock, patch


def test_analyzing_empty_translation_unit(translation_unit, analyzer):
    analyze.analyze_nodes(MagicMock(), translation_unit)
    assert analyzer.call_count == 0


def test_analyzing_one_namespace(translation_unit, analyzer):
    translation_unit.with_namespace('Foo')
    analyze.analyze_nodes(MagicMock(), translation_unit)
    assert analyzer.call_count == 1


@pytest.fixture
def analyzer(request):
    result = patch('analyze.analyze_namespace', autospec=True)
    request.addfinalizer(patch.stopall)
    return result.start()


@pytest.fixture
def translation_unit():
    return _Node()


class _Node:
    def __init__(self):
        self.children = []
        self.cursor = MagicMock()
        self._update_child_iterator()

    def with_namespace(self, name):
        return self.with_declaration(clang.cindex.CursorKind.NAMESPACE, name)

    def with_declaration(self, cursor_kind, name):
        declaration = _Node()
        declaration.kind = cursor_kind
        self.children.append(declaration)
        return self

    def _update_child_iterator(self):
        self.cursor.get_children.return_value = iter(self.children)
