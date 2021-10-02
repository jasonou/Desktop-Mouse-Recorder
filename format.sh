#!/bin/sh

set -e

source $PWD/env/Scripts/activate
autopep8 --in-place --aggressive --aggressive $PWD/app/*.py
deactivate
