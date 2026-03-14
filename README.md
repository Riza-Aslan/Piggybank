# 🐷 Piggybank - Taschengeld-Tracker für Home Assistant

[![Build](https://github.com/Riza-Aslan/Piggybank/actions/workflows/build.yaml/badge.svg)](https://github.com/Riza-Aslan/Piggybank/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/Riza-Aslan/Piggybank)](LICENSE)

Ein modernes Taschengeld-Tracking-System als Home Assistant Add-on. Verwalte die Taschengeld-Konten deiner Familie mit einer schönen, responsiven Web-Oberfläche.

![Piggybank Screenshot](https://via.placeholder.com/800x400/6366f1/ffffff?text=Piggybank+Dashboard)

## ✨ Features

- **Mehrere Konten** - Verwalte separate Konten für jedes Familienmitglied
- **Einnahmen & Ausgaben** - Buche Taschengeld und Ausgaben mit Notizen
- **Übersichtliches Dashboard** - Alle Konten auf einen Blick mit aktuellem Saldo
- **Monatsstatistiken** - Einnahmen und Ausgaben pro Monat
- **Interaktive Charts** - Visualisiere die Saldo-Entwicklung über Zeit
- **Historie & Suche** - Durchsuche alle Buchungen, filtere nach Datum und Konto
- **Dunkelmodus** - Schone deine Augen beim Abend-Check
- **Import/Export** - Sichere und wiederherstelle deine Daten als JSON
- **Home Assistant Integration** - REST-Sensoren für Dashboards

## 🚀 Installation als Home Assistant Add-on

### Voraussetzungen

- Home Assistant (Core oder OS)
- Docker (wird von HA mitgebracht)
- Zugriff auf das Dateisystem (z.B. via Samba oder SSH)

### Schritt 1: Repository hinzufügen

1. Öffne Home Assistant
2. Gehe zu **Einstellungen** → **Add-ons** → **Add-on-Store** (unten rechts die 3 Punkte)
3. Klicke auf **Repository hinzufügen**
4. Füge diese URL ein:
   ```
   https://github.com/Riza-Aslan/Piggybank
   ```
5. Klicke auf **Hinzufügen**

### Schritt 2: Add-on installieren

1. Aktualisiere die Add-on-Liste
2. Suche nach **Piggybank**
3. Klicke auf das Add-on und dann auf **Installieren**
4. Warte bis die Installation abgeschlossen ist

### Schritt 3: Add-on starten

1. Klicke auf **Starten**
2. Aktiviere **Watchdog** für automatische Neustarts
3. Aktiviere **Auto-Start** falls gewünscht
4. Öffne die Web-Oberfläche über den **Open Web UI** Button

## 📊 Home Assistant Integration

Piggybank stellt automatisch REST-Sensoren bereit, die du in Home Assistant verwenden kannst.

### Sensor-URL

Wenn du das Add-on über die Home Assistant-Oberfläche öffnest (Ingress), ist die URL:

```
http://<HA-IP>:8099/api/sensors
```

Falls du Ingress verwendest (empfohlen), kannst du auch die interne URL nutzen:

```
http://localhost:8099/api/sensors
```

### Beispiel-Antwort

```json
{
  "emma": 45.50,
  "max": 12.75,
  "lisa": -5.00
}
```

### REST-Sensor konfigurieren

Füge folgendes zu deiner `configuration.yaml` hinzu:

```yaml
rest:
  - scan_interval: 60
    resource: http://localhost:8099/api/sensors
    sensor:
      - name: "Taschengeld Emma"
        value_template: "{{ value_json.emma }}"
        unit_of_measurement: "€"
        icon: mdi:piggy-bank
        
      - name: "Taschengeld Max"
        value_template: "{{ value_json.max }}"
        unit_of_measurement: "€"
        icon: mdi:piggy-bank
        
      - name: "Taschengeld Lisa"
        value_template: "{{ value_json.lisa }}"
        unit_of_measurement: "€"
        icon: mdi:piggy-bank
```

Nach einem Neustart von Home Assistant stehen die Sensoren zur Verfügung.

### Dashboard-Karte erstellen

#### Einfache Entities-Karte

```yaml
type: entities
title: 🐷 Taschengeld
entities:
  - entity: sensor.taschengeld_emma
    name: Emma
  - entity: sensor.taschengeld_max
    name: Max
  - entity: sensor.taschengeld_lisa
    name: Lisa
```

#### Schöne Glance-Karte mit Farben

```yaml
type: glance
title: 🐷 Taschengeld
entities:
  - entity: sensor.taschengeld_emma
    name: Emma
  - entity: sensor.taschengeld_max
    name: Max
  - entity: sensor.taschengeld_lisa
    name: Lisa
```

#### Fortgeschrittene Karte mit bedingten Farben

```yaml
type: custom:button-card
entity: sensor.taschengeld_emma
name: Emma
icon: mdi:piggy-bank
show_state: true
state:
  - value: 0
    operator: ">="
    color: green
  - value: 0
    operator: "<"
    color: red
```

#### Markdown-Karte mit allen Konten

```yaml
type: markdown
content: |
  ## 🐷 Taschengeld-Übersicht
  
  | Kind | Kontostand |
  |------|------------|
  | Emma | {{ states('sensor.taschengeld_emma') }} € |
  | Max  | {{ states('sensor.taschengeld_max') }} € |
  | Lisa | {{ states('sensor.taschengeld_lisa') }} € |
```

### Automatisierung: Benachrichtigung bei negativem Saldo

```yaml
automation:
  - alias: "Taschengeld Negativ-Warnung"
    trigger:
      - platform: numeric_state
        entity_id: sensor.taschengeld_emma
        below: 0
    action:
      - service: notify.mobile_app_dein_telefon
        data:
          title: "🐷 Taschengeld-Warnung"
          message: "Emma hat ein negatives Kontostand: {{ states('sensor.taschengeld_emma') }} €"
```

## 🛠️ Entwicklung

### Lokal starten

```bash
# Backend
cd piggybank/backend
pip install -r requirements.txt
python main.py

# Frontend (in neuem Terminal)
cd piggybank/frontend
npm install
npm run dev
```

### Docker Build

```bash
cd piggybank
docker build -t piggybank .
docker run -p 8099:8099 piggybank
```

## 📁 Projektstruktur

```
Piggybank/
├── .github/workflows/    # GitHub Actions CI/CD
├── piggybank/
│   ├── backend/          # FastAPI Backend
│   │   ├── api.py        # REST API Endpoints
│   │   ├── database.py   # SQLAlchemy Datenbank
│   │   ├── models.py     # Datenbank-Modelle
│   │   └── schemas.py    # Pydantic Schemas
│   ├── frontend/         # Vue 3 Frontend
│   │   └── src/
│   │       └── App.vue   # Hauptkomponente
│   ├── Dockerfile        # Multi-Stage Build
│   └── run.sh            # Startskript
└── README.md
```

## 🔧 API Endpoints

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| GET | `/api/accounts/` | Alle Konten abrufen |
| POST | `/api/accounts/` | Neues Konto erstellen |
| DELETE | `/api/accounts/{id}` | Konto löschen |
| GET | `/api/transactions/` | Alle Buchungen abrufen |
| POST | `/api/transactions/` | Neue Buchung erstellen |
| DELETE | `/api/transactions/{id}` | Buchung löschen |
| GET | `/api/sensors` | HA-Sensoren (JSON) |
| GET | `/api/export` | Daten exportieren |
| POST | `/api/import` | Daten importieren |

## 🤝 Beitrag

Beiträge sind willkommen! Erstelle einfach einen Pull Request.

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/amazing-feature`)
3. Committe deine Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Erstelle einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert. Siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagung

- [FastAPI](https://fastapi.tiangolo.com/) - Modernes Python Web Framework
- [Vue.js](https://vuejs.org/) - Progressive JavaScript Framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-First CSS Framework
- [Home Assistant](https://www.home-assistant.io/) - Open Source Home Automation

---

Made with ❤️ for families who want to teach their kids about money.
