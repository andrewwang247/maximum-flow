#!/bin/bash

# Copyright 2026. Andrew Wang.
# Run static checks on all Python code.

set -uo pipefail

# List of all Python files.
pyfiles=$(find . -name "*.py" -type f -not -path "./env/*");

printf "Running autopep...\n\n"
autopep8 -i -a -a $pyfiles

printf "Running pylint...\n\n"
pylint $pyfiles

printf "Running pycodestyle...\n\n"
pycodestyle $pyfiles

printf "\nRunning pydocstyle...\n\n"
pydocstyle $pyfiles

printf "\nRunning mypy...\n\n"
mypy $pyfiles
