#!/bin/bash

set -e
cd "$(dirname "$0")";

if [ ! -d ".venv" ]; then
  echo "Run setup.sh first"
fi

source ".venv/bin/activate";
python src/main.py
