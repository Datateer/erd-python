"""Main module."""

from enum import Enum, auto

from .parser import parse

# def parse(filepath: str):
#     with open('tests/erds/one.er') as f:
#         lxer.input(f.read())

#         for tok in parser:
#             print(tok)



class Option(Enum):
    LABEL = 'label'
    BG_COLOR = 'bgcolor'
    COLOR = 'color'
    FONT_FACE = 'font'
    FONT_SIZE = 'size'
    BORDER = 'border'
    BORDER_COLOR = 'border-color'
    CELL_SPACING = 'cellspacing'
    CELL_BORDER = 'cellborder'
    CELL_PADDING = 'cellpadding'
    TEXT_ALIGNMENT = 'text-alignment'



DEFAULT_TITLE_OPTIONS = [(Option.FONT_SIZE, 30)]
DEFAULT_HEADER_OPTIONS = [(Option.FONT_SIZE, 16)]
DEFAULT_ENTITY_OPTIONS = [
    (Option.BORDER, 0),
    (Option.CELL_BORDER, 1),
    (Option.CELL_SPACING, 0),
    (Option.CELL_PADDING, 4),
    (Option.FONT_FACE, 'Helvetica')
]