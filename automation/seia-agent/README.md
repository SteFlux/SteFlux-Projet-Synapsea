# SEIA Agent – Automatisation du site Synapsea

Ce dossier contient le système SEIA Agent, responsable de :
- Démarrer l’API SEIA (`server.py`)
- Mettre à jour automatiquement les fichiers du site vers `/var/www/html`
- Loguer toutes les mises à jour

## Fichiers :
- `auto_update_site.sh` : script de synchro via `rsync`
- `launch_seia.sh` : lance l’API + update
- `seia-agent.service` : service systemd auto
