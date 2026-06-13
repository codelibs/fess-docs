==========
Cache-API
==========

Dieses Dokument beschreibt die v2-Cache-API von |Fess|.
Informationen zum gemeinsamen Antwort-Envelope, zum Fehlermodell und zu CSRF finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

Gecachtes Dokument abrufen
==========================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/cache/{docId}``
==================  ====================================================

Gibt das gecachte (mit Hervorhebung versehene) HTML eines Dokuments zurück.

Wenn die Anmeldepflicht-Einstellung (Systemeinstellung „Anmeldung erforderlich“) aktiviert ist und der Aufrufer anonym ist, wird ``auth_required`` (401) zurückgegeben.

Anfrageparameter
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrageparameter

   * - ``docId``
     - Dokumentbezeichner (path, Pflicht, Muster ``^[A-Za-z0-9_-]+$``).
   * - ``hq``
     - Hervorhebungs-Suchbegriff (query). Kann mehrfach angegeben werden (Array).

Tabelle: Anfrageparameter

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` im gemeinsamen Envelope zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "mimetype": "text/html",
        "content": "<html><body>...</body></html>",
        "url": "https://example.com/",
        "created": "2024-05-31T12:00:00.000Z",
        "charset": "UTF-8"
      }
    }

Die einzelnen Felder sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``doc_id``
     - Dokument-ID (str).
   * - ``mimetype``
     - MIME-Typ (enum: ``text/html``).
   * - ``content``
     - Gecachter HTML-Text (str).
   * - ``url``
     - Dokument-URL (str). Falls vorhanden das Feld ``url_link``, andernfalls die Roh-URL aus dem Index. Wird weggelassen, wenn keines von beidem vorhanden ist.
   * - ``created``
     - Erstellungszeitstempel des Dokuments im Index (str). Wird weggelassen, wenn nicht vorhanden.
   * - ``charset``
     - Zeichensatz, der aus dem Mimetype des Dokuments ermittelt wurde (str). Wenn nicht vorhanden, ist ``UTF-8`` der Standardwert.

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
     - Wenn Authentifizierung erforderlich ist (Anmeldepflicht-Einstellung aktiviert und anonymer Aufrufer).
   * - 404 Not Found
     - Wenn die Ressource nicht gefunden wurde.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort
