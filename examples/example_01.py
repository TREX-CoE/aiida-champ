#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run a test calculation on localhost.

Usage: ./example_01.py
"""
from os import path
import click
from aiida import cmdline, engine
from aiida.plugins import DataFactory, CalculationFactory
from aiida_diff import helpers

INPUT_DIR = path.join(path.dirname(path.realpath(__file__)), 'input_files')
POOL_DIR = path.join(path.dirname(path.realpath(__file__)), 'input_files/pool')

print ("Input dir ", INPUT_DIR)
print ("pool dir ", POOL_DIR)


def test_run(diff_code):
    """Run a calculation on the localhost computer.

    Uses test helpers to create AiiDA Code on the fly.
    """
    if not diff_code:
        # get code
        computer = helpers.get_computer()
        diff_code = helpers.get_code(entry_point='vmc_mov1', computer=computer)

    # Prepare input parameters
    DiffParameters = DataFactory('vmc_mov1')
    parameters = DiffParameters({})

    SinglefileData = DataFactory('singlefile')
    file1 = SinglefileData(file=path.join(INPUT_DIR, 'vmc.inp'))

    print("Parameters ", parameters)
    print ("file 1", file1)
    # set up calculation
    inputs = {
        'code': diff_code,
        'parameters': parameters,
        'file1': file1,
        'metadata': {
            'description': 'Test job submission with the aiida_diff plugin',
        },
    }

    print ("Inputs dict", inputs)
    # Note: in order to submit your calculation to the aiida daemon, do:
    # from aiida.engine import submit
    # future = submit(CalculationFactory('diff'), **inputs)
    result = engine.run(CalculationFactory('vmc_mov1'), **inputs)

    print ("results ", result)
    print ("results vmc mov1 ", result['vmc_mov1'])
    computed_diff = result['vmc_mov1'].get_content()
    print('Computed diff between files: \n{}'.format(computed_diff))


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.

    Example usage: $ ./example_01.py --code diff@localhost

    Alternative (creates diff@localhost-test code): $ ./example_01.py

    Help: $ ./example_01.py --help
    """
    test_run(code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
