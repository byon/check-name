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
        self.include_statements = set()

    def add_child(self, child):
        self.children.append(child)
        self._open_child = child

    def add_child_to_type(self, child_to_add, required_type):
        is_type = lambda n: isinstance(n, required_type)
        assert self._add_child_based_on_condition(child_to_add, is_type)

    def _add_child_based_on_condition(self, child_to_add, condition):
        if condition(self):
            self.add_child(child_to_add)
            return True
        for child in reversed(self.children):
            if child._add_child_based_on_condition(child_to_add, condition):
                return True
        return False

    def require_include_statement(self, to_include):
        statement = '#include <' + to_include + '>'
        self.include_statements.add(statement)

    def generate(self):
        result = self.start
        for child in self.children:
            result += child.generate()
        result += self.end
        return result

    def generate_statements(self):
        result = ''
        for statement in self.include_statements:
            result += statement + '\n'
        for child in self.children:
            result += child.generate_statements()
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
            content = self._generate_content()
            file.write(content)
            return content

    @property
    def path_in_execution_directory(self):
        return os.path.join(TEST_EXECUTION_DIRECTORY, self.path)

    def _generate_content(self):
        return self.generate_statements() + self.generate()


class Namespace(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'namespace ' + name + '{\n', '}\n')


class Class(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'class ' + name + ' {\n', '};\n')


class Struct(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'struct ' + name + ' {\n', '};\n')


class InterfaceClass(Class):
    def __init__(self, name):
        Class.__init__(self, name)
        self.add_child(PureVirtualMethodDeclaration('pureVirtualMethod'))


class AbstractClass(Class):
    def __init__(self, name):
        Class.__init__(self, name)
        self.add_child(PureVirtualMethodDeclaration('pureVirtualMethod'))
        self.add_child(MethodDeclaration('someMethod'))


class TemplateClass(_Node):
    def __init__(self, name, parameter, non_type):
        parameters = self._build_parameters(parameter, non_type)
        start = 'template <' + parameters + '>\nclass ' + name + ' {\n'
        _Node.__init__(self, name, start, '};\n')

    def _build_parameters(self, parameter, non_type):
        first = ['typename ' + parameter] if parameter else []
        second = ['int ' + non_type] if non_type else []
        return ', '.join(first + second)


class PreprocessorCondition(_Node):
    def __init__(self, condition):
        _Node.__init__(self, condition, '#ifdef ' + condition + '\n',
                       '#endif\n')


class Typedef(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'typedef int ' + name + ';', '\n')


class PureVirtualMethodDeclaration(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'virtual void ' + name + '() = 0;\n', '')


class FunctionPrototype(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'void ' + name + '(', ')')


class FunctionDeclaration(_Node):
    def __init__(self, name):
        _Node.__init__(self, 'declaration', '', ';')
        self.add_child(FunctionPrototype(name))


class Block(_Node):
    def __init__(self):
        _Node.__init__(self, 'block', '{\n', '}\n')


class Function(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, '', '')
        self.add_child(FunctionPrototype(name))
        self.add_child(Block())


class TemplateFunction(_Node):
    def __init__(self, name):
        start = 'template <typename T>\nvoid ' + name + '('
        _Node.__init__(self, name, start, ')\n{\n}\n')


class Method(Function):
    def __init__(self, name):
        Function.__init__(self, name)


class MethodDeclaration(FunctionDeclaration):
    def __init__(self, name):
        FunctionDeclaration.__init__(self, name)


class Constructor(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, name + '();\n', '')


class Variable(_Node):
    def __init__(self, name, type=None, value=None):
        type = type if type else 'int'
        assignment = ' = ' + value if value else ''
        _Node.__init__(self, name, type + ' ' + name, assignment + ';\n')


class StaticVariable(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'static int ' + name, ';\n')


class Parameter(_Node):
    def __init__(self, name, type=None):
        type = type if type else 'int'
        _Node.__init__(self, name, type + ' ' + name, '')


class ReferenceParameter(Parameter):
    def __init__(self, name, type=None):
        type = type if type else 'int'
        _Node.__init__(self, name, type + '& ' + name, '')


class PointerParameter(Parameter):
    def __init__(self, name, type=None):
        type = type if type else 'int'
        _Node.__init__(self, name, type + '* ' + name, '')


class ArrayVariable(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'int ' + name + '[20]', ';\n')


class PointerArrayVariable(_Node):
    def __init__(self, name):
        _Node.__init__(self, name, 'int* ' + name + '[20]', ';\n')


class PointerVariable(Variable):
    def __init__(self, name):
        Variable.__init__(self, name, 'int*', 0)


class SmartPointerVariable(Variable):
    def __init__(self, name):
        Variable.__init__(self, name, 'std::unique_ptr<int>')
        self.require_include_statement('memory')


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
