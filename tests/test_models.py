#!/usr/bin/env python

"""Tests for generator.py"""


import unittest

from erd.models import Attribute, Cardinality, Entity, Relationship

class TestModels(unittest.TestCase):
    """Tests for models module."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def test_relationship_to_dot_renders_cardinalities(self):
        a = Entity('a')
        b = Entity('b')
        rel = Relationship(entity1=a, entity2=b, card1=Cardinality.ONE, card2=Cardinality.ONE_PLUS)
        dot = rel.to_dot()
        self.assertIn('[headlabel="1", taillabel="1..*"]', dot)

        rel = Relationship(entity1=a, entity2=b, card1=Cardinality.ZERO_PLUS, card2=Cardinality.ZERO_ONE)
        dot = rel.to_dot()
        self.assertIn('[headlabel="0..*", taillabel="0..1"]', dot)

    def test_attribute_removes_leading_special_characters(self):
        e = Entity('e')
        attr = Attribute('*primary_id', e)
        self.assertEqual('primary_id', attr.name)

        attr = Attribute('+foreign_id', e)
        self.assertEqual('foreign_id', attr.name)

    def test_attribute_to_dot_renders_ports(self):
        e = Entity('e')
        attr = Attribute('+foreign_id', e)

        dot = attr.to_dot()

        self.assertIn('PORT="foreign_id"><FONT>foreign_id</FONT> (FK)</TD>', dot)

    def test_relationship_handles_empty_cardinality(self):

        a = Entity('a')
        b = Entity('b')
        rel = Relationship(entity1=a, entity2=b, card1=None, card2=None)
        
        dot = rel.to_dot()

        self.assertNotIn('headlabel', dot)
        self.assertNotIn('taillabel', dot)

    def test_relationship_to_dot_renders_ports(self):
        a = Entity('a')
        b = Entity('b')
        attra = Attribute('fk_b_id', a)
        attrb = Attribute('pk_b_id', b)
        rel = Relationship(entity1=a, entity2=b, attr1=attra, attr2=attrb)

        dot = rel.to_dot()

        self.assertIn('"a":"fk_b_id"', dot)
        self.assertIn('"b":"pk_b_id"', dot)
