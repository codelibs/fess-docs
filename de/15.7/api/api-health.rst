===========
Health-API
===========

Abrufen des Status
===================

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v1/health``
==================  ====================================================

Durch Senden einer Anfrage wie ``http://<Servername>/api/v1/health`` an |Fess| können Sie den Serverstatus von |Fess| im JSON-Format erhalten.

Anfrageparameter
----------------

Es sind keine Anfrageparameter verfügbar.

Antwort
-------

Es wird folgende Antwort zurückgegeben:

::

    {
      "data": {
        "status": "green",
        "timed_out": false
      }
    }

Die einzelnen Elemente sind wie folgt definiert:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Antwortinformationen

   * - data
     - Übergeordnetes Element der Suchergebnisse.
   * - status
     - Status des Systems. Bei normalem Betrieb wird ``green`` zurückgegeben, bei Warnungen ``yellow``, bei Fehlern ``red``.
   * - timed_out
     - Gibt an, ob eine Zeitüberschreitung aufgetreten ist. ``false`` wird zurückgegeben, wenn die Antwort innerhalb der angegebenen Zeit zurückgegeben wurde, ``true`` bei Zeitüberschreitung.

Fehlerantworten
===============

Wenn die Health-API fehlschlägt, wird folgende Fehlerantwort zurückgegeben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantworten

   * - Statuscode
     - Beschreibung
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler aufgetreten ist
