#!/usr/bin/env bash

# Try Python3 first. If it's not found, try Python.
PYTHON=""
command -v python3 >/dev/null 2>&1
if [ $? -eq 0 ]; then
  PYTHON="python3"
else
  command -v python >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    PYTHON="python"
  else
    echo "Python not found. Please install Python."
    exit 1
  fi
fi

# Check for correct python version
VERSION=`$PYTHON --version 2>&1 | awk '{print $2}'`
MAJOR_VERSION=`echo $VERSION | cut -d. -f1`
MINOR_VERSION=`echo $VERSION | cut -d. -f2`
if [ $MAJOR_VERSION -ne 3 ] || [ $MINOR_VERSION -lt 7 ]; then
  echo "You must use Python 3.7+ You are using $VERSION"
  echo "When upgrading, remember to install python3.X-dev and python3.X-venv (and maybe the right pip)"
  exit 1
else
  echo -e "You are using Python $VERSION"
fi

# Create a virtual environment for dependencies
if [ ! -d env ]
then
  echo virtual environment 'env' not found. Creating a new one
  $PYTHON -m venv env
fi

if [ "$OSTYPE" = "msys" ]
then
  source ./env/Scripts/activate
else
  source ./env/bin/activate
fi

echo "Installing Requirements"
# upgrade pip
pip install --upgrade pip

# install requirements
pip install -r requirements.txt
# To generate a new requirements.txt file, run "pip freeze > requirements.txt"

$PYTHON ./app/updateConfPages.py

echo "Resetting Database"
DATASOURCE=$1
echo $DATASOURCE

if [ "${DATASOURCE}" = 'test' ] || [ "${DATASOURCE}" = 'conf' ];
then
  $PYTHON ./app/reset_database.py $DATASOURCE
else
  echo -e "\e[31mUnable to reset database (Invalid argument).\nPass in 'test' to use the test data or 'conf' to use the data from confluence\e[0m"
fi


