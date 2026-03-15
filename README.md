# 🐷 Piggybank - Gemeinsames Budget-Tracker für Home Assistant

[![Build](https://github.com/Riza-Aslan/Piggybank/actions/workflows/build.yaml/badge.svg)](https://github.com/Riza-Aslan/Piggybank/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/Riza-Aslan/Piggybank)](LICENSE)

Ein modernes Budget-Tracking-System als Home Assistant Add-on für Paare und Familien. Verwalte gemeinsame Konten und teile verbleibendes Budget fair auf – damit jeder sein Hobby ohne schlechtes Gewissen genießen kann!

![Piggybank Screenshot](https://via.placeholder.com/800x400/6366f1/ffffff?text=Piggybank+Dashboard)

## 💡 Use Case

**Das Problem:** Ihr teilt euch Bankkonten und nach allen monatlichen Ausgaben bleibt etwas Geld übrig. Das wollt ihr für eure Hobbies ausgeben – aber wer gibt wie viel aus?

**Die Lösung:** Piggybank! Tragt den verbleibenden Betrag ein, teilt ihn fair auf und jeder kann seinen Teil für Hobbies, Technik, Kosmetik oder was auch immer ausgeben – ganz ohne schlechtes Gewissen. Bezahlt wird einfach per Kreditkarte oder Bar vom gemeinsamen Konto.

### Beispiel

1. Monatlich bleiben nach allen Fixkosten **300€** übrig
2. Ihr teilt es auf: **150€ für dich**, **150€ für deinen Partner**
3. Du kaufst dir für **80€** neue Kopfhörer → Dein Budget: **70€**
4. Dein Partner kauft für **120€** Sportausrüstung → Budget: **30€**
5. Am Monatsende seht ihr genau, wer wie viel ausgegeben hat

## 🔄 Abonnements (Abos)

Verwalte wiederkehrende Ausgaben wie Streaming-Dienste, Mitgliedschaften oder andere Abonnements. Diese werden automatisch vom Budget abgezogen.

### Unterstützte Intervalle

- **Täglich** - Für tägliche Ausgaben
- **Wöchentlich** - Für wöchentliche Dienste
- **Monatlich** - Für monatliche Abonnements (Netflix, Spotify, etc.)
- **Vierteljährlich** - Für quartalsweise Zahlungen

### Automatische Ausführung

Abonnements werden automatisch ausgeführt, wenn sie fällig sind. Die App prüft regelmäßig und erstellt die entsprechenden Buchungen.

## ✨ Features

- **👥 Mehrere Konten** - Verwalte separate Konten für dich, deinen Partner oder die ganze Familie
- **💰 Budget-Zuweisung** - Trage verbleibendes Geld ein und teile es fair auf
- **📊 Einnahmen & Ausgaben** - Buche Budget-Zuweisungen und Ausgaben mit Notizen
- **🔄 Abonnements (Abos)** - Verwalte wiederkehrende Ausgaben wie Streaming-Dienste, Mitgliedschaften etc. – werden automatisch vom Budget abgezogen
- **📈 Jahresübersicht** - Prognostiziere die Budget-Entwicklung über das ganze Jahr
- **🎨 Übersichtliches Dashboard** - Alle Konten auf einen Blick mit aktuellem Saldo
- **📉 Monatsstatistiken** - Einnahmen und Ausgaben pro Monat
- **🔍 Historie & Suche** - Durchsuche alle Buchungen, filtere nach Datum und Konto
- **🌙 Dunkelmodus** - Schone deine Augen beim Abend-Check
- **💾 Import/Export** - Sichere und wiederherstelle deine Daten als JSON
- **🏠 Home Assistant Integration** - REST-Sensoren für Dashboards und Automatisierungen

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
  "ich": 150.00,
  "partner": 150.00
}
```

### REST-Sensor konfigurieren

Füge folgendes zu deiner `configuration.yaml` hinzu:

```yaml
rest:
  - scan_interval: 60
    resource: http://localhost:8099/api/sensors
    sensor:
      - name: "Mein Hobby-Budget"
        value_template: "{{ value_json.ich }}"
        unit_of_measurement: "€"
        icon: mdi:piggy-bank
        
      - name: "Partner Hobby-Budget"
        value_template: "{{ value_json.partner }}"
        unit_of_measurement: "€"
        icon: mdi:piggy-bank
```

Nach einem Neustart von Home Assistant stehen die Sensoren zur Verfügung.

### Dashboard-Karte erstellen

#### Einfache Entities-Karte

```yaml
type: entities
title: 🐷 Hobby-Budget
entities:
  - entity: sensor.mein_hobby_budget
    name: Mein Budget
  - entity: sensor.partner_hobby_budget
    name: Partner Budget
```

#### Schöne Glance-Karte mit Farben

```yaml
type: glance
title: 🐷 Hobby-Budget
entities:
  - entity: sensor.mein_hobby_budget
    name: Mein Budget
  - entity: sensor.partner_hobby_budget
    name: Partner Budget
```

#### Fortgeschrittene Karte mit bedingten Farben

```yaml
type: custom:button-card
entity: sensor.mein_hobby_budget
name: Mein Budget
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
  ## 🐷 Hobby-Budget Übersicht
  
  | Person | Verfügbares Budget |
  |--------|-------------------|
  | Ich    | {{ states('sensor.mein_hobby_budget') }} € |
  | Partner| {{ states('sensor.partner_hobby_budget') }} € |
```

### Automatisierung: Benachrichtigung bei niedrigem Budget

```yaml
automation:
  - alias: "Hobby-Budget Warnung"
    trigger:
      - platform: numeric_state
        entity_id: sensor.mein_hobby_budget
        below: 20
    action:
      - service: notify.mobile_app_dein_telefon
        data:
          title: "🐷 Budget-Warnung"
          message: "Dein Hobby-Budget ist fast aufgebraucht: {{ states('sensor.mein_hobby_budget') }} €"
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
| GET | `/api/accounts/{id}` | Konto mit Buchungen abrufen |
| DELETE | `/api/accounts/{id}` | Konto löschen |
| GET | `/api/transactions/` | Alle Buchungen abrufen |
| POST | `/api/transactions/` | Neue Buchung erstellen |
| PUT | `/api/transactions/{id}` | Buchung aktualisieren |
| DELETE | `/api/transactions/{id}` | Buchung löschen |
| GET | `/api/recurring/` | Alle Abonnements abrufen |
| POST | `/api/recurring/` | Neues Abo erstellen |
| PUT | `/api/recurring/{id}` | Abo aktualisieren |
| DELETE | `/api/recurring/{id}` | Abo löschen |
| POST | `/api/recurring/execute` | Fällige Abos ausführen |
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
