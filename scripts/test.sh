#!/bin/bash
IP=`curl orange.tw 2>/dev/null | head -n1 | tr -d '\n'`
[[ -n "$1" ]] && PORT=$1 || PORT=8888
python3 ./app.py -l $IP -p $PORT -d