================================
Suchbezogene Konfigurationen
================================

Die nachfolgend beschriebenen Einstellungen werden in fess_config.properties angegeben.
Nach Änderungen ist ein Neustart von |Fess| erforderlich.

Fuzzy-Suche
===========

Für 4 oder mehr Zeichen wird Fuzzy-Suche angewendet, die auch bei einem Zeichenunterschied Treffer erzielt.
Um diese Einstellung zu deaktivieren, geben Sie ``-1`` an.
::

    query.boost.fuzzy.min.length=-1

Standardwert ist ``4``. Detaillierte Einstellungen zur Fuzzy-Suche finden Sie im nachfolgenden Abschnitt „Einstellungen für Relevanz (Boost)".

Such-Timeout-Wert
=================

Sie können den Timeout-Wert für Suchen in Millisekunden angeben.
Standardwert ist 10 Sekunden (10000 Millisekunden).
::

    query.timeout=10000

Maximale Zeichenanzahl bei der Suche
=====================================

Sie können die maximale Zeichenanzahl für Suchanfragen angeben.
Suchanfragen, die diese Länge überschreiten, werden nicht akzeptiert.
Standardwert ist 1000 Zeichen.
::

    query.max.length=1000

Protokollierung von Such-Timeouts
==================================

Protokollierungseinstellung für den Fall von Such-Timeouts.
Standardwert ist ``true`` (aktiviert).
::

    query.timeout.logging=true

Anzeige der Trefferzahl
=======================

Gibt die Obergrenze für die exakt ermittelte Trefferzahl an.
Bei der Standardeinstellung wird bei über 10.000 Treffern folgende Anzeige ausgegeben:

``Suchergebnisse für xxxxx ca. 10.000 oder mehr Treffer 1 - 10 von (4,94 Sekunden)``

Wenn eine genaue Trefferzahl über 10.000 angezeigt werden soll, geben Sie einen größeren Wert an.
::

    query.track.total.hits=10000

.. note::
   Größere Werte können die Suchleistung beeinträchtigen. Wählen Sie einen für Ihren Anwendungsfall geeigneten Wert.

Maximaler Offset bei Suchergebnissen
=====================================

Gibt die Obergrenze für den Offset (Startposition der Suche) bei Suchergebnissen an.
Wird ein Offset angegeben, der diesen Wert überschreitet, führt die Suche zu einem Fehler.
Dieser Wert dient als Obergrenze für das Blättern zu tiefen Seiten per Paging.
Standardwert ist 100000.
::

    query.max.search.result.offset=100000

Schwellenwert für erneute Suche per ODER-Verknüpfung
======================================================

Liegt die Trefferzahl einer normalen Suche unter dem hier angegebenen Wert, wird die Suche mit dem ODER-Operator wiederholt.
Dadurch können Ergebnisse ergänzt werden, wenn die UND-Suche nur wenige Treffer liefert.
Standardwert ist ``-1``; diese Funktion ist deaktiviert.
::

    query.orsearch.min.hit.count=-1

Feldname für die Standortsuche
================================

Gibt den Feldnamen an, der bei der Standortsuche verwendet wird.
Mehrere Felder werden durch Komma getrennt angegeben.
Standardwert ist ``location``.
::

    query.geo.fields=location

Informationen zur Verwendung der Standortsuche finden Sie unter :doc:`search-geosearch`.

Sprachangabe über Request-Parameter
=====================================

Gibt den Parameternamen für die Sprachangabe über Request-Parameter an.
Wird beispielsweise ``browser_lang=en`` als Request-Parameter in der URL übergeben, wechselt die Anzeigesprache des Bildschirms zu Englisch.
::

    query.browser.lang.parameter.name=browser_lang

Standardsprache für die Suche
================================

Gibt die Standardsprache für Suchanfragen als kommagetrennte Liste an.
Ist ein Wert gesetzt, hat dieser Vorrang vor dem Request-Parameter und der Browsersprache.
Standardwert ist leer (nicht angegeben); in diesem Fall wird der Request-Parameter oder die Browsersprache verwendet.
::

    query.default.languages=

Zuordnung von Sprachcodes
===========================

Gibt die Normalisierungszuordnung für Sprachcodes an, die bei der Suche verwendet werden.
Sprachcodes vom Browser oder aus dem Request werden in die intern von |Fess| verwendeten Sprachcodes umgewandelt.
In der Regel muss diese Einstellung nicht geändert werden. Im Standardwert sind die Zuordnungen der wichtigsten Sprachen definiert.
::

    query.language.mapping=\
    ar=ar\n\
    bg=bg\n\
    ...

Angabe der Präfixsuche
========================

Wird am Ende eines Suchbegriffs ``*`` angegeben (Beispiel: ``Suche*``), wird dieser Begriff als Präfixabfrage gesucht.
Standardwert ist ``true`` (aktiviert). Bei Angabe von ``false`` wird ein Begriff mit abschließendem ``*`` unverändert gesucht.
::

    query.replace.term.with.prefix.query=true

Hervorhebungszeichen
====================

Sätze werden mit den hier angegebenen Zeichenfolgen getrennt, um eine natürliche Hervorhebungsanzeige zu realisieren.
Die angegebenen Zeichenfolgen werden als Unicode-Zeichen mit u als Anfangstrennzeichen angegeben.
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

Standardwerte sind wie folgt konfiguriert (dekodiert):

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

Hervorhebungsfragmente
======================

Gibt die Zeichenanzahl und die Fragmentanzahl für Hervorhebungsfragmente an, die von OpenSearch abgerufen werden.
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

Hervorhebungs-Generierungsmethode
===================================

Gibt die Hervorhebungs-Generierungsmethode von OpenSearch an.
::

    query.highlight.type=fvh

Tags für die Hervorhebung
===========================

Gibt Start- und End-Tags für die Hervorhebung an.
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

An den OpenSearch-Highlighter übergebene Werte
================================================

Gibt die an den OpenSearch-Highlighter übergebenen Werte an.
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

Erweiterte Hervorhebungseinstellungen
======================================

Einstellungen zur Steuerung des detaillierten Hervorhebungsverhaltens.
::

    query.highlight.force.source=false
    query.highlight.fragmenter=span
    query.highlight.fragment.offset=-1
    query.highlight.no.match.size=0
    query.highlight.order=score
    query.highlight.phrase.limit=256
    query.highlight.content.description.fields=hl_content,digest
    query.highlight.boundary.position.detect=true
    query.highlight.text.fragment.type=query
    query.highlight.text.fragment.size=3
    query.highlight.text.fragment.prefix.length=5
    query.highlight.text.fragment.suffix.length=5

Zu Response hinzuzufügende Feldnamen
======================================

Gibt Feldnamen an, die zur Response bei normaler Suche oder API-Suche hinzugefügt werden.
Jeweils entsprechend für normale Suche, API-(JSON/GSA-)Suche, Scroll-Suche und Cache-Anzeige.
::

    query.additional.response.fields=
    query.additional.api.response.fields=
    query.additional.scroll.response.fields=
    query.additional.cache.response.fields=

Weitere Details zu den Response-Feldern der Scroll-Suche finden Sie unter :doc:`search-scroll`.

Hinzufügen von Feldnamen
==========================

Wird angegeben, wenn Suchfeldnamen, Facetten-Feldnamen, Sortierfelder und ähnliche Felder hinzugefügt werden sollen.
::

    query.additional.default.fields=
    query.additional.search.fields=
    query.additional.facet.fields=
    query.additional.sort.fields=
    query.additional.highlighted.fields=
    query.additional.analyzed.fields=
    query.additional.not.analyzed.fields=

Die Bedeutung der einzelnen Einstellungen ist wie folgt:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Einstellung
     - Beschreibung
   * - ``query.additional.default.fields``
     - Fügt dem Standard-Suchfeld hinzu, das bei Abfragen ohne Feldangabe durchsucht wird.
   * - ``query.additional.search.fields``
     - Fügt Felder hinzu, die bei feldspezifischer Suche angegeben werden können.
   * - ``query.additional.facet.fields``
     - Fügt Felder hinzu, die als Facetten verwendet werden können.
   * - ``query.additional.sort.fields``
     - Fügt Felder hinzu, die als Sortierkriterien verwendet werden können.
   * - ``query.additional.highlighted.fields``
     - Fügt Felder hinzu, die für die Hervorhebung vorgesehen sind.
   * - ``query.additional.analyzed.fields``
     - Fügt Felder hinzu, die durch den Analyzer analysiert werden.
   * - ``query.additional.not.analyzed.fields``
     - Fügt Felder hinzu, die nicht durch den Analyzer analysiert werden.

Zusammenfassen ähnlicher Dokumente (Collapse)
===============================================

Einstellungen für die Collapse-Funktion, die ähnliche (nahezu doppelte) Dokumente anhand des Feldes ``content_minhash_bits`` zusammenfasst und gebündelt anzeigt.
``query.collapse.inner.hits.name`` ist der Feldname, unter dem ähnliche Dokumente im Suchergebnis gespeichert werden;
``query.collapse.inner.hits.size`` ist die Anzahl ähnlicher Dokumente, die pro Gruppe abgerufen werden (``0`` bedeutet kein Abruf);
``query.collapse.inner.hits.sorts`` gibt die Sortierreihenfolge beim Abruf ähnlicher Dokumente an;
``query.collapse.max.concurrent.group.results`` gibt die maximale Anzahl gleichzeitiger Anfragen beim Gruppenabruf an.
::

    query.collapse.max.concurrent.group.results=4
    query.collapse.inner.hits.name=similar_docs
    query.collapse.inner.hits.size=0
    query.collapse.inner.hits.sorts=

Such-Präferenz
================

Gibt die Präferenz (Wert zur Bestimmung des zu durchsuchenden Shards) an, die bei API-Suche im JSON-Format an OpenSearch übergeben wird.
Bei Angabe von ``_query`` wird der Hash-Wert der Suchanfrage als Präferenz verwendet, sodass dieselbe Anfrage immer demselben Shard zugewiesen wird.
Standardwert ist ``_query``.
::

    query.json.default.preference=_query

Einstellungen für Relevanz (Boost)
=====================================

Gibt die Boost-Werte an, die bei der Relevanzkalkulation (Score) während der Suche verwendet werden.
Einstellungen mit ``.lang`` beziehen sich auf sprachspezifische Felder (z. B. ``content_ja``).
::

    query.boost.title=0.5
    query.boost.title.lang=1.0
    query.boost.content=0.05
    query.boost.content.lang=0.1
    query.boost.important_content=-1.0
    query.boost.important_content.lang=-1.0

Boost-Werte und Verhalten der Fuzzy-Suche werden wie folgt angegeben.
``query.boost.fuzzy.min.length`` ist die minimale Zeichenanzahl, ab der Fuzzy-Suche angewendet wird (``-1`` deaktiviert sie).
::

    query.boost.fuzzy.min.length=4
    query.boost.fuzzy.title=0.01
    query.boost.fuzzy.title.fuzziness=AUTO
    query.boost.fuzzy.title.expansions=10
    query.boost.fuzzy.title.prefix_length=0
    query.boost.fuzzy.title.transpositions=true
    query.boost.fuzzy.content=0.005
    query.boost.fuzzy.content.fuzziness=AUTO
    query.boost.fuzzy.content.expansions=10
    query.boost.fuzzy.content.prefix_length=0
    query.boost.fuzzy.content.transpositions=true

Einstellungen für den Abfragetyp
==================================

Gibt den bei der Suche verwendeten Abfragetyp sowie dessen detailliertes Verhalten an.
``query.default.query_type`` ist der standardmäßig verwendete Abfragetyp;
``query.dismax.tie_breaker`` ist der Tie-Breaker-Wert für dismax-Abfragen;
``query.bool.minimum_should_match`` ist der minimum_should_match-Wert für bool-Abfragen (leer bedeutet nicht angegeben).
::

    query.default.query_type=bool
    query.dismax.tie_breaker=0.1
    query.bool.minimum_should_match=

Detaillierte Einstellungen für Präfix- und Fuzzy-Suche
========================================================

Gibt das detaillierte Verhalten von Präfix- und Fuzzy-Abfragen an.
::

    query.prefix.expansions=50
    query.prefix.slop=0
    query.fuzzy.prefix_length=0
    query.fuzzy.expansions=50
    query.fuzzy.transpositions=true

Facetteneinstellungen
======================

Gibt das Standardverhalten der Facettensuche an.
``query.facet.fields`` gibt die Facettenfelder an;
``query.facet.fields.size`` gibt die maximale Anzahl der abzurufenden Facettenwerte an;
``query.facet.fields.min_doc_count`` gibt die minimale Dokumentanzahl für die Anzeige in der Facette an;
``query.facet.fields.sort`` gibt die Sortierreihenfolge der Facetten an;
``query.facet.fields.missing`` gibt den Wert an, der Dokumenten ohne entsprechenden Wert zugewiesen wird.
::

    query.facet.fields=label
    query.facet.fields.size=100
    query.facet.fields.min_doc_count=1
    query.facet.fields.sort=count.desc
    query.facet.fields.missing=

Konfiguration für GSA-kompatibles XML-Format bei Suchergebnissen
=================================================================

Wird beim Abrufen von Suchergebnissen im GSA-kompatiblen XML-Format verwendet.

Gibt Feldnamen an, die zur Response bei Verwendung des GSA-kompatiblen XML-Formats hinzugefügt werden.
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

Gibt die Sprache bei Verwendung des GSA-kompatiblen XML-Formats an.
    ::

        query.gsa.default.lang=en

Gibt die Standard-Sortierung bei Verwendung des GSA-kompatiblen XML-Formats an.
    ::

        query.gsa.default.sort=

Gibt den Metadaten-Präfix bei Verwendung des GSA-kompatiblen XML-Formats an.
    ::

        query.gsa.meta.prefix=MT_

Gibt das charset-Feld bei Verwendung des GSA-kompatiblen XML-Formats an.
    ::

        query.gsa.index.field.charset=charset

Gibt das content_type-Feld bei Verwendung des GSA-kompatiblen XML-Formats an.
    ::

        query.gsa.index.field.content_type.=content_type

Gibt die Standard-Präferenz bei Verwendung des GSA-kompatiblen XML-Formats an.
    ::

        query.gsa.default.preference=_query
