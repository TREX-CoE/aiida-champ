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
    # RemoteData = DataFactory('remotedata')

    filemain = SinglefileData(file=path.join(INPUT_DIR, 'vmc.inp'))
    molecule = SinglefileData(file=path.join(INPUT_DIR, 'butadiene.xyz'))

    # pooldir = RemoteData(file=POOL_DIR)

    ecp1 = SinglefileData(file=path.join(INPUT_DIR, 'BFD.gauss_ecp.dat.C'))
    ecp2 = SinglefileData(file=path.join(INPUT_DIR, 'BFD.gauss_ecp.dat.H'))

    orbitals = SinglefileData(file=path.join(INPUT_DIR, 'cas44.lcao'))
    determinants = SinglefileData(file=path.join(INPUT_DIR, 'cas44.det'))
    symmetry = SinglefileData(file=path.join(INPUT_DIR, 'cas44.sym'))
    jastrow = SinglefileData(file=path.join(INPUT_DIR, 'jastrow_good_b3lyp.0'))
    jastrowder = SinglefileData(file=path.join(INPUT_DIR, 'jastrow.der'))
    numericalbasisinfo = SinglefileData(file=path.join(POOL_DIR, 'BFD-Q.bfinfo'))
    numericalbasis1 = SinglefileData(file=path.join(INPUT_DIR, 'BFD-Q.basis.C'))
    numericalbasis2 = SinglefileData(file=path.join(INPUT_DIR, 'BFD-Q.basis.H'))


    # set up calculation
    inputs = {
        'code': champ_code,
        'filemain': filemain,
        'molecule': molecule,
        # 'pooldir': pooldir,
        'ecp1': ecp1,
        'ecp2': ecp2,
        'orbitals': orbitals,
        'determinants': determinants,
        'symmetry': symmetry,
        'jastrow': jastrow,
        'jastrowder': jastrowder,
        'numericalbasisinfo': numericalbasisinfo,
        'numericalbasis1': numericalbasis1,
        'numericalbasis2': numericalbasis2,
        'metadata': {
            'description': 'Sample job submission with the aiida_champ plugin example 01',
        },
    }

    # Note: in order to submit your calculation to the aiida daemon, do:
    result = engine.run(CalculationFactory('CHAMP'), **inputs)
    computed_diff = result['Output'].get_content()
    print('Outout of the Calculation: \n{}'.format(computed_diff))


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
