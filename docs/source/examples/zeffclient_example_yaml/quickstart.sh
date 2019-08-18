#!/bin/sh

for pyname in 'python3.8' 'python3.7' 'python3' 'python'
do
	PYTHON=`which ${pyname}`
	if [ $? -eq 0 ]; then
		break
	fi
done

if [ ! -x "${PYTHON}" ]; then
	echo No python interpreter found in current PATH. >&2
	exit 1
fi

${PYTHON} -c 'import sys; sys.exit(0) if sys.version_info >= (3, 7) else sys.exit(1)'
if [ $? -eq 1 ]; then
	echo Python 3.7 or greater is required to use ZeffClient. >&2
	exit 1
fi

echo
echo ==========================================
echo Setup virtual environment and install zeff
echo ==========================================
${PYTHON} -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install git+ssh://git@github.com/ziff/ZeffClient.git@0.0.2
if [ $? -ne 0 ]; then
	exit $?
fi

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
