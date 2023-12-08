from typing import Callable, Optional
from itertools import filterfalse

def unique(collection: list[str]) -> list[str]:
    return list(dict.fromkeys(collection))


def flatten(collection: list[str | list]) -> list[str]:
    result = []

    for element in collection:
        if isinstance(element, list):
            result.extend(flatten(element))
        else:
            result.append(element)

    return result


def get_type(obj: 'Node') -> Callable[[str], str]:
    def inner(name) ->  str:
        field = obj.__getattribute__(name)

        if field is None:
            return None

        if isinstance(field, list):
            for element in field:
                if hasattr(element, 'check_types'):
                    element.check_types()

            return [element.type for element in field]
        
        if hasattr(field, 'check_types'):
            field.check_types()

        return field.type

    return inner


def children_types(obj: 'Node', names: list[str]) -> tuple[str, ...]:
    return tuple(map(
        get_type(obj),
        names
    ))


def assign_to_children(obj: 'Node', names: list[str], type: str) -> None:
    for name in names:
        obj.__getattribute__(name).type = type


def typecheck_method(source: list[str], sink: list[str]) -> Callable[['Node'], None]:
    def check_types(obj: 'Node'):
        nonlocal source, sink

        for ancessor in obj.__class__.__mro__:
            if hasattr(ancessor, 'typed_fields'):
                source.extend(ancessor.typed_fields['source'])
                sink.extend(ancessor.typed_fields['sink'])

        source = unique(source)
        sink = unique(sink)

        if len(source) == 0:  # TODO something more general
            if hasattr(obj, 'typing_hook'):  # Invoke hook anyway to provide more customizable behaviour
                obj.typing_hook()

            return

        type = children_types(obj, source)

        if hasattr(obj, 'dispatch'):
            type = obj.dispatch(type)
        else:  # TODO error if type has length other than 1 here
            type = type[0] or 'nothing'
        
        if len(sink) == 0:
            obj.type = type
        else:
            assign_to_children(obj, sink, type)

        if hasattr(obj, 'typing_hook'):
            obj.typing_hook()

        obj.checked = True

    return check_types


def dispatch_method(key: str, type_table: dict[tuple[str, ...], str]) -> Callable[['Node'], None]:
    def dispatch(obj: 'Node', types: list[str]) -> Optional[str]:
        variants = type_table[obj.__getattribute__(key)]
        
        if types in variants:
            return variants[types]
        
        if 'default' in variants:
            return variants['default']

        return 'any'

    return dispatch
