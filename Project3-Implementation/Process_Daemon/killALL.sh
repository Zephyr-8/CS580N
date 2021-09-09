#!/bin/bash
ps -ef | grep daemon_flask.sh | grep -v grep | awk '{print $2}' | xargs kill -9
echo "daemon_flask.sh was killed!"
ps -ef | grep get_input.py | grep -v grep | awk '{print $2}' | xargs kill -9
echo "FLASK was killed!"