#!/bin/bash

IS_DEBUG_ACTIVE=${-//[^x]/}

[[ -n $IS_DEBUG_ACTIVE ]] && set +x

echo "usage: source ./activate.sh"

export PYTHONPATH=$(pwd)
test -d venv && source venv/bin/activate

[[ -n $IS_DEBUG_ACTIVE ]] && set -x
