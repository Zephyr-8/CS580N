#!/bin/bash

while true;
do
    server=`ps aux | grep job_issuer | grep -v grep`
    if [ ! "$server" ]; then
        cd ~/project-1-2-implementation-cmt/reddit
        time=$(date "+%m-%d-%Y %H:%M:%S")
        nohup python3 -u job_issuer.py xeoxoe DLkt89CnaYmKERy &
        echo "Process restart at ${time}"
    fi
    sleep 30
done