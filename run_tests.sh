#!/bin/bash
export PYTHONPATH=$(pwd)/src:$PYTHONPATH
python -m pytest tests/assurance_exchange/
