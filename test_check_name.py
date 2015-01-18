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
import check_name
from mock import MagicMock, patch
import pytest


def test_analysis_will_set_llvm_path(tester):
    tester.with_llvm_path('path')
    tester.test()
    tester.configuration.set_library_path.assert_called_once_with('path')


def test_analysis_will_create_clang_index(tester):
    tester.test()
    tester.index_class.create.assert_called_once_with()


def test_analysis_will_pass_target_file_to_clang(tester):
    tester.with_target_path('target').test()
    passed_target = tester.index.parse.call_args[0][0]
    assert 'target' == passed_target


def test_analysis_will_pass_unknown_options_to_clang(tester):
    tester.with_target_path('t').with_additional_option('option', '1').test()
    passed_options = tester.index.parse.call_args[0][1]
    assert '--option', '1' in passed_options


def test_analysis_will_add_clang_builtin_headers_as_include_path(tester):
    tester.with_llvm_path('path').test()
    passed_options = tester.index.parse.call_args[0][1]
    assert 'path/clang/3.6.0/include/' in passed_options


def test_analysis_will_add_clang_builtin_headers_as_filtering_option(tester):
    tester.with_llvm_path('path').test()
    assert 'path/clang/3.6.0/include/' in tester.exclude_options_for_analyser


def test_analysis_is_done(tester):
    tester.test()
    assert tester.analyser.call_count == 1
    assert tester.output_for_analyser == tester.output
    assert tester.translation_unit_for_analyser == tester.parse_result


def test_passing_include_directory_to_analysis(tester):
    tester.with_include_directory('a').test()
    assert 'a' in tester.include_options_for_analyser


def test_passing_multiple_include_directories_to_analysis(tester):
    tester.with_include_directory('a').with_include_directory('b').test()
    assert 'a' in tester.include_options_for_analyser
    assert 'b' in tester.include_options_for_analyser


def test_passing_exclude_directory_to_analysis(tester):
    tester.with_exclude_directory('a').test()
    assert 'a' in tester.exclude_options_for_analyser


def test_passing_include_and_exclude_directories_to_analysis(tester):
    tester.with_include_directory('a').with_include_directory('b')
    tester.with_exclude_directory('c').with_exclude_directory('d').test()
    assert 'a' in tester.include_options_for_analyser
    assert 'b' in tester.include_options_for_analyser
    assert 'c' in tester.exclude_options_for_analyser
    assert 'd' in tester.exclude_options_for_analyser


def test_missing_source_file_is_an_error(tester):
    assert 0 != tester.with_missing_target_path().test()


def test_missing_source_file_is_reported(tester):
    tester.with_missing_target_path().test()
    expected = str(clang.cindex.TranslationUnitLoadError())
    tester.output.error.assert_called_once_with(expected)


def test_errors_are_noticed(tester):
    assert 0 != tester.with_errors().test()


def test_success_noticed(tester):
    assert 0 == tester.without_errors().test()


def test_one_diagnostic_is_reported(tester):
    tester.with_diagnostic('reason').test()
    tester.output.diagnostic.assert_called_once_with(2, 'location', 'reason')


def test_multiple_diagnostics_are_reported(tester):
    tester.with_diagnostic('reason').with_diagnostic('reason2').test()
    assert tester.output.diagnostic.call_count == 2


@pytest.fixture
def tester(request):
    result = _Tester()
    request.addfinalizer(patch.stopall)
    return result


class _Tester:
    def __init__(self):
        self.llvm_path = 'llvm_path'
        self.target_path = 'target_path'
        self.extra_arguments = []

        self.configuration = self._add_patch_without_autospec(
            'clang.cindex.conf')

        self.index_class = self._add_patch('clang.cindex.Index')
        self.index_class.create.return_value = self.index = MagicMock()
        self.parse_result = MagicMock(diagnostics=[])
        self.index.parse.return_value = self.parse_result
        self.index_class.return_value = self.index

        self.analyser = self._add_patch('analyse.analyse_translation_unit')

        self.output_creator = self._add_patch('report.Output')
        self.output = MagicMock()
        self.output_creator.return_value = self.output

        self.without_errors()

    def with_llvm_path(self, path):
        self.llvm_path = path
        return self

    def with_include_directory(self, directory):
        return self.with_additional_option('include', directory)

    def with_exclude_directory(self, directory):
        return self.with_additional_option('exclude', directory)

    def with_additional_option(self, name, value):
        self.extra_arguments += _option_as_list(name, value)
        return self

    def with_missing_target_path(self):
        exception = clang.cindex.TranslationUnitLoadError()
        self.index.parse.side_effect = exception
        return self

    def without_errors(self):
        self.output.has_errors = False
        return self

    def with_errors(self):
        self.output.has_errors = True
        return self

    def with_diagnostic(self, reason):
        diagnostic = MagicMock(location='location', severity=2,
                               spelling=reason)
        self.parse_result.diagnostics += [diagnostic]
        return self

    def with_target_path(self, path):
        self.target_path = path
        return self

    def test(self):
        return check_name.main(self._build_argument_list())

    @property
    def output_for_analyser(self):
        return self.analyser.call_args[0][0]

    @property
    def translation_unit_for_analyser(self):
        return self.analyser.call_args[0][1]

    @property
    def include_options_for_analyser(self):
        return self.analyser.call_args[0][2][0]

    @property
    def exclude_options_for_analyser(self):
        return self.analyser.call_args[0][2][1]

    def _build_argument_list(self):
        arguments = ['executable']
        arguments += _option_as_list('llvm_path', self.llvm_path)
        arguments += _option_as_list('target', self.target_path)
        arguments += self.extra_arguments
        return arguments

    def _add_patch(self, name):
        patcher = patch(name, autospec=True)
        return patcher.start()

    def _add_patch_without_autospec(self, name):
        patcher = patch(name, autospec=False)
        return patcher.start()


def _option_as_list(name, value):
    if not value:
        return []
    return ['--' + name, value]
