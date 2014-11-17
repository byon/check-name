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


import subprocess
from test import eq_, not_eq_

PATH_TO_ANALYZER = 'check_name.py'


def run(arguments):
    return call(['python2', PATH_TO_ANALYZER] + arguments)


def check_for_success(result):
    eq_(0, result.exit_code, _unexpected_success_description(result))


def check_for_failure(result):
    not_eq_(0, result.exit_code, _unexpected_failure_description(result))


def call(arguments):
    process = subprocess.Popen(args=arguments, universal_newlines=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return Result(process.returncode, stdout, stderr)


def _unexpected_success_description(result):
    return _unexpected_result_description('succeed', 'failed', result)


def _unexpected_failure_description(result):
    return _unexpected_result_description('fail', 'succeeded', result)


def _unexpected_result_description(expectation, actual_result, result):
    template = ('Expected analysis to {}, but {}\n' +
                _template_for_output('stdout') +
                _template_for_output('stderr'))
    return template.format(expectation, actual_result,
                           result.stdout, result.stderr)


def _template_for_output(identifier):
    separator = '-' * 80 + '\n'
    return identifier + ':\n' + separator + '{}' + separator


class Result:
    def __init__(self, exit_code, stdout, stderr):
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
