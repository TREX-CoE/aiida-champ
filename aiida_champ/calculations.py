# -*- coding: utf-8 -*-
"""
Calculations provided by aiida_champ.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData, Float



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
        # spec.input('pooldir', valid_type=RemoteData, required=False,
            # help='An optional pool directory containing the frequently used files to be used in the calculation.')
        spec.input('trexio', valid_type=SinglefileData, required=False, help='Input trexio hdf5 file')
        spec.input('molecule', valid_type=SinglefileData, required=True, help='Molecule structure File')
        spec.input('ecp1', valid_type=SinglefileData, required=False, help='Input ECP file for atom type 1')
        spec.input('ecp2', valid_type=SinglefileData, required=False, help='Input ECP file for atom type 2')
        spec.input('orbitals', valid_type=SinglefileData, required=False, help='Input orbitals file')
        spec.input('determinants', valid_type=SinglefileData, required=True, help='Input determinants file')
        spec.input('symmetry', valid_type=SinglefileData, required=False, help='Input symmetry file')
        spec.input('jastrow', valid_type=SinglefileData, required=False, help='Input jastrow file')
        spec.input('jastrowder', valid_type=SinglefileData, required=False, help='Input jastrowder file')
        spec.input('numericalbasis1', valid_type=SinglefileData, required=False, help='Input numerical basis file atom 1')
        spec.input('numericalbasis2', valid_type=SinglefileData, required=False, help='Input numerical basis file atom 2')
        spec.input('numericalbasisinfo', valid_type=SinglefileData, required=False, help='Input numerical basis information file')

        # new output ports
        spec.output('Output', valid_type=SinglefileData, help='Output file of the VMC/DMC calculation')
        spec.output('Energy', valid_type=Float, required=False, help='Output total energy of the VMC/DMC calculation')

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
            (self.inputs.molecule.uuid, self.inputs.molecule.filename, self.inputs.molecule.filename),
            (self.inputs.ecp1.uuid, self.inputs.ecp1.filename, self.inputs.ecp1.filename),
            (self.inputs.ecp2.uuid, self.inputs.ecp2.filename, self.inputs.ecp2.filename),
            (self.inputs.orbitals.uuid, self.inputs.orbitals.filename, self.inputs.orbitals.filename),
            (self.inputs.determinants.uuid, self.inputs.determinants.filename, self.inputs.determinants.filename),
            (self.inputs.symmetry.uuid, self.inputs.symmetry.filename, self.inputs.symmetry.filename),
            (self.inputs.jastrow.uuid, self.inputs.jastrow.filename, self.inputs.jastrow.filename),
            (self.inputs.jastrowder.uuid, self.inputs.jastrowder.filename, self.inputs.jastrowder.filename),
            (self.inputs.numericalbasisinfo.uuid, self.inputs.numericalbasisinfo.filename, self.inputs.numericalbasisinfo.filename),
            (self.inputs.numericalbasis1.uuid, self.inputs.numericalbasis1.filename, self.inputs.numericalbasis1.filename),
            (self.inputs.numericalbasis2.uuid, self.inputs.numericalbasis2.filename, self.inputs.numericalbasis2.filename),
        ]

        if 'trexio' in self.inputs:
            calcinfo.local_copy_list.append(self.inputs.trexio.uuid, self.inputs.trexio.filename, self.inputs.trexio.filename)

        # if 'pooldir' in self.inputs:
        #     calcinfo.local_copy_list.append(self.inputs.pooldir.uuid, self.inputs.pooldir.filename, self.inputs.pooldir.filename)

        calcinfo.retrieve_list = [self.metadata.options.output_filename]

        return calcinfo
