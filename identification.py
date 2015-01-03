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


def is_class(node):
    return clang.cindex.CursorKind.CLASS_DECL == node.kind


def is_interface_class(node):
    for method in [c for c in node.get_children() if is_method(c)]:
        if method.is_pure_virtual_method():
            return True
    return False


def is_function(node):
    return clang.cindex.CursorKind.FUNCTION_DECL == node.kind


def is_member(node):
    return clang.cindex.CursorKind.FIELD_DECL == node.kind


def is_method(node):
    return clang.cindex.CursorKind.CXX_METHOD == node.kind


def is_namespace(node):
    return clang.cindex.CursorKind.NAMESPACE == node.kind


def is_struct(node):
    return clang.cindex.CursorKind.STRUCT_DECL == node.kind


def is_variable(node):
    return clang.cindex.CursorKind.VAR_DECL == node.kind


def is_reference(node):
    return clang.cindex.TypeKind.LVALUEREFERENCE == node.type.kind


def is_pointer(node):
    return clang.cindex.TypeKind.POINTER == node.type.kind


def is_array(node):
    type = node.type.kind
    return (type == clang.cindex.TypeKind.CONSTANTARRAY or
            type == clang.cindex.TypeKind.INCOMPLETEARRAY or
            type == clang.cindex.TypeKind.VARIABLEARRAY or
            type == clang.cindex.TypeKind.DEPENDENTSIZEDARRAY)
