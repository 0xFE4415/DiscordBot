#!/usr/bin/env bash
set -e

VENV_PY="./venv/bin/python"
TARGET="src"

echo ">>> Running Black..."
"$VENV_PY" -m black "$TARGET"

echo ">>> Running isort..."
"$VENV_PY" -m isort "$TARGET"

echo ">>> Running Pylint..."
"$VENV_PY" -m pylint "$TARGET"/*

echo ">>> Running mypy (strict)..."
"$VENV_PY" -m mypy "$TARGET" --strict

echo " All checks finished."
