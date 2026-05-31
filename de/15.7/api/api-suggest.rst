==============
Vorschlags-API
==============

Vorschlagswörterliste abrufen
==============================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/suggest-words``
==================  ====================================================

Durch Senden einer Anfrage wie ``http://<Server Name>/api/v2/suggest-words?q=fes`` an |Fess| können Sie eine Liste von Vorschlagswörtern für das eingegebene Präfix im JSON-Format erhalten.
Um die Vorschlags-API zu nutzen, muss in der Administrationsoberfläche unter System > Allgemein entweder „Vorschläge aus Dokumenten" oder „Vorschläge aus Suchbegriffen" aktiviert sein.

Informationen zum gemeinsamen Antwort-Envelope und zum Fehlermodell finden Sie unter :doc:`api-overview`.

Anfrageparameter
~~~~~~~~~~~~~~~~

Die verfügbaren Anfrageparameter sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Anfrageparameter

   * - q
     - Suchbegriff (Präfix) für den Vorschlag. (Beispiel) ``q=fes``
   * - num
     - Anzahl der vorgeschlagenen Wörter (ganze Zahl >= 0). Standard ``10``. (Beispiel) ``num=20``
   * - fn
     - Feldname zur Eingrenzung der Vorschlagsziele. Kann mehrfach angegeben werden (Array). (Beispiel) ``fn=content&fn=title``
   * - lang
     - Angabe der Suchsprache. Kann mehrfach angegeben werden (Array). (Beispiel) ``lang=en``
   * - label
     - Zu filternder Label-Name. Kann mehrfach angegeben werden (Array). (Beispiel) ``label=java``

.. note::

   In v2 wird der Feldname über den Parameter ``fn`` angegeben (nicht ``fields`` wie in v1).
   Außerdem wird der Label-Name über den Parameter ``label`` angegeben (nicht ``labels`` wie in v1).

Antwort
-------

Bei Erfolg wird eine Antwort im gemeinsamen Envelope-Format zurückgegeben:

::

    {
      "response": {
        "status": 0,
        "q": "fes",
        "page_size": 10,
        "record_count": 355,
        "query_time": 18,
        "suggest_words": [
          {
            "text": "fess",
            "types": [
              "document",
              "query"
            ]
          }
        ]
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortinformationen

   * - q
     - Angefragter Suchbegriff (Zeichenkette).
   * - page_size
     - Seitengröße (ganze Zahl).
   * - record_count
     - Anzahl der übereinstimmenden Vorschlagswörter (64-Bit-Ganzzahl).
   * - query_time
     - Abfrageverarbeitungszeit in Millisekunden (64-Bit-Ganzzahl).
   * - suggest_words
     - Array der Vorschlagswörter. Jedes Element enthält ``text`` und ``types``.
   * - text
     - Vorschlagswort (Zeichenkette).
   * - types
     - Array der Vorschlagswort-Typen (Array von Zeichenketten).

.. note::

   In v2 sind die Felder eines Vorschlagseintrags ``text`` und ``types`` (nicht ``labels`` wie in v1).

Verwendungsbeispiel
===================

Beispielanfrage mit curl:

::

    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

Fehlerantwort
=============

Wenn die Vorschlags-API fehlschlägt, wird der gemeinsame Fehler-Envelope zurückgegeben. Details zum Fehlermodell finden Sie unter :doc:`api-overview`.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 405 Method Not Allowed
     - Wenn eine nicht unterstützte HTTP-Methode angegeben wurde.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.
