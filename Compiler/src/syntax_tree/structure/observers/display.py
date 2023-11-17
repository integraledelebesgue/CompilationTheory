from typing import *
from dataclasses import dataclass


vertical_line = '│'
vertical_branch = '├'
vertical_branch_end = '└'
horizontal_line = '──'

branch = vertical_branch + horizontal_line + ' '
branch_end = vertical_branch_end + horizontal_line + ' '


def for_each(func: Callable, final: Optional[Callable], collection: list[str]) -> None:
    match len(collection):
        case 0:
            return
        
        case 1 if final is not None:
            final(collection[0])

        case _ if final is None:
            for element in collection:
                func(element)

        case _ if final is not None:
            for element in collection[:-1]:
                func(element)

            final(collection[-1])


def display_list(collection: list['Node'], prefix: str) -> None:
    prefix_last = prefix
    prefix = prefix.replace(vertical_branch_end, vertical_branch)

    for_each(
        lambda element: element.display(prefix),
        lambda element: element.display(prefix_last),
        collection
    )


def get_and_display(obj: 'Node', prefix: str) -> Callable:
    def call_display(name: str):
        attribute = obj.__getattribute__(name)

        if attribute is None:
            return

        if isinstance(attribute, list):
            display_list(attribute, prefix)
            return
        
        attribute.display(prefix)

    return call_display


def display_recursive_attributes(obj: 'Node', attributes: list[str], prefix: str, prefix_last: str) -> None:
    for_each(
        get_and_display(obj, prefix),
        get_and_display(obj, prefix_last),
        attributes
    )


def display_recursive_attributes_no_end(obj: 'Node', attributes: list[str], prefix: str) -> None:
    for name in attributes:
        attribute = obj.__getattribute__(name)

        if isinstance(attribute, list):
            display_list(attribute, prefix)
            continue
        
        attribute.display(prefix)


def display_simple_attributes_no_end(obj: 'Node', attributes: list[str], prefix: str):
    for name in attributes: 
        print(prefix + f'{name}: {obj.__getattribute__(name)}')


def get_and_print(obj: 'Node', prefix: str) -> Callable:
    def call_print(name: str):
        print(prefix + f'{name}: {obj.__getattribute__(name)}')

    return call_print


def display_simple_attributes(obj: 'Node', attributes: list[str], prefix: str, prefix_last: str) -> None:
    for_each(
        get_and_print(obj, prefix),
        get_and_print(obj, prefix_last),
        attributes
    )


def clean(prefix: str) -> str:
    return prefix\
        .replace(vertical_branch, vertical_line)\
        .replace(vertical_branch_end, ' ')\
        .replace(horizontal_line, '  ')


def next_prefixes(current: str) -> tuple[str, str]:
    clean_prefix = clean(current)

    return (
        clean_prefix + branch, 
        clean_prefix + branch_end
    )


def unique(collection: list[str]) -> list[str]:
    return list(dict.fromkeys(collection))


def inline_postfix(obj: 'Node', attributes: list[str]) -> str:
    if len(attributes) == 0:
        return ''
    
    values = [obj.__getattribute__(name) for name in attributes]

    return '(' + ', '.join(values) + ')'


def display_method(inline: Optional[list[str]], simple: Optional[list[str]], recursive: Optional[list[str]]) -> None:
    def display(obj: 'Node', prefix: str = ''):
        nonlocal inline, simple, recursive

        next_prefix, next_prefix_last = next_prefixes(prefix)

        for ancessor in obj.__class__.__mro__:
            if hasattr(ancessor, 'display_fields'):
                inline.extend(ancessor.display_fields['inline'])
                simple.extend(ancessor.display_fields['simple'])
                recursive.extend(ancessor.display_fields['recursive'])

        inline = unique(inline)
        simple = unique(simple)
        recursive = unique(recursive)

        print(prefix + obj.__class__.__name__ + inline_postfix(obj, inline))

        match (simple, recursive):
            case ([], []):
                pass

            case (_, []):
                display_simple_attributes(obj, simple, next_prefix, next_prefix_last)

            case([], _):
                display_recursive_attributes(obj, recursive, next_prefix, next_prefix_last)

            case (_, _):
                display_simple_attributes_no_end(obj, simple, next_prefix)
                display_recursive_attributes(obj, recursive, next_prefix, next_prefix_last)

    return display
