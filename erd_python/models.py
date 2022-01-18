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
        if self.entity:
            return f'<Attribute: {self.entity.name}.{self.name}>'
        else:
            return f'<Attribute: {self.name}>'

    def to_dot(self):
        base = ATTRIBUTE_TAGS.format(
            ' ALIGN="LEFT"', self.name, '{key_opening}{name}{key_closing}')
        key_opening = ''
        key_closing = ''
        if self.is_primary_key:
            key_opening = '<u>'
            key_closing=' (PK)</u>' 
        elif self.is_foreign_key:
            key_closing=' (FK)'
        return base.format(key_opening=key_opening, name=FONT_TAGS.format(self.name), key_closing=key_closing)


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
        if self.attr1 and self.attr2:
            return f'<Relationship: {self.entity1}:{self.attr1} {self.card1}--{self.card2} {self.entity2}:{self.attr2}>'
        else:
            return f'<Relationship: {self.entity1} {self.card1}--{self.card2} {self.entity2}>'

    def to_dot(self, flip=False):
        labels = []
        label_str = ''
        port1 = ''
        port2 = ''
        card1 = self.card2 if flip else self.card1
        card2 = self.card1 if flip else self.card2
        if card1:
            labels.append(f'headlabel="{CARDINALITY_MAP[card1]}"')
        if card2 and not flip:
            labels.append(f'taillabel="{CARDINALITY_MAP[card2]}"')
        if card1 or card2:
            label_str = ' [{}]'.format(', '.join(labels))

        attr1 = self.attr2 if flip else self.attr1
        attr2 = self.attr1 if flip else self.attr2
        if attr1:
            port1 = f':"{attr1.name}"'
        if attr2:
            port2 = f':"{attr2.name}"'

        entity1 = self.entity2 if flip else self.entity1
        entity2 = self.entity1 if flip else self.entity2
        return f'"{entity1.name}"{port1} -- "{entity2.name}"{port2}{label_str}'
        # "Person" -> "Hand"  [headlabel="*", taillabel="1"]
