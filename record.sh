#!/bin/sh

set -e

if [ "$1" == "" ]; then
  echo "$0: Usage: ./replay.sh [recording]"
  exit 1
fi

source $PWD/env/Scripts/activate
py $PWD/app/record.py "$1"
deactivate
