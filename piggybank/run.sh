#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "==================================================="
bashio::log.info " Starte Piggybank Taschengeld-Tracker Add-on..."
bashio::log.info "==================================================="

DATA_DIR="/data"
export DB_PATH="sqlite:///${DATA_DIR}/piggybank.db"

bashio::log.info "Datenbank wird gespeichert in: ${DB_PATH}"

# Function to execute due recurring transactions using curl
execute_recurring() {
    bashio::log.info "Prüfe fällige wiederkehrende Transaktionen..."
    response=$(curl -s -X POST http://localhost:8099/api/recurring/execute)
    if [ $? -eq 0 ]; then
        executed=$(echo "$response" | grep -o '"executed":[0-9]*' | cut -d: -f2)
        if [ -n "$executed" ] && [ "$executed" -gt 0 ]; then
            bashio::log.info "Es wurden $executed wiederkehrende Transaktionen ausgeführt."
        else
            bashio::log.info "Keine fälligen wiederkehrenden Transaktionen gefunden."
        fi
    else
        bashio::log.error "Fehler beim Aufruf der Recurring-Execute API."
    fi
}

if [ -d "/app/backend" ]; then
    cd /app/backend

    # Execute due recurring transactions once at startup (catch up missed executions)
    bashio::log.info "Prüfe beim Start auf ausstehende Abo-Abbuchungen..."
    execute_recurring

    # Start recurring transaction checker in background (every 12 hours)
    bashio::log.info "Starte Hintergrundprozess für wiederkehrende Transaktionen (alle 12 Stunden)..."
    while true; do
        sleep 43200
        execute_recurring
    done &

    bashio::log.info "Starte Uvicorn auf Port 8099..."
    # Use explicit venv path to ensure uvicorn is found regardless of PATH
    exec /opt/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8099
else
    bashio::log.error "FEHLER: Backend-Verzeichnis nicht gefunden. Ist das Projekt vollständig?"
    exit 1
fi
