# Neo42 MCP Server – Application Package Center & ESM Integration

Dieses Projekt ist ein **Model Context Protocol (MCP) Server**, der speziell für die Ökosysteme von **Neo42** entwickelt wurde. Er ermöglicht KI-Agenten (wie Claude oder LangGraph-basierte Bots), direkt mit dem **Application Package Center (APC)** und dem **Service Management Depot (SMD)** zu interagieren.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange)](https://modelcontextprotocol.io)

## 🚀 Überblick

Der Neo42 MCP Server schließt die Lücke zwischen Large Language Models (LLMs) und der internen IT-Infrastrukturverwaltung. Anstatt manuell in Dashboards zu suchen, können Support-Mitarbeiter oder Kunden einfach natürliche Sprache verwenden, um komplexe Abfragen zu Deployment-Status, Inventar oder Lizenz-Compliance zu stellen.

## ✨ Hauptfunktionen

### 📦 Application Package Center (APC)
- **Deployment-Status**: Abfrage des Echtzeit-Status von Softwarepaketen auf spezifischen Endpoints (z. B. "Ist Google Chrome auf SRV-PROD-01 erfolgreich installiert?").
- **Server-Inventar**: Auflistung aller verwalteten Pakete auf einem bestimmten Host.
- **Paketsuche**: Schnelles Auffinden von verfügbaren Softwarepaketen im Repository.

### 🏢 Service Management Depot (SMD) Integration
- **Asset Rental Management**: Prüfung der Verfügbarkeit von Leihgeräten wie Hochleistungs-Notebooks, Beamern oder Testgeräten.
- **Lizenz-Compliance**: Automatisierter Abgleich zwischen installierten Software-Instanzen und erworbenen Lizenzen, um Überlizenzierung oder Compliance-Risiken zu vermeiden.

### 🤖 KI-Ready
- Volle Kompatibilität mit **LangGraph** für komplexe Workflow-Automatisierung.
- Nahtlose Integration in die **Claude Desktop App**.

## 🛠 Technologie-Stack
- **Sprache**: Python 3.10+
- **Framework**: [FastMCP](https://github.com/jlowin/fastmcp)
- **Datenbank**: SQLite (Mocking des Neo42 Backends)
- **Protokoll**: Model Context Protocol (MCP)

## 📦 Installation & Setup

1. **Repository klonen**:
   ```bash
   git clone https://github.com/MaksymDoroshenkoDCI/MPC-Server-Neo42.git
   cd MPC-Server-Neo42
   ```

2. **Virtuelle Umgebung erstellen**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Abhängigkeiten installieren**:
   ```bash
   pip install fastmcp sqlite3
   ```

4. **Datenbank initialisieren**:
   ```bash
   python3 database.py
   ```

## 🖥 Nutzung

### MCP Server starten
```bash
python3 server.py
```

### Demo-Client ausführen
Um die Tools in Aktion zu sehen, starten Sie den mitgelieferten Demo-Client:
```bash
python3 client_demo.py
```

## ⚙️ Konfiguration für Claude Desktop

Fügen Sie Folgendes zu Ihrer `claude_desktop_config.json` hinzu:

```json
{
  "mcpServers": {
    "neo42-server": {
      "command": "/PFAD/ZU/DEINEM/VENV/bin/python",
      "args": ["/PFAD/ZU/DEINEM/PROJEKT/server.py"]
    }
  }
}
```

## 🎯 Warum dieses Projekt?
Dieses Projekt wurde als technisches Demo für **Neo42** entwickelt, um das Potenzial von KI-gestütztem Enterprise Service Management (ESM) zu demonstrieren. Es zeigt, wie moderne Protokolle wie MCP die Effizienz im IT-Support und in der Infrastrukturverwaltung drastisch steigern können.

---
**Entwickelt von [Maksym Doroshenko](https://github.com/MaksymDoroshenkoDCI)**
