#!/bin/bash
python ./app.py &
python ./train.py & > /dev/null 2>&1