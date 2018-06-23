#!/bin/bash
python ./app.py &
cd python
python train.py > /dev/null 2&>1 &
