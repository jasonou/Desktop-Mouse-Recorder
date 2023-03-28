#!/bin/sh

set -e

if [ "$1" == "" ]; then
  echo "$0: Usage: ./replay.sh [required: script name] [optional: loops]"
  exit 1
fi

source $PWD/env/Scripts/activate
py $PWD/app/play.py "$@"
deactivate
