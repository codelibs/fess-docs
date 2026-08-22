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

Die zurückgegebene Label-Liste wird abhängig vom anfragenden Benutzer und dem Anfrageinhalt wie folgt gefiltert:

- **Filterung nach Berechtigungen**: Die Liste wird anhand der dem Label zugewiesenen Zugriffsrechte und der Rollen des Benutzers gefiltert. Da v2 sitzungsbasierte Authentifizierung verwendet, erhalten angemeldete Benutzer nur die Labels, auf die ihre Rollen Zugriff haben. Labels, deren Zugriffsrechte nicht übereinstimmen, werden nicht in der Liste zurückgegeben.
- **Filterung nach Gebietsschema**: Labels können je nach Gebietsschema registriert werden. Es werden Labels zurückgegeben, die dem im ``Accept-Language``-Anfrage-Header angegebenen Gebietsschema entsprechen, sowie Labels, die ohne Gebietsschemaangabe registriert wurden.
- **Filterung nach virtuellem Host**: Wenn virtuelle Hosts verwendet werden, werden nur die dem jeweiligen virtuellen Host zugewiesenen Labels zurückgegeben.

Anfrageparameter
----------------

Es sind keine Anfrageparameter verfügbar. Die Filterung der zurückgegebenen Labels erfolgt wie oben beschrieben anhand der Berechtigungen des authentifizierten Benutzers und des ``Accept-Language``-Anfrage-Headers.

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
     - Anzahl der zurückgegebenen Labels (integer).
   * - ``labels``
     - Array der Labels.
   * - ``label``
     - Anzeigename des Labels (Label-Name).
   * - ``value``
     - Wert des Labels. Durch Angabe dieses Werts als ``fields.label``-Parameter in der :doc:`api-search` können Suchergebnisse nach dem betreffenden Label gefiltert werden.

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
     - Wenn eine andere HTTP-Methode als GET angegeben wurde. ``error.code`` ist ``method_not_allowed`` und der ``Allow: GET``-Header wird beigefügt.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt. ``error.code`` ist ``internal_error``.

Tabelle: Fehlerantwort
