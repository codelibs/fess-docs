===========
Suchbezogene Konfigurationen
===========

Die nachfolgend beschriebenen Einstellungen werden in fess_config.properties angegeben.
Nach Änderungen ist ein Neustart von |Fess| erforderlich.

Fuzzy-Suche
=========

Für 4 oder mehr Zeichen wird Fuzzy-Suche angewendet, die auch bei einem Zeichenunterschied Treffer erzielt.
Um diese Einstellung zu deaktivieren, geben Sie `-1` an.
::

    query.boost.fuzzy.min.length=-1

Such-Timeout-Wert
=================

Sie können den Timeout-Wert für Suchen angeben.
Standardwert ist 10 Sekunden.
::

    query.timeout=10000

Maximale Zeichenanzahl bei Suche
==============

Sie können die maximale Zeichenanzahl bei Suchen angeben.
Standardwert ist 1000 Zeichen.
::

    query.max.length=1000

Protokollierung von Such-Timeouts
=======================

Protokollierungseinstellung für den Fall von Such-Timeouts.
Standardwert ist `true (aktiviert)`.
::

    query.timeout.logging=true

Anzeige der Trefferzahl
===========

Geben Sie dies an, wenn Anzeige der Trefferzahl von über 10.000 Treffern erforderlich ist.
Bei Standardeinstellung erfolgt bei über 10.000 Treffern folgende Anzeige:

`Suchergebnisse für xxxxx ca. 10.000 oder mehr Treffer 1 - 10 von (4,94 Sekunden)`

::

    query.track.total.hits=10000

Indexname für Standortsuche
=======================

Gibt den Indexnamen für Standortsuche an.
Standardwert ist `location`.
::

    query.geo.fields=location

Sprachspezifikation über Request-Parameter
=======================

Gibt den Parameternamen für Sprachspezifikation über Request-Parameter an.
Beispielsweise wechselt die Anzeigesprache des Bildschirms zu Englisch, wenn der Request-Parameter als `browser_lang=en` in der URL übergeben wird.
::

    query.browser.lang.parameter.name=browser_lang

Spezifikation der Präfixsuche
==============

Bei exakter Suche mit Angabe von `~\*` wird als Präfixsuche gesucht.
Standardwert ist `true (aktiviert)`.
::

    query.replace.term.with.prefix.query=true

Hervorhebungszeichen
==============

Sätze werden mit den hier angegebenen Zeichenfolgen getrennt, um natürliche Hervorhebung zu realisieren.
Angegebene Zeichenfolgen werden als Unicode-Zeichen mit u als Anfangstrennzeichen angegeben.
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

Standardwerte sind wie folgt konfiguriert (dekodiert konvertiert):

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

Hervorhebungsfragmente
==================

Gibt Anzahl Zeichen und Anzahl Fragmente für Hervorhebungsfragmente an, die von OpenSearch abgerufen werden.
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

Hervorhebungs-Generierungsmethode
==============

Gibt die Hervorhebungs-Generierungsmethode von OpenSearch an.
::

    query.highlight.type=fvh

Tags für Hervorhebung
===============

Gibt Start- und End-Tags für Hervorhebung an.
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

An OpenSearch-Highlighter übergebene Werte
===========================

Gibt an OpenSearch-Highlighter übergebene Werte an.
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

Zu Response hinzuzufügende Feldnamen
========================

Gibt Feldnamen an, die zu Response bei normaler Suche oder API-Suche hinzugefügt werden.
::

    query.additional.response.fields=
    query.additional.api.response.fields=

Hinzufügen von Feldnamen
==============

Gibt an, wenn Suchfeldnamen oder Facetten-Feldnamen hinzugefügt werden.
::

    query.additional.search.fields=
    query.additional.facet.fields=

Konfiguration für GSA-kompatibles XML-Format bei Suchergebnissen
===================================

Wird beim Abrufen von Suchergebnissen im GSA-kompatiblen XML-Format verwendet.

Gibt Feldnamen an, die zu Response bei Verwendung von GSA-kompatiblem XML-Format hinzugefügt werden.
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

Gibt Sprache bei Verwendung von GSA-kompatiblem XML-Format an.
    ::

        query.gsa.default.lang=en

Gibt Standard-Sortierung bei Verwendung von GSA-kompatiblem XML-Format an.
    ::

        query.gsa.default.sort=
