#!/bin/bash

# Copyright 2026. Andrew Wang.
# Run static checks on all Python code.

set -uo pipefail

printf "Running ruff check...\n"
ruff check --fix .

printf "Running ruff format...\n"
ruff format .

printf "Running mypy...\n"
mypy .
