#!/bin/bash

ps -ef | grep daemon.sh | grep -v grep | awk '{print $2}' | xargs kill -9
echo "daemon.sh was killed!"
ps -ef | grep process_daemon.py | grep -v grep | awk '{print $2}' | xargs kill -9
echo "tw.py was killed!"