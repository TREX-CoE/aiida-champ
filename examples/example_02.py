#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run a test calculation involving a trexio file on localhost.

Usage: python example_02.py
"""
from os import path
import click
from aiida import cmdline, engine
from aiida.plugins import DataFactory, CalculationFactory
from aiida_champ import helpers

INPUT_DIR = path.join(path.dirname(path.realpath(__file__)), 'example02')
POOL_DIR = path.join(path.dirname(path.realpath(__file__)), 'example02/pool')


def test_run(champ_code):
    """Run a test calculation on the localhost computer.

    Uses test helpers to create AiiDA Code on the fly.
    """
    if not champ_code:
        # get code
        computer = helpers.get_computer()
        champ_code = helpers.get_code(entry_point='CHAMP', computer=computer)


    SinglefileData = DataFactory('singlefile')
    FolderData = DataFactory('folder')

    filemain = SinglefileData(file=path.join(INPUT_DIR, 'vmc_optimization_500_hdf5.inp'))
    pooldir = FolderData(tree=POOL_DIR)

    trexio = SinglefileData(file=path.join(INPUT_DIR, 'gamess_butadiene.hdf5'))
    orbitals = SinglefileData(file=path.join(INPUT_DIR, 'TZ_1M_15k.orb'))
    determinants = SinglefileData(file=path.join(INPUT_DIR, 'TZ_1M_500.det'))
    symmetry = SinglefileData(file=path.join(INPUT_DIR, 'cas1010.sym'))
    jastrow = SinglefileData(file=path.join(INPUT_DIR, 'jastrow_good_b3lyp.0'))
    jastrowder = SinglefileData(file=path.join(INPUT_DIR, 'jastrow.der'))


    # set up calculation
    inputs = {
        'code': champ_code,
        'filemain': filemain,
        'pooldir': pooldir,
        'trexio': trexio,
        'orbitals': orbitals,
        'determinants': determinants,
        'symmetry': symmetry,
        'jastrow': jastrow,
        'jastrowder': jastrowder,
        'metadata': {
            'description': 'Sample job submission with the aiida_champ plugin example 02',
        },
    }

    # Note: in order to submit your calculation to the aiida daemon, do:
    result = engine.run(CalculationFactory('CHAMP'), **inputs)
    computed_output = result['Output'].get_content()
    print('Outout of the Calculation: \n{}'.format(computed_output))


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.

    Example usage: $ python example_02.py --code CHAMP@localhost

    Alternative (creates CHAMP@localhost-test code): $ python example_01.py

    Help: $ python example_02.py --help
    """
    test_run(code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
