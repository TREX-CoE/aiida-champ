[![Build Status](https://travis-ci.org/aiidateam/aiida-diff.svg?branch=master)](https://travis-ci.org/aiidateam/aiida-diff) 
[![Coverage Status](https://coveralls.io/repos/github/aiidateam/aiida-diff/badge.svg?branch=master)](https://coveralls.io/github/aiidateam/aiida-diff?branch=master) 
[![Docs status](https://readthedocs.org/projects/aiida-diff/badge)](http://aiida-diff.readthedocs.io/) 
[![PyPI version](https://badge.fury.io/py/aiida-diff.svg)](https://badge.fury.io/py/aiida-diff)

# aiida-diff

AiiDA demo plugin that computes the difference between two files.

Templated using the [AiiDA plugin cutter](https://github.com/aiidateam/aiida-plugin-cutter).

## Installation

```shell
git clone https://github.com/aiidateam/aiida-diff .
cd aiida-diff
pip install -e .  # also installs aiida, if missing (but not postgres)
# pip install -e .[pre-commit,testing] # install extras for more features
verdi quicksetup  # better to set up a new profile
verdi plugin list aiida.calculations  # should now show your calclulation plugins
```

## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:
```shell
verdi daemon start         # make sure the daemon is running
cd examples
verdi run submit.py        # submit test calculation
verdi process list -a  # check status of calculation
```

The plugin also includes verdi commands to inspect its data types:
```shell
verdi data diff list
verdi data diff export <PK>
```

## Tests

The following will discover and run all unit tests:
```shell
pip install -e .[testing]
pytest -v
```

## License

MIT


