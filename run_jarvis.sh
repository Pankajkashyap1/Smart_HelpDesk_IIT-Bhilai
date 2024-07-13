#!/usr/bin/env bash
# --------------------------------
# Start MongoDB service
# --------------------------------
sudo launchctl start mongodb

# --------------------------------
# Start Jarvis service with virtualenv
# --------------------------------
./jarvis_virtualenv/bin/python ./src/jarvis/start.py # run jarvis from here

# --------------------------------
# Stop MongoDB service
# --------------------------------
sudo launchctl stop mongodb
