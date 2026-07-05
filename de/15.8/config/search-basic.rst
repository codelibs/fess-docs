================
Suchfunktionen
================

Übersicht
=========

|Fess| bietet leistungsstarke Volltextsuchfunktionen.
Dieser Abschnitt beschreibt detaillierte Konfigurationen und Verwendungsmethoden der Suchfunktionen.

Anzeige der Anzahl Suchergebnisse
==================================

Standardverhalten
-----------------

Der Standardwert von ``query.track.total.hits`` ist ``10000``.
Wenn Suchergebnisse 10.000 Treffer überschreiten, wird auf dem Suchergebnisbildschirm „ca. 10.000 oder mehr Treffer" angezeigt.
Dies ist die Standardeinstellung, bei der OpenSearch die Obergrenze für die genaue Gesamttrefferanzahl auf den Wert von ``query.track.total.hits`` begrenzt, um die Leistungsauswirkungen bei umfangreichen Suchen zu reduzieren.

Suchbeispiel

|image0|

.. |image0| image:: ../../../resources/images/de/15.8/config/search-result.png

Anzeige der genauen Trefferzahl
--------------------------------

Um die genaue Trefferzahl bis zu einer größeren Anzahl anzuzeigen, ändern Sie in ``fess_config.properties`` den Wert von ``query.track.total.hits``:

::

    query.track.total.hits=100000

Mit obiger Einstellung können Sie die genaue Trefferzahl bis zu maximal 100.000 Treffern abrufen.
Der Schwellenwert, ab dem die Anzeige „ca. N oder mehr Treffer" erscheint, ändert sich ebenfalls in Abhängigkeit von diesem Konfigurationswert.
Beachten Sie jedoch, dass große Werte die Leistung beeinträchtigen können.

.. warning::
   Zu große Werte können die Suchleistung beeinträchtigen.
   Konfigurieren Sie angemessene Werte entsprechend der tatsächlichen Nutzung.

Suchoptionen
============

Grundlegende Suche
------------------

In |Fess| wird durch einfache Eingabe von Schlüsselwörtern in das Suchfeld eine Volltextsuche ausgeführt.
Bei Eingabe mehrerer Schlüsselwörter wird eine UND-Suche ausgeführt.

::

    Suche Engine

Im obigen Beispiel werden Dokumente gesucht, die sowohl „Suche" als auch „Engine" enthalten.

ODER-Suche
----------

Für ODER-Suchen fügen Sie ``OR`` zwischen Schlüsselwörtern ein.

::

    Suche OR Engine

NICHT-Suche
-----------

Um bestimmte Schlüsselwörter auszuschließen, setzen Sie ein ``-`` (Minuszeichen) vor das Schlüsselwort.

::

    Suche -Engine

Phrasensuche
------------

Für exakte Phrasensuchen setzen Sie die Phrase in Anführungszeichen.

::

    "Suchmaschine"

Feldspezifische Suche
---------------------

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
- ``mimetype``: MIME-Typ (z. B. text/html, application/pdf)
- ``filename``: Dateiname
- ``host``: Hostname
- ``site``: Website (Kombination aus Hostname und Pfad)
- ``lang``: Sprache

Weitere Suchfelder können in ``fess_config.properties`` über ``query.additional.search.fields`` hinzugefügt werden.

Platzhaltersuche
----------------

Platzhaltersuche ist möglich.

- ``*``: Beliebige Zeichenfolge (0 oder mehr Zeichen)
- ``?``: Beliebiges einzelnes Zeichen

::

    Such*
    Such?ine

Fuzzy-Suche
-----------

Fuzzy-Suche für Rechtschreibfehler und Schreibvarianten ist verfügbar.
Standardmäßig wird bei Schlüsselwörtern mit 4 oder mehr Zeichen zusätzlich zur normalen Suche eine Fuzzy-Suchabfrage ausgeführt.

::

    Suchmaschine~

Durch Angabe einer Zahl nach ``~`` kann die Editierdistanz angegeben werden.

Sortierung der Suchergebnisse
==============================

Suchergebnisse werden standardmäßig nach Relevanz sortiert.
In den Verwaltungseinstellungen oder API-Parametern können Sie folgende Sortierreihenfolgen angeben:

- Nach Relevanz (``score``, Standard)
- Nach Aktualisierungsdatum (``last_modified``)
- Nach Erstellungsdatum (``created``)
- Nach Dateigröße (``content_length``)
- Nach Dateiname (``filename``)
- Nach Klickanzahl (``click_count``)
- Nach Anzahl Favoriten (``favorite_count``)

Weitere Sortierfelder können in ``fess_config.properties`` über ``query.additional.sort.fields`` hinzugefügt werden.

Facettensuche
=============

Mit Facettensuche können Sie Suchergebnisse nach Kategorien filtern.
Standardmäßig ist das Label-Feld (label) als Facette konfiguriert.

Durch Klicken auf Facetten links im Suchbildschirm können Sie Suchergebnisse eingrenzen.

Hervorhebung von Suchergebnissen
=================================

Suchschlüsselwörter werden in Titel und Zusammenfassung der Suchergebnisse hervorgehoben.
Hervorhebungseinstellungen können in ``fess_config.properties`` angepasst werden.

::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>
    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

- ``query.highlight.tag.pre`` / ``query.highlight.tag.post``: Tags, die hervorgehobene Stellen umschließen (Standard: ``<strong>`` / ``</strong>``)
- ``query.highlight.fragment.size``: Zeichenanzahl eines hervorgehobenen Fragments (Standard: ``60``)
- ``query.highlight.number.of.fragments``: Maximale Anzahl der angezeigten Fragmente (Standard: ``2``)

Die Felder, die als Zusammenfassung (Snippet) für die Hervorhebung herangezogen werden, lassen sich über ``query.highlight.content.description.fields`` festlegen (Standard: ``hl_content,digest``).

Vorschlagsfunktion
==================

Bei Eingabe in das Suchfeld werden Vorschläge (Autovervollständigung) angezeigt.
Vorschläge basieren auf früheren Suchschlüsselwörtern oder beliebten Suchschlüsselwörtern.

Die Vorschlagsfunktion kann in den allgemeinen Einstellungen der Verwaltungsoberfläche aktiviert/deaktiviert werden.

Suchprotokoll
=============

|Fess| protokolliert alle Suchabfragen und Klickprotokolle.
Diese Protokolle können für folgende Zwecke verwendet werden:

- Analyse und Verbesserung der Suchqualität
- Analyse des Benutzerverhaltens
- Identifizierung beliebter Suchschlüsselwörter
- Identifizierung von Schlüsselwörtern ohne Suchergebnisse

Suchprotokolle und Klickprotokolle werden in OpenSearch-Indizes mit dem Präfix ``fess_log`` gespeichert
(Suchabfragen im Index ``fess_log.search_log``, Klickprotokolle im Index ``fess_log.click_log``).
Diese Protokolle können mit OpenSearch Dashboards visualisiert und analysiert werden.
|Fess| enthält eine mitgelieferte Dashboard-Definitionsdatei zur Visualisierung. Weitere Informationen finden Sie unter :doc:`admin-opensearch-dashboards`.

Leistungsoptimierung
====================

Konfiguration des Such-Timeouts
--------------------------------

Sie können die Such-Timeout-Zeit konfigurieren. Standard ist 10 Sekunden.

::

    query.timeout=10000

Maximale Zeichenanzahl für Suchabfragen
----------------------------------------

Aus Sicherheits- und Leistungsgründen können Sie die maximale Zeichenanzahl für Suchabfragen begrenzen.

::

    query.max.length=1000

Cache-Nutzung
-------------

|Fess| selbst verfügt über keine Funktion zum Cachen von Suchergebnissen (Suchantworten).
Das Backend OpenSearch stellt jedoch auf Engine-Ebene einen Shard-Request-Cache sowie einen Query-Cache bereit, die zur Verkürzung der Antwortzeiten bei identischen Suchabfragen beitragen.
Da es sich hierbei um Funktionen auf OpenSearch-Seite handelt, nehmen Sie bei Bedarf Anpassungen in der OpenSearch-Konfiguration vor.

Fehlersuche
===========

Keine Suchergebnisse angezeigt
-------------------------------

1. Überprüfen Sie, ob der Index korrekt erstellt wurde.
2. Überprüfen Sie, ob das Crawling erfolgreich abgeschlossen wurde.
3. Überprüfen Sie, ob die rolle- bzw. berechtigungsbasierte Suchfilterung das Zieldokument für den aktuellen Benutzer (einschließlich Gastbenutzer) ausblendet.
4. Überprüfen Sie, ob OpenSearch ordnungsgemäß funktioniert.

Langsame Suchgeschwindigkeit
-----------------------------

1. Überprüfen Sie die Heap-Speichergröße von OpenSearch.
2. Optimieren Sie Anzahl Shards und Replikate des Index.
3. Überprüfen Sie die Komplexität der Suchabfrage.
4. Überprüfen Sie Hardwareressourcen (CPU, Speicher, Disk-I/O).

Ergebnisse mit geringer Relevanz angezeigt
-------------------------------------------

1. Passen Sie Boost-Einstellungen an (``query.boost.title``, ``query.boost.content`` usw.).
2. Überprüfen Sie Fuzzy-Such-Einstellungen.
3. Überprüfen Sie die Analyzer-Konfiguration.
4. Konsultieren Sie bei Bedarf kommerziellen Support.
5. Sie können die Suchgenauigkeit auch durch den Einsatz von Rank Fusion verbessern. Weitere Informationen finden Sie unter :doc:`rank-fusion`.
