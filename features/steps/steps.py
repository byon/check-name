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

import analysis
import ast
from test import eq_, match_

import os
from behave import given, when, then

LLVM_PATH = os.environ['LLVM_PATH']


@given('an empty source file')
def an_empty_source_file(context):
    context.ast.create_file()


@given('source file does not exist')
def source_file_does_not_exist(context):
    context.skip_file_creation = True


@given('source with {type} "{name}"')
def source_with_type(context, type, name):
    context.ast.add_child(_identify_type(type)(name))


@given('nested {type} "{name}"')
def contains_type(context, type, name):
    context.ast.open_child.add_child(_identify_type(type)(name))


@given('source file with a syntax warning')
def source_with_a_syntax_warning(context):
    context.expected_warning = "warning from test"
    context.ast.add_child(ast.Warning(context.expected_warning))


@given('source file with a syntax error')
def source_with_a_syntax_error(context):
    context.expected_error = "error from test"
    context.ast.add_child(ast.Error(context.expected_error))


@given('source file that includes file "{path}"')
def source_file_that_includes_file(context, path):
    context.ast.add_child(ast.Include(path))


@given('source file "{path}" contains {type} "{name}"')
def source_file_contains_type(context, path, type, name):
    file = ast.TranslationUnit(path)
    context.included.append(file)
    file.add_child(_identify_type(type)(name))
    file.create_file()


@given('preprocessor definitions contain "{definition}"')
def preprocessor_definitions_contain(context, definition):
    context.additional_options += ['-D' + definition]


@given('filter includes directory "{directory}"')
def filter_includes_directory(context, directory):
    context.additional_options += ['--include', directory]


@given('filter excludes directory "{directory}"')
def filter_excludes_directory(context, directory):
    context.additional_options += ['--exclude', directory]


@when('analysis is made')
def analysis_is_made(context):
    if not context.skip_file_creation:
        context.ast.create_file()
    context.result = analysis.run(_build_command(context,
                                                 context.additional_options))


@then('analysis should succeed')
def analysis_should_succeed(context):
    analysis.check_for_success(context.result)


@then('analysis should fail')
def analysis_should_fail(context):
    analysis.check_for_failure(context.result)


@then('analysis error cause should be missing source file')
def analysis_error_cause_should_be_missing_source_file(context):
    match_('Error parsing translation unit', context.result.stderr)


@then('warning cause should be reported')
def warning_cause_should_be_reported(context):
    match_(context.expected_warning, context.result.stderr)


@then('error cause should be reported')
def error_cause_should_be_reported(context):
    match_(context.expected_error, context.result.stderr)


@then('there should be no output')
def there_should_be_no_output(context):
    eq_(context.result.stderr, '')
    eq_(context.result.stdout, '')


@then('analysis should report no rule violations')
def analysis_should_report_no_rule_violations(context):
    analysis.check_for_success(context.result)
    eq_(context.result.stderr, '')
    eq_(context.result.stdout, '')


@then('analysis reports "{type}" "{name}" as "{cause}" rule violation')
def analysis_reports_rule_violation(context, type, name, cause):
    analysis.check_for_failure(context.result)
    match_(': ' + type + ' "' + name + '" .*' + cause,
           context.result.stderr)


def _build_command(context, additional_arguments):
    return _mandatory_options(context.ast.path) + additional_arguments


def _mandatory_options(path):
    return ['--llvm_path', LLVM_PATH, '--target', path]


def _identify_type(name):
    type_map = {'class': ast.Class,
                'method': ast.Method,
                'namespace': ast.Namespace,
                'preprocessor_condition': ast.PreprocessorCondition,
                'pure_virtual_method': ast.PureVirtualMethod,
                'struct': ast.Struct,
                'variable': ast.Variable}
    return type_map[name.replace(' ', '_').lower()]
