============================
Anwendungsfälle von Fess
============================

Einführung
==========

Fess wird von Organisationen verschiedener Branchen und Größenordnungen eingesetzt.
Diese Seite stellt repräsentative Anwendungsfälle und praktische Beispiele für die Bereitstellung von Fess vor.

.. note::

   Die folgenden Beispiele veranschaulichen gängige Bereitstellungsmuster für Fess.
   Für konkrete Fallstudien wenden Sie sich bitte an den `kommerziellen Support <../support-services.html>`__.

----

Branchenspezifische Anwendungsfälle
====================================

Fertigung
---------

**Herausforderung**: Konstruktionszeichnungen, technische Dokumente und Qualitätsmanagement-Unterlagen sind über mehrere Dateiserver verteilt, wodurch das Auffinden benötigter Informationen zeitaufwändig ist.

**Fess-Lösung**:

- Einheitliche Suche über CAD-Zeichnungen, technische PDF-Dokumente und Office-Dokumente auf Dateiservern
- Übergreifende Suche nach Produktmodellnummern, Zeichnungsnummern und Projektnamen
- Anzeige von Suchergebnissen basierend auf Zugriffsberechtigungen (rollenbasierte Suche)

**Architekturbeispiel**:

.. code-block:: text

    [Dateiserver]   →  [Fess]  →  [Internes Portal]
         │               │
         ├─ Zeichnungen   ├─ OpenSearch-Cluster
         ├─ Tech. Doku    └─ Active-Directory-Integration
         └─ QS-Unterlagen

**Verwandte Funktionen**:

- `Dateiserver-Crawling <https://fess.codelibs.org/de/15.5/config/config-filecrawl.html>`__
- `Rollenbasierte Suche <https://fess.codelibs.org/de/15.5/config/config-role.html>`__
- `Thumbnail-Anzeige <https://fess.codelibs.org/de/15.5/admin/admin-general.html>`__

Finanzdienstleistungen und Versicherungen
-----------------------------------------

**Herausforderung**: Compliance-Dokumente, Verträge und interne Vorschriften sind umfangreich, wodurch Audit-Reaktionen und die Bearbeitung von Anfragen zeitaufwändig sind.

**Fess-Lösung**:

- Übergreifende Suche in internen Vorschriften, Handbüchern und FAQs
- Textsuche in Verträgen und Antragsunterlagen
- Wissenssuche aus früheren Anfrageverläufen

**Sicherheitsfunktionen**:

- Authentifizierung über LDAP/Active-Directory-Integration
- Single Sign-On über SAML
- API-Authentifizierung über Zugriffstoken

**Verwandte Funktionen**:

- `LDAP-Authentifizierung <https://fess.codelibs.org/de/15.5/config/config-security.html>`__
- `SAML-Authentifizierung <https://fess.codelibs.org/de/15.5/config/config-saml.html>`__

Bildung
-------

**Herausforderung**: Forschungsarbeiten, Vorlesungsmaterialien und Campus-Dokumente sind über verschiedene Fachbereichsserver verteilt, was den Informationsaustausch erschwert.

**Fess-Lösung**:

- Einheitliche Suche vom Campus-Portal aus
- Suche im Forschungsarbeiten-Repository
- Suche in Vorlesungsmaterialien und Vorlesungsverzeichnissen

**Architekturbeispiele**:

- Crawling von Campus-Websites
- Integration mit Arbeiten-Repositorys (DSpace usw.)
- Suche in Materialien auf Google Drive / SharePoint

**Verwandte Funktionen**:

- `Web-Crawling <https://fess.codelibs.org/de/15.5/config/config-webcrawl.html>`__
- `Google-Drive-Crawling <https://fess.codelibs.org/de/15.5/config/config-crawl-gsuite.html>`__

IT und Software
---------------

**Herausforderung**: Quellcode, Dokumentation, Wikis und Informationen aus Ticket-Management-Systemen sind verstreut, was die Entwicklungseffizienz verringert.

**Fess-Lösung**:

- Code-Suche in GitHub-/GitLab-Repositorys
- Suche in Confluence-/Wiki-Seiten
- Suche in Slack-/Teams-Nachrichten

**Entwicklerfunktionen**:

- Integration in bestehende Systeme über die Such-API
- Code-Hervorhebung
- Filterung nach Dateityp

**Verwandte Funktionen**:

- `Git-Repository-Crawling <https://fess.codelibs.org/de/15.5/config/config-crawl-git.html>`__
- `Confluence-Crawling <https://fess.codelibs.org/de/15.5/config/config-crawl-atlassian.html>`__
- `Slack-Crawling <https://fess.codelibs.org/de/15.5/config/config-crawl-slack.html>`__

----

Größenabhängige Anwendungsfälle
================================

Kleine Unternehmen (KMU, bis 100 Mitarbeiter)
----------------------------------------------

**Merkmale**: Einfache Bereitstellung und Betrieb mit begrenzten IT-Ressourcen gewünscht.

**Empfohlene Konfiguration**:

- Einfache Bereitstellung über Docker Compose
- Einzelserver-Konfiguration (Fess + OpenSearch)
- Erforderlicher Arbeitsspeicher: 8 GB oder mehr

**Bereitstellungsschritte**:

.. code-block:: bash

    # Bereitstellung in 5 Minuten
    mkdir fess && cd fess
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml
    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Kosten**:

- Software: Kostenlos (Open Source)
- Nur Serverkosten (Cloud oder On-Premise)

Mittelstand (100-1000 Mitarbeiter)
----------------------------------

**Merkmale**: Nutzung durch mehrere Abteilungen, angemessene Verfügbarkeit erforderlich.

**Empfohlene Konfiguration**:

- 2 Fess-Server (Redundanz)
- 3-Knoten-OpenSearch-Cluster
- Load Balancer für die Lastverteilung
- Active-Directory-Integration

**Kapazitätsrichtlinien**:

- Dokumente: bis zu 5 Millionen
- Gleichzeitige Suchbenutzer: bis zu 100

**Verwandte Funktionen**:

- `Cluster-Konfiguration <https://fess.codelibs.org/de/15.5/install/clustering.html>`__
- `Backup und Wiederherstellung <https://fess.codelibs.org/de/15.5/admin/admin-backup.html>`__

Großunternehmen (über 1000 Mitarbeiter)
---------------------------------------

**Merkmale**: Große Datenmengen, hohe Verfügbarkeit, strenge Sicherheitsanforderungen.

**Empfohlene Konfiguration**:

- Mehrere Fess-Server (auf Kubernetes betrieben)
- OpenSearch-Cluster (dedizierte Knotenkonfiguration)
- Dedizierte Crawl-Server
- Integration in Überwachungs- und Protokollierungsinfrastruktur

**Skalierbarkeit**:

- Dokumente: Hunderte von Millionen möglich
- Horizontale Skalierung durch OpenSearch-Shard-Aufteilung

**Enterprise-Funktionen**:

- Abteilungsspezifische Label-Verwaltung
- Detaillierte Zugriffsprotokollierung
- Integration in andere Systeme über API

.. note::

   Für große Bereitstellungen empfehlen wir die Nutzung des `kommerziellen Supports <../support-services.html>`__.

----

Technische Anwendungsfälle
===========================

Internes Wiki / Wissensdatenbank-Suche
--------------------------------------

**Übersicht**: Ermöglicht eine übergreifende Suche in Confluence, MediaWiki und internen Wikis.

**Vorteile**:

- Einheitliche Suche über mehrere Wiki-Systeme hinweg
- Automatisches Crawling basierend auf der Aktualisierungshäufigkeit
- Wiki-Seitenanhänge sind im Suchbereich enthalten

**Implementierung**:

1. Confluence Data Store-Plugin installieren
2. Verbindungseinstellungen im Admin-Panel konfigurieren
3. Crawl-Zeitplan festlegen (z. B. täglich)

Einheitliche Dateiserver-Suche
------------------------------

**Übersicht**: Suche in Dokumenten auf Windows-Dateiservern und NAS.

**Unterstützte Protokolle**:

- SMB/CIFS (Windows-Freigabeordner)
- NFS
- Lokales Dateisystem

**Sicherheit**:

- Zugriffskontrolle basierend auf NTLM-Authentifizierung
- Datei-ACLs werden in den Suchergebnissen berücksichtigt

**Konfigurationshinweise**:

- Dediziertes Crawl-Konto erstellen
- Stufenweises Crawling bei großen Dateimengen
- Netzwerkbandbreite berücksichtigen

Website-Suche (Site Search)
---------------------------

**Übersicht**: Suchfunktionalität zu öffentlichen Websites hinzufügen.

**Bereitstellungsmethoden**:

1. **JavaScript-Einbettung**

   Verwenden Sie Fess Site Search (FSS), um mit nur wenigen Zeilen JavaScript ein Suchfeld hinzuzufügen

2. **API-Integration**

   Erstellen Sie eine benutzerdefinierte Such-UI mit der Such-API

**FSS-Beispiel**:

.. code-block:: html

    <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      fess.src = 'https://your-fess-server/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      fess.setAttribute('fess-url', 'https://your-fess-server/json');
      document.body.appendChild(fess);
    })();
    </script>
    <fess:search></fess:search>

Datenbanksuche
--------------

**Übersicht**: Daten in relationalen Datenbanken durchsuchbar machen.

**Unterstützte Datenbanken**:

- MySQL / MariaDB
- PostgreSQL
- Oracle
- SQL Server

**Anwendungsfälle**:

- Kundenstammdaten-Suche
- Produktkatalog-Suche
- FAQ-Datenbank-Suche

**Implementierung**:

1. Database Data Store-Plugin konfigurieren
2. Crawl-Ziel mit SQL-Abfrage angeben
3. Feld-Mapping konfigurieren

----

Zusammenfassung
===============

Fess kann dank seines flexiblen Designs verschiedene Branchen, Größenordnungen und Anwendungsfälle abdecken.

**Für diejenigen, die eine Bereitstellung in Betracht ziehen**:

1. Probieren Sie Fess zunächst mit dem `Schnellstart <../quick-start.html>`__ aus
2. Prüfen Sie die benötigten Funktionen in der `Dokumentation <../documentation.html>`__
3. Für den Produktivbetrieb wenden Sie sich an den `kommerziellen Support <../support-services.html>`__

**Verwandte Ressourcen**:

- `Artikelliste <../articles.html>`__ - Detaillierte technische Artikel
- `Diskussionsforum <https://discuss.codelibs.org/c/fessen/>`__ - Community-Support
- `GitHub <https://github.com/codelibs/fess>`__ - Quellcode und Issue-Tracking
