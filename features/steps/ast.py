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

from environment import TEST_EXECUTION_DIRECTORY
import os.path


class _Node:
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end
        self.children = []
        self._open_child = None

    def add_child(self, child):
        self.children.append(child)
        self._open_child = child

    def generate(self):
        result = self.start
        for child in self.children:
            result += child.generate()
        result += self.end
        return result

    @property
    def has_open_child(self):
        return self._open_child is not None

    @property
    def open_child(self):
        assert self._open_child, '"' + self.id + '" does not have open child'
        if self._open_child.has_open_child:
            return self._open_child.open_child
        return self._open_child


class TranslationUnit(_Node):
    def __init__(self, path=None):
        self.path = _choose_path(path)
        _Node.__init__(self, path, '', '')

    def create_file(self):
        _ensure_parent_exists(self.path_in_execution_directory)
        with open(self.path_in_execution_directory, 'w') as file:
            file.write(self.generate())

    @property
    def path_in_execution_directory(self):
        return os.path.join(TEST_EXECUTION_DIRECTORY, self.path)


class Namespace(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'namespace ' + name + '{\n', '}\n')


class Class(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'class ' + name + ' {\n', '};\n')


class Struct(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'struct ' + name + ' {\n', '};\n')


class PreprocessorCondition(_Node):
    def __init__(self, condition):
        _Node.__init__(self, condition, '#ifdef ' + condition + '\n',
                       '#endif\n')


class PureVirtualMethod(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'virtual void ' + name + '() = 0;\n', '')


class Function(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'void ' + name + '();\n', '')


# Currently Method is exactly the same as Function
class Method(Function):
    pass


class Constructor(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, name + '();\n', '')


class Variable(_Node):
    def __init__(self, name, type=None, value=None):
        type = type if type else 'int'
        assignment = ' = ' + value if value else ''
        _Node.__init__(self, name, type + ' ' + name, assignment + ';\n')


class ArrayVariable(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'int ' + name + '[20]', ';\n')


class PointerVariable(Variable):
    def __init__(self, name):
        Variable.__init__(self, name, 'int*', 0)


class ReferenceVariable(Variable):
    def __init__(self, name, referencedVariable=None):
        Variable.__init__(self, name, 'int&', referencedVariable)


class Warning(_Node):
    def __init__(self, description):
        _Node.__init__(self, description, '#warning ' + description, '')


class Error(_Node):
    def __init__(self, description):
        _Node.__init__(self, description, '#error ' + description, '')


class Include(_Node):
    def __init__(self, path):
        _Node.__init__(self, path, '#include "' + path + '"', '')


def _choose_path(path):
    if not path:
        return _default_path()
    return path


def _ensure_parent_exists(path):
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)


def _default_path():
    return 'source.cpp'
