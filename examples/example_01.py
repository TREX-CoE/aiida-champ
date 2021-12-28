#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run a test calculation on localhost.

Usage: python example_01.py
"""
from os import path
import click
from aiida import cmdline, engine
from aiida.plugins import DataFactory, CalculationFactory
from aiida_champ import helpers

INPUT_DIR = path.join(path.dirname(path.realpath(__file__)), 'example01')
POOL_DIR = path.join(path.dirname(path.realpath(__file__)), 'example01/pool')


def test_run(champ_code):
    """Run a calculation on the localhost computer.

    Uses test helpers to create AiiDA Code on the fly.
    """
    if not champ_code:
        # get code
        computer = helpers.get_computer()
        champ_code = helpers.get_code(entry_point='CHAMP', computer=computer)


    SinglefileData = DataFactory('singlefile')
    FolderData = DataFactory('folder')

    filemain = SinglefileData(file=path.join(INPUT_DIR, 'vmc.inp'))
    pooldir = FolderData(tree=POOL_DIR)

    orbitals = SinglefileData(file=path.join(INPUT_DIR, 'cas44.lcao'))
    determinants = SinglefileData(file=path.join(INPUT_DIR, 'cas44.det'))
    symmetry = SinglefileData(file=path.join(INPUT_DIR, 'cas44.sym'))
    jastrow = SinglefileData(file=path.join(INPUT_DIR, 'jastrow_good_b3lyp.0'))
    jastrowder = SinglefileData(file=path.join(INPUT_DIR, 'jastrow.der'))


    # set up calculation
    inputs = {
        'code': champ_code,
        'filemain': filemain,
        'pooldir': pooldir,
        'orbitals': orbitals,
        'determinants': determinants,
        'symmetry': symmetry,
        'jastrow': jastrow,
        'jastrowder': jastrowder,
        'metadata': {
            'description': 'Sample job submission with the aiida_champ plugin example 01',
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

    Example usage: $ python example_01.py --code CHAMP@localhost

    Alternative (creates CHAMP@localhost-test code): $ python example_01.py

    Help: $ ./example_01.py --help
    """
    test_run(code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
