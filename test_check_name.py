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

import check_name
from mock import MagicMock, patch
import pytest


def test_analysis_will_create_clang_index(tester):
    tester.test()
    tester.index_class.create.assert_called_once_with()


def test_analysis_will_pass_target_file_to_clang(tester):
    tester.test()
    tester.index.parse.assert_called_once_with('path')


def test_analysis_is_done(tester):
    tester.test()
    tester.analyzer.assert_called_once_with(tester.output, 'TranslationUnit')


def test_errors_are_noticed(tester):
    assert 0 != tester.with_errors().test()


def test_success_noticed(tester):
    assert 0 == tester.without_errors().test()


@pytest.fixture
def tester(request):
    result = _Tester()
    request.addfinalizer(patch.stopall)
    return result


class _Tester:
    def __init__(self):
        self.arguments = ['executable', 'path']

        self.index_class = self._add_patch('clang.cindex.Index')
        self.index_class.create.return_value = self.index = MagicMock()
        self.index.parse.return_value = 'TranslationUnit'
        self.index_class.return_value = self.index

        self.analyzer = self._add_patch('check_name.analyze_translation_unit')

        self.output_creator = self._add_patch('check_name.Output')
        self.output = MagicMock()
        self.output_creator.return_value = self.output

        self.without_errors()

    def without_errors(self):
        self.output.has_errors = False
        return self

    def with_errors(self):
        self.output.has_errors = True
        return self

    def test(self):
        return check_name.main(self.arguments)

    def _add_patch(self, name):
        patcher = patch(name, autospec=True)
        return patcher.start()
