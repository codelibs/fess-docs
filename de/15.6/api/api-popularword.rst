=====================
Beliebte-Wörter-API
=====================

Abrufen beliebter Wörter
=========================

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v1/popular-words``
==================  ====================================================

Durch Senden einer Anfrage wie ``http://<Servername>/api/v1/popular-words?seed=123`` an |Fess| können Sie die in |Fess| registrierten beliebten Wörter als Liste im JSON-Format erhalten.
Um die Beliebte-Wörter-API zu nutzen, muss in der Administrationsoberfläche unter System > Allgemeine Einstellungen die Antwort für beliebte Wörter aktiviert sein.

Anfrageparameter
----------------

Die verfügbaren Anfrageparameter sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Anfrageparameter

   * - seed
     - Seed zum Abrufen beliebter Wörter (durch diesen Wert können verschiedene Muster von Wörtern abgerufen werden)
   * - label
     - Gefilterter Label-Name
   * - field
     - Feldname zur Generierung beliebter Wörter


Antwort
-------

Es wird folgende Antwort zurückgegeben:

::

    {
      "record_count": 3,
      "data": [
        "python",
        "java",
        "javascript"
      ]
    }

Die einzelnen Elemente sind wie folgt definiert:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Antwortinformationen

   * - record_count
     - Anzahl der registrierten beliebten Wörter
   * - data
     - Array der beliebten Wörter

Fehlerantworten
===============

Wenn die Beliebte-Wörter-API fehlschlägt, wird folgende Fehlerantwort zurückgegeben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantworten

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrageparameter ungültig sind
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler aufgetreten ist
