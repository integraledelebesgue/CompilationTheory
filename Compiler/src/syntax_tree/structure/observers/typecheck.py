from typing import Callable, Optional
from semantics.types import nothing, Type

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
        child = obj.__getattribute__(name)
        child.type = type

        if hasattr(child, 'typing_hook'):
            child.typing_hook()


def typecheck_method(source: list[str], sink: list[str], decapsulate: bool) -> Callable[['Node'], None]:
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
            type = type[0] or nothing
        
        if len(sink) > 0:
            assign_to_children(obj, sink, type.element_type if decapsulate else type)

        if hasattr(obj, 'type'):
            obj.type = type

        if hasattr(obj, 'typing_hook'):
            obj.typing_hook()

        obj.checked = True

    return check_types


def dispatch_method(key: str, type_table: dict[tuple[Type, ...], Type]) -> Callable[['Node'], Type]:
    def dispatch(obj: 'Node', types: list[Type]) -> Optional[str]:
        variants = type_table[obj.__getattribute__(key)]

        print(f'Dispatching {obj}({types})')
        
        if types in variants:
            return variants[types]

        raise RuntimeError(f'No dispatch available for {obj} & {types}')

    return dispatch
