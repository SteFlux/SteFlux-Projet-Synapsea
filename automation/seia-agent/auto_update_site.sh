#!/bin/bash

SRC_DIR=~/site
DEST_DIR=/var/www/html
LOG_FILE=~/SteFlux-Projet-Synapsea/automation/seia-agent/update.log

echo "[$(date)] ➜ Synchronisation des fichiers depuis $SRC_DIR vers $DEST_DIR" >> $LOG_FILE

rsync -avz --delete "$SRC_DIR/" "$DEST_DIR/" >> $LOG_FILE 2>&1

echo "[$(date)] ✅ Mise à jour terminée" >> $LOG_FILE

