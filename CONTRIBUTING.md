# Contributor Guide

Thank you for your interest in improving this project.
This project is open-source under the [Apache 2.0 license] and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code](https://github.com/watz-inc/watz-py)
- [Documentation](https://watz-inc.github.io/watz-py)
- [Issue Tracker](https://github.com/watz-inc/watz-py/issues)
- [Code of Conduct](CODE_OF_CONDUCT.md)

[apache 2.0 license]: https://opensource.org/licenses/Apache-2.0

## How to report a bug

Report bugs on the [Issue Tracker](https://github.com/watz-inc/watz-py/issues).

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker](https://github.com/watz-inc/watz-py/issues).

## How to set up your development environment

You need Python 3.9+ and [PDM](https://pdm.fming.dev/) installed.

Install the package with development requirements:
`pdm install` to setup for the first time
`pdm venv activate` to activate the virtual environment (whenever you open the project to work)

### Running tests

- `pdm run nox` to run all sessions
- `pdm run nox -s qa` to run everything that runs on a git commit, plus `pyright`
- `pdm run nox -s test` to run tests
- `pdm run nox -s coverage` for a coverage report based on the last `test` session run
- `pdm run nox -s docs -- serve` to build the docs and run a local copy at `http://localhost:8000`

Unit tests are located in the _tests_ directory,
and are written using the [pytest] testing framework.

[pytest]: https://pytest.readthedocs.io/

## How to submit changes

Open a [pull request](https://github.com/watz-inc/watz-py/pulls) to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.
