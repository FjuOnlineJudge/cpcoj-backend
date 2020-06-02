#!/bin/bash
IP=`curl orange.tw 2>/dev/null | head -n1 | tr -d '\n'`
sudo python3 ./app.py -l $IP