# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_champ.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
from aiida.common import exceptions
from aiida.orm import SinglefileData, Float

CHAMPCalculation = CalculationFactory('CHAMP')


class CHAMPParser(Parser):
    """
    Parser class for parsing output of calculation.
    """
    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a CHAMPCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.ProcessNode`
        """
        super().__init__(node)
        if not issubclass(node.process_class, CHAMPCalculation):
            raise exceptions.ParsingError('Can only parse CHAMPCalculation')

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """

        output_filename = self.node.get_option('output_filename')

        # Check that folder content is as expected
        files_retrieved = self.retrieved.list_object_names()
        files_expected = [output_filename]

        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error("Found files '{}', expected to find '{}'".format(
                files_retrieved, files_expected))
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # add output file
        self.logger.info("Parsing '{}'".format(output_filename))
        with self.retrieved.open(output_filename, 'rb') as handle:
            output_node = SinglefileData(file=handle)
            energy = Float()

            outputfile = handle.readlines()
            for line in outputfile:
                if 'total E =' in line:
                    token = line.split()
                    energy = Float(float(token[3]))
                    print ("energy parsed from the output = {}".format(energy))
            self.out('Energy', energy)

        self.out('Output', output_node)

        return ExitCode(0)
