# -*- coding: utf-8 -*-
""" Tests for calculations

"""
import os
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run
from aiida.orm import SinglefileData

from . import TEST_DIR


def test_process(diff_code):
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""

    # Prepare input parameters
    DiffParameters = DataFactory('vmc_mov1')
    parameters = DiffParameters({})

    file1 = SinglefileData(
        file=os.path.join(TEST_DIR, 'input_files', 'vmc.inp'))

    # set up calculation
    inputs = {
        'code': diff_code,
        'parameters': parameters,
        'file1': file1,
        'metadata': {
            'options': {
                'max_wallclock_seconds': 300
            },
        },
    }

    result = run(CalculationFactory('vmc_mov1'), **inputs)
    computed_diff = result['vmc_mov1'].get_content()

    # assert 'content1' in computed_diff
    # assert 'content2' in computed_diff
