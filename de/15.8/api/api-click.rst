==================
Klickprotokoll-API
==================

Dieses Dokument beschreibt die v2-Klickprotokoll-API von |Fess|.
Informationen zum gemeinsamen Antwort-Envelope, zum Fehlermodell und zu CSRF finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

Klick protokollieren
====================

Anfrage
-------

==================  ====================================================
HTTP-Methode         POST
Endpunkt             ``/api/v2/click``
==================  ====================================================

Protokolliert einen Klick auf ein Suchergebnis im Suchprotokoll.
Bei anonymen Aufrufern sowie bei Installationen, bei denen die Suchprotokollfunktion deaktiviert ist, wird ``logged: false`` in einer Erfolgsantwort zurückgegeben (kein Fehler).

Da es sich um eine zustandsändernde Anfrage handelt, ist der ``X-Fess-CSRF-Token``-Header erforderlich (siehe :doc:`api-overview`).

Anfrage-Body
~~~~~~~~~~~~

Sendet ein JSON (ClickRequest) mit ``Content-Type: application/json`` und den folgenden Feldern:

::

    {
      "doc_id": "a1b2c3d4e5f6",
      "query_id": "f8b1c2d3e4a5",
      "rank": 1,
      "rt": 1717142400000
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrage-Body

   * - ``doc_id``
     - Dokument-ID (str, Pflicht, Muster ``^[A-Za-z0-9_-]+$``). Gibt das Dokument an, dessen Klick protokolliert wird.
   * - ``query_id``
     - Die von der Such-API (``/search``) zurückgegebene ``query_id`` (str, optional). Verknüpft den Klick mit der zugehörigen Suchanfrage.
   * - ``rank``
     - Position in der Ergebnisliste (1-basiert, int, optional).
   * - ``rt``
     - Epoch-Millisekunden der ursprünglichen Suchanfrage (int64, optional). Wenn nicht angegeben, wird die aktuelle Serverzeit als Standardwert verwendet.

Tabelle: Anfrage-Body

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` im gemeinsamen Envelope zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "ok": true,
        "logged": true
      }
    }

Die einzelnen Felder sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``ok``
     - Stets ``true`` (bool).
   * - ``logged``
     - ``false`` (bool), wenn die Persistierung des Suchprotokolls deaktiviert ist oder der Aufrufer anonym ist. In diesem Fall wird dennoch eine ``200``-Antwort zurückgegeben.

Tabelle: Antwortfelder

.. note::

   ``logged: true`` zeigt an, dass der Klick in die Warteschlange des Suchprotokolls aufgenommen wurde. Die Persistierung erfolgt asynchron.

Fehlerantwort
~~~~~~~~~~~~~

Details zum Fehlermodell finden Sie unter :doc:`api-overview`. Folgende HTTP-Statuscodes können von diesem Endpunkt zurückgegeben werden:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Der Anfrage-Body ist kein gültiges JSON, oder ``doc_id`` fehlt bzw. entspricht nicht dem Muster.
   * - 403 Forbidden
     - Wenn die Anfrage aufgrund eines fehlenden oder abgelaufenen CSRF-Tokens nicht erlaubt ist.
   * - 404 Not Found
     - Es wurde kein Dokument gefunden, das der angegebenen ``doc_id`` entspricht.
   * - 405 Method Not Allowed
     - Es wurde eine andere HTTP-Methode als ``POST`` verwendet (es wird ein ``Allow: POST``-Header zurückgegeben).
   * - 413 Payload Too Large
     - Der Anfrage-Body überschreitet die Größenbegrenzung (2 KiB).
   * - 415 Unsupported Media Type
     - Der ``Content-Type`` ist nicht ``application/json`` (UTF-8 ist erforderlich).
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort
