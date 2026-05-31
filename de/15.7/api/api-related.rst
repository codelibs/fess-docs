================================================
Verwandte-Abfragen- und Verwandte-Inhalte-API
================================================

Diese Seite beschreibt zwei Endpunkte zum Abrufen verwandter Informationen zu einer Abfrage.

- ``GET /related-queries`` — Ruft verwandte Abfragevorschläge zu einer Abfrage ab.
- ``GET /related-content`` — Ruft verwandten HTML-Inhalt zu einer Abfrage ab.

Informationen zum gemeinsamen Antwort-Envelope und zum Fehlermodell finden Sie unter :doc:`api-overview`.

Verwandte Abfragen abrufen
==========================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/related-queries``
==================  ====================================================

Durch Senden einer Anfrage wie ``http://<Server Name>/api/v2/related-queries?q=fess`` an |Fess| können Sie eine Liste verwandter Abfrageausdrücke zur angegebenen Abfrage im JSON-Format erhalten.

Wenn ``q`` leer oder nicht angegeben ist, wird kein Fehler zurückgegeben, sondern ein leeres Array ``queries``. Die Antwort ist stets ein Erfolgs-Envelope.

Anfrageparameter
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Anfrageparameter

   * - q
     - Suchbegriff, für den verwandte Abfragen abgerufen werden sollen. (Beispiel) ``q=fess``

Antwort
-------

Bei Erfolg wird eine Antwort im gemeinsamen Envelope-Format zurückgegeben:

::

    {
      "response": {
        "status": 0,
        "queries": [
          "fess search",
          "fess install"
        ]
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortinformationen

   * - queries
     - Array verwandter Abfrageausdrücke (Array von Zeichenketten). Wenn ``q`` leer oder nicht angegeben ist, wird ein leeres Array zurückgegeben.

Fehlerantwort
~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 405 Method Not Allowed
     - Wenn eine nicht unterstützte HTTP-Methode angegeben wurde.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Verwandten Inhalt abrufen
=========================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/related-content``
==================  ====================================================

Durch Senden einer Anfrage wie ``http://<Server Name>/api/v2/related-content?q=fess`` an |Fess| können Sie verwandten HTML-Inhalt zur angegebenen Abfrage im JSON-Format erhalten.

Wenn mehrere Inhaltselemente übereinstimmen, werden diese durch Zeilenumbrüche verbunden.
Wenn ``q`` leer oder nicht angegeben ist, wird kein Fehler zurückgegeben, sondern ein leerer Zeichenkette als ``content``. Die Antwort ist stets ein Erfolgs-Envelope.

Anfrageparameter
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Anfrageparameter

   * - q
     - Suchbegriff, für den verwandter Inhalt abgerufen werden soll. (Beispiel) ``q=fess``

Antwort
-------

Bei Erfolg wird eine Antwort im gemeinsamen Envelope-Format zurückgegeben:

::

    {
      "response": {
        "status": 0,
        "content": "<div>...verwandter HTML-Inhalt...</div>",
        "content_type": "html"
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortinformationen

   * - content
     - Verwandter HTML-Inhalt (Zeichenkette). Wenn mehrere Elemente übereinstimmen, werden sie durch Zeilenumbrüche verbunden. Wenn ``q`` leer oder nicht angegeben ist, wird eine leere Zeichenkette zurückgegeben.
   * - content_type
     - Typ des Inhalts. Der Wert ist stets ``html``.

Fehlerantwort
~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 405 Method Not Allowed
     - Wenn eine nicht unterstützte HTTP-Methode angegeben wurde.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.
