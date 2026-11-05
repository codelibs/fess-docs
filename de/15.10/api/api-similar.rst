======================
Ähnliche-Dokumente-API
======================

Dieses Dokument beschreibt die v2-API für ähnliche Dokumente von |Fess|, die die Dokumente auflistet, die denselben Inhalt wie ein bestimmtes Dokument haben. Informationen zum gemeinsamen Antwort-Envelope und zum Fehlermodell finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

.. note::

   Diese API findet Kopien und nahezu identische Dokumente. Dokumente, die lediglich dasselbe Thema behandeln, findet sie nicht (siehe „Welche Dokumente zurückgegeben werden" weiter unten).

Ähnliche Dokumente abrufen
==========================

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v2/documents/{docId}/similar``
==================  ====================================================

Gibt die Dokumente zurück, die dieselbe Inhaltssignatur wie das Dokument ``docId`` haben. So kann ein Client neben einem Treffer einen Link „Ähnliche Dokumente" anbieten.

- Für das angegebene Dokument und für die zurückgegebenen Dokumente gelten derselbe Rollenfilter, Filter für virtuelle Hosts und dieselbe zusätzliche Abfrage wie bei ``/api/v2/search``. Ein nicht vorhandenes Dokument und ein für den Aufrufer nicht sichtbares Dokument liefern beide ``not_found`` (404). Das angegebene Dokument selbst und jedes andere Dokument mit derselben URL werden nie zurückgegeben.
- Bei ``login.required=true`` erhält ein anonymer Aufrufer ``auth_required`` (401). Ein Zugriffstoken kann wie bei ``/api/v2/search`` verwendet werden.
- Anfragen sind auf ``api.search.similar.rate.limit.per.minute`` (Standard: ``30``; ``0`` bedeutet unbegrenzt) pro Minute begrenzt, gezählt je angemeldetem Benutzer bzw. je Client-IP bei einem Gast. Bei Überschreitung antwortet der Endpunkt mit ``429`` und einem ``Retry-After``-Header.
- Es wird nur eine Seite zurückgegeben, sortiert nach URL und dann nach Dokument-ID. Es gibt keinen Parameter ``start`` oder Offset.

Welche Dokumente zurückgegeben werden
-------------------------------------

|Fess| berechnet beim Indexieren für jedes Dokument eine Inhaltssignatur (``content_minhash_bits``). Die API gibt die Dokumente zurück, deren Signatur mit der des angegebenen Dokuments übereinstimmt. Es ist dieselbe Gruppierung wie im Duplikatbericht (:doc:`../admin/docreport-guide`), im Suchparameter ``sdh`` und in den Feldern ``similar_docs_*``; sie funktioniert jedoch auch ohne Zusammenfassen von Suchergebnissen.

- Zurückgegeben werden Kopien oder Dokumente mit nahezu demselben Inhalt. Ein Dokument, dessen Inhalt so weit bearbeitet wurde, dass sich die Signatur ändert, wird nicht zurückgegeben; es ist also keine Suche nach Dokumenten zu einem ähnlichen Thema.
- ``data`` ist ein leeres Array (kein Fehler), wenn das angegebene Dokument keinen Inhalt oder kein Wort hat und wenn die Suchmaschine ohne die CodeLibs-Plugins läuft (``search_engine.type`` mit ``vanilla``, ``aws`` oder dem veralteten ``cloud``; siehe :doc:`../config/search-engine-type`).

Anfrageparameter
----------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrageparameter
   :widths: 27 73
   :header-rows: 1

   * - Parameter
     - Beschreibung
   * - ``docId``
     - Dokumentkennung (Pfad, erforderlich, Muster ``[A-Za-z0-9_-]{1,512}``). Ein nicht passender Wert führt zu ``invalid_request`` (400).
   * - ``num``
     - Anzahl der zurückzugebenden Dokumente (Query, Standard ``10``). Ein Wert über ``20`` oder über ``paging.search.page.max.size`` wird auf den kleineren der beiden Werte gekürzt; ``page_size`` in der Antwort zeigt das Ergebnis. Ein Wert von ``0`` oder weniger führt zu ``invalid_request`` (400). Ein Wert, der keine Zahl ist, wird ignoriert, und der Standardwert gilt.

Tabelle: Anfrageparameter

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` im gemeinsamen Envelope zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "exec_time": "0.01",
        "query_time": 5,
        "page_size": 10,
        "record_count": 1,
        "record_count_relation": "EQUAL_TO",
        "partial": false,
        "timed_out": false,
        "shard_failed": false,
        "data": [
          {
            "doc_id": "f6e5d4c3b2a1",
            "url": "https://example.com/copy/",
            "title": "Example",
            "content_description": "An example document about Fess."
          }
        ]
      }
    }

Die Felder im Einzelnen:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder
   :widths: 27 73
   :header-rows: 1

   * - Feld
     - Beschreibung
   * - ``doc_id``
     - ID des angegebenen Dokuments.
   * - ``exec_time``
     - Ausführungszeit in Sekunden (eine Dezimalzahl als Zeichenfolge, z. B. ``"0.01"``).
   * - ``query_time``
     - Abfragezeit der Suchmaschine (int64, Millisekunden).
   * - ``page_size``
     - Angeforderte Anzahl an Dokumenten nach Anwendung der oben beschriebenen Begrenzung.
   * - ``record_count``
     - Anzahl der Dokumente mit derselben Signatur, nicht nur der in ``data`` enthaltenen. Die genaue Anzahl wird nur bis ``query.track.total.hits`` (Standard: ``10000``) verfolgt.
   * - ``record_count_relation``
     - Bei ``EQUAL_TO`` ist die Anzahl exakt; bei ``GREATER_THAN_OR_EQUAL_TO`` ist nur die untere Grenze bekannt.
   * - ``partial``
     - Ob das Ergebnis unvollständig sein kann (bool). Wie bei einer Suche gilt das Abfrage-Timeout (``query.timeout``).
   * - ``timed_out``
     - Ob das Abfrage-Timeout abgelaufen ist (bool).
   * - ``shard_failed``
     - Ob ein oder mehrere Shards fehlgeschlagen sind (bool).
   * - ``data``
     - Array der Dokumente, sortiert nach URL und dann nach Dokument-ID. Jedes Element hat dieselben Felder wie ein Treffer von ``/api/v2/search`` (siehe :doc:`api-search`), einschließlich ``tags`` (die für den Aufrufer sichtbaren Tags, siehe :doc:`api-tag`). Es gibt keine Abfrage zum Hervorheben, daher ist ``content_description`` der Auszug des Inhalts, und es gibt kein ``score``.

Tabelle: Antwortfelder

Fehlerantwort
-------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort
   :widths: 25 75
   :header-rows: 1

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - ``docId`` entspricht nicht dem Muster, oder ``num`` ist ``0`` oder kleiner.
   * - 401 Unauthorized
     - Eine Authentifizierung ist erforderlich (die Einstellung „Anmeldung erforderlich" ist aktiviert und der Aufrufer anonym, oder die Anfrage enthält ein nicht registriertes oder abgelaufenes Zugriffstoken).
   * - 404 Not Found
     - Das angegebene Dokument existiert nicht oder ist für den Aufrufer nicht sichtbar (``not_found``).
   * - 405 Method Not Allowed
     - Die HTTP-Methode ist nicht erlaubt.
   * - 429 Too Many Requests
     - Das Limit an Anfragen pro Minute wurde überschritten. Ein ``Retry-After``-Header gibt die Wartezeit in Sekunden an (``60``).
   * - 500 Internal Server Error
     - Ein interner Serverfehler ist aufgetreten.
   * - 503 Service Unavailable
     - Die Suchmaschine konnte die Anfrage nicht annehmen: Sie ist nicht erreichbar oder hat die Anfrage wegen fehlender Kapazität abgelehnt. ``error.code`` ist ``service_unavailable``, und ein ``Retry-After``-Header gibt die Wartezeit in Sekunden an (``5``). Die Anfrage selbst ist in Ordnung; versuchen Sie es nach kurzer Wartezeit erneut.

Tabelle: Fehlerantwort
