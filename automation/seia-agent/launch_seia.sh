#!/bin/bash

cd ~/seia-api
python3 server.py &

sleep 5
bash ~/SteFlux-Projet-Synapsea/automation/seia-agent/auto_update_site.sh

