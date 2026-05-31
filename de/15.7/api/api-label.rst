=========
Label-API
=========

Dieses Dokument beschreibt die v2-Label-API von |Fess|.
Informationen zum gemeinsamen Antwort-Envelope und zum Fehlermodell finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

Labels abrufen
==============

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/labels``
==================  ====================================================

Ruft die Liste der in |Fess| konfigurierten Labels im gemeinsamen Envelope ab.

Anfrageparameter
~~~~~~~~~~~~~~~~

Es sind keine Anfrageparameter verfügbar.

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` im gemeinsamen Envelope zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "labels": [
          {
            "label": "AWS",
            "value": "aws"
          },
          {
            "label": "Azure",
            "value": "azure"
          }
        ]
      }
    }

Die einzelnen Felder sind wie folgt beschrieben:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Antwortfelder

   * - ``record_count``
     - Anzahl der registrierten Labels (integer).
   * - ``labels``
     - Array der Labels.
   * - ``label``
     - Name des Labels.
   * - ``value``
     - Wert des Labels.

Tabelle: Antwortfelder

Verwendungsbeispiel
===================

Beispielanfrage mit curl:

::

    curl "http://localhost:8080/api/v2/labels"

Fehlerantwort
=============

Details zum Fehlermodell finden Sie unter :doc:`api-overview`. Folgende HTTP-Statuscodes können von diesem Endpunkt zurückgegeben werden:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort
