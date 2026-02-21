#!/bin/bash
# Wrapper script to run upload.py with environment selection
# Usage:
#   upload file.md             -> uses local environment
#   upload local file.md       -> explicitly uses local
#   upload stage file.md       -> uses stage environment
#   upload prod file.md        -> uses production environment

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON="$SCRIPT_DIR/venv/bin/python"

if [ ! -f "$PYTHON" ]; then
    echo "Error: Python venv not found. Please run:"
    echo "  cd $SCRIPT_DIR && python3 -m venv venv && source venv/bin/activate && pip install requests"
    exit 1
fi

# Check if first argument is an environment specifier
ENV=""
if [ "$1" = "local" ] || [ "$1" = "stage" ] || [ "$1" = "prod" ]; then
    ENV="$1"
    shift  # Remove first argument, pass rest to python
fi

# Set environment variable if specified
if [ -n "$ENV" ]; then
    export MEMSHARD_ENV="$ENV"
fi

"$PYTHON" "$SCRIPT_DIR/upload.py" "$@"
