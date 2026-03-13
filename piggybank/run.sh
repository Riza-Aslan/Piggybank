#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "==================================================="
bashio::log.info " Starte Piggybank Taschengeld-Tracker Add-on..."
bashio::log.info "==================================================="

DATA_DIR="/data"
export DB_PATH="sqlite:///${DATA_DIR}/piggybank.db"

bashio::log.info "Datenbank wird gespeichert in: ${DB_PATH}"

if [ -d "/app/backend" ]; then
    cd /app/backend

    bashio::log.info "Starte Uvicorn auf Port 8099..."
    # Use explicit venv path to ensure uvicorn is found regardless of PATH
    exec /opt/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8099
else
    bashio::log.error "FEHLER: Backend-Verzeichnis nicht gefunden. Ist das Projekt vollständig?"
    exit 1
fi
