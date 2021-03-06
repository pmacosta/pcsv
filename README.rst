.. README.rst
.. Copyright (c) 2013-2019 Pablo Acosta-Serafini
.. See LICENSE for details

.. image:: https://badge.fury.io/py/pcsv.svg
    :target: https://pypi.org/project/pcsv
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/l/pcsv.svg
    :target: https://pypi.org/project/pcsv
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/pcsv.svg
    :target: https://pypi.org/project/pcsv
    :alt: Python versions supported

.. image:: https://img.shields.io/pypi/format/pcsv.svg
    :target: https://pypi.org/project/pcsv
    :alt: Format

|

.. image::
    https://dev.azure.com/pmasdev/pcsv/_apis/build/status/pmacosta.pcsv?branchName=master
    :target: https://dev.azure.com/pmasdev/pcsv/_build?definitionId=7&_a=summary
    :alt: Continuous integration test status

.. image::
    https://img.shields.io/azure-devops/coverage/pmasdev/pcsv/7.svg
    :target: https://dev.azure.com/pmasdev/pcsv/_build?definitionId=7&_a=summary
    :alt: Continuous integration test coverage

.. image::
    https://readthedocs.org/projects/pip/badge/?version=stable
    :target: https://pip.readthedocs.io/en/stable/?badge=stable
    :alt: Documentation status

|

Description
===========

.. role:: bash(code)
	:language: bash

.. _Cog: https://nedbatchelder.com/code/cog
.. _Coverage: https://coverage.readthedocs.io
.. _Docutils: http://docutils.sourceforge.net/docs
.. _Mock: https://docs.python.org/3/library/unittest.mock.html
.. _Pexdoc: https://pexdoc.readthedocs.org
.. _Pmisc: https://pmisc.readthedocs.org
.. _PyContracts: https://andreacensi.github.io/contracts
.. _Pydocstyle: http://www.pydocstyle.org
.. _Pylint: https://www.pylint.org
.. _Py.test: http://pytest.org
.. _Pytest-coverage: https://pypi.org/project/pytest-cov
.. _Pytest-pmisc: https://pytest-pmisc.readthedocs.org
.. _Pytest-xdist: https://pypi.org/project/pytest-xdist
.. _Sphinx: http://sphinx-doc.org
.. _ReadTheDocs Sphinx theme: https://github.com/rtfd/sphinx_rtd_theme
.. _Inline Syntax Highlight Sphinx Extension:
   https://bitbucket.org/klorenz/sphinxcontrib-inlinesyntaxhighlight
.. _Shellcheck Linter Sphinx Extension:
   https://pypi.org/project/sphinxcontrib-shellcheck
.. _Tox: https://testrun.org/tox
.. _Virtualenv: https://docs.python-guide.org/dev/virtualenvs

This module can be used to handle comma-separated values (CSV) files and do
lightweight processing of their data with support for row and column
filtering. In addition to basic read, write and data replacement, files can be
concatenated, merged, and sorted

Examples
--------

Read/write
^^^^^^^^^^

.. code-block:: python

    # pcsv_example_1.py
    import pmisc, pcsv

    def main():
        with pmisc.TmpFile() as fname:
            ref_data = [["Item", "Cost"], [1, 9.99], [2, 10000], [3, 0.10]]
            # Write reference data to a file
            pcsv.write(fname, ref_data, append=False)
            # Read the data back
            obj = pcsv.CsvFile(fname)
        # After the object creation the I/O is done,
        # can safely remove file (exit context manager)
        # Check that data read is correct
        assert obj.header() == ref_data[0]
        assert obj.data() == ref_data[1:]
        # Add a simple row filter, only look at rows that have
        # values 1 and 3 in the "Items" column
        obj.rfilter = {"Item": [1, 3]}
        assert obj.data(filtered=True) == [ref_data[1], ref_data[3]]

    if __name__ == "__main__":
        main()

Replace data
^^^^^^^^^^^^

.. code-block:: python

    # pcsv_example_2.py
    import pmisc, pcsv

    def main():
        ctx = pmisc.TmpFile
        with ctx() as fname1:
            with ctx() as fname2:
                with ctx() as ofname:
                    # Create first (input) data file
                    input_data = [["Item", "Cost"], [1, 9.99], [2, 10000], [3, 0.10]]
                    pcsv.write(fname1, input_data, append=False)
                    # Create second (replacement) data file
                    replacement_data = [
                        ["Staff", "Rate", "Days"],
                        ["Joe", 10, "Sunday"],
                        ["Sue", 20, "Thursday"],
                        ["Pat", 15, "Tuesday"],
                    ]
                    pcsv.write(fname2, replacement_data, append=False)
                    # Replace "Cost" column of input file with "Rate" column
                    # of replacement file for "Items" 2 and 3 with "Staff" data
                    # from Joe and Pat. Save resulting data to another file
                    pcsv.replace(
                        fname1=fname1,
                        dfilter1=("Cost", {"Item": [1, 3]}),
                        fname2=fname2,
                        dfilter2=("Rate", {"Staff": ["Joe", "Pat"]}),
                        ofname=ofname,
                    )
                    # Verify that resulting file is correct
                    ref_data = [["Item", "Cost"], [1, 10], [2, 10000], [3, 15]]
                    obj = pcsv.CsvFile(ofname)
                    assert obj.header() == ref_data[0]
                    assert obj.data() == ref_data[1:]

    if __name__ == "__main__":
        main()

Concatenate two files
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # pcsv_example_3.py
    import pmisc, pcsv

    def main():
        ctx = pmisc.TmpFile
        with ctx() as fname1:
            with ctx() as fname2:
                with ctx() as ofname:
                    # Create first data file
                    data1 = [[1, 9.99], [2, 10000], [3, 0.10]]
                    pcsv.write(fname1, data1, append=False)
                    # Create second data file
                    data2 = [
                        ["Joe", 10, "Sunday"],
                        ["Sue", 20, "Thursday"],
                        ["Pat", 15, "Tuesday"],
                    ]
                    pcsv.write(fname2, data2, append=False)
                    # Concatenate file1 and file2. Filter out
                    # second column of file2
                    pcsv.concatenate(
                        fname1=fname1,
                        fname2=fname2,
                        has_header1=False,
                        has_header2=False,
                        dfilter2=[0, 2],
                        ofname=ofname,
                        ocols=["D1", "D2"],
                    )
                    # Verify that resulting file is correct
                    ref_data = [
                        ["D1", "D2"],
                        [1, 9.99],
                        [2, 10000],
                        [3, 0.10],
                        ["Joe", "Sunday"],
                        ["Sue", "Thursday"],
                        ["Pat", "Tuesday"],
                    ]
                    obj = pcsv.CsvFile(ofname)
                    assert obj.header() == ref_data[0]
                    assert obj.data() == ref_data[1:]

    if __name__ == "__main__":
        main()

Merge two files
^^^^^^^^^^^^^^^

.. code-block:: python

    # pcsv_example_4.py
    import pmisc, pcsv

    def main():
        ctx = pmisc.TmpFile
        with ctx() as fname1:
            with ctx() as fname2:
                with ctx() as ofname:
                    # Create first data file
                    data1 = [[1, 9.99], [2, 10000], [3, 0.10]]
                    pcsv.write(fname1, data1, append=False)
                    # Create second data file
                    data2 = [
                        ["Joe", 10, "Sunday"],
                        ["Sue", 20, "Thursday"],
                        ["Pat", 15, "Tuesday"],
                    ]
                    pcsv.write(fname2, data2, append=False)
                    # Merge file1 and file2
                    pcsv.merge(
                        fname1=fname1,
                        has_header1=False,
                        fname2=fname2,
                        has_header2=False,
                        ofname=ofname,
                    )
                    # Verify that resulting file is correct
                    ref_data = [
                        [1, 9.99, "Joe", 10, "Sunday"],
                        [2, 10000, "Sue", 20, "Thursday"],
                        [3, 0.10, "Pat", 15, "Tuesday"],
                    ]
                    obj = pcsv.CsvFile(ofname, has_header=False)
                    assert obj.header() == list(range(0, 5))
                    assert obj.data() == ref_data

    if __name__ == "__main__":
        main()

Sort a file
^^^^^^^^^^^

.. code-block:: python

    # pcsv_example_5.py
    import pmisc, pcsv

    def main():
        ctx = pmisc.TmpFile
        with ctx() as ifname:
            with ctx() as ofname:
                # Create first data file
                data = [
                    ["Ctrl", "Ref", "Result"],
                    [1, 3, 10],
                    [1, 4, 20],
                    [2, 4, 30],
                    [2, 5, 40],
                    [3, 5, 50],
                ]
                pcsv.write(ifname, data, append=False)
                # Sort
                pcsv.dsort(
                    fname=ifname,
                    order=[{"Ctrl": "D"}, {"Ref": "A"}],
                    has_header=True,
                    ofname=ofname,
                )
                # Verify that resulting file is correct
                ref_data = [[3, 5, 50], [2, 4, 30], [2, 5, 40], [1, 3, 10], [1, 4, 20]]
                obj = pcsv.CsvFile(ofname, has_header=True)
                assert obj.header() == ["Ctrl", "Ref", "Result"]
                assert obj.data() == ref_data

    if __name__ == "__main__":
        main()

Interpreter
===========

The package has been developed and tested with Python 2.7, 3.5, 3.6 and 3.7
under Linux (Debian, Ubuntu), Apple macOS and Microsoft Windows

Installing
==========

.. code-block:: console

	$ pip install pcsv

Documentation
=============

Available at `Read the Docs <https://pcsv.readthedocs.io>`_

Contributing
============

1. Abide by the adopted `code of conduct
   <https://www.contributor-covenant.org/version/1/4/code-of-conduct>`_

2. Fork the `repository <https://github.com/pmacosta/pcsv>`_ from GitHub and
   then clone personal copy [#f1]_:

    .. code-block:: console

        $ github_user=myname
        $ git clone --recurse-submodules \
              https://github.com/"${github_user}"/pcsv.git
        Cloning into 'pcsv'...
        ...
        $ cd pcsv || exit 1
        $ export PCSV_DIR=${PWD}
        $

3. The package uses two sub-modules: a set of custom Pylint plugins to help with
   some areas of code quality and consistency (under the ``pylint_plugins``
   directory), and a lightweight package management framework (under the
   ``pypkg`` directory). Additionally, the `pre-commit framework
   <https://pre-commit.com/>`_ is used to perform various pre-commit code
   quality and consistency checks. To enable the pre-commit hooks:

    .. code-block:: console

        $ cd "${PCSV_DIR}" || exit 1
        $ pre-commit install
        pre-commit installed at .../pcsv/.git/hooks/pre-commit
        $

4. Ensure that the Python interpreter can find the package modules
   (update the :bash:`$PYTHONPATH` environment variable, or use
   `sys.paths() <https://docs.python.org/3/library/sys.html#sys.path>`_,
   etc.)

   .. code-block:: console

       $ export PYTHONPATH=${PYTHONPATH}:${PCSV_DIR}
       $

5. Install the dependencies (if needed, done automatically by pip):

    * `Cog`_ (2.5.1 or newer)

    * `Coverage`_ (4.5.3 or newer)

    * `Docutils`_ (0.14 or newer)

    * `Inline Syntax Highlight Sphinx Extension`_ (0.2 or newer)

    * `Mock`_ (Python 2.x only, 2.0.0 or newer)

    * `Pexdoc`_ (1.1.4 or newer)

    * `Pmisc`_ (1.5.8 or newer)

    * `Py.test`_ (4.3.1 or newer)

    * `PyContracts`_ (1.8.2 or newer)

    * `Pydocstyle`_ (3.0.0 or newer)

    * `Pylint`_ (Python 2.x: 1.9.4 or newer, Python 3.x: 2.3.1 or newer)

    * `Pytest-coverage`_ (2.6.1 or newer)

    * `Pytest-pmisc`_ (1.0.7 or newer)

    * `Pytest-xdist`_ (optional, 1.26.1 or newer)

    * `ReadTheDocs Sphinx theme`_ (0.4.3 or newer)

    * `Shellcheck Linter Sphinx Extension`_ (1.0.8 or newer)

    * `Sphinx`_ (1.8.5 or newer)

    * `Tox`_ (3.7.0 or newer)

    * `Virtualenv`_ (16.4.3 or newer)

6. Implement a new feature or fix a bug

7. Write a unit test which shows that the contributed code works as expected.
   Run the package tests to ensure that the bug fix or new feature does not
   have adverse side effects. If possible achieve 100\% code and branch
   coverage of the contribution. Thorough package validation
   can be done via Tox and Pytest:

   .. code-block:: console

       $ PKG_NAME=pcsv tox
       GLOB sdist-make: .../pcsv/setup.py
       py27-pkg create: .../pcsv/.tox/py27
       py27-pkg installdeps: -r.../pcsv/requirements/tests_py27.pip, -r.../pcsv/requirements/docs_py27.pip
       ...
         py27-pkg: commands succeeded
         py35-pkg: commands succeeded
         py36-pkg: commands succeeded
         py37-pkg: commands succeeded
         congratulations :)
       $

   `Setuptools <https://bitbucket.org/pypa/setuptools>`_ can also be used
   (Tox is configured as its virtual environment manager):

   .. code-block:: console

       $ PKG_NAME=pcsv python setup.py tests
       running tests
       running egg_info
       writing pcsv.egg-info/PKG-INFO
       writing dependency_links to pcsv.egg-info/dependency_links.txt
       writing requirements to pcsv.egg-info/requires.txt
       ...
         py27-pkg: commands succeeded
         py35-pkg: commands succeeded
         py36-pkg: commands succeeded
         py37-pkg: commands succeeded
         congratulations :)
       $

   Tox (or Setuptools via Tox) runs with the following default environments:
   ``py27-pkg``, ``py35-pkg``, ``py36-pkg`` and ``py37-pkg`` [#f3]_. These use
   the 2.7, 3.5, 3.6 and 3.7 interpreters, respectively, to test all code in
   the documentation (both in Sphinx ``*.rst`` source files and in
   docstrings), run all unit tests, measure test coverage and re-build the
   exceptions documentation. To pass arguments to Pytest (the test runner) use
   a double dash (``--``) after all the Tox arguments, for example:

   .. code-block:: console

       $ PKG_NAME=pcsv tox -e py27-pkg -- -n 4
       GLOB sdist-make: .../pcsv/setup.py
       py27-pkg inst-nodeps: .../pcsv/.tox/.tmp/package/1/pcsv-1.0.8.zip
       ...
         py27-pkg: commands succeeded
         congratulations :)
       $

   Or use the :code:`-a` Setuptools optional argument followed by a quoted
   string with the arguments for Pytest. For example:

   .. code-block:: console

       $ PKG_NAME=pcsv python setup.py tests -a "-e py27-pkg -- -n 4"
       running tests
       ...
         py27-pkg: commands succeeded
         congratulations :)
       $

   There are other convenience environments defined for Tox [#f3]_:

    * ``py27-repl``, ``py35-repl``, ``py36-repl`` and ``py37-repl`` run the
      Python 2.7, 3.5, 3.6 and 3.7 REPL, respectively, in the appropriate
      virtual environment. The ``pcsv`` package is pip-installed by Tox when
      the environments are created.  Arguments to the interpreter can be
      passed in the command line after a double dash (``--``).

    * ``py27-test``, ``py35-test``, ``py36-test`` and ``py37-test`` run Pytest
      using the Python 2.7, 3.5, 3.6 and 3.7 interpreter, respectively, in the
      appropriate virtual environment. Arguments to pytest can be passed in
      the command line after a double dash (``--``) , for example:

      .. code-block:: console

       $ PKG_NAME=pcsv tox -e py27-test -- -x test_pcsv.py
       GLOB sdist-make: .../pcsv/setup.py
       py27-pkg inst-nodeps: .../pcsv/.tox/.tmp/package/1/pcsv-1.0.8.zip
       ...
         py27-pkg: commands succeeded
         congratulations :)
       $
    * ``py27-test``, ``py35-test``, ``py36-test`` and ``py37-test`` test code
      and branch coverage using the 2.7, 3.5, 3.6 and 3.7 interpreter,
      respectively, in the appropriate virtual environment. Arguments to
      pytest can be passed in the command line after a double dash (``--``).
      The report can be found in
      :bash:`${PCSV_DIR}/.tox/py[PV]/usr/share/pcsv/tests/htmlcov/index.html`
      where ``[PV]`` stands for ``2.7``, ``3.5``, ``3.6`` or ``3.7`` depending
      on the interpreter used.

8. Verify that continuous integration tests pass. The package has continuous
   integration configured for Linux, Apple macOS and Microsoft Windows (all via
   `Azure DevOps <https://dev.azure.com/pmasdev>`_).

9. Document the new feature or bug fix (if needed). The script
   :bash:`${PCSV_DIR}/pypkg/build_docs.py` re-builds the whole package
   documentation (re-generates images, cogs source files, etc.):

   .. code-block:: console

       $ "${PCSV_DIR}"/pypkg/build_docs.py -h
       usage: build_docs.py [-h] [-d DIRECTORY] [-r]
                            [-n NUM_CPUS] [-t]

       Build pcsv package documentation

       optional arguments:
         -h, --help            show this help message and exit
         -d DIRECTORY, --directory DIRECTORY
                               specify source file directory
                               (default ../pcsv)
         -r, --rebuild         rebuild exceptions documentation.
                               If no module name is given all
                               modules with auto-generated
                               exceptions documentation are
                               rebuilt
         -n NUM_CPUS, --num-cpus NUM_CPUS
                               number of CPUs to use (default: 1)
         -t, --test            diff original and rebuilt file(s)
                               (exit code 0 indicates file(s) are
                               identical, exit code 1 indicates
                               file(s) are different)

.. rubric:: Footnotes

.. [#f1] All examples are for the `bash <https://www.gnu.org/software/bash/>`_
   shell

.. [#f2] It is assumed that all the Python interpreters are in the executables
   path. Source code for the interpreters can be downloaded from Python's main
   `site <https://www.python.org/downloads/>`_

.. [#f3] Tox configuration largely inspired by
   `Ionel's codelog <https://blog.ionelmc.ro/2015/04/14/
   tox-tricks-and-patterns/>`_

License
=======

The MIT License (MIT)

Copyright (c) 2013-2019 Pablo Acosta-Serafini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
