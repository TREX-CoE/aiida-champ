===============
Developer guide
===============

Running the tests
+++++++++++++++++

The following will discover and run all unit test::

    pip install -e .[testing]
    python manage.py

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
