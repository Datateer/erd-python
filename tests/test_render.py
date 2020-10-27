#!/usr/bin/env python

"""Tests for generator.py"""


import unittest

from erd.render import render
from erd.models import Attribute, Cardinality, Entity, Relationship

class TestGenerator(unittest.TestCase):
    """Tests for generator module."""

    def setUp(self):
        """Set up test fixtures, if any."""
        arthur = Entity('King Arthur')
        bedevere = Entity('Sir Bedevere')
        lancelot = Entity('Sir Lancelot')
        attr_arthur_pk = Attribute('attr_arthur_pk', arthur)
        attr_arthur_fk_bedevere = Attribute('attr_arthur_fk_bedevere', arthur)
        attr_arthur_fk_lancelot = Attribute('attr_arthur_fk_lancelot', arthur)
        attr_bedevere_pk = Attribute('attr_bedevere_pk', bedevere)
        attr_lancelot_pk = Attribute('attr_lancelot_pk', lancelot)
        arthur.attributes = {
            'attr_arthur_pk': attr_arthur_pk,
            'attr_arthur_fk_bedevere': attr_arthur_fk_bedevere,
            'attr_arthur_fk_lancelot': attr_arthur_fk_lancelot,
        }
        bedevere.attributes = {
            'attr_bedevere_pk': attr_bedevere_pk,
            'attr1': Attribute('attr1', bedevere),
            'attr2': Attribute('attr2', bedevere),
            'attr3': Attribute('attr3', bedevere)
        }
        lancelot.attributes = {
            'attr_lancelot_pk': attr_lancelot_pk,
            'attr1': Attribute('attr1', lancelot),
            'attr2': Attribute('attr2', lancelot),
            'attr3': Attribute('attr3', lancelot)
        }
        self.objects = {
            'entities': [
                arthur,
                bedevere,
                lancelot
            ],
            'relationships': [
                Relationship(arthur, bedevere, attr1=attr_arthur_fk_bedevere, attr2=attr_bedevere_pk, card1=Cardinality.ONE, card2=Cardinality.ZERO_PLUS),
                Relationship(arthur, lancelot, attr1=attr_arthur_fk_lancelot, attr2=attr_lancelot_pk, card1=Cardinality.ONE, card2=Cardinality.ZERO_PLUS)
            ]
        }

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_render_returns_output_path_if_provided(self):
        expected_path = 'test-output/tester.dot'
        
        actual_path = render(self.objects, output_path=expected_path, format='dot')

        self.assertEqual(actual_path, expected_path)

    def test_render_returns_string_output(self):
        expected_contents = ['"King Arthur":"attr_arthur_fk_bedevere" -- "Sir Bedevere":"attr_bedevere_pk"', '"King Arthur":"attr_arthur_fk_lancelot" -- "Sir Lancelot":"attr_lancelot_pk"', 'graph {']

        output = render(self.objects)
        for expected in expected_contents:
            self.assertIn(expected, output)



        