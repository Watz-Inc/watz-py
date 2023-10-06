"""Nox sessions."""

import os
from pathlib import Path

import nox

# https://pdm.fming.dev/latest/usage/advanced/
os.environ.update({"PDM_IGNORE_SAVED_PYTHON": "1"})


@nox.session(reuse_venv=True)
def qa(session: nox.Session):
    """Run the pre commit hooks and pyright type checking."""
    session.run("pdm", "install", "-dG", "qa", external=True)

    session.run("pre-commit", "run", "--all-files")
    session.run("pyright", "cookiecutter_test_build")


@nox.session(reuse_venv=True)
def test(session: nox.Session):
    """Runs the pytest test suite and generates coverage files."""
    session.run("pdm", "install", "-dG", "test", external=True)
    session.run("pdm", "install", "-dG", "coverage", external=True)

    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


# Note this must come below the test session to have access to the up-to-date coverage files
@nox.session(reuse_venv=True)
def coverage(session: nox.Session) -> None:
    """Finds the coverage files created during test session & produces the report."""
    session.run("pdm", "install", "-dG", "coverage", external=True)

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    args = session.posargs or ["report"]
    session.run("coverage", *args)


@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:
    """Build the documentation. To serve locally run `nox -s docs -- --serve`."""
    session.run("pdm", "install", "-dG", "docs", external=True)

    # Build the docs locally:
    session.run("mike", "deploy", "develop")

    # So root redirects to develop rather than having to navigate to /develop:
    session.run("mike", "set-default", "develop")

    # If serve passed in, also run mike serve:
    if session.posargs and session.posargs[0] == "serve":
        session.run("mike", "serve", *session.posargs[1:])
