=============
Vorschlags-API
=============

Abrufen von Vorschlagswörtern
==============================

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v1/suggest-words``
==================  ====================================================

Durch Senden einer Anfrage wie ``http://<Servername>/api/v1/suggest-words?q=Vorschlagswort`` an |Fess| können Sie die in |Fess| registrierten Vorschlagswörter als Liste im JSON-Format erhalten.
Um die Vorschlags-API zu nutzen, muss in der Administrationsoberfläche unter System > Allgemeine Einstellungen entweder "Vorschläge aus Dokumenten" oder "Vorschläge aus Suchbegriffen" aktiviert sein.

Anfrageparameter
----------------

Die verfügbaren Anfrageparameter sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Anfrageparameter

   * - q
     - Schlüsselwort für Vorschläge. (Beispiel) ``q=fess``
   * - num
     - Anzahl der vorgeschlagenen Wörter. Standard: 10. (Beispiel) ``num=20``
   * - label
     - Gefilterter Label-Name. (Beispiel) ``label=java``
   * - fields
     - Feldname zur Eingrenzung der Vorschlagsziele. Standard: keine Eingrenzung. (Beispiel) ``fields=content,title``
   * - lang
     - Angabe der Suchsprache. (Beispiel) ``lang=en``


Antwort
-------

Es wird folgende Antwort zurückgegeben:

::

    {
      "query_time": 18,
      "record_count": 355,
      "page_size": 10,
      "data": [
        {
          "text": "fess",
          "labels": [
            "java",
            "python"
          ]
        }
      ]
    }

Die einzelnen Elemente sind wie folgt definiert:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Antwortinformationen

   * - query_time
     - Abfrageverarbeitungszeit (Einheit: Millisekunden).
   * - record_count
     - Anzahl der registrierten Vorschlagswörter.
   * - page_size
     - Seitengröße.
   * - data
     - Übergeordnetes Element der Suchergebnisse.
   * - text
     - Vorschlagswort.
   * - labels
     - Array der Label-Werte.

Fehlerantworten
===============

Wenn die Vorschlags-API fehlschlägt, wird folgende Fehlerantwort zurückgegeben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantworten

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrageparameter ungültig sind
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler aufgetreten ist
