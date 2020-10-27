from enum import Enum, auto

from .templates import ATTRIBUTE_TAGS, ENTITY, FONT_TAGS

CARDINALITIES = r'1\*\+\?'


class Cardinality(Enum):
    ONE = '1'
    ZERO_PLUS = '*'
    ONE_PLUS = '+'
    ZERO_ONE = '?'


CARDINALITY_MAP = {
    Cardinality.ONE: '1',
    Cardinality.ONE_PLUS: '1..*',
    Cardinality.ZERO_ONE: '0..1',
    Cardinality.ZERO_PLUS: '0..*'
}


class SPECIAL(Enum):
    PRIMARY_KEY = '*'
    FOREIGN_KEY = '+'


class Attribute():
    def __init__(self, name: str, entity: 'Entity'=None):
        self.name = name
        for char in SPECIAL:
            self.name = self.name.replace(char.value, '')
        self.entity = entity
        self.is_primary_key = name.startswith(SPECIAL.PRIMARY_KEY.value)
        self.is_foreign_key = name.startswith(SPECIAL.FOREIGN_KEY.value)

    def __repr__(self):
        return f'<Attribute: {self.entity.name}.{self.name}>'

    def to_dot(self):
        base = ATTRIBUTE_TAGS.format(
            ' ALIGN="LEFT"', self.name, '{key_opening}{name}{key_closing}')
        return base.format(
            key_opening='<u>' if self.is_primary_key else '',
            key_closing='</u>' if self.is_primary_key else '',
            name=FONT_TAGS.format(self.name)
        )


class Entity():
    def __init__(self, name: str, attributes: Attribute=None, hoptions={}, eoptions={}):
        self.name = name
        self.attributes = attributes or {}
        self.hoptions = hoptions
        self.eoptions = eoptions

    def __repr__(self):
        return f'<Entity: {self.name}>'

    @property
    def header_dot(self):
        return ATTRIBUTE_TAGS.format('', self.name, f'<B><FONT POINT-SIZE="16">{self.name}</FONT></B>')

    def to_dot(self):
        attrs = ''.join(attr.to_dot()
                             for attr in self.attributes.values())
        return ENTITY.format(self.name, self.header_dot, attrs)


class Relationship():
    def __init__(self, entity1: Entity, entity2: Entity, attr1: Attribute = None, attr2: Attribute = None, card1: Cardinality = None, card2: Cardinality = None, roptions={}):
        self.entity1 = entity1
        self.entity2 = entity2
        self.attr1 = attr1
        self.attr2 = attr2
        self.card1 = card1
        self.card2 = card2
        self.roptions = roptions

    def __repr__(self):
        return f'<Relationship: {self.entity1} {self.card1}--{self.card2} {self.entity2}>'

    def to_dot(self):
        labels = []
        label_str = ''
        port1 = ''
        port2 = ''
        if self.card1:
            labels.append(f'headlabel="{CARDINALITY_MAP[self.card1]}"')
        if self.card2:
            labels.append(f'taillabel="{CARDINALITY_MAP[self.card2]}"')
        if self.card1 or self.card2:
            label_str = ' [{}]'.format(', '.join(labels))

        if self.attr1:
            port1 = f':"{self.attr1.name}"'
        if self.attr2:
            port2 = f':"{self.attr2.name}"'

        return f'"{self.entity1.name}"{port1} -- "{self.entity2.name}"{port2}{label_str}'
        # "Person" -> "Hand"  [headlabel="*", taillabel="1"]
