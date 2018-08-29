===============
Developer guide
===============

Running the tests
+++++++++++++++++

The following will discover and run all unit test::

    pip install -e .[testing]
    python manage.py

Automatic coding style checks
+++++++++++++++++++++++++++++

Enable enable automatic checks of code sanity and coding style::

    pip install -e .[pre-commit]
    pre-commit install

After this, the `yapf <https://github.com/google/yapf>`_ formatter, 
the `pylint <https://www.pylint.org/>`_ linter
and the `prospector <https://pypi.org/project/prospector/>` code analyzer will
run at every commit.

If you ever need to skip these pre-commit hooks, just use::

    git commit -n


Continuous integration
++++++++++++++++++++++

``aiida-diff`` comes with a ``.travis.yml`` file for continuous integration tests on every commit using `Travis CI <http://travis-ci.org/>`_. It will:

#. run all tests for the ``django`` and ``sqlalchemy`` ORM
#. build the documentation
#. check coding style and version number (not required to pass by default)

Just enable Travis builds for the ``aiida-diff`` repository in your Travis account. 

Online documentation
++++++++++++++++++++

The documentation of ``aiida-diff``
is ready for `ReadTheDocs <https://readthedocs.org/>`_:

#. Add the ``aiida-diff`` repository on your RTD profile, preferably using ``aiida-diff`` as the project name
#. In **Admin => Advanced settings => Requirements file** enter ``docs/requirements_for_rtd.txt``

Done.

PyPI release
++++++++++++

Your plugin is already prepared for being uploaded to the `Python Package Index <https://pypi.org/>`_.
Just register for an account and::

    pip install twine
    python setup.py sdist bdist_wheel
    twine upload dist/*

After this, you (and everyone else) should be able to::

    pip install aiida-diff

