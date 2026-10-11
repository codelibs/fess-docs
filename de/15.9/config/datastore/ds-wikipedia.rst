==================================
Wikipedia-Konnektor
==================================

Übersicht
=========

Der Wikipedia-Konnektor bietet die Funktionalität, eine Wikipedia-Dumpdatei zu lesen
und ihre Seiten im |Fess|-Index zu registrieren.
Er funktioniert mit den Dumps von Wikipedia, anderen Wikimedia-Projekten und jeder MediaWiki-Site.

Für diese Funktion ist das Plugin ``fess-ds-wikipedia`` erforderlich.

Unterstützte Dumps
==================

Der Parameter ``source`` wählt das Dumpformat.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ``source``
     - Beschreibung
   * - ``cirrus``
     - Ein CirrusSearch-Indexdump, den Wikimedia für seine Wikis unter
       ``https://dumps.wikimedia.org/other/cirrus_search_index/`` veröffentlicht. Er enthält den Text, den MediaWiki selbst gerendert hat, mit expandierten Vorlagen,
       sodass kein Wikitext-Markup in den Index gelangt. Dies ist das empfohlene Format für Wikipedia und andere Wikimedia-Wikis
   * - ``xml``
     - Ein MediaWiki-XML-Export (``*-pages-articles.xml.bz2`` oder die Ausgabe von ``Special:Export`` bzw. ``dumpBackup.php`` eines beliebigen MediaWiki).
       Er enthält Wikitext, den der Konnektor in Klartext umwandelt (siehe „Klartext aus XML-Dumps“)
   * - ``auto``
     - Der Standardwert. Ein Speicherort, der ``cirrus_search_index`` enthält oder auf ``.json.bz2`` bzw. ``.json`` endet, wird als ``cirrus`` gelesen; jeder andere als ``xml``

Die Komprimierung eines Dumps (etwa bzip2 oder gzip) wird anhand seines Inhalts erkannt, und auch eine unkomprimierte Datei kann gelesen werden.

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Die Dumpdatei muss erreichbar sein, entweder als HTTP(S)-URL oder als Pfad auf dem |Fess|-Server
3. Zeit für den Crawl: Der Dump einer großen Wikipedia umfasst mehrere Gigabyte. Probieren Sie eine Konfiguration zunächst mit ``limit`` aus

Plugin-Installation
-------------------

Installieren Sie über die Administrationsoberfläche unter "System" -> "Plugins" oder führen Sie ``bin/fess-setup install plugin fess-ds-wikipedia`` aus
und starten Sie |Fess| neu.
Weitere Details finden Sie unter :doc:`../../admin/plugin-guide`.

Konfiguration
=============

Konfigurieren Sie über die Administrationsoberfläche unter "Crawler" -> "Datenspeicher" -> "Neu erstellen".

Grundeinstellungen
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beispielwert
   * - Name
     - Japanese Wikipedia
   * - Handler-Name
     - WikipediaDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    limit=10000

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``url``
     - Nein
     - Speicherort des Dumps: eine HTTP(S)-URL, eine ``file:``-URL oder ein lokaler Pfad. Der Standardwert ist der Dump der englischen Wikipedia
       (``http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2``), geben Sie diesen Parameter daher explizit an.
       Welche Formen bei ``source=cirrus`` möglich sind, steht unter „CirrusSearch-Dumps“
   * - ``source``
     - Nein
     - ``auto``, ``cirrus`` oder ``xml`` (Standard: ``auto``)
   * - ``limit``
     - Nein
     - Nach dieser Anzahl Seiten anhalten. ``0`` bedeutet keine Begrenzung (Standard: ``0``). Damit lässt sich eine Konfiguration an wenigen Seiten ausprobieren
   * - ``user_agent``
     - Nein
     - User-Agent-Header, der beim Herunterladen des Dumps gesendet wird. Ohne Angabe wird der User-Agent-Name des |Fess|-Crawlers verwendet
   * - ``max_digest_length``
     - Nein
     - Maximale Länge von ``digest`` in Zeichen (Standard: ``100``)
   * - ``total_entity_size_limit``
     - Nein
     - Obergrenze in Bytes für die Gesamtgröße der Entitäten, die der XML-Parser verarbeitet (Standard: ``100000000``). Gilt nur für ``source=xml``
   * - ``text_extractor``
     - Nein
     - Wie der Wikitext eines XML-Dumps in Klartext umgewandelt wird: ``sweble`` (Standard) oder ``regex``. Siehe „Klartext aus XML-Dumps“
   * - ``drop_templates``
     - Nein
     - Kommagetrennte Vorlagennamen, deren Text aus dem Inhalt eines XML-Dumps entfernt wird, oder ``*`` für alle Vorlagen
   * - ``keep_templates``
     - Nein
     - Kommagetrennte Vorlagennamen, deren Text erhalten bleibt, obwohl ``drop_templates`` auf sie zutrifft
   * - ``drop_captions``
     - Nein
     - Bild- und Galerieunterschriften aus dem Inhalt eines XML-Dumps entfernen (Standard: ``false``)

CirrusSearch-Dumps
~~~~~~~~~~~~~~~~~~

Ein CirrusSearch-Dump wird als nummerierte Teile veröffentlicht, etwa ``jawiki_content-20261004-00000.json.bz2``.
Bei ``source=cirrus`` akzeptiert ``url`` eine kommagetrennte Liste, deren Einträge jeweils Folgendes sein können:

- eine einzelne Datei (eine HTTP(S)-URL oder ein lokaler Pfad)
- ein lokales Verzeichnis: Jede Datei darin, deren Name auf ``.json.bz2`` oder ``.json`` endet, wird in Namensreihenfolge gelesen
- eine HTTP(S)-URL, die auf ``/`` endet: Die Verzeichnisliste wird abgerufen und jede Datei, deren Name auf ``.json.bz2`` oder ``.json`` endet, wird in Namensreihenfolge gelesen

Um zum Beispiel alle Teile des Content-Index der japanischen Wikipedia zu lesen:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

.. note::

   Wikimedia entfernt alte Datumsstände vom Server. Suchen Sie ein vorhandenes Datum in der Liste unter
   ``https://dumps.wikimedia.org/other/cirrus_search_index/``, bevor Sie den Crawl konfigurieren.

Skript-Einstellungen
--------------------

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    anchor=
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

Verfügbare Felder
~~~~~~~~~~~~~~~~~

Die folgenden Werte können im Skript referenziert werden.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``id``
     - Seiten-ID
   * - ``title``
     - Seitentitel
   * - ``encodedTitle``
     - Der Titel in der Form, die in einer MediaWiki-Seiten-URL verwendet wird (Leerzeichen werden zu ``_``, andere Zeichen werden prozentcodiert)
   * - ``content``
     - Klartext der Seite
   * - ``digest``
     - ``content``, gekürzt auf ``max_digest_length`` Zeichen
   * - ``contentLength``
     - Länge von ``content``
   * - ``wikitext``
     - Wikitext der Seite, sofern der Dump ihn enthält
   * - ``format``, ``model``
     - Format und Inhaltsmodell der Seite
   * - ``timestamp``
     - Zeitstempel der Seite
   * - ``ns``
     - Namensraumnummer
   * - ``categories``, ``links``
     - Kategorien der Seite und die Seiten, auf die sie verlinkt
   * - ``redirect``, ``redirectTitle``
     - Ob die Seite eine Weiterleitung ist, und ihr Ziel
   * - ``stub``, ``disambiguation``
     - Ob die Seite ein Stub ist und ob sie eine Begriffsklärungsseite ist
   * - ``lang``, ``host``, ``site``, ``url``
     - Aus dem Speicherort des Dumps abgeleitet. Siehe „Aus dem Speicherort des Dumps abgeleitete Werte“

Bei ``source=cirrus`` stehen zusätzlich die folgenden Werte zur Verfügung:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``openingText``
     - Der einleitende Text der Seite
   * - ``headings``
     - Überschriften
   * - ``externalLinks``
     - Externe Links
   * - ``templates``
     - Von der Seite verwendete Vorlagen
   * - ``redirects``
     - Titel, die auf die Seite weiterleiten
   * - ``auxiliaryText``
     - Hilfstext, etwa Bildunterschriften
   * - ``weightedTags``
     - Gewichtete Tags
   * - ``wikibaseItem``
     - Wikidata-Item-ID
   * - ``incomingLinks``
     - Anzahl eingehender Links
   * - ``popularityScore``
     - Beliebtheitswert
   * - ``revisionId``
     - Revisions-ID

Aus dem Speicherort des Dumps abgeleitete Werte
-----------------------------------------------

``lang``, ``host``, ``site`` und ``url`` werden aus dem Namen des Dumps abgeleitet: Ein Name wie ``jawiki-latest-pages-articles.xml.bz2``
oder ``index_name=jawiki_content`` ergibt für ``lang`` den Wert ``ja``, für ``host`` und ``site`` ``ja.wikipedia.org`` und für ``url`` ``https://ja.wikipedia.org/wiki/<codierter Titel>``.
Der Name muss den Sprachcode enthalten, unmittelbar gefolgt von ``wiki`` und dann ``-``, ``_`` oder ``.``.
Schwesterprojekte wie Wikiquote (``jawikiquote-...``) werden absichtlich nicht abgeleitet, weil ein falscher Host tote Links erzeugen würde.

.. warning::

   Passt der Name des Dumps nicht, werden ``host``, ``site`` und ``url`` nicht gesetzt, und ``url`` behält den Wert des Parameters ``url``,
   also den Speicherort des Dumps. Verwendet das Skript ``url`` unverändert, erhält jede Seite dieselbe URL, und der gesamte Crawl landet als ein einziges Dokument im Index,
   ohne Fehlermeldung.
   Bei einem umbenannten Dump oder einem anderen Wikimedia-Projekt bauen Sie die URL im Skript zusammen, wie im Beispiel oben, zum Beispiel
   ``url="https://ja.wikiquote.org/wiki/" + encodedTitle``.

Klartext aus XML-Dumps
----------------------

Bei ``source=xml`` wird der Wikitext mit dem Sweble-Wikitext-Parser in Klartext umgewandelt. Die Namensraumnamen werden aus dem ``<siteinfo>`` des Exports gelesen,
sodass Bilder und Kategorieangaben in jeder Sprache (``[[ファイル:...]]``, ``[[Kategorie:...]]``) und in Wikis mit eigenen Namensraumnamen erkannt werden.
Eine Seite, an der Sweble scheitert, wird stattdessen mit regulären Ausdrücken umgewandelt.

``text_extractor=regex`` verwendet für jede Seite reguläre Ausdrücke. Das ist mehrfach schneller, aber verschachtelte Vorlagen, Tabellen und mehrzeiliges Markup bleiben im Text.

Standardmäßig bleiben der Text jedes Vorlagenarguments (ohne die Parameternamen) und jede Bild- und Galerieunterschrift in ``content`` erhalten, damit dieser Text gefunden werden kann.
Mit ``drop_templates``, ``keep_templates`` und ``drop_captions`` lässt sich das filtern:

::

    # Den Text dieser Vorlagen entfernen, auch wenn sie verschachtelt sind ("*" entfernt alle Vorlagen)
    drop_templates=Cite web,Cite news,Use dmy dates
    # Diese Vorlagen behalten, obwohl drop_templates sie erfasst
    # (drop_templates=* mit keep_templates=Note,Warning behält nur diese beiden)
    keep_templates=
    # Bild- und Galerieunterschriften entfernen
    drop_captions=false

Vorlagennamen werden so abgeglichen, wie MediaWiki sie auflöst: Der erste Buchstabe ist nicht groß-/kleinschreibungsabhängig, ``_`` entspricht einem Leerzeichen, und das Präfix ``Template:`` ist optional.
Vorlagen werden nicht expandiert, eine beibehaltene Vorlage liefert also den Text ihrer Argumente und nicht das, was MediaWiki rendern würde.
Ein CirrusSearch-Dump enthält bereits den von MediaWiki gerenderten Text, daher gelten diese Parameter nicht für ``source=cirrus``.

Anwendungsbeispiele
===================

Japanische Wikipedia aus einem CirrusSearch-Dump
------------------------------------------------

Parameter:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

Skript:

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

Japanische Wikipedia aus einem XML-Dump, ohne Quellenvorlagen
-------------------------------------------------------------

Parameter:

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    source=xml
    drop_templates=Cite web,Cite news
    limit=10000

Das Skript ist dasselbe wie unter „Skript-Einstellungen“.

Ein anderes Wikimedia-Projekt (Wikiquote)
-----------------------------------------

Aus dem Dumpnamen ``jawikiquote-...`` werden ``host`` und ``url`` nicht abgeleitet, bauen Sie sie daher im Skript zusammen.

Skript:

::

    lang="ja"
    url="https://ja.wikiquote.org/wiki/" + encodedTitle
    host="ja.wikiquote.org"
    site="ja.wikiquote.org"
    title=title
    content=content
    digest=digest
    last_modified=timestamp
    timestamp=timestamp

Fehlerbehebung
==============

Es wird nur ein Dokument indexiert
----------------------------------

Siehe „Aus dem Speicherort des Dumps abgeleitete Werte“. Prüfen Sie, ob das Skript ``url`` für jede Seite setzt.

Der Crawl dauert zu lange
-------------------------

1. Beginnen Sie mit ``limit``, um die Konfiguration zu prüfen
2. Verwenden Sie ``source=cirrus``, bei einem XML-Dump ``text_extractor=regex``
3. Legen Sie den Dump auf dem |Fess|-Server ab und geben Sie einen lokalen Pfad an

Wikitext-Markup bleibt im Inhalt
--------------------------------

Verwenden Sie einen CirrusSearch-Dump (``source=cirrus``). Bei ``source=xml`` belässt ``text_extractor=regex`` verschachtelte Vorlagen, Tabellen und mehrzeiliges Markup im Text, verwenden Sie daher ``sweble`` (der Standard).

Der Dump kann nicht gelesen werden
----------------------------------

1. Prüfen Sie, ob URL oder Pfad korrekt sind (das Datum eines CirrusSearch-Dumps kann vom Server entfernt worden sein)
2. Prüfen Sie bei einer Verzeichnis-URL, ob sie auf ``/`` endet und die Dateien darin auf ``.json.bz2`` oder ``.json`` enden
3. Den genauen Fehler finden Sie im Log

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- :doc:`../../admin/plugin-guide` - Leitfaden zur Plugin-Verwaltung
- `Wikimedia Downloads <https://dumps.wikimedia.org/>`_
- `CirrusSearch index dumps <https://dumps.wikimedia.org/other/cirrus_search_index/>`_
