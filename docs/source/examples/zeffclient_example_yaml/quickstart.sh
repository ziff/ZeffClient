#!/bin/sh

python3 -c 'import sys; sys.exit(0) if sys.version_info >= (3, 7) else sys.exit(1)'
if [ $? -eq 1 ]; then
	echo Python 3.7 or greater is required to use ZeffClient. >&2
	exit 1
fi

echo
echo ==========================================
echo Setup virtual environment and install zeff
echo ==========================================
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install git+ssh://git@github.com/ziff/ZeffClient.git@0.0.2

echo
echo ==========================================
echo Initialize the project
echo When asked enter your org_id and user_id
echo All other questions accept default by
echo hitting enter
echo ==========================================
zeff init
if [ $? -ne 0 ]; then
	exit $?
fi

echo ==========================================
echo Start the upload of some records
echo ==========================================
zeff upload --no-train
