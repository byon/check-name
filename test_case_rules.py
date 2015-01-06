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

import case_rules


def test_recognizing_camel_case_with_one_part():
    assert case_rules.is_camel_case('Foo')


def test_recognizing_camel_case_with_multiple_parts():
    assert case_rules.is_camel_case('FooBar')


def test_recognizing_camel_case_with_number_at_end():
    assert case_rules.is_camel_case('Foo1234Bar')


def test_recognizing_camel_case_with_number_at_end_of_part():
    assert case_rules.is_camel_case('Foo1234Bar')


def test_recognizing_camel_case_error_when_all_lowercase():
    assert not case_rules.is_camel_case('foo')


def test_recognizing_camel_case_error_when_starts_with_lowercase():
    assert not case_rules.is_camel_case('fooBar')


def test_recognizing_camel_case_error_when_snake_case():
    assert not case_rules.is_camel_case('foo_bar')


def test_recognizing_camel_case_error_when_capitalized_snake_case():
    assert not case_rules.is_camel_case('Foo_Bar')


def test_recognizing_camel_case_error_when_too_many_uppercase():
    assert not case_rules.is_camel_case('MMHeight')


def test_recognizing_camel_case_error_with_number_at_middle_of_part():
    assert not case_rules.is_camel_case('Fo1234oBar')


def test_recognizing_headless_camel_case_with_one_part():
    assert case_rules.is_headless_camel_case('foo')


def test_recognizing_headless_camel_case_with_multiple_parts():
    assert case_rules.is_headless_camel_case('fooBar')


def test_recognizing_headless_camel_case_with_number_at_end():
    assert case_rules.is_headless_camel_case('fooBar1234')


def test_recognizing_headless_camel_case_with_number_at_end_of_part():
    assert case_rules.is_headless_camel_case('foo1234Bar')


def test_recognizing_headless_camel_case_error_when_all_uppercase():
    assert not case_rules.is_headless_camel_case('FOO')


def test_recognizing_headless_camel_case_error_when_starts_with_Uppercase():
    assert not case_rules.is_headless_camel_case('FooBar')


def test_recognizing_headless_camel_case_error_when_snake_case():
    assert not case_rules.is_headless_camel_case('foo_bar')


def test_recognizing_headless_camel_case_error_when_capitalized_snake_case():
    assert not case_rules.is_headless_camel_case('Foo_Bar')


def test_recognizing_headless_camel_case_error_when_too_many_uppercase():
    assert not case_rules.is_headless_camel_case('isInWWF')


def test_recognizing_headless_camel_case_error_with_number_at_middle_of_part():
    assert not case_rules.is_headless_camel_case('fo1234oBar')


def test_recognizing_screaming_snake_case_with_single_part():
    assert case_rules.is_screaming_snake_case('SCREAM')


def test_recognizing_screaming_snake_case_with_multiple_parts():
    assert case_rules.is_screaming_snake_case('SCREAM_SOME_MORE')


def test_recognizing_screaming_snake_case_with_numbers_at_end():
    assert case_rules.is_screaming_snake_case('SCREAM_WITH_NUMBERS_1234')


def test_recognizing_screaming_snake_case_with_numbers_at_middle():
    assert case_rules.is_screaming_snake_case('SCREAM_2_LOUD')


def test_recognizing_screaming_snake_case_error_with_lowercase():
    assert not case_rules.is_screaming_snake_case('whimper')


def test_recognizing_screaming_snake_case_error_with_capital_start():
    assert not case_rules.is_screaming_snake_case('Capital')


def test_recognizing_screaming_snake_case_error_with_camel_case():
    assert not case_rules.is_screaming_snake_case('notSnakyEnough')


def test_recognizing_screaming_snake_case_error_with_lower_case():
    assert not case_rules.is_screaming_snake_case('not_screaming')


def test_recognizing_screaming_snake_case_error_with_underscore_at_start():
    assert not case_rules.is_screaming_snake_case('_SOMETHING')


def test_recognizing_screaming_snake_case_error_with_underscore_at_end():
    assert not case_rules.is_screaming_snake_case('SOMETHING_')


def test_recognizing_screaming_snake_case_error_with_numbers_in_middle():
    assert not case_rules.is_screaming_snake_case('D15GU5T1NG')


def test_recognizing_screaming_snake_case_error_with_numbers_at_start():
    assert not case_rules.is_screaming_snake_case('2_MANY_PROBLEMS')


def test_recognizing_screaming_snake_case_error_with_numbers_in_end_of_part():
    assert not case_rules.is_screaming_snake_case('AREA51_PARTY')
