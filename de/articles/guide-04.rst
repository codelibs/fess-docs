============================================================
Teil 4 Verstreute Dateien zentral durchsuchen -- Quellenuebergreifende Suche in Multi-Source-Umgebungen
============================================================

Einfuehrung
============

Im vorherigen Teil haben wir gezeigt, wie Sie die Suchfunktion von Fess in eine bestehende Website integrieren koennen.
In der Praxis sind Informationen in Unternehmen jedoch nicht nur auf Websites zu finden, sondern verteilen sich auf Dateiserver, Cloud-Speicher und viele weitere Speicherorte.

In diesem Artikel bauen wir eine Umgebung auf, in der mehrere Datenquellen in Fess integriert werden und Benutzer ueber ein einziges Suchfeld alle Dokumente quellenuebergreifend durchsuchen koennen.

Zielgruppe
==========

- Personen, deren interne Dokumente an mehreren Orten verteilt sind
- Personen, die mit der Suche auf Dateiservern oder in Cloud-Speichern unzufrieden sind
- Voraussetzung: Fess ist bereits gemaess der Anleitung aus Teil 2 gestartet

Szenario
========

Wir gehen von einem mittelstaendischen Unternehmen aus. In diesem Unternehmen sind Dokumente an folgenden Orten verstreut:

- **Interne Website**: Internes Portal, interner Blog
- **Dateiserver**: Gemeinsame Ordner pro Abteilung (SMB/CIFS)
- **Lokale Dateien**: Bestimmte Verzeichnisse auf dem Server

Wenn Mitarbeiter sich fragen: "Wo war dieses Dokument nochmal?", muessen sie jedes Tool einzeln durchsuchen.
Mit Fess zentralisieren wir diese Suche, sodass alle Quellen ueber ein einziges Suchfeld durchsucht werden koennen.

Entwurf der Datenquellen
=========================

Beim Aufbau einer quellenuebergreifenden Suche ist der erste wichtige Schritt die Planung: "Was soll wie in den Suchindex aufgenommen werden?"

Uebersicht der Suchobjekte
----------------------------

Zunaechst verschaffen wir uns einen Ueberblick ueber die Datenquellen, die in die Suche einbezogen werden sollen.

.. list-table:: Uebersicht der Datenquellen
   :header-rows: 1
   :widths: 20 25 25 30

   * - Datenquelle
     - Art
     - Geschaetzter Umfang
     - Aktualisierungshaeufigkeit
   * - Internes Portal
     - Web-Crawling
     - Einige hundert Seiten
     - Woechentlich
   * - Technischer Blog
     - Web-Crawling
     - Einige Dutzend bis hundert Seiten
     - Unregelmaessig
   * - Gemeinsame Ordner
     - Datei-Crawling
     - Zehntausende Dateien
     - Taeglich
   * - Archiv
     - Datei-Crawling
     - Einige tausend Dateien
     - Monatlich

Klassifikation durch Labels
-----------------------------

Mit der Label-Funktion von Fess koennen Sie Suchobjekte in Kategorien einteilen.
Benutzer koennen bei der Suche ein Label auswaehlen, um die Ergebnisse auf eine bestimmte Kategorie einzuschraenken.

In unserem Szenario richten wir folgende Labels ein:

- **Portal**: Informationen aus dem internen Portal und Blog
- **Gemeinsame Dateien**: Dokumente auf dem Dateiserver
- **Archiv**: Aeltere Unterlagen

Konfiguration der Labels
^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Waehlen Sie in der Verwaltungsoberflaeche [Crawler] > [Labels]
2. Erstellen Sie ein Label mit [Neu erstellen]

Fuer jedes Label legen Sie einen "Namen" und einen "Wert" fest.
Der Wert wird in alphanumerischen Zeichen angegeben und dient zur Verknuepfung mit der Crawl-Konfiguration.

Aufbau der Crawl-Konfiguration
================================

Web-Crawl-Konfiguration
--------------------------

Dies ist die Crawl-Konfiguration fuer das interne Portal.

1. [Crawler] > [Web] > [Neu erstellen]
2. Folgende Einstellungen vornehmen:

   - URL: ``https://portal.example.com/``
   - Einzuschliessende URLs: ``https://portal.example.com/.*``
   - Auszuschliessende URLs: ``https://portal.example.com/admin/.*``
   - Maximale Zugriffe: ``500``
   - Threads: ``3``
   - Intervall: ``5000``
   - Label: Portal

3. Klicken Sie auf [Erstellen]

Durch die Konfiguration auszuschliessender URLs koennen Sie Seiten wie Verwaltungsoberflaechen von der Suche ausschliessen.

Datei-Crawl-Konfiguration
----------------------------

Dies ist die Crawl-Konfiguration fuer die gemeinsamen Ordner.

1. [Crawler] > [Dateisystem] > [Neu erstellen]
2. Folgende Einstellungen vornehmen:

   - Pfad: ``smb://fileserver.example.com/shared/``
   - Einzuschliessende Pfade: ``smb://fileserver.example.com/shared/.*``
   - Auszuschliessende Pfade: ``.*\\.tmp$``
   - Maximale Zugriffe: ``10000``
   - Threads: ``5``
   - Intervall: ``1000``
   - Label: Gemeinsame Dateien

3. Klicken Sie auf [Erstellen]

**SMB-Authentifizierung konfigurieren**

Wenn der Dateiserver eine Authentifizierung erfordert, muss die Dateiauthentifizierung konfiguriert werden.

1. [Crawler] > [Dateiauthentifizierung] > [Neu erstellen]
2. Folgende Einstellungen vornehmen:

   - Hostname: ``fileserver.example.com``
   - Schema: ``Samba``
   - Benutzername: Benutzername des Dienstkontos
   - Passwort: Passwort des Dienstkontos

3. Klicken Sie auf [Erstellen]

Crawling lokaler Dateien
--------------------------

Um ein bestimmtes Verzeichnis auf dem Server zu crawlen, geben Sie den Dateipfad direkt an.

1. [Crawler] > [Dateisystem] > [Neu erstellen]
2. Folgende Einstellungen vornehmen:

   - Pfad: ``file:///data/archive/``
   - Einzuschliessende Pfade: ``file:///data/archive/.*``
   - Auszuschliessende Pfade: ``.*\\.(log|bak)$``
   - Maximale Zugriffe: ``5000``
   - Label: Archiv

3. Klicken Sie auf [Erstellen]

Planung des Crawl-Zeitplans
=============================

Beim Crawling mehrerer Datenquellen ist die Zeitplanung besonders wichtig.
Wenn alle Crawl-Vorgaenge gleichzeitig ausgefuehrt werden, belastet dies sowohl die Serverressourcen als auch die Zielsysteme erheblich.

Verteilung des Zeitplans
--------------------------

Verteilen Sie die Crawl-Zeitplaene entsprechend der Aktualisierungshaeufigkeit der Datenquellen.

.. list-table:: Beispiel fuer einen Crawl-Zeitplan
   :header-rows: 1
   :widths: 25 25 50

   * - Datenquelle
     - Ausfuehrungszeitpunkt
     - Begruendung
   * - Internes Portal
     - Taeglich um 2:00 Uhr
     - Geringe Seitenzahl, daher schnell abgeschlossen
   * - Gemeinsame Ordner
     - Taeglich um 3:00 Uhr
     - Hohe Dateianzahl, daher Ausfuehrung in der Nacht
   * - Archiv
     - Jeden Sonntag um 4:00 Uhr
     - Geringe Aktualisierungshaeufigkeit, woechentlich ausreichend

Scheduler-Konfiguration
--------------------------

Ueber [System] > [Scheduler] in der Verwaltungsoberflaeche koennen Sie den Ausfuehrungszeitpunkt der Crawl-Jobs festlegen.
Der Standard-Job "Default Crawler" fuehrt alle Crawl-Konfigurationen gebuendelt aus.

Pfad-Mapping fuer benutzerfreundliche Suchergebnisse
======================================================

Die gecrawlten URLs und Dateipfade koennen fuer Benutzer schwer verstaendlich sein.
Mit dem Pfad-Mapping koennen Sie die in den Suchergebnissen angezeigten URLs umwandeln.

Konfigurationsbeispiel
------------------------

Wandeln Sie die Dateipfade des Dateiservers in URLs um, ueber die Benutzer direkt im Browser zugreifen koennen.

1. [Crawler] > [Pfad-Mapping] > [Neu erstellen]
2. Folgende Einstellungen vornehmen:

   - Regulaerer Ausdruck: ``smb://fileserver.example.com/shared/(.*)``
   - Ersetzung: ``https://fileserver.example.com/shared/$1``

Dadurch koennen Benutzer auf einen Link in den Suchergebnissen klicken und direkt im Browser auf die Datei zugreifen.

Nutzung der quellenuebergreifenden Suche
==========================================

Eingrenzung durch Labels
--------------------------

Sobald das Crawling abgeschlossen ist, koennen Sie die quellenuebergreifende Suche auf der Suchoberflaeche ausprobieren.

Auf der Suchoberflaeche werden Tabs oder Dropdown-Menues fuer die Labels angezeigt.
Benutzer koennen "Alle" waehlen, um quellenuebergreifend zu suchen, oder ein bestimmtes Label auswaehlen, um die Suche auf diese Kategorie einzuschraenken.

Wenn Sie beispielsweise nach "Projektplan" suchen, werden Ergebnisse aus Portal-Artikeln, Word-Dateien im gemeinsamen Ordner und PDFs im Archiv gemischt angezeigt.
Durch die Eingrenzung auf das Label "Gemeinsame Dateien" koennen Sie die Ergebnisse auf Dokumente im Dateiserver beschraenken.

Sortierung der Suchergebnisse
-------------------------------

Standardmaessig werden die Ergebnisse nach Relevanz (Score) zum Suchbegriff sortiert.
Unabhaengig von der Art der Datenquelle werden die relevantesten Dokumente zuerst angezeigt.

Zusammenfassung
================

In diesem Artikel haben wir mehrere Datenquellen in Fess integriert und eine quellenuebergreifende Suchumgebung aufgebaut.

- Crawl-Konfiguration fuer drei Typen: Websites, Dateiserver und lokale Dateien
- Kategorisierung durch Labels und Eingrenzung der Suche
- Verteilte Planung der Crawl-Zeitplaene
- URL-Umwandlung durch Pfad-Mapping

Durch die Einfuehrung der quellenuebergreifenden Suche koennen Benutzer die benoetigten Informationen finden, ohne sich Gedanken darueber machen zu muessen, wo sie gespeichert sind.

Im naechsten Teil behandeln wir die rollenbasierte Suche, bei der Suchergebnisse entsprechend den Berechtigungen der einzelnen Abteilungen gesteuert werden.

Referenzen
==========

- `Fess Administratorhandbuch <https://fess.codelibs.org/ja/15.5/admin/index.html>`__

- `Fess Datei-Crawl-Konfiguration <https://fess.codelibs.org/ja/15.5/admin/filecrawl.html>`__
