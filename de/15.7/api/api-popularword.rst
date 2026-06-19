=====================
Beliebte-Wörter-API
=====================

Liste beliebter Wörter abrufen
================================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/popular-words``
==================  ====================================================

Durch Senden einer Anfrage wie ``http://<Server Name>/api/v2/popular-words?seed=123`` an |Fess| können Sie eine Liste beliebter Suchbegriffe im JSON-Format erhalten.

Wenn ``web.api.popularword=false`` gesetzt ist, gibt diese API ``invalid_request`` (HTTP 400) zurück (entspricht dem Verhalten „unsupported operation" in v1).

Informationen zum gemeinsamen Antwort-Envelope und zum Fehlermodell finden Sie unter :doc:`api-overview`.

Anfrageparameter
~~~~~~~~~~~~~~~~

Die verfügbaren Anfrageparameter sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Anfrageparameter

   * - seed
     - Seed zum Abrufen beliebter Wörter (Zeichenkette). Durch diesen Wert können verschiedene Muster von Wörtern abgerufen werden. (Beispiel) ``seed=123``
   * - label
     - Zu filternder Label-Name. Kann mehrfach angegeben werden (Array). (Beispiel) ``label=java``
   * - field
     - Feldname zur Generierung beliebter Wörter. Kann mehrfach angegeben werden (Array). (Beispiel) ``field=label``

Antwort
-------

Bei Erfolg wird eine Antwort im gemeinsamen Envelope-Format zurückgegeben:

::

    {
      "response": {
        "status": 0,
        "record_count": 3,
        "popular_words": [
          "python",
          "java",
          "javascript"
        ]
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortinformationen

   * - record_count
     - Anzahl der beliebten Wörter (ganze Zahl).
   * - popular_words
     - Array der beliebten Wörter (Array von Zeichenketten).

.. note::

   In v2 werden die beliebten Wörter als ``popular_words`` (Array von Zeichenketten) zurückgegeben (nicht als ``data`` wie in v1).

Verwendungsbeispiel
===================

Beispielanfrage mit curl:

::

    curl "http://localhost:8080/api/v2/popular-words?seed=123"

Fehlerantwort
=============

Wenn die Beliebte-Wörter-API fehlschlägt, wird der gemeinsame Fehler-Envelope zurückgegeben. Details zum Fehlermodell finden Sie unter :doc:`api-overview`.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrage ungültig ist (einschließlich des Falls, dass die Funktion durch ``web.api.popularword=false`` deaktiviert ist). ``error.code`` ist ``invalid_request``.
   * - 405 Method Not Allowed
     - Wenn eine nicht unterstützte HTTP-Methode angegeben wurde.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.
