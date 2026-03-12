=========
Label-API
=========

Abrufen von Labels
==================

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v1/labels``
==================  ====================================================

Durch Senden einer Anfrage wie ``http://<Servername>/api/v1/labels`` an |Fess| können Sie die in |Fess| registrierten Labels als Liste im JSON-Format erhalten.

Anfrageparameter
----------------

Es sind keine Anfrageparameter verfügbar.


Antwort
-------

Es wird folgende Antwort zurückgegeben:

::

    {
      "record_count": 9,
      "data": [
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

Die einzelnen Elemente sind wie folgt definiert:

.. tabularcolumns:: |p{3cm}|p{12cm}|

.. list-table::

   * - record_count
     - Anzahl der registrierten Labels.
   * - data
     - Übergeordnetes Element der Suchergebnisse.
   * - label
     - Name des Labels.
   * - value
     - Wert des Labels.

Tabelle: Antwortinformationen

Verwendungsbeispiele
====================

Beispielanfrage mit curl:

::

    curl "http://localhost:8080/api/v1/labels"

Beispielanfrage mit JavaScript:

::

    fetch('http://localhost:8080/api/v1/labels')
      .then(response => response.json())
      .then(data => {
        console.log('Label-Liste:', data.data);
      });

Fehlerantworten
===============

Wenn die Label-API fehlschlägt, wird folgende Fehlerantwort zurückgegeben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantworten

   * - Statuscode
     - Beschreibung
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler aufgetreten ist
