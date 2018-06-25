#!/bin/bash
cd server
python app.py &
cd ../ai
python train.py & 
# > /dev/null 2>&1