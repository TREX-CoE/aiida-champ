# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_champ.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
from aiida.common import exceptions
from aiida.orm import SinglefileData, Float, RemoteData, load_code, load_computer

DiffCalculation = CalculationFactory('vmc_mov1')


class DiffParser(Parser):
    """
    Parser class for parsing output of calculation.
    """
    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a DiffCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.ProcessNode`
        """
        super().__init__(node)
        if not issubclass(node.process_class, DiffCalculation):
            raise exceptions.ParsingError('Can only parse CHAMPCalculation')

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        output_folder = self.retrieved
        output_filename = self.node.get_option('output_filename')
        print ("output filename from parser", output_filename)

        # Check that folder content is as expected
        files_retrieved = self.retrieved.list_object_names()
        files_expected = [output_filename]
        print ("files retrieved ", files_retrieved)
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error("Found files '{}', expected to find '{}'".format(
                files_retrieved, files_expected))
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # add output file
        self.logger.info("Parsing '{}'".format(output_filename))
        with self.retrieved.open(output_filename, 'r') as handle:
            output_node = SinglefileData(file=handle)
            total_energy_found = False

            for line in handle:
                if 'total E =' in line:
                    energy = Float(float(line.split()[3]))
                    total_energy_found = True

            self.out('output_energy', energy)



        self.out('vmc_mov1', output_node)

        return ExitCode(0)
