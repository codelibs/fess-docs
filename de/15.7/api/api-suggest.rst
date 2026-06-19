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

Vorschlagswörter stammen aus drei Quellen:

- **Dokumente** — Werden aus gecrawlten Dokumenten generiert. Um sie zu erhalten, aktivieren Sie „Vorschläge aus Dokumenten" in der Administrationsoberfläche unter System > Allgemein.
- **Suchbegriffe (Suchprotokoll)** — Werden aus den Suchprotokollen der Benutzer generiert. Um sie zu erhalten, aktivieren Sie „Vorschläge aus Suchbegriffen" in der Administrationsoberfläche unter System > Allgemein.
- **Benutzerwörterbuch** — Von Administratoren eingetragene Vorschlagswörter. Diese werden unabhängig von den obigen Einstellungen stets zurückgegeben.

Auch wenn „Vorschläge aus Dokumenten" und „Vorschläge aus Suchbegriffen" deaktiviert sind, gibt die API keinen Fehler zurück; die entsprechenden Vorschlagswörter werden lediglich aus den Ergebnissen ausgelassen.
Vorschlagswörter werden außerdem automatisch anhand der Rollen des anfragenden Benutzers gefiltert.

Informationen zum gemeinsamen Antwort-Envelope und zum Fehlermodell finden Sie unter :doc:`api-overview`.

Anfrageparameter
----------------

Die verfügbaren Anfrageparameter sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Anfrageparameter

   * - q
     - Suchbegriff (Präfix) für den Vorschlag. Wenn nicht angegeben, werden Vorschlagswörter ohne Präfixfilterung zurückgegeben. (Beispiel) ``q=fes``
   * - num
     - Anzahl der vorgeschlagenen Wörter (ganze Zahl >= 0). Standard ``10``. Bei Angabe eines nicht-numerischen Werts wird der Standardwert verwendet. (Beispiel) ``num=20``
   * - fn
     - Feldname zur Eingrenzung der Vorschlagsziele. Kann mehrfach angegeben werden (Array). (Beispiel) ``fn=content&fn=title``
   * - lang
     - Angabe der Suchsprache. Kann mehrfach angegeben werden (Array). (Beispiel) ``lang=en``
   * - label
     - Label-(Tag-)Name zum Filtern. Kann mehrfach angegeben werden (Array). Die angegebenen Werte werden mit den ``types`` der jeweiligen Vorschlagswörter abgeglichen. (Beispiel) ``label=java``

.. note::

   In v2 wird der Feldname über den Parameter ``fn`` angegeben (nicht ``fields`` wie in v1).
   Anstatt Werte als kommagetrennte Zeichenkette aufzulisten, wird ``fn`` wiederholt angegeben, um mehrere Werte zu übergeben.

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
              "label1"
            ]
          }
        ]
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortinformationen

   * - q
     - Angefragter Suchbegriff (Zeichenkette). Gibt eine leere Zeichenkette zurück, wenn ``q`` nicht angegeben wurde.
   * - page_size
     - Angefragte Anzahl der Vorschlagswörter (der Wert von ``num``, ganze Zahl).
   * - record_count
     - Gesamtanzahl der übereinstimmenden Vorschlagswörter (64-Bit-Ganzzahl).
   * - query_time
     - Abfrageverarbeitungszeit in Millisekunden (64-Bit-Ganzzahl).
   * - suggest_words
     - Array der Vorschlagswörter. Jedes Element enthält ``text`` und ``types``.
   * - text
     - Vorschlagswort (Zeichenkette).
   * - types
     - Array der dem Vorschlagswort zugeordneten Tags (Array von Zeichenketten). Jeder Tag wird aus dem Feld ``label`` oder ``virtual_host`` eines Dokuments abgeleitet oder aus Filterbedingungen, die aus dem Suchprotokoll extrahiert wurden. Gibt ein leeres Array zurück, wenn keine Tags vorhanden sind.

.. note::

   ``types`` enthält Tag-Werte und nicht die Art des Vorschlagsworts (wie z. B. ``document`` oder ``query``). Dieses Array entspricht dem Feld ``labels`` von Vorschlagseinträgen in v1.
   Der Anfrageparameter ``label`` filtert anhand dieser ``types``-Werte.

Verwendungsbeispiele
====================

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
     - Wenn eine nicht unterstützte HTTP-Methode angegeben wurde. Der ``Allow``-Header gibt ``GET`` an.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.
