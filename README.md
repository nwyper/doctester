doctester
=========

A simple wrapper for Python's doctest module

Doctester searches for all .py files in a project, and executes all doctests contained in each file.  The results
are logged to a log-file ('doctest.log' by default).

To use doctester as part of a bigger project, just run `./start --test`.  `start` demonstrates how to
import and call the tester according to a command-line argument.

To use doctester by itself, on all "*.py" files under a project root, run `./doctester/doctester.py --root test_project`

