#!/usr/bin/env sh

set -e

# Don't let CDPATH interfere with the cd command
unset CDPATH
cd "$(dirname "$0")"

# activate the python virtualenv
source ".venv/bin/activate"

# Execute the bot
exec python3.6 ./run.py
