#!/bin/bash

while true;
do
    server=`ps aux | grep tw.py | grep -v grep`
    if [ ! "$server" ]; then
        cd ..
        time=$(date "+%m-%d-%Y %H:%M:%S")
        nohup python3 tw.py &
        echo "Process restart at ${time}"
    fi
    sleep 30
done