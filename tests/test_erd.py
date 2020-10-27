#!/usr/bin/env python

"""Tests for `erd` package."""


import unittest
from click.testing import CliRunner

from erd import erd
from erd import cli


class TestErd(unittest.TestCase):
    """Tests for `erd` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'erd.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    @unittest.skip('not implemented yet')
    def test_input_filename_required(self):
        raise NotImplementedError()

    @unittest.skip('not implemented yet')
    def test_outputfilename_required(self):
        raise NotImplementedError()

    @unittest.skip('not implemented yet')
    def test_errors_if_input_file_not_found(self):
        raise NotImplementedError()

    @unittest.skip('not implemented yet')
    def test_produces_output_file(self):
        raise NotImplementedError()
    
