========
Suchfunktionen
========

Übersicht
====

|Fess| bietet leistungsstarke Volltextsuchfunktionen.
Dieser Abschnitt beschreibt detaillierte Konfigurationen und Verwendungsmethoden der Suchfunktionen.

Anzeige der Anzahl Suchergebnisse
==================

Standardverhalten
----------------

Wenn Suchergebnisse 10.000 Treffer überschreiten, wird auf dem Suchergebnisbildschirm „ca. 10.000 oder mehr Treffer" angezeigt.
Dies ist die Standardeinstellung unter Berücksichtigung der OpenSearch-Leistung.

Suchbeispiel

|image0|

.. |image0| image:: ../../../resources/images/en/15.5/config/search-result.png

Anzeige der genauen Trefferzahl
----------------------

Um die genaue Trefferzahl von über 10.000 Treffern anzuzeigen, ändern Sie in ``fess_config.properties`` folgende Einstellung:

::

    query.track.total.hits=100000

Mit dieser Einstellung können Sie die genaue Trefferzahl bis zu maximal 100.000 Treffern abrufen.
Beachten Sie jedoch, dass große Werte die Leistung beeinträchtigen können.

.. warning::
   Zu große Werte können die Suchleistung beeinträchtigen.
   Konfigurieren Sie angemessene Werte entsprechend der tatsächlichen Nutzung.

Suchoptionen
==============

Grundlegende Suche
------------

In |Fess| wird durch einfache Eingabe von Schlüsselwörtern in das Suchfeld eine Volltextsuche ausgeführt.
Bei Eingabe mehrerer Schlüsselwörter wird eine UND-Suche ausgeführt.

::

    Suche Engine

Im obigen Beispiel werden Dokumente gesucht, die sowohl „Suche" als auch „Engine" enthalten.

ODER-Suche
------

Für ODER-Suchen fügen Sie ``OR`` zwischen Schlüsselwörtern ein.

::

    Suche OR Engine

NICHT-Suche
-------

Um bestimmte Schlüsselwörter auszuschließen, setzen Sie ein ``-`` (Minuszeichen) vor das Schlüsselwort.

::

    Suche -Engine

Phrasensuche
------------

Für exakte Phrasensuchen setzen Sie die Phrase in Anführungszeichen.

::

    "Suchmaschine"

Feldspezifische Suche
------------------

Sie können nach bestimmten Feldern suchen.

::

    title:Suchmaschine
    url:https://fess.codelibs.org/

Hauptfelder:

- ``title``: Dokumenttitel
- ``content``: Dokumenthaupttext
- ``url``: Dokument-URL
- ``filetype``: Dateityp (z. B. pdf, html, doc)
- ``label``: Label (Kategorie)

Platzhaltersuche
------------------

Platzhaltersuche ist möglich.

- ``*``: Beliebige Zeichenfolge (0 oder mehr Zeichen)
- ``?``: Beliebiges einzelnes Zeichen

::

    Such*
    Such?ine

Fuzzy-Suche
------------

Fuzzy-Suche für Rechtschreibfehler und Schreibvarianten ist verfügbar.
Standardmäßig wird Fuzzy-Suche automatisch auf Schlüsselwörter mit 4 oder mehr Zeichen angewendet.

::

    Suchmaschine~

Durch Angabe einer Zahl nach ``~`` kann die Editierdistanz angegeben werden.

Sortierung der Suchergebnisse
================

Suchergebnisse werden standardmäßig nach Relevanz sortiert.
In den Verwaltungseinstellungen oder API-Parametern können Sie folgende Sortierreihenfolgen angeben:

- Nach Relevanz (Standard)
- Nach Aktualisierungsdatum
- Nach Erstellungsdatum
- Nach Dateigröße

Facettensuche
==============

Mit Facettensuche können Sie Suchergebnisse nach Kategorien filtern.
Standardmäßig ist das Label-Feld (label) als Facette konfiguriert.

Durch Klicken auf Facetten links im Suchbildschirm können Sie Suchergebnisse eingrenzen.

Hervorhebung von Suchergebnissen
====================

Suchschlüsselwörter werden in Titel und Zusammenfassung der Suchergebnisse hervorgehoben.
Hervorhebungseinstellungen können in ``fess_config.properties`` angepasst werden.

::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>
    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

Vorschlagsfunktion
==============

Bei Eingabe in das Suchfeld werden Vorschläge (Autovervollständigung) angezeigt.
Vorschläge basieren auf früheren Suchschlüsselwörtern oder beliebten Suchschlüsselwörtern.

Die Vorschlagsfunktion kann in den allgemeinen Einstellungen der Verwaltungsoberfläche aktiviert/deaktiviert werden.

Suchprotokoll
========

|Fess| protokolliert alle Suchabfragen und Klickprotokolle.
Diese Protokolle können für folgende Zwecke verwendet werden:

- Analyse und Verbesserung der Suchqualität
- Analyse des Benutzerverhaltens
- Identifizierung beliebter Suchschlüsselwörter
- Identifizierung von Schlüsselwörtern ohne Suchergebnisse

Suchprotokolle werden im ``fess_log``-Index von OpenSearch gespeichert
und können in OpenSearch Dashboards visualisiert und analysiert werden.
Details siehe :doc:`kibana`.

Leistungsoptimierung
==========================

Konfiguration des Such-Timeouts
----------------------

Sie können die Such-Timeout-Zeit konfigurieren. Standard ist 10 Sekunden.

::

    query.timeout=10000

Maximale Anzahl Zeichen für Suchabfragen
----------------------

Aus Sicherheits- und Leistungsgründen können Sie die maximale Anzahl Zeichen für Suchabfragen begrenzen.

::

    query.max.length=1000

Cache-Nutzung
----------------

Durch Aktivierung des Caching von Suchergebnissen kann die Antwortzeit für identische Suchabfragen verkürzt werden.
Passen Sie Cache-Einstellungen entsprechend den Systemanforderungen an.

Fehlersuche
======================

Keine Suchergebnisse angezeigt
----------------------

1. Überprüfen Sie, ob der Index korrekt erstellt wurde.
2. Überprüfen Sie, ob das Crawling erfolgreich abgeschlossen wurde.
3. Überprüfen Sie, ob keine Zugriffsberechtigungen für Zieldokumente konfiguriert sind.
4. Überprüfen Sie, ob OpenSearch ordnungsgemäß funktioniert.

Langsame Suchgeschwindigkeit
--------------

1. Überprüfen Sie die Heap-Speichergröße von OpenSearch.
2. Optimieren Sie Anzahl Shards und Replikate des Index.
3. Überprüfen Sie die Komplexität der Suchabfrage.
4. Überprüfen Sie Hardwareressourcen (CPU, Speicher, Disk-I/O).

Ergebnisse mit geringer Relevanz angezeigt
----------------------------

1. Passen Sie Boost-Einstellungen an (``query.boost.title``, ``query.boost.content`` usw.).
2. Überprüfen Sie Fuzzy-Such-Einstellungen.
3. Überprüfen Sie Analyzer-Konfiguration.
4. Konsultieren Sie bei Bedarf kommerziellen Support.
