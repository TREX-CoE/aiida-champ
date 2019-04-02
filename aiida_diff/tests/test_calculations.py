""" Tests for calculations

"""
from __future__ import print_function
from __future__ import absolute_import

import os
import aiida_diff.tests as tests
import pytest


@pytest.mark.process_execution
def test_process(new_workdir):  # pylint: disable=too-many-locals
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""
    from aiida.plugins import DataFactory, CalculationFactory
    from aiida.engine import run_get_node

    # get code
    computer = tests.get_computer(workdir=new_workdir)
    code = tests.get_code(entry_point='diff', computer=computer)

    # Prepare input parameters
    DiffParameters = DataFactory('diff')
    parameters = DiffParameters({'ignore-case': True})

    from aiida.orm import SinglefileData
    file1 = SinglefileData(
        file=os.path.join(tests.TEST_DIR, "input_files", 'file1.txt'))
    file2 = SinglefileData(
        file=os.path.join(tests.TEST_DIR, "input_files", 'file2.txt'))

    # set up calculation
    options = {
        "resources": {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 1,
        },
        "max_wallclock_seconds": 30,
    }

    inputs = {
        'code': code,
        'parameters': parameters,
        'file1': file1,
        'file2': file2,
        'metadata': {
            'options': options,
            'label': "aiida_diff test",
            'description': "Test job submission with the aiida_diff plugin",
        },
    }

    _result, node = run_get_node(CalculationFactory('diff'), **inputs)

    computed_diff = node.outputs.diff.get_content()
    assert 'content1' in computed_diff
    assert 'content2' in computed_diff
