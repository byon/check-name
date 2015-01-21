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

from clang.cindex import CursorKind, StorageClass, TypeKind
import re


def is_class(node):
    return (CursorKind.CLASS_DECL == node.kind or
            CursorKind.CLASS_TEMPLATE == node.kind)


def is_interface_class(node):
    methods = _list_methods(node)
    if not methods:
        return False
    return all(m.is_pure_virtual_method() for m in methods)


def is_abstract_class(node):
    methods = _list_methods(node)
    if not methods:
        return False
    return (any(m.is_pure_virtual_method() for m in methods) and
            any(not m.is_pure_virtual_method() for m in methods))


def is_function(node):
    return CursorKind.FUNCTION_DECL == node.kind


def is_static(node):
    return node.storage_class == StorageClass.STATIC


def is_member(node):
    return CursorKind.FIELD_DECL == node.kind


def is_global(node):
    parent = node.lexical_parent.kind
    return (parent == CursorKind.NAMESPACE or
            parent == CursorKind.TRANSLATION_UNIT)


def is_method(node):
    return CursorKind.CXX_METHOD == node.kind


def is_namespace(node):
    return CursorKind.NAMESPACE == node.kind


def is_struct(node):
    return CursorKind.STRUCT_DECL == node.kind


def is_any_kind_of_variable(node):
    return is_member(node) or is_variable(node) or is_parameter(node)


def is_variable(node):
    return CursorKind.VAR_DECL == node.kind


def is_parameter(node):
    return CursorKind.PARM_DECL == node.kind


def is_reference(node):
    return TypeKind.LVALUEREFERENCE == node.type.kind


def is_typedef_declaration(type):
    return type.kind == CursorKind.TYPEDEF_DECL


def is_pointer(node):
    return (is_pure_pointer(node) or is_smart_pointer(node)
            or is_array_pointer(node))


def is_pure_pointer(node):
    return (TypeKind.POINTER == node.type.kind or
            TypeKind.MEMBERPOINTER == node.type.kind)


def is_smart_pointer(node):
    if not _is_type_possibly_smart_array_or_pointer(node.type):
        return False
    return is_name_for_smart_pointer(node.type.get_canonical().spelling)


def is_name_for_smart_pointer(name):
    if re.compile(r'^(std|boost)::([a-z]+_)ptr').search(name):
        return True
    return False


def is_array_pointer(node):
    array_type = node.type.get_array_element_type()
    return array_type.get_pointee().kind is not TypeKind.INVALID


def is_array(node):
    return is_pure_array(node) or is_smart_array(node)


def is_pure_array(node):
    type = node.type.kind
    return (type == TypeKind.CONSTANTARRAY or
            type == TypeKind.INCOMPLETEARRAY or
            type == TypeKind.VARIABLEARRAY or
            type == TypeKind.DEPENDENTSIZEDARRAY)


def is_smart_array(node):
    if not _is_type_possibly_smart_array_or_pointer(node.type):
        return False
    return is_name_for_smart_array(node.type.get_canonical().spelling)


def is_name_for_smart_array(name):
    if re.compile(r'^boost::([a-z]+_)array').search(name):
        return True
    return False


def _is_type_possibly_smart_array_or_pointer(type):
    return (type.kind == TypeKind.UNEXPOSED or type.kind == TypeKind.TYPEDEF)


def _list_methods(node):
    return [c for c in node.get_children() if is_method(c)]
