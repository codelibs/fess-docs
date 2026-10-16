=======================
Suchergebnis-Export-API
=======================

Dieses Dokument beschreibt die v2-Export-API von |Fess|, mit der Suchergebnisse als CSV- oder
JSON-Datei heruntergeladen werden. Informationen zum gemeinsamen Antwort-Envelope und zum
Fehlermodell finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

.. note::

   Der Export ist standardmäßig deaktiviert. Um ihn zu nutzen, setzen Sie ``api.search.export=true``
   in ``fess_config.properties``. Ist er aktiviert, zeigt das mitgelieferte Theme ``bootstrap`` neben
   der Trefferzahl ein Exportmenü (CSV / JSON). ``features.search_export`` von ``/api/v2/ui/config``
   meldet den Zustand.

Suchergebnisse herunterladen
============================

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v2/documents/export``
==================  ====================================================

Gibt die zur Suche passenden Dokumente als Datei-Download zurück (``Content-Disposition:
attachment``, Dateiname ``search_results.csv`` oder ``search_results.json``).

- Es gilt derselbe Rollenfilter wie bei ``/api/v2/search``. Bei ``login.required=true`` kann wie bei
  ``/api/v2/search`` ein Zugriffstoken verwendet werden.
- Höchstens ``api.search.export.max.size`` (Standard: ``1000``) Dokumente werden exportiert. Die
  Blätterparameter (``start``, ``num``) werden nicht verwendet.
- Exportiert werden die Felder aus ``api.search.export.fields`` (Standard:
  ``title,url_link,last_modified,content_length,filetype``), die auch in API-Antworten erscheinen
  dürfen.
- Anfragen sind auf ``api.search.export.rate.limit.per.minute`` (Standard: ``10``; ``0`` bedeutet
  unbegrenzt) pro Minute begrenzt, gezählt je angemeldetem Benutzer bzw. je Client-IP bei Gästen.
  Darüber antwortet der Endpunkt mit ``429`` und einem ``Retry-After``-Header.
- Ein Export wird nicht im Suchprotokoll aufgezeichnet.

Anfrageparameter
----------------

Es können dieselben Suchbedingungen wie bei ``/api/v2/documents/all`` angegeben werden, etwa ``q``,
``ex_q``, ``fields.*``, ``sort`` und ``lang`` (siehe :doc:`api-search`). Zusätzlich:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrageparameter

   * - ``format``
     - Dateiformat: ``csv`` (Standard) oder ``json``. Jeder andere Wert ergibt ``invalid_request`` (400).

Tabelle: Anfrageparameter

Antwort
-------

Die CSV-Datei hat eine Kopfzeile mit den Feldnamen und wird in der Kodierung von
``csv.file.encoding`` geschrieben (eine UTF-8-Datei beginnt mit einer Byte-Order-Mark). Ein Wert, der
mit ``=``, ``+``, ``-``, ``@``, einem Tabulator oder einem Wagenrücklauf beginnt, erhält ein
vorangestelltes ``'``, damit eine Tabellenkalkulation ihn nicht als Formel ausführt. Mehrwertige
Felder werden mit einem Leerzeichen verbunden.

::

    "title","url_link","last_modified","content_length","filetype"
    "Example","https://example.com/","2025-01-01T00:00:00.000Z","1234","html"

Die JSON-Datei hat die Form ``{"data":[{...},...]}``; mehrwertige Felder bleiben Arrays.

Ein Fehler vor Beginn der Datei liefert den üblichen Fehler-Envelope. Ein Fehler danach lässt sich in
der Datei nicht melden; der Download endet vorzeitig mit einer abgeschnittenen CSV-Datei oder einem
nicht parsebaren JSON.

Fehlerantwort
-------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Eine fehlerhafte Abfrage, ein anderes ``format`` als ``csv`` / ``json`` oder ein mit
       ``api.search.export=false`` deaktivierter Export.
   * - 401 Unauthorized
     - Wenn eine Authentifizierung erforderlich ist (z. B. anonymer Aufrufer bei ``login.required=true``).
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht zulässig ist.
   * - 429 Too Many Requests
     - Wenn das Anfragelimit pro Minute überschritten ist.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort
