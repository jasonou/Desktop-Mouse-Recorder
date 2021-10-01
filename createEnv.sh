#!/bin/sh

set -e
rm -rf env
py -m venv env

source $PWD/env/Scripts/activate
py -m pip install --upgrade pip
pip3 install PyAutoGUI==0.9.52
pip3 install pynput==1.7.3
pip3 install twilio==6.63.0
pip3 install opencv-python==4.5.3.56
pip3 install python-dotenv==0.19.0
pip3 install keyboard==0.13.5
pip3 install autopep8

deactivate
