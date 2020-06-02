#!/bin/bash
IP=`curl orange.tw 2>/dev/null | head -n1 | tr -d '\n'`
python3 ./app.py -l $IP -p 8888 -d