# -*- coding: utf-8 -*-
"""
Calculations provided by aiida_champ.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData, Float, FolderData
import os


class CHAMPCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the CHAMP's vmc executable.

    aiida-champ can be used to manage the workflow of a vmc/dmc calculation of the CHAMP code.

    Author :: Ravindra Shinde
    Email  :: r.l.shinde@utwente.nl

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
        spec.inputs['metadata']['options']['parser_name'].default = 'CHAMP'

        # new input ports
        spec.input('metadata.options.output_filename', valid_type=str, default='vmc.out')
        spec.input('filemain', valid_type=SinglefileData, required=True, help='Input File')
        spec.input('pooldir', valid_type=FolderData, required=False,
            help='An optional pool directory containing the frequently used files to be used in the calculation.')
        spec.input('trexio', valid_type=SinglefileData, required=False, help='Input trexio hdf5 file')
        spec.input('orbitals', valid_type=SinglefileData, required=False, help='Input orbitals file')
        spec.input('determinants', valid_type=SinglefileData, required=True, help='Input determinants file')
        spec.input('symmetry', valid_type=SinglefileData, required=False, help='Input symmetry file')
        spec.input('jastrow', valid_type=SinglefileData, required=False, help='Input jastrow file')
        spec.input('jastrowder', valid_type=SinglefileData, required=False, help='Input jastrowder file')

        # new output ports
        spec.output('Output', valid_type=SinglefileData, help='Output file of the VMC/DMC calculation')
        spec.output('Energy', valid_type=Float, required=False, help='Output total energy of the VMC/DMC calculation')
        spec.output('Restart', valid_type=SinglefileData, help='Restart file of the VMC/DMC calculation')
        spec.output('ParserLog', valid_type=SinglefileData, help='Parser log file of the VMC/DMC calculation')
        spec.exit_code(300, 'ERROR_MISSING_OUTPUT_FILES', message='Calculation did not produce all expected output files.')


    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files
            needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        codeinfo = datastructures.CodeInfo()
        # codeinfo.cmdline_params = ['-i', self.inputs.file1.filename, '-o', self.inputs.file2.filename]
        codeinfo.cmdline_params = ['-i', self.inputs.filemain.filename, '-o', self.metadata.options.output_filename]
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = [
            (self.inputs.filemain.uuid, self.inputs.filemain.filename, self.inputs.filemain.filename),
            (self.inputs.orbitals.uuid, self.inputs.orbitals.filename, self.inputs.orbitals.filename),
            (self.inputs.determinants.uuid, self.inputs.determinants.filename, self.inputs.determinants.filename),
            (self.inputs.symmetry.uuid, self.inputs.symmetry.filename, self.inputs.symmetry.filename),
            (self.inputs.jastrow.uuid, self.inputs.jastrow.filename, self.inputs.jastrow.filename),
            (self.inputs.jastrowder.uuid, self.inputs.jastrowder.filename, self.inputs.jastrowder.filename),
        ]

        if 'trexio' in self.inputs:
            calcinfo.local_copy_list.append((self.inputs.trexio.uuid, self.inputs.trexio.filename, self.inputs.trexio.filename))

        # Copy the pool directory
        if 'pooldir' in self.inputs:
            for filename in self.inputs.pooldir.list_object_names():
                calcinfo.local_copy_list.append((self.inputs.pooldir.uuid, filename,  os.path.join('pool', filename) ))

        calcinfo.retrieve_list = [self.metadata.options.output_filename, 'parser.log', 'restart_vmc']

        return calcinfo
