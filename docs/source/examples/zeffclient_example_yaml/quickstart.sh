#!/bin/sh

echo
echo ==========================================
echo Setup virtual environment and install zeff
echo ==========================================
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install git+ssh://git@github.com/ziff/ZeffClient.git@0.0.1

echo
echo ==========================================
echo Initialize the project
echo When asked enter your org_id and user_id
echo All other questions accept default by
echo hitting enter
echo ==========================================
zeff init

echo ==========================================
echo Start the upload of some records
echo ==========================================
zeff upload --no-train
