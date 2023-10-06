#!/bin/bash

# Stop on error:
set -e

pdm install

source .venv/bin/activate

pre-commit install
