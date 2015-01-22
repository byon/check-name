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

import steps.analysis as analysis
import steps.ast as ast
from test import eq_, match_

import os
from behave import given, when, then

LLVM_PATH = os.environ['LLVM_PATH']


@given('an empty source file')
def an_empty_source_file(context):
    context.given_input = context.ast.create_file()


@given('source file does not exist')
def source_file_does_not_exist(context):
    context.skip_file_creation = True


@given('source with reference variable "{name}"')
def source_with_reference_variable(context, name):
    referenced = _ensure_variable_exists(context.ast, 'referenced')
    context.ast.add_child(ast.ReferenceVariable(name, referenced))


@given('source with template class "{name}" with type parameter "{parameter}"')
def source_with_template_class_type(context, name, parameter):
    context.ast.add_child(ast.TemplateClass(name, parameter, None))


@given('source with template class "{name}" with non-type parameter "{non}"')
def source_with_template_class_with_nontype_parameter(context, name, non):
    context.ast.add_child(ast.TemplateClass(name, None, non))


@given('source with {type} "{name}"')
def source_with_type(context, type, name):
    context.ast.add_child(_create_node(type, name))


@given('nested reference variable "{name}"')
def contains_reference_variable(context, name):
    open_child = context.ast.open_child
    referenced = _ensure_variable_exists(open_child, 'referenced')
    open_child.add_child(ast.ReferenceVariable(name, referenced))


@given('nested {type} "{name}"')
def contains_type(context, type, name):
    context.ast.open_child.add_child(_create_node(type, name))


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
    file.add_child(_create_node(type, name))
    context.given_input = file.create_file()


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
        context.given_input = context.ast.create_file()
    context.result = analysis.run(_build_command(context,
                                                 context.additional_options))


@then('analysis should succeed')
def analysis_should_succeed(context):
    analysis.check_for_success(context.result, context.given_input)


@then('analysis should fail')
def analysis_should_fail(context):
    analysis.check_for_failure(context.result, context.given_input)


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
    analysis.check_for_success(context.result, context.given_input)
    eq_(context.result.stderr, '')
    eq_(context.result.stdout, '')


@then('analysis reports "{type}" "{name}" as "{cause}" rule violation')
def analysis_reports_rule_violation(context, type, name, cause):
    analysis.check_for_failure(context.result, context.given_input)
    match_(_expression_for_failure(type, name, cause), context.result.stderr)


def _build_command(context, additional_arguments):
    return _mandatory_options(context.ast.path) + additional_arguments


def _mandatory_options(path):
    return ['--llvm_path', LLVM_PATH, '--target', path, '-std=c++11']


def _ensure_variable_exists(parent, name):
    actual_name = name
    if isinstance(parent, ast.Class):
        actual_name += 'M'
    elif isinstance(parent, ast.TranslationUnit):
        actual_name += 'G'
    else:
        print('it is not either')
    parent.add_child(ast.Variable(actual_name))
    return actual_name


def _create_node(type, name):
    if 'const' in type:
        return ast.Variable(name, type='const int', value='0')
    return _identify_type(type)(name)


def _identify_type(name):
    type_map = {'abstract_class': ast.AbstractClass,
                'array_variable': ast.ArrayVariable,
                'class': ast.Class,
                'constant_variable': ast.Variable,
                'function': ast.Function,
                'function_implementation': ast.FunctionImplementation,
                'interface_class': ast.InterfaceClass,
                'method': ast.Method,
                'namespace': ast.Namespace,
                'parameter': ast.Parameter,
                'reference_parameter': ast.ReferenceParameter,
                'pointer_parameter': ast.PointerParameter,
                'pointer_variable': ast.PointerVariable,
                'pointer_array_variable': ast.PointerArrayVariable,
                'preprocessor_condition': ast.PreprocessorCondition,
                'pure_virtual_method': ast.PureVirtualMethod,
                'smart_pointer_variable': ast.SmartPointerVariable,
                'static_variable': ast.StaticVariable,
                'struct': ast.Struct,
                'reference_variable': ast.ReferenceVariable,
                'template_function': ast.TemplateFunction,
                'typedef': ast.Typedef,
                'variable': ast.Variable}
    return type_map[name.strip().replace(' ', '_').lower()]


def _expression_for_failure(type, name, cause):
    type_expression = _expression_for_type(type)
    return type_expression + ' "' + name + '" .*' + cause


def _expression_for_type(type):
    stripped = type.strip()
    if stripped == 'pointer array variable':
        return '(pointer|array) variable'
    if stripped == 'smart pointer variable':
        return 'pointer variable'
    return stripped
