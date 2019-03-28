""" Tests for calculations

"""
from __future__ import print_function
from __future__ import absolute_import

from aiida.manage.fixtures import PluginTestCase


class TestDataCli(PluginTestCase):
    def setUp(self):
        from click.testing import CliRunner
        from aiida.plugins import DataFactory

        DiffParameters = DataFactory('diff')
        self.parameters = DiffParameters({'ignore-case': True})
        self.parameters.store()
        self.runner = CliRunner()

    def test_data_diff_list(self):
        """Test whether 'verdi data diff list' can be reached"""
        from aiida_diff.cli import list_

        self.runner.invoke(list_, catch_exceptions=False)

    def test_data_diff_export(self):
        """Test whether 'verdi data diff export' can be reached"""
        from aiida_diff.cli import export

        self.runner.invoke(
            export, [str(self.parameters.pk)], catch_exceptions=False)
