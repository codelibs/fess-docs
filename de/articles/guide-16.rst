============================================================
Teil 16: Automatisierung der Suchinfrastruktur -- Verwaltung mit CI/CD-Pipelines und Infrastructure as Code
============================================================

Einleitung
==========

Wenn die Konfiguration eines Suchsystems manuell verwaltet wird, wird die Reproduktion von Umgebungen schwierig und das Risiko von Konfigurationsfehlern steigt.
Durch die Anwendung moderner DevOps-Methoden sollten Sie auch die Suchinfrastruktur als Code verwalten und automatisieren.

In diesem Artikel wird ein Ansatz vorgestellt, wie Sie Fess-Konfigurationen als Code verwalten und Deployments automatisieren.

Zielgruppe
==========

- Personen, die den Betrieb von Suchsystemen automatisieren moechten
- Personen, die DevOps/IaC-Methoden auf die Suchinfrastruktur anwenden moechten
- Personen mit Grundkenntnissen in Docker und CI/CD

Anwendung von Infrastructure as Code
======================================

Die folgenden Elemente werden fuer Fess-Umgebungen als "Code" verwaltet.

.. list-table:: IaC-Verwaltungsobjekte
   :header-rows: 1
   :widths: 25 35 40

   * - Objekt
     - Verwaltungsmethode
     - Versionskontrolle
   * - Docker-Konfiguration
     - compose.yaml
     - Git
   * - Fess-Einstellungen
     - Backup-Dateien / Admin-API
     - Git
   * - Woerterbuchdaten
     - Export ueber Admin-API
     - Git
   * - OpenSearch-Einstellungen
     - Konfigurationsdateien
     - Git

Umgebungsdefinition mit Docker Compose
========================================

Docker-Compose-Datei fuer die Produktionsumgebung
---------------------------------------------------

Wir erweitern die in Teil 2 verwendete Grundkonfiguration und definieren eine fuer Produktionsumgebungen geeignete Konfiguration.

.. code-block:: yaml

    services:
      fess:
        image: ghcr.io/codelibs/fess:15.5.1
        environment:
          - SEARCH_ENGINE_HTTP_URL=http://opensearch:9200
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        ports:
          - "8080:8080"
        depends_on:
          opensearch:
            condition: service_healthy
        restart: unless-stopped

      opensearch:
        image: ghcr.io/codelibs/fess-opensearch:3.6.0
        environment:
          - discovery.type=single-node
          - OPENSEARCH_JAVA_OPTS=-Xmx4g -Xms4g
          - DISABLE_INSTALL_DEMO_CONFIG=true
          - DISABLE_SECURITY_PLUGIN=true
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        volumes:
          - opensearch-data:/usr/share/opensearch/data
          - opensearch-dictionary:/usr/share/opensearch/config/dictionary
        healthcheck:
          test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
          interval: 30s
          timeout: 10s
          retries: 3
          start_period: 90s
        restart: unless-stopped

    volumes:
      opensearch-data:
      opensearch-dictionary:

Die wichtigsten Punkte sind die folgenden.

- Health-Check-Definition: Fess wird erst gestartet, wenn OpenSearch bereit ist
- Volume-Persistenz: Daten werden dauerhaft gespeichert
- Neustartrichtlinie: Automatische Wiederherstellung bei Ausfaellen
- Explizite Konfiguration des JVM-Heaps

Automatisierung der Konfiguration mit der Admin-API
=====================================================

Durch die Verwendung der Fess-Admin-API koennen Sie Konfigurationen programmatisch verwalten, ohne die GUI zu verwenden.

Einstellungen exportieren
--------------------------

Exportieren Sie die aktuellen Fess-Einstellungen und speichern Sie sie als Code.

Sie koennen den Export ueber die Administrationskonsole unter [Systeminformationen] > [Backup] durchfuehren.
Es ist auch moeglich, den Export ueber Skripte mit der Admin-API durchzufuehren.

Einstellungen importieren
--------------------------

Wenden Sie Einstellungen auf eine neue Fess-Umgebung an, indem Sie gespeicherte Konfigurationsdateien verwenden.
Dies erleichtert die Wiederherstellung oder Replikation von Umgebungen.

Verwendung der fessctl-CLI
============================

fessctl ist ein Kommandozeilenwerkzeug fuer Fess.
Viele Operationen, die in der Administrationskonsole durchgefuehrt werden koennen, lassen sich auch ueber die Kommandozeile ausfuehren.

Hauptoperationen
-----------------

- Erstellen, Aktualisieren und Loeschen von Crawl-Einstellungen (Web, Dateisystem, Datenspeicher)
- Ausfuehren von Scheduler-Jobs
- Verwaltung von Benutzern, Rollen und Gruppen
- Verwaltung von Sucheinstellungen wie Key Match, Labels und Boosts

Durch die Verwendung der CLI koennen Sie Konfigurationsaenderungen skripten und in CI/CD-Pipelines integrieren.

Aufbau von CI/CD-Pipelines
============================

Workflow fuer Konfigurationsaenderungen
-----------------------------------------

Verwalten Sie Konfigurationsaenderungen des Suchsystems mit dem folgenden Workflow.

1. **Aenderung**: Konfigurationsdateien aendern und in einem Git-Branch verwalten
2. **Review**: Aenderungen ueber Pull Requests ueberpruefen
3. **Test**: Verhalten in einer Staging-Umgebung verifizieren
4. **Deployment**: Einstellungen in der Produktionsumgebung anwenden

Automatisierungsbeispiel mit GitHub Actions
---------------------------------------------

Dies ist ein Beispiel fuer die automatische Anwendung von Aenderungen in der Produktionsumgebung, wenn Konfigurationsdateiaenderungen gemergt werden.

.. code-block:: yaml

    name: Deploy Fess Config
    on:
      push:
        branches: [main]
        paths:
          - 'fess-config/**'
          - 'dictionary/**'

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Apply dictionary updates
            run: |
              # Woerterbuchdateien an den Fess-Server uebertragen
              scp dictionary/* fess-server:/opt/fess/dictionary/

          - name: Verify Fess health
            run: |
              # Betriebsstatus von Fess ueber die Health-API pruefen
              curl -s https://fess.example.com/api/v1/health

Automatisierung von Backups
=============================

Automatisieren Sie auch regelmaessige Backups.

Backup-Skript
--------------

Verwenden Sie cron oder CI/CD-Planungsfunktionen, um regelmaessige Backups zu erstellen.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    BACKUP_DIR="/backup/fess/$(date +%Y%m%d)"
    mkdir -p "${BACKUP_DIR}"

    # Liste der Fess-Backup-Dateien abrufen
    curl -s -o "${BACKUP_DIR}/fess-backup-files.json" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/files"

    # Konfigurationsdaten herunterladen (z.B. fess_config.bulk)
    curl -s -o "${BACKUP_DIR}/fess_config.bulk" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/file/fess_config.bulk"

    # Alte Backups loeschen (aelter als 30 Tage)
    find /backup/fess -type d -mtime +30 -exec rm -rf {} +

    echo "Backup completed: ${BACKUP_DIR}"

Verfahren zur Umgebungsrekonstruktion
=======================================

Dokumentieren Sie das Verfahren zur vollstaendigen Rekonstruktion einer Umgebung fuer die Notfallwiederherstellung oder den Aufbau von Testumgebungen.

1. Container mit Docker Compose starten
2. Warten, bis der OpenSearch-Health-Check green/yellow zurueckgibt
3. Fess-Einstellungen importieren (ueber Admin-API oder Wiederherstellungsfunktion)
4. Woerterbuchdateien platzieren
5. Crawl-Jobs ausfuehren
6. Betrieb verifizieren (Suchtests)

Wenn Sie dieses Verfahren skripten, koennen Sie Umgebungen schnell rekonstruieren.

Zusammenfassung
================

In diesem Artikel wurde ein Ansatz vorgestellt, wie Sie die Fess-Suchinfrastruktur mit DevOps-Methoden verwalten koennen.

- Kodifizierung von Umgebungsdefinitionen mit Docker Compose
- Automatisierung der Konfiguration mit der Admin-API und fessctl
- Automatisierung des Deployments von Konfigurationsaenderungen mit CI/CD-Pipelines
- Automatisierung von Backups und Verfahren zur Umgebungsrekonstruktion

Entwickeln Sie den Betrieb Ihrer Suchinfrastruktur von "Handbuecher lesen und manuell konfigurieren" zu "Code ausfuehren und automatisch deployen" weiter.

Im naechsten Artikel wird die Erweiterung von Fess durch Plugin-Entwicklung behandelt.

Referenzen
==========

- `Fess Admin API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__
