#!/bin/bash

ps -ef | grep daemon_reddit.sh | grep -v grep | awk '{print $2}' | xargs kill -9
echo "daemon_reddit.sh was killed!"
ps -ef | grep job_issuer.py | grep -v grep | awk '{print $2}' | xargs kill -9
echo "job_issuer.py was killed!"