import ply.lex as lex

from erd_python.models import Attribute, CARDINALITIES, Entity, Relationship, Cardinality

# List of token names.   This is always required
tokens = (
  'ENTITY',
  'COMMENT',
  'NEWLINE',
  'RELATIONSHIP',
  'ATTRIBUTE'
)

# Regular expression rules for simple tokens
def t_ENTITY(t):
    r'\[[`\'"]?(.*?)[`\'"]?\]'
    t.value = lexer.lexmatch.group(2) # get the value between the [] and any quotes
    entity = Entity(t.value)
    t.lexer.current_entity = entity
    t.value = entity
    return t

def t_RELATIONSHIP(t):
    # r'[`\'"]?(.*?)[`\'"]?\s([1\*\?\+])--([1\*\?\+])\s[`\'"]?([^`\n]+)[`\'"]?'
    r'[`\'"]?(.*?)(?::(\w+))?[`\'"]?\s+([1\*\?\+])--([1\*\?\+])\s+[`\'"]?([^`:\n]+)[`\'"]?(?::(\w+))?'
    t.value = Relationship(
        entity1=Entity(lexer.lexmatch.group(4)),
        entity2=Entity(lexer.lexmatch.group(8)),
        attr1=Attribute(lexer.lexmatch.group(5)),
        attr2=Attribute(lexer.lexmatch.group(9)),
        card1=Cardinality(lexer.lexmatch.group(6)),
        card2=Cardinality(lexer.lexmatch.group(7))
    )
    return t

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs). t_ignore is a special rule
t_ignore  = ' \t'

def t_ATTRIBUTE(t):
    r'[^\n]+'
    name = t.value.replace('"', '').replace("'", '').replace('`', '')
    attr = Attribute(name, t.lexer.current_entity)
    t.lexer.current_entity.attributes[attr.name] = attr
    # print(t.lexer.current_entity.name, attr.name)
    t.value = attr
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def parse(data):
    lexer.input(data)
    parsed_objects = {
        'entities': [],
        'relationships': []
    }
    for token in lexer:
        # print(token)
        if token.type == 'ENTITY':
            parsed_objects['entities'].append(token.value)
        elif token.type == 'RELATIONSHIP':
            parsed_objects['relationships'].append(token.value)

    return parsed_objects
