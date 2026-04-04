#!/usr/bin/with-contenv bashio

bashio::log.info "==================================================="
bashio::log.info " Starte Piggybank Taschengeld-Tracker Add-on..."
bashio::log.info "==================================================="

DATA_DIR="/data"
export DB_PATH="sqlite:///${DATA_DIR}/piggybank.db"

# Use timezone from Home Assistant configuration (TZ environment variable)
# If not set, default to Europe/Berlin (German timezone)
if [ -z "$TZ" ]; then
    export TZ="Europe/Berlin"
    bashio::log.info "Zeitzone nicht gesetzt, verwende Default: Europe/Berlin"
else
    bashio::log.info "Verwende Zeitzone aus Home Assistant: $TZ"
fi

bashio::log.info "Datenbank wird gespeichert in: ${DB_PATH}"

# Function to execute due recurring transactions using curl
# This function NEVER fails - it only logs errors
execute_recurring() {
    bashio::log.info "Prüfe fällige wiederkehrende Transaktionen..."
    # Check if curl is available
    if ! command -v curl &> /dev/null; then
        bashio::log.error "curl ist nicht verfügbar! Überspringe wiederkehrende Transaktionen."
        return 0
    fi
    
    # Try to execute, but never fail
    response=$(curl -s -X POST --connect-timeout 5 --max-time 10 http://localhost:8099/api/recurring/execute 2>/dev/null) || {
        bashio::log.warn "Konnte keine Verbindung zu http://localhost:8099/api/recurring/execute herstellen (Server vielleicht noch nicht bereit)."
        return 0
    }
    
    # Parse response
    executed=$(echo "$response" | grep -o '"executed":[0-9]*' | cut -d: -f2 2>/dev/null)
    if [ -n "$executed" ] && [ "$executed" -gt 0 ]; then
        bashio::log.info "Es wurden $executed wiederkehrende Transaktionen ausgeführt."
    else
        bashio::log.info "Keine fälligen wiederkehrenden Transaktionen gefunden."
    fi
}

if [ -d "/app/backend" ]; then
    cd /app/backend

    # Start recurring transaction checker in background (every 12 hours)
    bashio::log.info "Starte Hintergrundprozess für wiederkehrende Transaktionen (alle 12 Stunden)..."
    (
        # Wait a bit for server to start before first check
        sleep 10
        while true; do
            execute_recurring
            sleep 43200
        done
    ) &

    bashio::log.info "Starte Uvicorn auf Port 8099..."
    # Use python3 from PATH (Home Assistant provides it) or fallback to explicit path
    if [ -x "/opt/venv/bin/python3" ]; then
        PYTHON_CMD="/opt/venv/bin/python3"
    else
        PYTHON_CMD="python3"
    fi
    
    # Check if uvicorn is available
    if $PYTHON_CMD -c "import uvicorn" 2>/dev/null; then
        exec $PYTHON_CMD -m uvicorn main:app --host 0.0.0.0 --port 8099
    else
        bashio::log.error "Uvicorn ist nicht installiert oder nicht verfügbar!"
        exit 1
    fi
else
    bashio::log.error "FEHLER: Backend-Verzeichnis nicht gefunden. Ist das Projekt vollständig?"
    exit 1
fi
