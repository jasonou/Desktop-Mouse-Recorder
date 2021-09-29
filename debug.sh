#!/bin/sh

set -e

source $PWD/env/Scripts/activate
py app_debug.py
deactivate
