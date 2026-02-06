==========================================
Fess im Vergleich zu anderen Suchlösungen
==========================================

Einführung
==========

Bei der Auswahl eines Volltextsuchsystems gibt es verschiedene Optionen.
Diese Seite vergleicht Fess mit wichtigen Suchlösungen und erläutert die Merkmale und geeigneten Anwendungsfälle der jeweiligen Lösung.

.. note::

   Dieser Vergleich basiert auf Informationen mit Stand Januar 2026.
   Für die neuesten Funktionen und Änderungen beziehen Sie sich bitte auf die offizielle Dokumentation des jeweiligen Projekts.

----

Fess vs. OpenSearch/Elasticsearch Standalone
============================================

Überblick
---------

OpenSearch und Elasticsearch sind leistungsstarke Suchmaschinen, aber die eigenständige Nutzung erfordert zusätzliche Entwicklung, um ein vollständiges "Suchsystem" zu erstellen.
Fess verwendet OpenSearch/Elasticsearch als Backend und bietet ein sofort einsatzfähiges, vollständiges Suchsystem.

Vergleich
---------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Funktion
     - Fess
     - OpenSearch/Elasticsearch Standalone
   * - Such-UI
     - ✅ Integriert
     - ❌ Entwicklung erforderlich
   * - Admin-UI
     - ✅ Webbasiertes Admin-Panel
     - ❌ Entwicklung oder separate Tools erforderlich
   * - Crawler
     - ✅ Integriert (Web/Datei/DB)
     - ❌ Entwicklung oder separate Tools erforderlich
   * - Bereitstellungszeit
     - Minuten (Docker)
     - Wochen bis Monate (einschließlich Entwicklung)
   * - Anpassbarkeit
     - Mittel (JSP/CSS-Anpassung)
     - Hoch (vollständig individuelle Entwicklung möglich)
   * - Anfangskosten
     - Niedrig
     - Hoch (Entwicklungskosten)
   * - Betriebskosten
     - Niedrig bis Mittel
     - Mittel bis Hoch
   * - Skalierbarkeit
     - Hoch
     - Hoch
   * - Erforderliche Kenntnisse
     - Grundlegende IT-Kenntnisse
     - Programmierung und Suchmaschinen-Expertise

Wann Fess wählen
-----------------

- **Wenn Sie schnell ein Suchsystem aufbauen müssen**
- **Wenn Entwicklungsressourcen begrenzt sind**
- **Wenn Standardsuchfunktionen ausreichen**
- **Wenn Web-Crawling und Dateisuche die Hauptanwendungsfälle sind**

Wann OpenSearch/Elasticsearch Standalone wählen
------------------------------------------------

- **Wenn Sie ein vollständig individuelles Sucherlebnis benötigen**
- **Wenn Sie Suche in eine bestehende Anwendung integrieren**
- **Wenn spezielle Suchlogik erforderlich ist**
- **Wenn Ihr Team über Suchmaschinen-Expertise verfügt**

.. tip::

   Nach der Bereitstellung von Fess können Sie auch eine benutzerdefinierte Such-UI über die API erstellen.
   Erwägen Sie, mit Fess zu beginnen und bei Bedarf anzupassen.

----

Fess vs. Apache Solr
=====================

Überblick
---------

Apache Solr ist eine auf Lucene basierende Open-Source-Suchplattform.
Es bietet hohe Anpassbarkeit, erfordert aber im Vergleich zu Fess mehr Expertise für Bereitstellung und Betrieb.

Vergleich
---------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Funktion
     - Fess
     - Apache Solr
   * - Such-UI
     - ✅ Integriert
     - ❌ Entwicklung erforderlich
   * - Admin-UI
     - ✅ Intuitive Web-UI
     - △ Technische Admin-UI
   * - Crawler
     - ✅ Integriert
     - ❌ Separates Tool erforderlich (Nutch usw.)
   * - Einrichtungsaufwand
     - Niedrig
     - Mittel bis Hoch
   * - Dokumentation
     - ✅ Umfassend
     - ✅ Umfassend
   * - Cloud-Unterstützung
     - ✅ Docker/Kubernetes
     - ✅ SolrCloud
   * - Community
     - Japan-fokussiert
     - Global

Wann Fess wählen
-----------------

- **Wenn Web-/Datei-Crawling der Hauptanwendungsfall ist**
- **Wenn GUI-Verwaltung wichtig ist**
- **Wenn einfache Bereitstellung Priorität hat**

Wann Solr wählen
-----------------

- **Wenn Sie bereits über Solr-Expertise verfügen**
- **Wenn verteilte SolrCloud-Suche benötigt wird**
- **Wenn bestimmte Solr-Plugins erforderlich sind**

----

Fess vs. Google Site Search / Custom Search
============================================

Überblick
---------

Google Site Search (GSS) wurde 2018 eingestellt.
Der Nachfolger, Google Custom Search (Programmable Search Engine), hat Einschränkungen.
Fess ist ein ideales Migrationsziel von GSS.

Vergleich
---------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Funktion
     - Fess
     - Google Custom Search
   * - Werbeanzeigen
     - ✅ Keine
     - ❌ Angezeigt (kostenlose Stufe)
   * - Datenspeicherort
     - ✅ Selbst verwaltet
     - ❌ Google-Server
   * - Indexkontrolle
     - ✅ Volle Kontrolle
     - △ Eingeschränkt
   * - Anpassung
     - ✅ Frei anpassbar
     - △ Eingeschränkt
   * - Suche interner Inhalte
     - ✅ Unterstützt
     - ❌ Nicht unterstützt
   * - Monatliche Kosten
     - Nur Serverkosten
     - Kostenlos (mit Werbung) bis kostenpflichtig
   * - Suchrelevanz-Tuning
     - ✅ Detailliertes Tuning möglich
     - △ Eingeschränkt

Wann Fess wählen
-----------------

- **Wenn Sie keine Werbung anzeigen möchten**
- **Wenn interne Inhalte durchsuchbar sein sollen**
- **Wenn Sie Kontrolle über die Suchergebnisse möchten**
- **Wenn Sie die Daten selbst verwalten möchten**

.. tip::

   Mit Fess Site Search (FSS) können Sie eine Website-Suche implementieren,
   indem Sie einfach JavaScript einbetten, genau wie bei Google Site Search.

----

Fess vs. kommerzielle Suchprodukte
====================================

Überblick
---------

Vergleich mit kommerziellen Produkten wie Microsoft SharePoint Search, Autonomy und Google Cloud Search.

Vergleich
---------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Funktion
     - Fess
     - Kommerzielle Produkte (allgemein)
   * - Lizenzkosten
     - ✅ Kostenlos (OSS)
     - ❌ Teuer
   * - Herstellerabhängigkeit
     - ✅ Keine
     - ❌ Ja
   * - Anpassung
     - ✅ Quellcode verfügbar
     - △ Eingeschränkt
   * - Funktionsumfang
     - ○ Basis bis Mittel
     - ✅ Erweiterte Funktionen
   * - Support
     - △ Community + Kommerziell
     - ✅ Hersteller-Support
   * - KI-/ML-Funktionen
     - △ Basis-Suggest
     - ✅ Erweiterte KI-Funktionen
   * - Enterprise-Integration
     - ○ Wichtige Systeme unterstützt
     - ✅ Breite Integration

Wann Fess wählen
-----------------

- **Wenn Sie die Kosten minimieren möchten**
- **Wenn Sie Herstellerabhängigkeit vermeiden möchten**
- **Wenn grundlegende Suchfunktionen ausreichen**
- **Wenn Sie Open Source nutzen möchten**

Wann kommerzielle Produkte wählen
----------------------------------

- **Wenn erweiterte KI-/ML-Funktionen benötigt werden**
- **Wenn umfassender Hersteller-Support erforderlich ist**
- **Wenn Integration in bestehende kommerzielle Ökosysteme benötigt wird**

.. note::

   Die kommerzielle Version von Fess, `N2 Search <https://www.n2sm.net/products/n2search.html>`__,
   bietet zusätzliche Enterprise-Funktionen und Support.

----

Auswahlrichtlinien
====================

Verwenden Sie das folgende Flussdiagramm, um die optimale Lösung auszuwählen:

::

    Verfügen Sie über ausreichende Entwicklungsressourcen?
          │
    ┌─────┴─────┐
    │           │
    Ja         Nein
    │           │
    ▼           ▼
  Sind die Anforderungen  →  Fess in Betracht ziehen
  speziell?
    │
    ├── Ja → OpenSearch/Elasticsearch Standalone
    │         oder kommerzielle Produkte
    │
    └── Nein → Reicht Fess aus?
              │
              ├── Ja → Fess
              │
              └── Nein → Anforderungen überprüfen

Zusammenfassung
===============

Fess ist in vielen Fällen die optimale Wahl als "sofort einsetzbares Suchsystem".

**Stärken von Fess**:

- Bereitstellung in Minuten
- Suchsystem ohne Entwicklung aufbauen
- Open Source und kostenlos

**Nächste Schritte**:

1. Probieren Sie Fess mit dem `Schnellstart <../quick-start.html>`__ aus
2. Bewerten Sie es anhand Ihrer Anforderungen
3. Wenden Sie sich bei Bedarf an den `kommerziellen Support <../support-services.html>`__
