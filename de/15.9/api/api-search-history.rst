===============
Suchverlauf-API
===============

Dieses Dokument beschreibt die v2-Suchverlauf-API von |Fess|.
Informationen zum gemeinsamen Antwort-Envelope und zum Fehlermodell finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

.. note::

   Der Suchverlauf ist verfügbar, solange sowohl ``search.history.enabled`` (Standard: ``true``) als
   auch das Suchprotokoll aktiviert sind. ``features.search_history`` von ``/api/v2/ui/config`` meldet
   den Zustand.

Letzte Suchen abrufen
=====================

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v2/search-history``
==================  ====================================================

Gibt die letzten Suchen zurück, die der angemeldete Benutzer mit ``/api/v2/search`` auf dem aktuellen
virtuellen Host ausgeführt hat, die neueste zuerst. Ein Client kann eine davon mit den
zurückgegebenen Bedingungen erneut ausführen.

- Nur Suchen auf der ersten Ergebnisseite werden aufgeführt. Suchen mit gleichen Bedingungen werden
  zur neuesten zusammengefasst, Suchen ohne Suchbegriff ausgelassen.
- Höchstens ``search.history.size`` (Standard: ``10``) Suchen werden zurückgegeben.
- Suchprotokolle werden von einem minütlich laufenden Job geschrieben; eine Suche kann daher bis zu
  etwa einer Minute brauchen, bis sie erscheint.
- Der Verlauf gehört zum angemeldeten Benutzer der Sitzung. Anonyme Aufrufer erhalten
  ``auth_required`` (401); ein Zugriffstoken ersetzt keine Anmeldung.
- Ist der Suchverlauf deaktiviert, antwortet der Endpunkt mit ``invalid_request`` (400).

Es gibt keine Anfrageparameter.

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` des gemeinsamen Envelopes zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "record_count": 1,
        "data": [
          {
            "q": "fess",
            "fields": { "label": ["docs"] },
            "sort": "last_modified.desc",
            "requested_at": "2026-10-01T09:00:00Z",
            "hit_count": 42
          }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``record_count``
     - Anzahl der Suchen in ``data`` (int).
   * - ``data``
     - Die letzten Suchen, die neueste zuerst. Die Schlüssel der Bedingungen sind die
       Anfrageparameternamen von ``/api/v2/search``; ein Schlüssel fehlt, wenn die Suche ihn nicht
       verwendet hat.
   * - ``data[].q``
     - Der Suchbegriff (str).
   * - ``data[].fields``
     - Mit ``fields.<name>`` angegebene Feldbedingungen, nach Feldnamen, jeweils mit ihren Werten.
   * - ``data[].ex_q``
     - Zusätzliche Abfragen (Array von str).
   * - ``data[].sort``
     - Sortierreihenfolge (str).
   * - ``data[].lang``
     - Mit ``lang`` angeforderte Sprachen (Array von str).
   * - ``data[].requested_at``
     - Zeitpunkt der Suche (UTC, ISO-8601).
   * - ``data[].hit_count``
     - Trefferzahl der Suche (int64).

Tabelle: Antwortfelder

Fehlerantwort
-------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn der Suchverlauf deaktiviert ist.
   * - 401 Unauthorized
     - Wenn der Aufrufer nicht angemeldet ist.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht zulässig ist.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort

Im mitgelieferten Theme
=======================

Im mitgelieferten Theme ``bootstrap`` sieht ein angemeldeter Benutzer die letzten Suchen in der
Vorschlagsliste, wenn er in das leere Suchfeld klickt oder darin die Pfeil-nach-unten-Taste drückt.
Ein ausgewählter Eintrag führt dieselbe Suche erneut aus, einschließlich Bedingungen wie Labels.
Suchprotokolle, die vor |Fess| 15.9 aufgezeichnet wurden, enthalten keine Bedingungen und werden nicht
aufgeführt.
