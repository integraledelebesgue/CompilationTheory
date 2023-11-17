from typing import Optional
from syntax_tree.structure.observers.display import display_method


class ObservableNode(type):
    def __new__(cls, name, bases, dct, *, inline: Optional[list[str]] = None, simple: Optional[list[str]] = None, recursive: Optional[list[str]] = None):
        inline = inline or []
        simple = simple or []
        recursive = recursive or []

        dct['display'] = display_method(inline, simple, recursive)
        
        dct['display_fields'] = {
            'inline': inline,
            'simple': simple,
            'recursive': recursive
        }
        
        return super().__new__(cls, name, bases, dct)
