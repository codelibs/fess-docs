=============================================
Bang-Suche (auf einer anderen Website suchen)
=============================================

Ein Bang leitet eine Suche an eine andere Website weiter, statt |Fess| zu durchsuchen. Er funktioniert wie die Bangs von DuckDuckGo: Fügen Sie der Suchanfrage ``!`` und ein kurzes Auslösewort hinzu, und |Fess| sendet den Rest der Anfrage an die Website, für die das Auslösewort steht.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Suchanfrage
     - Ziel
   * - ``airplane !g``
     - Google, Suche nach ``airplane``
   * - ``!w Ohm's law``
     - Wikipedia, Suche nach ``Ohm's law``
   * - ``!g``
     - Startseite von Google
   * - ``airplane !unknown``
     - |Fess|, als normale Suche (``!`` bedeutet NOT, siehe :doc:`search-not`)

Bangs werden vom Plugin ``fess-webapp-bangs`` bereitgestellt, das |Fess| 15.10 oder neuer voraussetzt. Installieren Sie es über [System > Plugin] in der Administrationsoberfläche oder mit ``bin/fess-setup install plugin fess-webapp-bangs`` (siehe :doc:`../admin/plugin-guide`) und starten Sie |Fess| neu.

Wann ein Bang erkannt wird
==========================

- Ein Bang besteht aus ``!`` gefolgt von einem Auslösewort und wird als eigenständiges Wort geschrieben. Beim Auslösewort wird Groß- und Kleinschreibung nicht unterschieden.
- Der Bang wird aus der Suchanfrage entfernt, und der Rest der Anfrage wird an die URL des Bangs gesendet.
- Enthält eine Suchanfrage mehrere definierte Bangs, zählt nur der erste.
- Ein nicht definiertes Auslösewort ist kein Bang. ``!unknown`` wird wie gewohnt gesucht und schließt das Wort ``unknown`` aus.
- ``-g`` und ``NOT g`` schließen weiterhin das Wort ``g`` aus. Nur ``!g`` ist ein Bang.

Die Suchseite und ``/api/v2/search`` folgen der Weiterleitung: Die API liefert ``redirect_url`` (siehe :doc:`../api/api-search`), und das mit |Fess| gelieferte Theme ``bootstrap`` navigiert dorthin. Andere Themes benötigen die gleiche Behandlung.

Aufrufer, die nicht weiterleiten können, etwa der Chat, MCP, die JSON-APIs v1 und Classic sowie die Suche in der Administrationsoberfläche, senden die Suche nicht an eine andere Website. Sie entfernen den Bang und durchsuchen den Rest der Anfrage.

Bangs definieren
================

Bangs werden mit der Systemeigenschaft ``bangs.definitions`` definiert. Tragen Sie sie in ``app/WEB-INF/conf/system.properties`` ein oder übergeben Sie sie als ``-Dfess.system.bangs.definitions=...``. Eine Änderung in ``system.properties`` wird ohne Neustart von |Fess| übernommen.

Der Wert ist eine durch Leerraum getrennte Liste von Einträgen der Form ``Auslösewort=URL``. In der URL wird ``{query}`` durch den URL-kodierten Rest der Suchanfrage ersetzt:

::

    bangs.definitions=g=https://www.google.com/search?q={query} w=https://en.wikipedia.org/wiki/Special:Search?search={query}

- Ein Auslösewort darf weder Leerraum noch ``(``, ``)``, ``!``, ``"``, ``=`` oder ``:`` enthalten.
- Akzeptiert werden nur absolute URLs mit ``http`` oder ``https``.
- Ein Eintrag, der diese Regeln nicht erfüllt, wird nicht verwendet. Im |Fess|-Protokoll wird eine Warnung ausgegeben, die übrigen Einträge bleiben in Kraft.
- Wird dasselbe Auslösewort zweimal definiert, gilt die erste Definition.
- Ein leerer Wert schaltet alle Bangs aus.

Ist ``bangs.definitions`` nicht gesetzt, stehen die folgenden fünf Bangs zur Verfügung:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Auslösewort
     - Website
   * - ``g``
     - Google
   * - ``b``
     - Bing
   * - ``ddg``
     - DuckDuckGo
   * - ``w``
     - Wikipedia (Englisch)
   * - ``gh``
     - GitHub

Das Setzen von ``bangs.definitions`` ersetzt diese Liste. Um die Standard-Bangs zu behalten und einen weiteren hinzuzufügen, schreiben Sie alle benötigten Einträge auf.

Siehe auch
==========

- :doc:`search-not` - NOT-Suche
- :doc:`special-char` - Sonderzeichen und Escape-Zeichen
- :doc:`../api/api-search` - Such-API
