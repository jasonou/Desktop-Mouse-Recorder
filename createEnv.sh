#!/bin/sh -e

rm -rf env
py -m venv env

source $PWD/env/Scripts/activate
py -m pip install --upgrade pip
pip install -r requirements.txt --use-pep517
deactivate
