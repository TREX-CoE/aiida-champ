# -*- coding: utf-8 -*-
"""
Calculations provided by aiida_champ.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""

from aiida.engine import CalcJob
from aiida.orm import SinglefileData, RemoteData
from aiida.common.datastructures import CalcInfo, CodeInfo
from aiida.common.folders import Folder
from aiida.plugins import DataFactory
from aiida import orm
from aiida.orm import Dict, Float, Code, Int, StructureData, load_code

DiffParameters = DataFactory('vmc_mov1')


class DiffCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the CHAMP executables :: vmc and dmc.

    
    """
    # Some default naming
    _INPUT_FILE = 'vmc.inp'
    _OUTPUT_FILE = 'vmc.out'
    _INPUT_COORDS_FILE = 'aiida.coords.xyz'


    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super().define(spec)

        # set default values for AiiDA options
        spec.input('parameters', valid_type=Dict, required=False, help='Command line parameters in the dict form to generate input file')
        spec.input('structure',  valid_type=StructureData, required=False, help='Input Structure file')
        spec.input('settings',   valid_type=Dict, required=False, help='Additional Input Parameters')
        spec.input('metadata.options.computer', valid_type=str, required=True, default='localhost')
        spec.input('code', valid_type=Code, help='The code bing run : CHAMP executables')

        # Input Metadata
        spec.inputs['metadata']['options']['resources'].default = {
            'num_machines': 1,
            'num_mpiprocs_per_machine': 1,
        }
        spec.inputs['metadata']['options']['parser_name'].default = 'vmc_mov1'
        spec.inputs['metadata']['options']['input_filename'].default = 'vmc.inp'
        spec.inputs['metadata']['options']['output_filename'].default = 'vmc.out'

        # new ports
        # spec.input('metadata.options.output_filename', valid_type=str, default='vmc.out')
        # spec.input('parameters', valid_type=DiffParameters, help='Command line parameters for diff')
        # spec.input('file1', valid_type=SinglefileData, help='First file to be compared.')

        # All the output parameters
        spec.output('output_energy', valid_type=Float, required=False, help='The total energy at the end of the calculation')        
        spec.output_node = 'output_energy'

        # spec.output('output_champ', valid_type=RemoteData, help='diff between file1 and file2.')


        spec.exit_code(300, 'ERROR_MISSING_OUTPUT_FILES', message='Calculation did not produce all expected output files.')
        spec.exit_code(400, 'ERROR_MISSING_OUTPUT_FILES', message='Calculation did not produce final energy value. ')        


    def prepare_for_submission(self, folder: Folder) -> CalcInfo:
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files
            needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """



        # Code Information
        codeinfo = CodeInfo()
        codeinfo.cmdline_params = [" -i ", self.metadata.options.input_filename, " -o ", self.metadata.options.output_filename,  " -e ", "error.err"]
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.withmpi = self.inputs.metadata.options.withmpi
        codeinfo.join_files = False

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.cmdline_params = codeinfo.cmdline_params
        calcinfo.codes_info = [codeinfo]

        calcinfo.local_copy_list = []
        #     (self.inputs.metadata.options.input_filename.uuid, self.inputs.metadata.options.input_filename, self.inputs.metadata.options.input_filename),
        #     (self.inputs.metadata.options.output_filename.uuid, self.inputs.metadata.options.output_filename, self.inputs.metadata.options.output_filename),
        # ]
        calcinfo.retrieve_list = [self.metadata.options.output_filename]
        print ("retrieve list ", calcinfo.retrieve_list)
        print ("calc info", calcinfo)
        print ("code info", codeinfo)
        return calcinfo
