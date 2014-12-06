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


def test_recognizing_camel_case_with_one_part():
    assert analyse.is_camel_case('Foo')


def test_recognizing_camel_case_with_multiple_parts():
    assert analyse.is_camel_case('FooBar')


def test_recognizing_camel_case_with_number_at_end():
    assert analyse.is_camel_case('Foo1234Bar')


def test_recognizing_camel_case_with_number_at_end_of_part():
    assert analyse.is_camel_case('Foo1234Bar')


def test_recognizing_camel_case_error_when_all_lowercase():
    assert not analyse.is_camel_case('foo')


def test_recognizing_camel_case_error_when_starts_with_lowercase():
    assert not analyse.is_camel_case('fooBar')


def test_recognizing_camel_case_error_when_snake_case():
    assert not analyse.is_camel_case('foo_bar')


def test_recognizing_camel_case_error_when_capitalized_snake_case():
    assert not analyse.is_camel_case('Foo_Bar')


def test_recognizing_camel_case_error_when_too_many_uppercase():
    assert not analyse.is_camel_case('MMHeight')


def test_recognizing_camel_case_error_with_number_at_middle_of_part():
    assert not analyse.is_camel_case('Fo1234oBar')
