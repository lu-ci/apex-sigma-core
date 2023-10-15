#!/usr/bin/env bash

#python -m pytest -v tests/

# E501 is are lines over 79 chars. Which is... really short...
python -m flake8 --ignore=E501 sigma/