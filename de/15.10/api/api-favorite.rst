================
Favoriten-API
================

Dieses Dokument beschreibt die v2-Favoriten-API von |Fess|.
Informationen zum gemeinsamen Antwort-Envelope, zum Fehlermodell und zu CSRF finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

.. note::

   Um die Favoriten-Funktion zu nutzen, muss die Einstellung ``user.favorite`` aktiviert sein (standardmäßig deaktiviert).

Favoritendokumente auflisten
============================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/favorites``
==================  ====================================================

Gibt die IDs der Dokumente zurück, die der aufrufende Benutzer in den durch ``query_id`` identifizierten Suchergebnissen als Favoriten gespeichert hat.
``query_id`` ist der von der Such-API (``/search``) zurückgegebene undurchsichtige Bezeichner (Feld ``query_id``).

Anonyme Aufrufer (ohne Benutzercode in der Sitzung) erhalten ``auth_required`` (401).
Wenn die Funktion ``user.favorite`` deaktiviert ist, wird ``invalid_request`` (400) zurückgegeben.
Wenn ``query_id`` nicht mit einem gecachten Ergebnissatz in der Sitzung übereinstimmt, werden ``200`` und ein leeres ``data``-Array zurückgegeben.

Anfrageparameter
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrageparameter

   * - ``query_id``
     - Undurchsichtiger ``query_id`` (query, Pflicht, str), der von der Such-API (``/search``) zurückgegeben wird.

Tabelle: Anfrageparameter

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` im gemeinsamen Envelope zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "data": [
          { "doc_id": "a1b2c3d4e5f6" },
          { "doc_id": "f6e5d4c3b2a1" }
        ]
      }
    }

Die einzelnen Felder sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``record_count``
     - Anzahl der Favoritendokumente in ``data`` (int).
   * - ``data``
     - Array der favorisierten Dokumente aus dem abgefragten Ergebnissatz in der Reihenfolge der Suchergebnisse. Jedes Element hat die Struktur ``{doc_id}``.

Tabelle: Antwortfelder

Fehlerantwort
~~~~~~~~~~~~~

Details zum Fehlermodell finden Sie unter :doc:`api-overview`. Folgende HTTP-Statuscodes können von diesem Endpunkt zurückgegeben werden:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrage ungültig ist (einschließlich des Falls, dass die Funktion ``user.favorite`` deaktiviert ist).
   * - 401 Unauthorized
     - Wenn Authentifizierung erforderlich ist (anonymer Aufrufer).
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort

Favoritenstatus abrufen
=======================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

Ruft den Favoritenstatus des angegebenen Dokuments ab.

Anonyme (nicht authentifizierte) Aufrufer können diesen Endpunkt ebenfalls verwenden. In diesem Fall gibt ``favorite`` den Wert ``false`` zurück, jedoch spiegelt ``count`` weiterhin die gespeicherte Favoritenanzahl wider (aus diesem Grund gibt dieser Endpunkt kein ``401`` zurück).

Wenn die Favoriten-Funktion (``user.favorite``) deaktiviert ist, antwortet der Endpunkt mit ``invalid_request`` (400).

Anfrageparameter
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrageparameter

   * - ``docId``
     - Dokumentbezeichner (path, Pflicht, Muster ``^[A-Za-z0-9_-]+$``).

Tabelle: Anfrageparameter

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` im gemeinsamen Envelope zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "favorite": true,
        "count": 5
      }
    }

Die einzelnen Felder sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``doc_id``
     - Dokument-ID (str).
   * - ``favorite``
     - Gibt an, ob das Dokument ein Favorit des aufrufenden Benutzers ist (bool).
   * - ``count``
     - Anzahl der Favoriten für dieses Dokument (int64).

Tabelle: Antwortfelder

Fehlerantwort
~~~~~~~~~~~~~

Details zum Fehlermodell finden Sie unter :doc:`api-overview`. Folgende HTTP-Statuscodes können von diesem Endpunkt zurückgegeben werden:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrage ungültig ist.
   * - 404 Not Found
     - Wenn die Ressource nicht gefunden wurde.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort

Dokument als Favorit speichern
==============================

Anfrage
-------

==================  ====================================================
HTTP-Methode         POST
Endpunkt             ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

Speichert das angegebene Dokument als Favoriten.
Da es sich um eine zustandsändernde Anfrage handelt, ist der ``X-Fess-CSRF-Token``-Header erforderlich (siehe :doc:`api-overview`).
Außerdem muss der aufrufende Benutzer authentifiziert sein; anonyme Aufrufer erhalten ``auth_required`` (401).

``query_id`` wird verwendet, um zu bestätigen, dass das Zieldokument zu einem aktuellen Suchergebnis gehört. Wenn ``query_id`` mit keinem gecachten Ergebnissatz in der Sitzung übereinstimmt, antwortet der Endpunkt mit ``invalid_request`` (400); wenn ``docId`` nicht in diesem Ergebnissatz enthalten ist, wird ``not_found`` (404) zurückgegeben.

Anfrageparameter
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrageparameter

   * - ``docId``
     - Dokumentbezeichner (path, Pflicht, Muster ``^[A-Za-z0-9_-]+$``).

Tabelle: Anfrageparameter

Anfrage-Body
~~~~~~~~~~~~

Sendet ein JSON (FavoritePostRequest) mit ``Content-Type: application/json`` (Zeichensatz UTF-8) und den folgenden Feldern. Die maximale Größe des Anfrage-Bodys beträgt 1 KiB (1024 Byte); wird diese überschritten, wird ``payload_too_large`` (413) zurückgegeben.

::

    {
      "query_id": "f8b1c2d3e4a5"
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrage-Body

   * - ``query_id``
     - Undurchsichtiger ``query_id`` (str, Pflicht), der von der Such-API (``/search``) zurückgegeben wird.

Tabelle: Anfrage-Body

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` im gemeinsamen Envelope zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "ok": true,
        "favorite": true,
        "count": 6
      }
    }

Die einzelnen Felder sind wie folgt beschrieben. Das obige Beispiel gilt für eine Neuregistrierung; wenn der Favorit bereits zuvor gespeichert wurde (idempotenter erneuter POST), enthält die Antwort zusätzlich das Feld ``already_existed`` (mit dem Wert ``true``).

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``doc_id``
     - Dokument-ID (str).
   * - ``ok``
     - Stets ``true`` (bool).
   * - ``favorite``
     - Stets ``true`` (bool). Das Dokument ist nun ein Favorit des aufrufenden Benutzers, unabhängig davon, ob es neu hinzugefügt oder bereits vorhanden war.
   * - ``count``
     - Aktuelle Favoritenanzahl nach der Operation (int64). Bei einer neuen Registrierung der vorherige Zähler +1 (optimistisch); bei einem idempotenten erneuten POST der gespeicherte Zähler.
   * - ``already_existed``
     - ``true``, wenn der Favorit zuvor bereits registriert war (bool, idempotenter erneuter POST). Fehlt beim ersten POST, der den Favoriten neu registriert.

Tabelle: Antwortfelder

Fehlerantwort
~~~~~~~~~~~~~

Details zum Fehlermodell finden Sie unter :doc:`api-overview`. Folgende HTTP-Statuscodes können von diesem Endpunkt zurückgegeben werden:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrage ungültig ist.
   * - 401 Unauthorized
     - Wenn Authentifizierung erforderlich ist.
   * - 403 Forbidden
     - Wenn die Anfrage aufgrund eines fehlenden oder abgelaufenen CSRF-Tokens nicht erlaubt ist.
   * - 404 Not Found
     - Wenn die Ressource nicht gefunden wurde.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 413 Payload Too Large
     - Wenn der Request-Body die Größenbegrenzung überschreitet.
   * - 415 Unsupported Media Type
     - Wenn ein nicht unterstützter ``Content-Type`` angegeben wurde.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort
