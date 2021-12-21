#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run a test calculation on localhost.

Usage: python example_01.py
"""
from os import path
import click
from aiida import cmdline, engine
from aiida.plugins import DataFactory, CalculationFactory
from aiida.orm import Dict, load_code, load_computer
from aiida.common.exceptions import NotExistent
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

    print ("diff code ", diff_code)
    print ("computer ", computer)
    diff_code = load_code('vmc_mov1@localhost-test')
    print ("diff code after loading ", diff_code)

    # Prepare input parameters
    DiffParameters = DataFactory('vmc_mov1')
    parameters = DiffParameters({})

    SinglefileData = DataFactory('singlefile')

    print("Parameters ", parameters)
    # set up calculation
    inputs = {
        'code': diff_code,
        'parameters': parameters,
        'metadata': {
            'description': 'Test job submission with the aiida_diff plugin',
        },
    }

    print ("Inputs dict", inputs)
    # Note: in order to submit your calculation to the aiida daemon, do:
    #from aiida.engine import submit
    #future = submit(CalculationFactory('vmc_mov1'), **inputs)
    result = engine.run(CalculationFactory('vmc_mov1'), **inputs)
    energy = float(result['output_energy'])
    #print ("results from submit ", future)
    # print ("results from submit output file ", future['output_filename'])
    print ("results from submit calc ", result)
    print("energy from the calculations ", float(result['output_energy']) )
    # print ("results ", result)
    # print ("results vmc mov1 ", result['vmc_mov1'])
    # computed_diff = result['vmc_mov1'].get_content()
    # print('Computed diff between files: \n{}'.format(computed_diff))


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
