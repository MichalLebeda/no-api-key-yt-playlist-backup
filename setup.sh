#!/bin/sh

set -e
cd "$(dirname "$0")";

if [ -d ".venv" ]; then
    echo "Python venv already exists";
else
    echo "Creating venv...";
    python -m venv .venv;
fi

source ".venv/bin/activate";
pip install -r requrements.txt

