# -*- coding: utf-8 -*-
"""
Calculations provided by aiida_diff.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData
from aiida.common.datastructures import CalcInfo, CodeInfo
from aiida.common.folders import Folder
from aiida.plugins import DataFactory
from aiida import orm

DiffParameters = DataFactory('vmc_mov1')


class DiffCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the diff executable.

    Simple AiiDA plugin wrapper for 'diffing' two files.
    """
    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super().define(spec)

        # set default values for AiiDA options
        spec.inputs['metadata']['options']['resources'].default = {
            'num_machines': 1,
            'num_mpiprocs_per_machine': 1,
        }
        spec.inputs['metadata']['options']['parser_name'].default = 'vmc_mov1'
        spec.inputs['metadata']['options']['input_filename'].default = 'vmc.inp'
        spec.inputs['metadata']['options']['output_filename'].default = 'vmc.out'

        # new ports
        spec.input('metadata.options.output_filename', valid_type=str, default='vmc.out')
        spec.input('parameters', valid_type=DiffParameters, help='Command line parameters for diff')
        spec.input('file1', valid_type=SinglefileData, help='First file to be compared.')
        spec.output('vmc_mov1', valid_type=SinglefileData, help='diff between file1 and file2.')
        # spec.input('vmc_mov1', valid_type=orm.Code, help='The code being run')

        spec.exit_code(300, 'ERROR_MISSING_OUTPUT_FILES', message='Calculation did not produce all expected output files.')


    def prepare_for_submission(self, folder: Folder) -> CalcInfo:
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files
            needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        codeinfo = datastructures.CodeInfo()
        codeinfo.cmdline_params = self.inputs.parameters.cmdline_params(
            file1_name=self.inputs.file1.filename)
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdin_name = self.options.input_filename
        codeinfo.stdout_name = self.options.output_filename        
        # codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = [
            (self.inputs.file1.uuid, self.inputs.file1.filename, self.inputs.file1.filename),
        ]
        calcinfo.retrieve_list = [self.options.output_filename]
        print ("retrieve list ", calcinfo.retrieve_list)
        print ("calc info", calcinfo)
        return calcinfo
