#!/usr/bin/env python

"""Tests for `erd` package."""


import unittest

from erd_python import parser

class TestErd(unittest.TestCase):
    """Tests for `erd.parser` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.test_file = 'tests/erds/one.er'

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_lexer_parses_objects(self):
        with open(self.test_file) as f:
            parser.lexer.input(f.read())

            tokens = []
            for t in parser.lexer:
                tokens.append((t.type, t.value))

            self.assertEqual(4, len(list(filter(lambda x: x[0] == 'ENTITY', tokens))))
            self.assertEqual(1, len(list(filter(lambda x: x[0] == 'RELATIONSHIP', tokens))))

    def test_parse_returns_objects(self):
        with open(self.test_file) as f:
            data = f.read()
        
        objects = parser.parse(data)

        # print(objects['entities'][0].attributes)
        self.assertEqual(4, len(objects['entities']))
        self.assertEqual(1, len(objects['relationships']))
            
