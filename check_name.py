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

from __future__ import print_function
import sys
import clang.cindex


def main(arguments):
    clang.cindex.conf.set_library_path('/home/byon/src/vendor/' +
                                       'llvm/build/Release/lib')
    index = clang.cindex.Index.create()
    output = Output()
    analyze_translation_unit(output, index.parse(arguments[1]))
    if output.has_errors:
        return 1
    return 0


def analyze_translation_unit(output, translation_unit):
    first = None
    try:
        first = next(translation_unit.cursor.get_children())
    except StopIteration:
        return
    analyze_namespace(output, first)


def analyze_namespace(output, namespace):
    output.error(namespace.location, 'namespace', namespace.spelling,
                 'is not in CamelCase')


class Output:

    def __init__(self):
        self.error_count = 0

    def error(self, location, type, symbol, reason):
        output = '{}: {} "{}" {}'.format(location_to_string(location),
                                         type, symbol, reason)
        print(output, file=sys.stderr)
        self.error_count += 1

    @property
    def has_errors(self):
        return self.error_count > 0


def location_to_string(location):
    return (str(location.file) + ' (' +
            str(location.line) + ', ' +
            str(location.column) + ')')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
