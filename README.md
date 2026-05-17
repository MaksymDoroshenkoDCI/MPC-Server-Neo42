# Neo42 MCP Server – AI-Driven ESM & UEM Orchestration

Dieses Projekt ist ein hochmoderner **Model Context Protocol (MCP) Server**, der speziell für die Anforderungen von **Neo42** entwickelt wurde. Er kombiniert die Power von **Gemini 2.5 Flash**, **LangGraph** und **MCP**, um eine intelligente, hochsichere Schnittstelle für das Matrix42-Ökosystem zu schaffen. 

Das gesamte System ist **vollständig dockerisiert** und läuft **live auf Google Cloud Platform (GCP) Cloud Run** unter einem globalen HTTPS-Endpunkt!

🌐 **Live-Demo:** [https://neo42-mcp-app-306318571213.europe-west3.run.app](https://neo42-mcp-app-306318571213.europe-west3.run.app)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![GCP Cloud Run](https://img.shields.io/badge/GCP-Cloud%20Run-green.svg)](https://cloud.google.com/run)

---

## 🚀 Key Features & Business Logic

Der Server bietet fortschrittliche Tools, die weit über einfache Datenbankabfragen hinausgehen:

### 🛠 Business Automation & ESM
- **Automatisches Onboarding (`start_employee_onboarding`)**: Ein einziger Befehl initiiert den kompletten Onboarding-Prozess – von der Personalanlage über die Hardware-Reservierung bis hin zur passgenauen Software-Zuweisung (IT vs. Sales Profile).
- **Lizenz-Optimierung (Reclamation) (`identify_reclaimable_licenses`)**: Identifiziert inaktive Software-Lizenzen (Inaktivität > 30 Tage) und bereitet die Lizenzrückgabe proaktiv vor.

### 🛡 Security & Incident Management
- **Automatische Ticket-Erstellung (`create_incident_ticket`)**: Ermöglicht dem KI-Agenten, bei Erkennung eines Deployment-Fehlers oder Lizenzkonflikts automatisch ein Incident-Ticket im Matrix42 Service Desk zu erstellen.
- **CVE Schwachstellen-Scanner (`check_cve_vulnerabilities`)**: Scannt installierte Softwarepakete live gegen eine simulierte CVE-Datenbank (Common Vulnerabilities and Exposures), um bekannte Sicherheitslücken sofort aufzudecken.

### 📊 Multi-Source Data Integration
- **Hybrid Database Engine**: Kombiniert strukturierte Asset-Daten aus **SQLite** mit unstrukturierten Telemetrie-Logs aus **MongoDB**.
- **Real-time Telemetry (`get_server_telemetry`)**: Abfrage von CPU-Last, RAM-Verbrauch und aktiven Prozessen direkt aus MongoDB-Mocks.

### 🎨 Premium Dark Edition UI (Streamlit)
- **Modernes Dark-Branding**: Elegantes, tiefschwarzes UI (`#0b0c10`) mit roten Akzenten im Neo42-Design.
- **Out-of-the-box Responsive & Interactive**:
  - Interaktive KPI-Karten, die auf Hover reagieren (CSS-Transformation).
  - Ästhetische, transparente Plotly-Diagramme, die sich nahtlos in die dunkle Oberfläche integrieren.
  - Ein hochoptimiertes Chat-Interface mit kontraststarkem, reinweißem Text für perfekte Lesbarkeit.

---

## ✨ Verfügbare MCP Tools (8 Tools)

| Tool | Beschreibung | Datenquelle |
| :--- | :--- | :--- |
| `start_employee_onboarding` | Initiiert automatisierte Workflows für neue Mitarbeiter | Logic Engine |
| `identify_reclaimable_licenses` | Findet ungenutzte Software-Lizenzen zur Kosteneinsparung | SQLite |
| `create_incident_ticket` | Erstellt ein Incident-Ticket im Matrix42 Service Desk | Service Desk |
| `check_cve_vulnerabilities` | Scannt Softwarepakete auf bekannte Sicherheitslücken (CVEs) | CVE-DB |
| `get_server_telemetry` | Ruft Echtzeit-Leistungsdaten (CPU, RAM) ab | MongoDB |
| `check_license_compliance` | Prüft Lizenzlimits vs. aktive Installationen | SQLite |
| `check_rental_availability` | Prüft Bestände im Service Management Depot (Leihgeräte) | SQLite |
| `get_package_status` | Zeigt den aktuellen Status von Software-Deployments (APC) | SQLite |

---

## 🛠 Setup & Installation

### Option 1: Lokales Ausführen (Python)

1. **Repository klonen**:
   ```bash
   git clone https://github.com/MaksymDoroshenkoDCI/MPC-Server-Neo42.git
   cd MPC-Server-Neo42
   ```

2. **Abhängigkeiten installieren**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Datenbank initialisieren & starten**:
   ```bash
   python3 database.py
   streamlit run app.py
   ```

### Option 2: Docker (Empfohlen für Produktion)

1. **Docker-Image lokal bauen**:
   ```bash
   docker build -t neo42-mcp-app .
   ```

2. **Container ausführen** (mit Ihrem Google Gemini API Key):
   ```bash
   docker run -p 8080:8080 -e GOOGLE_API_KEY=IHR_GEMINI_API_KEY neo42-mcp-app
   ```

---

## ☁️ GCP Deployment (Cloud Run)

Der Prototyp wird direkt über die Google Cloud CLI (gcloud) unter Verwendung von **Docker** und **GCP Artifact Registry** verwaltet:

1. **Repository in GCP erstellen**:
   ```bash
   gcloud artifacts repositories create neo42-mcp-repo --repository-format=docker --location=europe-west3
   ```

2. **Lokal bauen, taggen & pushen**:
   ```bash
   docker build -t neo42-mcp-app .
   docker tag neo42-mcp-app europe-west3-docker.pkg.dev/project-45ad5a31-e1e9-4b68-b3c/neo42-mcp-repo/neo42-mcp-app:latest
   docker push europe-west3-docker.pkg.dev/project-45ad5a31-e1e9-4b68-b3c/neo42-mcp-repo/neo42-mcp-app:latest
   ```

3. **In Cloud Run bereitstellen**:
   ```bash
   gcloud run deploy neo42-mcp-app --image=europe-west3-docker.pkg.dev/project-45ad5a31-e1e9-4b68-b3c/neo42-mcp-repo/neo42-mcp-app:latest --port 8080 --allow-unauthenticated --region europe-west3
   ```

---

## 🎯 Fazit & Interview-Relevanz
Dieses Projekt demonstriert tiefes Verständnis für **moderne AI-Infrastrukturen**, **Modulares API-Design (MCP)**, **Docker-Containerisierung** und **Cloud-Native-Deployments (GCP)**. Es spiegelt die Vision von **Neo42** wider: Die Automatisierung von IT-Prozessen auf das nächste Level zu heben!

---
**Entwickelt von [Maksym Doroshenko](https://github.com/MaksymDoroshenkoDCI)**
