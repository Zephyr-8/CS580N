#!/bin/bash
while true;
do
    server=`ps aux | grep get_input.py | grep -v grep`
    if [ ! "$server" ]; then
        cd ~/dashboard
        time=$(date "+%m-%d-%Y %H:%M:%S")
        nohup python3 -u get_input.py &
        echo "Process restart at ${time}"
    fi
    sleep 30
done