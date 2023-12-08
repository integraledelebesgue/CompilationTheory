from typing import Optional, Literal, Any
from syntax_tree.structure.observers.display import display_method
from syntax_tree.structure.observers.typecheck import typecheck_method, dispatch_method
from dataclasses import dataclass
import dataclasses
from itertools import count


class ObservableNode(type):
    def __new__(
            cls, 
            name, 
            bases, 
            dct, *, 
            display: Optional[dict[Literal['inline', 'simple', 'recursive'], list[str]]] = None, 
            typecheck: Optional[dict[Literal['source', 'sink'], list[str]]] = None,
            dispatch: Optional[dict[str, str | dict[tuple[str, ...], str]]] = None,
            defines: Optional[dict[Literal['scope', 'symbol', 'self'], bool]] = None
    ):
        if display is not None: 
            ObservableNode.setup_display(dct, display)

        if dispatch is not None:
            ObservableNode.setup_dispatch(dct, dispatch)
        
        if typecheck is not None:
            ObservableNode.setup_typecheck(dct, typecheck)

        ObservableNode.setup_scope(dct, defines or dict())

        return super().__new__(cls, name, bases, dct)
    
    @staticmethod
    def setup_display(dct, params: dict[Literal['inline', 'simple', 'recursive'], list[str]]) -> None:
        inline = params.get('inline', [])
        simple = params.get('simple', [])
        recursive = params.get('recursive', [])

        dct['display'] = display_method(inline, simple, recursive)
        
        dct['display_fields'] = {
            'inline': inline,
            'simple': simple,
            'recursive': recursive
        }

    @staticmethod
    def setup_dispatch(dct, params: dict[str, str | dict[tuple[str, ...], str]]) -> None:
        key = params['key']         # intentional throws
        table = params['table']     #

        dct['dispatch'] = dispatch_method(key, table)

    @staticmethod
    def setup_typecheck(dct, params: dict[Literal['source', 'sink'], list[str]]):
        source = params.get('source', [])
        sink = params.get('sink', [])

        dct['checked'] = False

        dct['check_types'] = typecheck_method(source, sink)

        dct['typed_fields'] = {
            'source': source,
            'sink': sink
        }

    @staticmethod
    def setup_scope(dct, params: dict[str, Any]) -> None:
        dct['defines_scope'] = params.get('scope', False)

        if dct['defines_scope']:
            dct['scope'] = None  # placeholder
        
        dct['defines_symbol'] = params.get('symbol', False)

        dct['defines_self'] = params.get('self', False)

