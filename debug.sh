#!/bin/sh -e

source $PWD/env/Scripts/activate
py $PWD/app/debug.py
deactivate
