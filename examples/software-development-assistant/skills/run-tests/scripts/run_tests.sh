#!/bin/bash
# Detect and run the appropriate test runner for this project.
set -e

if [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    python -m pytest "$@"
elif [ -f "package.json" ]; then
    npm test -- --run "$@"
elif [ -f "go.mod" ]; then
    go test ./... "$@"
else
    echo "Error: could not detect test runner." >&2
    exit 1
fi
