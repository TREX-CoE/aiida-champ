[![Build Status](https://github.com/neelravi/aiida-champ/workflows/ci/badge.svg?branch=master)](https://github.com/neelravi/aiida-champ/actions)
[![Coverage Status](https://coveralls.io/repos/github/neelravi/aiida-champ/badge.svg?branch=master)](https://coveralls.io/github/neelravi/aiida-champ?branch=master)
[![Docs status](https://readthedocs.org/projects/aiida-champ/badge)](http://aiida-champ.readthedocs.io/)
[![PyPI version](https://badge.fury.io/py/aiida-champ.svg)](https://badge.fury.io/py/aiida-champ)

<img src="docs/source/images/AiiDA_transparent_logo.png" width="250">  <img src="docs/source/images/logo_champ_reduced.png" height="100">

# aiida-champ

AiiDA plugin that wraps the `vmc` executable of the CHAMP code for computing the total energy of a molecular system.


## Repository contents

* [`.github/`](.github/): [Github Actions](https://github.com/features/actions) configuration
  * [`ci.yml`](.github/workflows/ci.yml): runs tests, checks test coverage and builds documentation at every new commit
  * [`publish-on-pypi.yml`](.github/workflows/publish-on-pypi.yml): automatically deploy git tags to PyPI - just generate a [PyPI API token](https://pypi.org/help/#apitoken) for your PyPI account and add it to the `pypi_token` secret of your github repository
* [`aiida_champ/`](aiida_champ/): The main source code of the plugin package
  * [`data/`](aiida_champ/data/): A new `CHAMPParameters` data class, used as input to the `CHAMPCalculation` `CalcJob` class
  * [`calculations.py`](aiida_champ/calculations.py): A new `CHAMPCalculation` `CalcJob` class
  * [`cli.py`](aiida_champ/cli.py): Extensions of the `verdi data` command line interface for the `champParameters` class
  * [`helpers.py`](aiida_champ/helpers.py): Helpers for setting up an AiiDA code for `champ` automatically
  * [`parsers.py`](aiida_champ/parsers.py): A new `Parser` for the `CHAMPCalculation`
* [`docs/`](docs/): A documentation template ready for publication on [Read the Docs](http://aiida-champ.readthedocs.io/en/latest/)
* [`examples/`](examples/): An example of how to submit a calculation using this plugin
* [`tests/`](tests/): Basic regression tests using the [pytest](https://docs.pytest.org/en/latest/) framework (submitting a calculation, ...). Install `pip install -e .[testing]` and run `pytest`.
* [`.coveragerc`](.coveragerc): Configuration of [coverage.py](https://coverage.readthedocs.io/en/latest) tool reporting which lines of your plugin are covered by tests
* [`.gitignore`](.gitignore): Telling git which files to ignore
* [`.pre-commit-config.yaml`](.pre-commit-config.yaml): Configuration of [pre-commit hooks](https://pre-commit.com/) that sanitize coding style and check for syntax errors. Enable via `pip install -e .[pre-commit] && pre-commit install`
* [`.readthedocs.yml`](.readthedocs.yml): Configuration of documentation build for [Read the Docs](https://readthedocs.org/)
* [`LICENSE`](LICENSE): License for your plugin
* [`MANIFEST.in`](MANIFEST.in): Configure non-Python files to be included for publication on [PyPI](https://pypi.org/)
* [`README.md`](README.md): This file
* [`conftest.py`](conftest.py): Configuration of fixtures for [pytest](https://docs.pytest.org/en/latest/)
* [`pytest.ini`](pytest.ini): Configuration of [pytest](https://docs.pytest.org/en/latest/) test discovery
* [`setup.json`](setup.json): Plugin metadata for registration on [PyPI](https://pypi.org/) and the [AiiDA plugin registry](https://aiidateam.github.io/aiida-registry/) (including entry points)
* [`setup.py`](setup.py): Installation script for pip / [PyPI](https://pypi.org/)


See also the following video sequences from the 2019-05 AiiDA tutorial:

 * [aiida-champ setup.json](https://www.youtube.com/watch?v=2CxiuiA1uVs&t=240s)
 * [run aiida-champ example calculation](https://www.youtube.com/watch?v=2CxiuiA1uVs&t=403s)
 * [aiida-champ CalcJob plugin](https://www.youtube.com/watch?v=2CxiuiA1uVs&t=685s)
 * [aiida-champ Parser plugin](https://www.youtube.com/watch?v=2CxiuiA1uVs&t=936s)
 * [aiida-champ computer/code helpers](https://www.youtube.com/watch?v=2CxiuiA1uVs&t=1238s)
 * [aiida-champ input data (with validation)](https://www.youtube.com/watch?v=2CxiuiA1uVs&t=1353s)
 * [aiida-champ cli](https://www.youtube.com/watch?v=2CxiuiA1uVs&t=1621s)
 * [aiida-champ tests](https://www.youtube.com/watch?v=2CxiuiA1uVs&t=1931s)
 * [Adding your plugin to the registry](https://www.youtube.com/watch?v=760O2lDB-TM&t=112s)
 * [pre-commit hooks](https://www.youtube.com/watch?v=760O2lDB-TM&t=333s)

For more information, see the [developer guide](https://aiida-champ.readthedocs.io/en/latest/developer_guide) of your plugin.


## Features

 * Add input files using `SinglefileData`:
   ```python
   SinglefileData = DataFactory('singlefile')
   filemain = SinglefileData(file='vmc.inp')
   molecule = SinglefileData(file='butadiene.xyz')
   orbitals = SinglefileData(file='cas44.lcao')
   determinants = SinglefileData(file='cas44.det')
   ```



## Installation

```shell
pip install aiida-champ
verdi quicksetup  # better to set up a new profile
verdi plugin list aiida.calculations  # should now show your calclulation plugins
```


## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:
```shell
verdi daemon start     # make sure the daemon is running
cd examples
python example_01.py        # run test calculation
verdi process list -a  # check record of calculation
```

The plugin also includes verdi commands to inspect its data types:
```shell
verdi data champ list
verdi data champ export <PK>
```

## Development

```shell
git clone https://github.com/neelravi/aiida-champ .
cd aiida-champ
pip install -e .[pre-commit,testing]  # install extra dependencies
pre-commit install  # install pre-commit hooks
pytest -v  # discover and run all tests
```

See the [developer guide](http://aiida-champ.readthedocs.io/en/latest/developer_guide/index.html) for more information.

## License

MIT


## Author

Name  :: Ravindra Shinde  (TREX-CoE)
Email :: r.l.shinde@utwente.nl