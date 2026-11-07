=============================================
Teil 4 Verstreute Dateien zentral durchsuchen
=============================================

Einführung
============

Im vorherigen Teil haben wir gezeigt, wie Sie die Suchfunktion von Fess in eine bestehende Website integrieren können.
In der Praxis sind Informationen in Unternehmen jedoch nicht nur auf Websites zu finden, sondern verteilen sich auf Dateiserver, Cloud-Speicher und viele weitere Speicherorte.

In diesem Artikel bauen wir eine Umgebung auf, in der mehrere Datenquellen in Fess integriert werden und Benutzer über ein einziges Suchfeld alle Dokumente quellenübergreifend durchsuchen können.

Zielgruppe
==========

- Personen, deren interne Dokumente an mehreren Orten verteilt sind
- Personen, die mit der Suche auf Dateiservern oder in Cloud-Speichern unzufrieden sind
- Voraussetzung: Fess ist bereits gemäß der Anleitung aus Teil 2 gestartet

Szenario
========

Wir gehen von einem mittelständischen Unternehmen aus. In diesem Unternehmen sind Dokumente an folgenden Orten verstreut:

- **Interne Website**: Internes Portal, interner Blog
- **Dateiserver**: Gemeinsame Ordner pro Abteilung (SMB/CIFS)
- **Lokale Dateien**: Bestimmte Verzeichnisse auf dem Server

Wenn Mitarbeiter sich fragen: "Wo war dieses Dokument nochmal?", müssen sie jedes Tool einzeln durchsuchen.
Mit Fess zentralisieren wir diese Suche, sodass alle Quellen über ein einziges Suchfeld durchsucht werden können.

Entwurf der Datenquellen
=========================

Beim Aufbau einer quellenübergreifenden Suche ist der erste wichtige Schritt die Planung: "Was soll wie in den Suchindex aufgenommen werden?"

Übersicht der Suchobjekte
----------------------------

Zunächst verschaffen wir uns einen Überblick über die Datenquellen, die in die Suche einbezogen werden sollen.

.. list-table:: Uebersicht der Datenquellen
   :header-rows: 1
   :widths: 20 25 25 30

   * - Datenquelle
     - Art
     - Geschätzter Umfang
     - Aktualisierungshäufigkeit
   * - Internes Portal
     - Web-Crawling
     - Einige hundert Seiten
     - Wöchentlich
   * - Technischer Blog
     - Web-Crawling
     - Einige Dutzend bis hundert Seiten
     - Unregelmäßig
   * - Gemeinsame Ordner
     - Datei-Crawling
     - Zehntausende Dateien
     - Täglich
   * - Archiv
     - Datei-Crawling
     - Einige tausend Dateien
     - Monatlich

Klassifikation durch Labels
-----------------------------

Mit der Label-Funktion von Fess können Sie Suchobjekte in Kategorien einteilen.
Benutzer können bei der Suche ein Label auswählen, um die Ergebnisse auf eine bestimmte Kategorie einzuschränken.

In unserem Szenario richten wir folgende Labels ein:

- **Portal**: Informationen aus dem internen Portal und Blog
- **Gemeinsame Dateien**: Dokumente auf dem Dateiserver
- **Archiv**: Ältere Unterlagen

Konfiguration der Labels
^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Wählen Sie in der Verwaltungsoberfläche [Crawler] > [Labels]
2. Erstellen Sie ein Label mit [Neu erstellen]

Für jedes Label legen Sie einen "Namen" und einen "Wert" fest.
Der Wert wird in alphanumerischen Zeichen angegeben und dient zur Verknüpfung mit der Crawl-Konfiguration.

Aufbau der Crawl-Konfiguration
================================

Web-Crawl-Konfiguration
--------------------------

Dies ist die Crawl-Konfiguration für das interne Portal.

1. [Crawler] > [Web] > [Neu erstellen]
2. Folgende Einstellungen vornehmen:

   - URL: ``https://portal.example.com/``
   - Einzuschließende URLs: ``https://portal.example.com/.*``
   - Auszuschließende URLs: ``https://portal.example.com/admin/.*``
   - Maximale Zugriffe: ``500``
   - Threads: ``3``
   - Intervall: ``5000``
   - Label: Portal

3. Klicken Sie auf [Erstellen]

Durch die Konfiguration auszuschließender URLs können Sie Seiten wie Verwaltungsoberflächen von der Suche ausschließen.

Datei-Crawl-Konfiguration
----------------------------

Dies ist die Crawl-Konfiguration für die gemeinsamen Ordner.

1. [Crawler] > [Dateisystem] > [Neu erstellen]
2. Folgende Einstellungen vornehmen:

   - Pfad: ``smb://fileserver.example.com/shared/``
   - Einzuschließende Pfade: ``smb://fileserver.example.com/shared/.*``
   - Auszuschließende Pfade: ``.*\\.tmp$``
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
   - Einzuschließende Pfade: ``file:///data/archive/.*``
   - Auszuschließende Pfade: ``.*\\.(log|bak)$``
   - Maximale Zugriffe: ``5000``
   - Label: Archiv

3. Klicken Sie auf [Erstellen]

Planung des Crawl-Zeitplans
=============================

Beim Crawling mehrerer Datenquellen ist die Zeitplanung besonders wichtig.
Wenn alle Crawl-Vorgänge gleichzeitig ausgeführt werden, belastet dies sowohl die Serverressourcen als auch die Zielsysteme erheblich.

Verteilung des Zeitplans
--------------------------

Verteilen Sie die Crawl-Zeitpläne entsprechend der Aktualisierungshäufigkeit der Datenquellen.

.. list-table:: Beispiel fuer einen Crawl-Zeitplan
   :header-rows: 1
   :widths: 25 25 50

   * - Datenquelle
     - Ausführungszeitpunkt
     - Begründung
   * - Internes Portal
     - Täglich um 2:00 Uhr
     - Geringe Seitenzahl, daher schnell abgeschlossen
   * - Gemeinsame Ordner
     - Täglich um 3:00 Uhr
     - Hohe Dateianzahl, daher Ausführung in der Nacht
   * - Archiv
     - Jeden Sonntag um 4:00 Uhr
     - Geringe Aktualisierungshäufigkeit, wöchentlich ausreichend

Scheduler-Konfiguration
--------------------------

Über [System] > [Scheduler] in der Verwaltungsoberfläche können Sie den Ausführungszeitpunkt der Crawl-Jobs festlegen.
Der Standard-Job "Default Crawler" führt alle Crawl-Konfigurationen gebündelt aus.

Pfad-Mapping für benutzerfreundliche Suchergebnisse
======================================================

Die gecrawlten URLs und Dateipfade können für Benutzer schwer verständlich sein.
Mit dem Pfad-Mapping können Sie die in den Suchergebnissen angezeigten URLs umwandeln.

Konfigurationsbeispiel
------------------------

Wandeln Sie die Dateipfade des Dateiservers in URLs um, über die Benutzer direkt im Browser zugreifen können.

1. [Crawler] > [Pfad-Mapping] > [Neu erstellen]
2. Folgende Einstellungen vornehmen:

   - Regulärer Ausdruck: ``smb://fileserver.example.com/shared/(.*)``
   - Ersetzung: ``https://fileserver.example.com/shared/$1``

Dadurch können Benutzer auf einen Link in den Suchergebnissen klicken und direkt im Browser auf die Datei zugreifen.

Nutzung der quellenübergreifenden Suche
==========================================

Eingrenzung durch Labels
--------------------------

Sobald das Crawling abgeschlossen ist, können Sie die quellenübergreifende Suche auf der Suchoberfläche ausprobieren.

Auf der Suchoberfläche werden Tabs oder Dropdown-Menüs für die Labels angezeigt.
Benutzer können "Alle" wählen, um quellenübergreifend zu suchen, oder ein bestimmtes Label auswählen, um die Suche auf diese Kategorie einzuschränken.

Wenn Sie beispielsweise nach "Projektplan" suchen, werden Ergebnisse aus Portal-Artikeln, Word-Dateien im gemeinsamen Ordner und PDFs im Archiv gemischt angezeigt.
Durch die Eingrenzung auf das Label "Gemeinsame Dateien" können Sie die Ergebnisse auf Dokumente im Dateiserver beschränken.

Sortierung der Suchergebnisse
-------------------------------

Standardmäßig werden die Ergebnisse nach Relevanz (Score) zum Suchbegriff sortiert.
Unabhängig von der Art der Datenquelle werden die relevantesten Dokumente zuerst angezeigt.

Zusammenfassung
================

In diesem Artikel haben wir mehrere Datenquellen in Fess integriert und eine quellenübergreifende Suchumgebung aufgebaut.

- Crawl-Konfiguration für drei Typen: Websites, Dateiserver und lokale Dateien
- Kategorisierung durch Labels und Eingrenzung der Suche
- Verteilte Planung der Crawl-Zeitpläne
- URL-Umwandlung durch Pfad-Mapping

Durch die Einführung der quellenübergreifenden Suche können Benutzer die benötigten Informationen finden, ohne sich Gedanken darüber machen zu müssen, wo sie gespeichert sind.

Im nächsten Teil behandeln wir die rollenbasierte Suche, bei der Suchergebnisse entsprechend den Berechtigungen der einzelnen Abteilungen gesteuert werden.

Referenzen
==========

- `Fess Administratorhandbuch <https://fess.codelibs.org/ja/15.5/admin/index.html>`__

- `Fess Datei-Crawl-Konfiguration <https://fess.codelibs.org/ja/15.5/admin/filecrawl.html>`__
