# Neo42 MCP Server – AI-Driven ESM & UEM Orchestration

Dieses Projekt ist ein hochmoderner **Model Context Protocol (MCP) Server**, der speziell für die Anforderungen von **Neo42** entwickelt wurde. Er kombiniert die Power von **Gemini 1.5 Flash**, **LangGraph** und **MCP**, um eine intelligente Schnittstelle für das Matrix42-Ökosystem zu schaffen.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange)](https://modelcontextprotocol.io)

## 🚀 Key Features & Business Logic

Der Server bietet fortschrittliche Tools, die weit über einfache Datenbankabfragen hinausgehen:

### 🛠 Business Automation
- **Automatisches Onboarding**: Ein einziger Befehl initiiert den kompletten Onboarding-Prozess – von der Personalanlage in Matrix42 über die Hardware-Reservierung bis hin zur Software-Zuweisung (IT vs. Sales Profile).
- **Lizenz-Optimierung (Reclamation)**: Identifiziert ungenutzte Software-Lizenzen (Inaktivität > 30 Tage), um proaktiv Kosten zu senken und die Compliance sicherzustellen.

### 📊 Multi-Source Data Integration
- **Hybrid Database Engine**: Kombiniert strukturierte Asset-Daten aus **SQLite** mit unstrukturierten Telemetrie-Logs aus **MongoDB**.
- **Real-time Telemetry**: Abfrage von CPU-Last, RAM-Verbrauch und aktiven Prozessen direkt über MongoDB-Mocks.

### 🧠 Intelligenter KI-Copilot
- **Gemini + LangGraph**: Ein KI-Agent, der den Kontext versteht. Er erkennt, ob er technische Logs analysieren, Bestände prüfen oder Lizenz-Compliance-Berichte erstellen soll.
- **Interaktives Dashboard**: Ein premium **Streamlit-Dashboard** im Neo42-Branding für die Echtzeit-Überwachung und Chat-Interaktion.

## ✨ Verfügbare MCP Tools

| Tool | Beschreibung | Datenquelle |
| :--- | :--- | :--- |
| `start_employee_onboarding` | Initiiert Workflows für neue Mitarbeiter | Logic Engine |
| `identify_reclaimable_licenses` | Findet ungenutzte Software-Lizenzen | SQLite |
| `get_server_telemetry` | Ruft Echtzeit-Leistungsdaten ab | MongoDB |
| `check_license_compliance` | Prüft Lizenzlimits vs. Installationen | SQLite |
| `check_rental_availability` | Prüft Bestände im Service Management Depot | SQLite |
| `get_package_status` | Status von Software-Deployments (APC) | SQLite |

## 🛠 Installation & Setup

1. **Repository klonen**:
   ```bash
   git clone https://github.com/MaksymDoroshenkoDCI/MPC-Server-Neo42.git
   cd MPC-Server-Neo42
   ```

2. **Setup-Skript**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install fastmcp sqlite3 mongomock streamlit pandas plotly langchain-google-genai langgraph
   ```

3. **Datenbanken initialisieren**:
   ```bash
   python3 database.py
   ```

4. **Dashboard starten**:
   ```bash
   streamlit run app.py
   ```

## 🎯 Vision
Dieser Prototyp demonstriert, wie Neo42-Kunden durch den Einsatz von KI-Agenten die operative Effizienz steigern können. Er transformiert komplexe ESM-Daten in handlungsorientierte Erkenntnisse.

---
**Entwickelt von [Maksym Doroshenko](https://github.com/MaksymDoroshenkoDCI)**
