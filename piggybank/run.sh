#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "==================================================="
bashio::log.info " Starte Piggybank Taschengeld-Tracker Add-on..."
bashio::log.info "==================================================="

DATA_DIR="/data"
export DB_PATH="sqlite:///${DATA_DIR}/piggybank.db"

bashio::log.info "Datenbank wird gespeichert in: ${DB_PATH}"

# Function to execute recurring transactions
# Runs twice daily (every 12 hours) to check for due recurring transactions
execute_recurring() {
    while true; do
        sleep 43200  # Check every 12 hours (2x daily)
        bashio::log.info "Prüfe fällige wiederkehrende Transaktionen..."
        /opt/venv/bin/python3 -c "
import requests
try:
    response = requests.post('http://localhost:8099/api/recurring/execute')
    if response.status_code == 200:
        data = response.json()
        if data.get('executed', 0) > 0:
            print(f'Executed {data[\"executed\"]} recurring transactions')
        else:
            print('No due recurring transactions')
    else:
        print(f'Error: {response.status_code}')
except Exception as e:
    print(f'Error checking recurring: {e}')
" || true
    done
}

if [ -d "/app/backend" ]; then
    cd /app/backend

    # Start recurring transaction checker in background
    bashio::log.info "Starte Hintergrundprozess für wiederkehrende Transaktionen..."
    execute_recurring &

    bashio::log.info "Starte Uvicorn auf Port 8099..."
    # Use explicit venv path to ensure uvicorn is found regardless of PATH
    exec /opt/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8099
else
    bashio::log.error "FEHLER: Backend-Verzeichnis nicht gefunden. Ist das Projekt vollständig?"
    exit 1
fi
