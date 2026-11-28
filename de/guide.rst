===============
Praxisleitfaden
===============

Wissen mit Fess nutzbar machen
==============================

Dieser Praxisleitfaden zeigt, wie Sie die Informationen Ihres Unternehmens mit Fess durchsuchbar machen und zu einer Suchplattform ausbauen, die dauerhaft genutzt wird.
Jeder Artikel bezieht sich auf Fess 15.9 und erklärt konkret die Felder der Einstellungsseiten, die Konfigurationsschlüssel und wie Sie prüfen, ob alles funktioniert hat.
Funktionen, die erst ab 15.10 verfügbar sind, werden in den Artikeln ausdrücklich gekennzeichnet.

Nach Ziel auswählen
===================

- **Fess zuerst ausprobieren**: :doc:`articles/guide-01` → :doc:`articles/guide-02`
- **Dateiserver durchsuchen**: :doc:`articles/file-server-search` → :doc:`articles/guide-04` → :doc:`articles/guide-05`
- **Daten aus der Cloud und aus SaaS-Diensten durchsuchen**: :doc:`articles/datastore-basics` → :doc:`articles/guide-07` / :doc:`articles/guide-06` / :doc:`articles/guide-12`
- **Suche in eine bestehende Website oder ein bestehendes System einbinden**: :doc:`articles/guide-03` → :doc:`articles/guide-11`
- **Je nach Abteilung oder Benutzer unterschiedliche Informationen anzeigen**: :doc:`articles/guide-05` → :doc:`articles/guide-15` → :doc:`articles/guide-13`
- **Die Suche mit KI erweitern**: :doc:`articles/guide-18` → :doc:`articles/guide-19` → :doc:`articles/guide-20`
- **Den Produktivbetrieb aufnehmen**: :doc:`articles/guide-10` → :doc:`articles/guide-16` → :doc:`articles/guide-14`

Erste Schritte
==============

- :doc:`articles/guide-01` - Der Aufbau von Fess, die Aufgabenteilung zwischen Fess und Plugins und Lesewege nach Ziel
- :doc:`articles/guide-02` - Fess mit Docker Compose starten und den gesamten Ablauf vom Crawlen bis zur Suche ausprobieren

Informationen sammeln
=====================

- :doc:`articles/guide-04` - Websites und Dateiserver crawlen und die Ergebnisse mit Labels eingrenzbar machen
- :doc:`articles/datastore-basics` - Einstellungen von Datenspeicher-Plugins, Berechtigungen, Labels, Zeitpläne und wie Sie die Ergebnisse prüfen
- :doc:`articles/guide-07` - Dateien in Google Drive, SharePoint Online / OneDrive und Box durchsuchbar machen
- :doc:`articles/guide-06` - Git-Repositorys, Confluence, Jira und Slack durchsuchbar machen
- :doc:`articles/guide-12` - Daten aus Datenbanken, CSV-Dateien und Salesforce durchsuchbar machen

Suche einbinden und ihr Erscheinungsbild anpassen
=================================================

- :doc:`articles/guide-03` - Ein Suchfeld in eine bestehende Website einfügen und das Aussehen der Suchseite mit Themes anpassen
- :doc:`articles/guide-11` - Mit der Such-API und Zugriffstoken aus Geschäftsanwendungen suchen und Dokumente registrieren

Zugriff steuern
===============

- :doc:`articles/guide-05` - Suchergebnisse nach Rollen und Gruppen unterscheiden und LDAP / Active Directory anbinden
- :doc:`articles/guide-15` - SSO (OIDC / SAML / Entra ID / SPNEGO) einführen und den Zugriff von außen schützen
- :doc:`articles/guide-13` - Eine einzige Fess-Instanz mit virtuellen Hosts und Rollen für mehrere Organisationen nutzen

Suchqualität verbessern
=======================

- :doc:`articles/guide-08` - Probleme in den Analyseseiten der Suchlogs finden und mit Synonymen und Schlüsselübereinstimmungen beheben
- :doc:`articles/guide-09` - Verstehen, wie mehrsprachige Dokumente indiziert und durchsucht werden, und jede Sprache abstimmen
- :doc:`articles/guide-22` - Suchlogs mit OpenSearch Dashboards nach eigenen Kriterien auswerten und visualisieren

Betrieb
=======

- :doc:`articles/guide-10` - Health Checks, Logs, Benachrichtigungen, Sicherung und Wiederherstellung sowie der Umgang mit Fehler-URLs
- :doc:`articles/guide-16` - Einstellungen mit fessctl und der Admin-API als Code verwalten und Umgebungen reproduzieren
- :doc:`articles/guide-14` - Speichereinstellungen, ein externer OpenSearch-Cluster und der Betrieb von Fess auf mehreren Servern
- :doc:`articles/guide-17` - Funktionen durch eigene Datenspeicher-Plugins und Ingester ergänzen

Die Suche mit KI erweitern
==========================

- :doc:`articles/guide-18` - Mit Vektorsuche und Rangfusion Dokumente auch bei abweichender Formulierung finden
- :doc:`articles/guide-19` - Ein LLM anbinden und den KI-Suchmodus nutzen, der auf Grundlage interner Dokumente antwortet
- :doc:`articles/guide-20` - KI-Agenten über das MCP-Server-Plugin in Fess suchen lassen
- :doc:`articles/guide-21` - Eine multimodale Suche aufbauen, die Bilder und Text gemeinsam durchsucht

Den unternehmensweiten Rollout planen
=====================================

- :doc:`articles/guide-23` - Was in jeder Phase von der Einführung bis zum unternehmensweiten Rollout zu konfigurieren und zu prüfen ist

Anwendungsfälle und Vergleiche
==============================

- :doc:`articles/use-cases` - Anwendungsfälle nach Branche und Größe und die jeweils hilfreichen Artikel
- :doc:`articles/comparison` - Fess im Vergleich mit anderen Suchlösungen (OpenSearch allein, Solr, kommerzielle Produkte usw.)
- :doc:`articles/file-server-search` - Was Sie vor der Einführung einer Volltextsuche für Dateiserver prüfen sollten

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-04
   articles/datastore-basics
   articles/guide-07
   articles/guide-06
   articles/guide-12
   articles/guide-03
   articles/guide-11
   articles/guide-05
   articles/guide-15
   articles/guide-13
   articles/guide-08
   articles/guide-09
   articles/guide-22
   articles/guide-10
   articles/guide-16
   articles/guide-14
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-23
   articles/use-cases
   articles/comparison
   articles/file-server-search
