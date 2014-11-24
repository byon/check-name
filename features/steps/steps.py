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
import source_file
from test import eq_, match_

import os
from behave import given, when, then

LLVM_PATH = os.environ['LLVM_PATH']


@given('an empty source file')
def an_empty_source_file(context):
    context.path = source_file.create(_add_content(context, ''))


@given('source file does not exist')
def source_file_does_not_exist(context):
    context.path = 'this/really/should/not/exist.cpp'


@given('source with namespace "{name}"')
def source_with_namespace(context, name):
    content = 'namespace ' + name + '{}\n'
    context.path = source_file.create(_add_content(context, content))


@given('source with nested namespace "{inner}" inside namespace "{outer}"')
def source_with_nested_namespaces(context, inner, outer):
    content = 'namespace ' + outer + '{ namespace ' + inner + '{}}\n'
    context.path = source_file.create(_add_content(context, content))


@when('analysis is made')
def analysis_is_made(context):
    context.result = analysis.run(_build_command(context))


@then('analysis should succeed')
def analysis_should_succeed(context):
    analysis.check_for_success(context.result)


@then(u'analysis should fail')
def analysis_should_fail(context):
    analysis.check_for_failure(context.result)


@then(u'analysis error cause should be missing source file')
def analysis_error_cause_should_be_missing_source_file(context):
    match_('Error parsing translation unit', context.result.stderr)


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
    match_(': ' + type + ' "' + name + '" is not in ' + cause,
           context.result.stderr)


def _build_command(context):
    return _mandatory_options() + [context.path]


def _mandatory_options():
    return ['--llvm_path', LLVM_PATH]


def _add_content(context, content):
    if context.content is None:
        context.content = ''
    context.content += content
    return context.content
