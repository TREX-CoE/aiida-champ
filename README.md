[![Build Status](https://travis-ci.org/aiidateam/aiida-diff.svg?branch=master)](https://travis-ci.org/aiidateam/aiida-diff) [![Docs status](https://readthedocs.org/projects/aiida-diff/badge)](http://aiida-diff.readthedocs.io/)

# aiida-diff

AiiDA demo plugin that computes the difference between two files.

Templated using the [AiiDA plugin cutter](https://github.com/aiidateam/aiida-plugin-cutter).

## Installation

```shell
git clone https://github.com/aiidateam/aiida-diff .
cd aiida-diff
pip install -e .  # also installs aiida, if missing (but not postgres)
#pip install -e .[precommit,testing] # install extras for more features
verdi quicksetup  # better to set up a new profile
verdi calculation plugins  # should now show your calclulation plugins
```

## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:
```shell
verdi daemon start         # make sure the daemon is running
cd examples
verdi run submit.py        # submit test calculation
verdi calculation list -a  # check status of calculation
```

If you have already set up your own aiida_diff code using `verdi code setup`, you may want to try the following command:
```
diff-submit  # uses aiida_diff.cli
```

## Tests

The following will discover and run all unit test:
```shell
pip install -e .[testing]
python manage.py
```

## License

MIT

## Contact


